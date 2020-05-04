import logging
import functools
import itertools
import random
from typing import Type, Iterable

from core.components import (
    Manager,
    Position,
    Visible,
    Movable,
    Actions,
    FOV,
    Vision,
    Viewer,
    UnderUserControl,
    AI,
)
from core.events import Event
from core.constants import BOARD_SIZE
from core.board import (
    get_fov_mask,
)
from core.events import (
    Move,
    SetActions,
    SetFOV,
    Clean,
)


_LOGGER = logging.getLogger(__name__)


class System:
    def __init__(self, manager: Manager):
        self._manager = manager

    def process(self) -> Iterable[Event]:
        pass


class World:
    def __init__(self, manager: Manager, systems: Iterable[Type[System]]):
        self._manager = manager
        self._systems = systems
        self._logger = _LOGGER.getChild('world')

    def step(self) -> 'World':
        manager = self._manager
        for system in self._systems:
            self._logger.info('Process system %s', system)
            events = system(manager).process() or []
            get_sort_key = lambda x: (x.entity, str(x.component_class))
            get_group_key = lambda x: (x.entity, x.component_class)
            grouped_events = itertools.groupby(sorted(events, key=get_sort_key), key=get_group_key)
            for (entity, component_class), events in grouped_events:
                self._logger.info('Process entity %s %s', entity, component_class)
                component = functools.reduce(
                    lambda r, e: e(r),
                    events,
                    manager.entities.get(entity=entity, component_class=component_class),
                )
                self._logger.info('Set entity %s %s component %s', entity, component_class, component)
                manager.entities.set(entity, component_class, component)
                manager.reinit()
        return World(manager, self._systems)

    def serialize(self):
        return self._manager.serialize()


class AISystem(System):
    def process(self):
        for entity in self._manager.entities.filter([Actions, AI]):
            actions = self._manager.entities.get(entity, Actions).actions
            action = random.choice(actions)
            yield action


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
            yield Move(
                entity=entity,
                component_class=Position,
                dx=result[0],
                dy=result[1],
                manager=self._manager,
            )


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
                yield SetActions(
                    entity=entity,
                    component_class=Actions,
                    event=Move(
                        entity=entity,
                        component_class=Position,
                        dx=dx,
                        dy=dy,
                        manager=self._manager,
                    ),
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
                yield Clean(
                    entity=entity,
                    component_class=cls,
                )


class FOVSystem(System):
    def process(self):
        for entity in self._manager.entities.filter([Vision, FOV, Position]):
            position = self._manager.entities.get(entity, Position)
            is_full = lambda x: self._manager.components.get(x)
            fov = get_fov_mask(position=position, fow_size=3, board_size=BOARD_SIZE, is_full=is_full)
            yield SetFOV(
                entity=entity,
                component_class=FOV,
                fov=fov,
            )
