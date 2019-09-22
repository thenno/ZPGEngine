#!/usr/bin/env python3

from core.components import (
    Manager,
    Position,
    Visible,
    Name,
    Movable,
    AI,
    Actions,
)
from core.systems import (
    World,
    AISystem,
    ViewSystem,
    CleanSystem,
    AllowActionSystem,
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
        AI: [
            AI(),
            AI(),
            None,
        ],
        Actions: [
            None,
            None,
            None,
        ]
    }
    cm = Manager(components)
    systems = [
        CleanSystem,
        ViewSystem,
        AllowActionSystem,
        AISystem,
    ]
    world = World(cm, systems)
    for i in range(30):
        events = world.step()
        world = world.new_state(events)


if __name__ == '__main__':
    main()
