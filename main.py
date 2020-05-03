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
    UnderUserControl,
)
from core.systems import (
    World,
    AISystem,
    ViewSystem,
    CleanupSystem,
    AllowActionSystem,
    FOVSystem,
    UserControlSystem,
)


def main():
    components = {
        Name: [
            Name('test1'),
            Name('test2'),
            Name('wall'),
            Name('wall'),
            Name('wall'),
            Name('test3'),
        ],
        Position: [
            Position(0, 9),
            Position(0, 0),
            Position(4, 4),
            Position(5, 4),
            Position(6, 4),
            Position(9, 9),
        ],
        Visible: [
            Visible('x'),
            Visible('y'),
            Visible('#'),
            Visible('#'),
            Visible('#'),
            Visible('z'),
        ],
        Movable: [
            Movable(),
            Movable(),
            None,
            None,
            None,
            Movable(),
        ],
        AI: [
            None,
            AI(),
            None,
            None,
            None,
            AI(),
        ],
        UnderUserControl: [
            UnderUserControl(),
            None,
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
            Vision(),
        ],
        Viewer: [
            Viewer(),
            None,
            None,
            None,
            None,
            None,
        ],
    }
    cm = Manager(components)
    systems = [
        CleanupSystem,
        FOVSystem,
        ViewSystem,
        AllowActionSystem,
        AISystem,
        UserControlSystem,
    ]
    world = World(cm, systems)
    for i in range(30):
        world = world.step()


if __name__ == '__main__':
    main()
