from dataclasses import dataclass

from core.board import Board, FOV
from core.game_objects import GameId


@dataclass(frozen=True)
class Vision:
    fov: FOV


@dataclass(frozen=True)
class Hearing:
    pass


@dataclass(frozen=True)
class Senses:

    vision: Vision
    hearing: Hearing

    @staticmethod
    def feel(board: Board, game_id: GameId) -> 'Senses':
        position = board.get_position(game_id)
        mask = board.get_fov_mask(position)
        return Senses(
            vision=Vision(
                fov=board.get_view(mask)
            ),
            hearing=Hearing(),
        )
