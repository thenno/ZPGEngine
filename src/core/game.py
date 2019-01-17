import dataclasses
from typing import Dict, List

from core.board import Board
from core.marines import MarineId, Marine
from core.goals import Goal


@dataclasses.dataclass
class Game:
    board: Board
    memory: Dict[MarineId, List]
    marines: Dict[MarineId, Marine]
    goals: Dict[MarineId, List[Goal]]
