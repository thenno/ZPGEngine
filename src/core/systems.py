import functools
import itertools
import random
from typing import Type, Callable, NewType, Iterable, Tuple
from dataclasses import dataclass

from core.components import (
    Manager,
    Position,
    Visible,
    Component,
    PermittedPositions,
    Movable,
)


BOARD_SIZE = 10
Distance = NewType('Distance', int)


@dataclass(frozen=True)
class Event:
    func: Callable
    entity: int
    component_class: Type[Component]


class World:
    def __init__(self, manager: Manager, systems):
        self._manager = manager
        self._systems = systems

    def step(self):
        for system in self._systems:
            yield from system(self._manager).process() or []

    def new_state(self, events) -> 'World':
        manager = self._manager.clone()
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


class MoveSystem(System):
    def process(self):
        for entity in self._manager.entities.filter([Position]):
            yield Event(
                entity=entity,
                component_class=Position,
                func=Move(self._manager, random.randint(-1, 1), random.randint(-1, 1))
            )


class AISystem(System):
    def process(self):
        for entity in self._manager.entities.filter([Movable, Position]):
            directions = self._manager.entities.get(entity, PermittedPositions).positions
            direction = random.choice(directions)
            yield Event(
                entity=entity,
                component_class=Position,
                func=Move(*direction)
            )


class ViewSystem(System):
    def _generate_board(self, size: int):
        replacer = '.'
        return [
            [replacer] * size for _ in range(size)
        ]

    def process(self):
        printed_board = self._generate_board(BOARD_SIZE)
        for entity in self._manager.entities.filter([Position, Visible]):
            position = self._manager.entities.get(entity, Position)
            char = self._manager.entities.get(entity, Visible)
            printed_board[position.y][position.x] = char.char
        print(' x ' + ''.join(map(str, range(BOARD_SIZE))))
        print('y')
        for number, line in zip(range(BOARD_SIZE), printed_board):
            line_serialized = map(str, line)
            print(str(number).zfill(2) + ' ' + ''.join(line_serialized))
        print()


class CleanSystem(System):
    def process(self):
        for cls in self._manager.components.get_need_clean():
            for entity in range(self._manager.entities.count):
                yield Event(
                    entity=entity,
                    component_class=cls,
                    func=lambda x: None,
                )
