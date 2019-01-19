from typing import List, NewType
from dataclasses import dataclass

from core.board import Position


class Goal:
    pass


Goals = NewType('Goals', List[Goal])


@dataclass(frozen=True)
class Walk(Goal):
    position: Position
