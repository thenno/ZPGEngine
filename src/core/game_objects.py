from typing import NewType

from core.board import Direction
from abc import ABCMeta, abstractmethod


MarineId = NewType('MarineId', str)


class GameObject(metaclass=ABCMeta):

    @property
    @abstractmethod
    def is_under_control(self) -> bool:
        pass


class Wall(GameObject):

    @property
    def is_under_control(self):
        return False


class Marine(GameObject):

    def __init__(self, name: MarineId, gaze_direction: Direction):
        self.name = name
        self.gaze_direction = gaze_direction

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    @property
    def is_alive(self) -> bool:
        return True

    @property
    def is_under_control(self):
        return True

    def __str__(self):
        return self.name
