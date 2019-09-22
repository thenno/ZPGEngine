#!/usr/bin/env python3

from core.components import (
    Manager,
    Position,
    Visible,
    Name,
    Movable,
    AI,
    Actions,
    FOV,
    Vision,
    Viewer,
)
from core.systems import (
    World,
    AISystem,
    ViewSystem,
    CleanupSystem,
    AllowActionSystem,
    FOVSystem,
)


def main():
    components = {
        Name: [
            Name('test1'),
            Name('test2'),
            Name('hidden'),
            Name('wall'),
            Name('wall'),
            Name('wall'),
        ],
        Position: [
            Position(0, 9),
            Position(0, 0),
            Position(4, 4),
            Position(5, 4),
            Position(6, 4),
            None,
        ],
        Visible: [
            Visible('x'),
            Visible('y'),
            Visible('#'),
            Visible('#'),
            Visible('#'),
            None,
        ],
        Movable: [
            Movable(),
            Movable(),
            None,
            None,
            None,
            None,
        ],
        AI: [
            AI(),
            AI(),
            None,
            None,
            None,
            None,
        ],
        Actions: [
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        FOV: [
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        Vision: [
            Vision(),
            Vision(),
            None,
            None,
            None,
            None,
        ],
        Viewer: [
            Viewer(),
            None,
            None,
            None,
            None,
            None,
        ]
    }
    cm = Manager(components)
    systems = [
        CleanupSystem,
        FOVSystem,
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
