#!/usr/bin/env python3

from core.components import (
    ComponentManager,
    Position,
    Visible,
    Name,
    Movable,
    PermittedPositions,
)
from core.systems import (
    World,
    MoveSystem,
    ViewSystem,
    PermittedPositionsSystem,
    CleanSystem,
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
        ],
        PermittedPositions: [
            None,
            None,
            None,
        ]
    }
    cm = ComponentManager(components)
    systems = [
        ViewSystem,
        PermittedPositionsSystem,
        MoveSystem,
        CleanSystem,
    ]
    world = World(cm, systems)
    for i in range(10):
        events = world.step()
        world = world.new_state(events)


if __name__ == '__main__':
    main()
