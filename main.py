#!/usr/bin/env python3

import random
import itertools
import functools

from typing import Type, Callable
from dataclasses import dataclass
from copy import deepcopy


BOARD_SIZE = 10


class Component:
    pass


class ComponentManager:
    def __init__(self, components):
        self._components = components

    def filter(self, component_classes):
        result = None
        for component_class in component_classes:
            entities = {
                entity
                for entity, _ in enumerate(self._components[component_class])
                if self._components[component_class][entity] is not None
            }
            result = entities if result is None else result & entities
        if result is not None:
            yield from result

    def get(self, entity, component_class):
        return self._components[component_class][entity]

    def set(self, entity, component_class, value):
        self._components[component_class][entity] = value

    def clone(self):
        return ComponentManager(deepcopy(self._components))

    def serialize(self):
        return self._components


@dataclass(frozen=True)
class Position(Component):
    x: int
    y: int


@dataclass(frozen=True)
class Visible(Component):
    char: str


@dataclass(frozen=True)
class Name(Component):
    name: str


class Movable:
    pass


@dataclass(frozen=True)
class Event:
    func: Callable
    entity: int
    component_class: Type[Component]


class World:
    def __init__(self, cm: ComponentManager, systems):
        self._cm = cm
        self._systems = systems

    def step(self):
        for system in self._systems:
            result = system(self._cm).process()
            if result is not None:
                yield from system(self._cm).process()

    def new_state(self, events):
        components = self._cm.clone()
        get_key = lambda x: (x.entity, x.component_class)
        for (entity, component_class), events in itertools.groupby(sorted(events, key=get_key), key=get_key):
            component = functools.reduce(
                lambda r, e: e.func(r),
                events,
                components.get(entity=entity, component_class=component_class),
            )
            components.set(entity, component_class, component)
        return World(components, self._systems)

    def serialize(self):
        return self._cm.serialize()


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


class MoveSystem:
    def __init__(self, cm: ComponentManager):
        self._cm = cm

    def process(self):
        for entity in self._cm.filter([Position]):
            yield Event(
                entity=entity,
                component_class=Position,
                func=Move(random.randint(-1, 1), random.randint(-1, 1))
            )


class ViewSystem:
    def __init__(self, cm: ComponentManager):
        self._cm = cm

    def _generate_board(self, size: int):
        replacer = '.'
        return [
            [replacer] * size for _ in range(size)
        ]

    def process(self):
        printed_board = self._generate_board(BOARD_SIZE)
        for entity in self._cm.filter([Position, Visible]):
            position = self._cm.get(entity, Position)
            char = self._cm.get(entity, Visible)
            printed_board[position.y][position.x] = char.char
        print(' x ' + ''.join(map(str, range(BOARD_SIZE))))
        print('y')
        for number, line in zip(range(BOARD_SIZE), printed_board):
            line_serialized = map(str, line)
            print(str(number).zfill(2) + ' ' + ''.join(line_serialized))
        print()


def main():
    components = {
        Name: [
            Name('test1'),
            Name('test2'),
            Name('hidden'),
        ],
        Position: [
            Position(0, 9),
            Position(0, 0),
            None,
        ],
        Visible: [
            Visible('x'),
            Visible('y'),
            None,
        ],
        Movable: [
            Movable(),
            Movable(),
            None,
        ]
    }
    cm = ComponentManager(components)
    systems = [
        MoveSystem,
        ViewSystem,
    ]
    world = World(cm, systems)
    for i in range(4):
        events = world.step()
        world = world.new_state(events)


if __name__ == '__main__':
    main()
