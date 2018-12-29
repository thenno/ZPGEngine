import dataclasses
from typing import NewType, Dict, List

from core.board import Board
from core.marines import MarineId, Marine

Memory = NewType('Memory', Dict[MarineId, List])


@dataclasses.dataclass
class Game:
    board: Board
    memory: Memory
    marines: Dict[MarineId, Marine]
