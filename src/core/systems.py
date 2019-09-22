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
    def __init__(self, dx, dy):
        self._dx = dx
        self._dy = dy

    def __call__(self, position):
        x = position.x + self._dx
        y = position.y + self._dy
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            return Position(position.x + self._dx, position.y + self._dy)
        return position


class SetPermittedPositions:
    def __init__(self, positions: Tuple[Position, ...]):
        self._positions = positions

    def __call__(self, positions: Tuple[Position, ...]):
        if positions is None:
            positions = PermittedPositions(tuple())
        return PermittedPositions(positions=positions.positions + self._positions)


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
                func=Move(random.randint(-1, 1), random.randint(-1, 1))
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


class PermittedPositionsSystem(System):
    def _generate_movements(self, pos: Position, distance: Distance = Distance(1)) -> Iterable[Position]:
        for mx in range(-distance, distance + 1):
            for my in range(-distance, distance + 1):
                new_pos = Position(mx + pos.x, my + pos.y)
                yield new_pos

    def _is_valid(self, position):
        if not self._manager.components.get(position):
            return True
        if 0 <= position.x < BOARD_SIZE and 0 <= position.y < BOARD_SIZE:
            return True
        return False

    def process(self):
        for entity in self._manager.entities.filter([Position, Movable]):
            positions = self._generate_movements(self._manager.entities.get(entity, Position))
            positions = (
                position
                for position in positions
                if self._is_valid(position)
            )
            yield Event(
                entity=entity,
                component_class=PermittedPositions,
                func=SetPermittedPositions(tuple(positions)),
            )


class CleanSystem(System):
    def process(self):
        for cls in self._manager.components.get_need_clean():
            for entity in range(self._manager.entities.count):
                yield Event(
                    entity=entity,
                    component_class=cls,
                    func=lambda x: None,
                )
