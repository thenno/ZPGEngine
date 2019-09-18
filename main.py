#!/usr/bin/env python3


from typing import Dict, NewType, Type, Callable
from dataclasses import dataclass
import random
import itertools
import functools
from copy import deepcopy


class Entity:
    pass


class Component:
    pass


@dataclass(frozen=False)
class Position(Component):
    x: int
    y: int


@dataclass(frozen=True)
class Visible(Component):
    char: str


@dataclass(frozen=True)
class Name(Component):
    name: str


@dataclass(frozen=True)
class Event:
    func: Callable
    entity: int
    component_class: Type[Component]


class World:
    def __init__(self, components):
        self._components = components

    def filter(self, component_types):
        for component_type in component_types:
            for entity, _ in enumerate(self._components[component_type]):
                if self._components[component_type][entity] is not None:
                    yield entity

    def new_state(self, events):
        components = deepcopy(self._components)
        get_key = lambda x: (x.entity, x.component_class)
        for key, events in itertools.groupby(sorted(events, key=get_key), key=get_key):
            entity, component_class = key
            components[component_class][entity] = functools.reduce(
                lambda r, e: e.func(r),
                events,
                components[component_class][entity],
            )
        return World(components)


class Move:
    def __init__(self, dx, dy):
        self._dx = dx
        self._dy = dy

    def __call__(self, position):
        return Position(position.x + self._dx, position.y + self._dy)


class MoveSystem:
    def __init__(self, world: World):
        self._world = world

    def process(self):
        for entity in self._world.filter([Position]):
            yield Event(
                entity=entity,
                component_class=Position,
                func=Move(random.randint(0, 1), random.randint(0, 1))
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
    }
    world = World(components)
    systems = [
        MoveSystem,
    ]
    import pprint
    pprint.pprint(world._components)
    events = []
    for system in systems:
        events += list(system(world).process())
    world = world.new_state(events)
    pprint.pprint(world._components)


if __name__ == '__main__':
    main()
