#!/usr/bin/env python3

from core.components import ComponentManager, Position, Visible, Name, Movable
from core.systems import World, MoveSystem, ViewSystem


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
        ViewSystem,
        MoveSystem,
    ]
    world = World(cm, systems)
    for i in range(4):
        events = world.step()
        world = world.new_state(events)


if __name__ == '__main__':
    main()
