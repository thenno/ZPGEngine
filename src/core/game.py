from dataclasses import dataclass
from typing import Dict, Set, NewType

from core.board import Board, FOV, Position
from core.marines import Marine
from core.memory import Memory


GameObject = NewType('GameObject', str)


MARINE = GameObject('marine')
WALL = GameObject('wall')


class GameId(int):

    current_id = 0

    @classmethod
    def next(cls):
        yield cls.current_id
        cls.current_id += 1


@dataclass(frozen=True)
class MarineKnowledge:
    game_id: GameId
    fov: FOV
    board_size: int
    position: Position
    mask: Set[Position]
    memory: Memory


@dataclass
class Game:
    # TODO: game object have to construct by completed game objects
    board: Board
    memory: Dict[GameId, Memory]
    marines: Dict[GameId, Marine]
    objects: Dict[GameId, GameObject]

    def get_marine_knowledge(self, game_id: GameId) -> MarineKnowledge:
        position = self.board.get_position(game_id)
        if position is None:
            raise Exception
        mask = self.board.get_fov_mask(position)
        fov = self.board.get_view(mask)
        return MarineKnowledge(
            game_id=game_id,
            position=position,
            fov=fov,
            board_size=self.board.size,
            mask=mask,  # mask in knowledge - WTF?
            memory=self.memory[game_id],
        )
