from typing import List, Dict, NewType

from dataclasses import dataclass
from core.board import Position


EnemyId = NewType('EnemyId', int)


@dataclass(frozen=True)
class Memory:
    way: List[Position]
    enemies: Dict[EnemyId, List[Position]]
