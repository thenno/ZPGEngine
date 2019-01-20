from typing import NewType

from core.board import Direction


MarineId = NewType('MarineId', str)


class Marine:

    def __init__(self, name: MarineId, gaze_direction: Direction):
        self.name = name
        self.gaze_direction = gaze_direction

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    @property
    def alive(self):
        return True

    def __str__(self):
        return self.name
