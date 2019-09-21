#!/usr/bin/env python3

import random
import itertools
import functools
import pprint

from typing import Type, Callable
from dataclasses import dataclass
from copy import deepcopy


class Entity:
    pass


class Component:
    pass


class ComponentManager:
    def __init__(self, components):
        self._components = components

    def filter(self, component_classes):
        for component_class in component_classes:
            for entity, _ in enumerate(self._components[component_class]):
                if self._components[component_class][entity] is not None:
                    yield entity

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
        return Position(position.x + self._dx, position.y + self._dy)


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
    ]
    world = World(cm, systems)
    events = world.step()
    new_world = world.new_state(events)
    pprint.pprint(world.serialize())
    pprint.pprint(new_world.serialize())


if __name__ == '__main__':
    main()
