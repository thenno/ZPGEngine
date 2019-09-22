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
    Movable,
    Actions,
    FOV,
    Vision,
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


class AISystem(System):
    def process(self):
        for entity in self._manager.entities.filter([Actions]):
            actions = self._manager.entities.get(entity, Actions).actions
            action = random.choice(actions)
            func, args = action
            yield Event(
                entity=entity,
                component_class=Position,
                func=func(self._manager, *args),
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
            fov = FOV(set())


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


class FOVSystem(System):
    def process(self):
        for entity in self._manager.entities.filter([Vision]):
            position = self._manager.entities.get(entity, Position)
            fov = self._get_fov_mask(position)
            yield Event(
                entity=entity,
                component_class=FOV,
                func=SetFOV(fov),
            )

    def _generate_movements(self, pos: Position, distance: Distance = Distance(1)) -> Iterable[Position]:
        for mx in range(-distance, distance + 1):
            for my in range(-distance, distance + 1):
                new_pos = Position(mx + pos.x, my + pos.y)
                yield new_pos

    def _get_fov_mask(self, position: Position):
        def is_visible(pos_to: Position) -> bool:
            line = list(self._get_line_of_view(position, pos_to))
            for i, pos_for_check in enumerate(line):
                if i not in (0, len(line) - 1) and not self._manager.components.get(Position):
                    return False
            return True

        positions = self._generate_movements(position, distance=Distance(5))
        result = set()
        for pos in positions:
            if not self._manager.components.get(pos):
                continue
            if is_visible(pos):
                result.add(pos)
        return result

    def _get_line_of_view(self, pos1: Position, pos2: Position) -> Iterable[Position]:
        """
        Bresenham's line algorithm

        There may be some problems, check it again and add tests
        """

        # TODO: check it again and add tests
        delta_x = abs(pos2.x - pos1.x)
        delta_y = abs(pos2.y - pos1.y)
        if delta_x > delta_y:
            a1, b1, a2, b2 = pos1.x, pos1.y, pos2.x, pos2.y
        else:
            a1, b1, a2, b2 = pos1.y, pos1.x, pos2.y, pos2.x
        delta_a = abs(a2 - a1)
        delta_b = abs(b2 - b1)
        error = 0.0
        delta_err = delta_b / delta_a if delta_a != 0 else 0
        b = b1
        direction = b2 - b1
        if direction > 0:
            direction = 1
        if direction < 0:
            direction = -1
        if a1 < a2:
            range_a = range(a1, a2 + 1)
        else:
            range_a = range(a2, a1 + 1)[::-1]
        for a in range_a:
            if delta_x > delta_y:
                yield Position(a, b)
            else:
                yield Position(b, a)
            error = error + delta_err
            if error >= 0.5:
                b = b + direction
                error = error - 1.0
