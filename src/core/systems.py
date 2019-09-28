import functools
import itertools
import random
from typing import Type, Callable, NewType, Iterable
from dataclasses import dataclass

from core.components import (
    Manager,
    Position,
    Visible,
    Component,
    Movable,
    Actions,
    FOV,
    Vision,
    Viewer,
    UnderUserControl,
    AI,
)
from core.board import (
    get_fov_mask,
)


BOARD_SIZE = 10


@dataclass(frozen=True)
class Event:
    func: Callable
    entity: int
    component_class: Type[Component]


class World:
    def __init__(self, manager: Manager, systems):
        self._manager = manager
        self._systems = systems

    def _process(self):
        for system in self._systems:
            yield system(self._manager).process() or []

    def step(self) -> 'World':
        manager = self._manager
        manager = manager.clone()
        for system in self._systems:
            events = system(manager).process() or []
            get_sort_key = lambda x: (x.entity, str(x.component_class))
            get_group_key = lambda x: (x.entity, x.component_class)
            for (entity, component_class), events in itertools.groupby(sorted(events, key=get_sort_key), key=get_group_key):
                component = functools.reduce(
                    lambda r, e: e.func(r),
                    events,
                    manager.entities.get(entity=entity, component_class=component_class),
                )
                manager.entities.set(entity, component_class, component)
        return World(manager, self._systems)

    def serialize(self):
        return self._manager.serialize()


class Move:
    def __init__(self, manager, dx, dy):
        self._dx = dx
        self._dy = dy
        self._manager = manager

    def _is_valid(self, position):
        if not (0 <= position.x < BOARD_SIZE and 0 <= position.y < BOARD_SIZE):
            return False
        if self._manager.components.get(position):
            return False
        return True

    def __call__(self, position):
        x = position.x + self._dx
        y = position.y + self._dy
        new_position = Position(x, y)
        if self._is_valid(new_position):
            return new_position
        return position


class System:
    def __init__(self, manager: Manager):
        self._manager = manager

    def process(self) -> Iterable[Event]:
        pass


class AISystem(System):
    def process(self):
        for entity in self._manager.entities.filter([Actions, AI]):
            actions = self._manager.entities.get(entity, Actions).actions
            action = random.choice(actions)
            func, args = action
            yield Event(
                entity=entity,
                component_class=Position,
                func=func(self._manager, *args),
            )


class UserControlSystem(System):
    def process(self):
        for entity in self._manager.entities.filter([UnderUserControl, Movable]):
            result = {
                'w': (0, -1),
                'a': (-1, 0),
                's': (0, 1),
                'd': (1, 0),
                'wa': (-1, -1),
                'wd': (1, -1),
                'sa': (-1, 1),
                'sd': (1, 1),
            }[input()]
            yield Event(
                entity=entity,
                component_class=Position,
                func=Move(self._manager, *result)
            )


class SetActions:
    def __init__(self, func, args):
        self._func = func
        self._args = args

    def __call__(self, actions):
        if actions is None:
            actions = Actions(tuple())
        return Actions(actions.actions + ((self._func, self._args),))


class SetFOV:
    def __init__(self, fov):
        self._fov = fov

    def __call__(self, fov):
        if fov is None:
            fov = FOV(frozenset())
        return FOV(fov.fov | self._fov)


class AllowActionSystem(System):
    def _generate_directions(self):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == dy == 0:
                    continue
                yield dx, dy

    def process(self):
        for entity in self._manager.entities.filter([Movable]):
            for dx, dy in self._generate_directions():
                yield Event(
                    entity=entity,
                    component_class=Actions,
                    func=SetActions(func=Move, args=(dx, dy))
                )


class ViewSystem(System):
    def _generate_board(self, size: int):
        replacer = '.'
        return [
            [replacer] * size for _ in range(size)
        ]

    def process(self):
        printed_board = self._generate_board(BOARD_SIZE)
        fov = set()
        for entity in self._manager.entities.filter([Position, Visible]):
            position = self._manager.entities.get(entity, Position)
            char = self._manager.entities.get(entity, Visible)
            printed_board[position.y][position.x] = char.char
        for entity in self._manager.entities.filter([Viewer, FOV]):
            fov |= self._manager.entities.get(entity, FOV).fov
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if Position(x, y) not in fov:
                    printed_board[y][x] = '?'
        print(' x ' + ''.join(map(str, range(BOARD_SIZE))))
        print('y')
        for number, line in zip(range(BOARD_SIZE), printed_board):
            line_serialized = map(str, line)
            print(str(number).zfill(2) + ' ' + ''.join(line_serialized))
        print()


class CleanupSystem(System):
    def process(self):
        for cls in self._manager.components.get_need_clean():
            for entity in range(self._manager.entities.count):
                yield Event(
                    entity=entity,
                    component_class=cls,
                    func=lambda x: None,
                )


class PositionWrapper:
    def __init__(self, position: Position):
        self._position = position


class FOVSystem(System):
    def process(self):
        for entity in self._manager.entities.filter([Vision, Position]):
            position = self._manager.entities.get(entity, Position)
            is_full = lambda x: self._manager.components.get(x)
            fov = get_fov_mask(position=position, fow_size=3, board_size=BOARD_SIZE, is_full=is_full)
            yield Event(
                entity=entity,
                component_class=FOV,
                func=SetFOV(fov),
            )
