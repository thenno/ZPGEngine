from typing import NewType
from abc import ABCMeta, abstractmethod

MarineId = NewType('MarineId', str)


class GameId(int):

    current_id = 0

    @classmethod
    def next(cls):
        yield cls.current_id
        cls.current_id += 1


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

    def __init__(self, name: MarineId):
        self.name = name

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
