from dataclasses import dataclass
from typing import Dict

from core.board import Board, Position
from core.game_objects import GameObject, GameId
from core.memory import Memory
from core.game_objects import Marine
from core.errors import BaseCoreError
from core.senses import Senses


@dataclass(frozen=True)
class MarineKnowledge:
    game_id: GameId
    position: Position
    memory: Memory
    senses: Senses


@dataclass
class Game:
    # TODO: game object have to construct by completed game objects
    board: Board
    memory: Dict[GameId, Memory]
    objects: Dict[GameId, GameObject]

    def get_marine_knowledge(self, game_id: GameId) -> MarineKnowledge:
        senses = Senses.feel(self.board, game_id)
        position = self.board.get_position(game_id)
        return MarineKnowledge(
            game_id=game_id,
            position=position,
            senses=senses,
            memory=self.memory[game_id],
        )

    def get_marine(self, game_id: GameId) -> Marine:
        marine_obj = self.objects[game_id]
        if not isinstance(marine_obj, Marine):
            raise BaseCoreError('There is not marine by id %s', game_id)
        return marine_obj
