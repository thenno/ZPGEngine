from dataclasses import dataclass

from core.board import Position


class Goal:
    pass


@dataclass
class Walk(Goal):
    position: Position
