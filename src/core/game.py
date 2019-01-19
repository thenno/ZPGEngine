from dataclasses import dataclass
from typing import Dict, List, Set

from core.board import Board, FOV, Position
from core.marines import MarineId, Marine
from core.goals import Goals


@dataclass(frozen=True)
class MarineKnowledge:
    marine_id: MarineId
    fov: FOV
    board_size: int
    position: Position
    goals: Goals
    mask: Set[Position]


@dataclass
class Game:
    board: Board
    memory: Dict[MarineId, List]
    marines: Dict[MarineId, Marine]
    goals: Dict[MarineId, Goals]

    def get_marine_knowledge(self, marine_id: MarineId) -> MarineKnowledge:
        position = self.board.get_position(marine_id)
        if position is None:
            raise Exception
        mask = self.board.get_fov_mask(position)
        fov = self.board.get_view(mask)
        return MarineKnowledge(
            marine_id=marine_id,
            position=position,
            fov=fov,
            board_size=self.board.size,
            goals=self.goals[marine_id],
            mask=mask,  # mask in knowledge - WTF?
        )
