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
    EntityBuilder,
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
    entities = [
        EntityBuilder(
            name=Name('test1'),
            position=Position(0, 9),
            visible=Visible('x'),
            movable=Movable(),
            under_user_control=UnderUserControl(),
            vision=Vision(),
            viewer=Viewer(),
        ),
        EntityBuilder(
            name=Name('test2'),
            position=Position(0, 0),
            visible=Visible('y'),
            movable=Movable(),
            ai=AI(),
            vision=Vision(),
        ),
        EntityBuilder(
            name=Name('wall'),
            position=Position(4, 4),
            visible=Visible('#'),
        ),
        EntityBuilder(
            name=Name('wall'),
            position=Position(5, 4),
            visible=Visible('#'),
        ),
        EntityBuilder(
            name=Name('wall'),
            position=Position(6, 4),
            visible=Visible('#'),
        ),
        EntityBuilder(
            name=Name('test3'),
            position=Position(9, 9),
            visible=Visible('z'),
            movable=Movable(),
            ai=AI(),
            vision=Vision(),
        ),
    ]
    cm = Manager()
    for entity in entities:
        cm = cm.add(entity)
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
