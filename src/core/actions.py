from typing import Iterable
from copy import deepcopy
from abc import ABCMeta, abstractmethod

from core.board import Position, generate_movements, Direction
from core.game import Game
from core.marines import MarineId


class Action(metaclass=ABCMeta):

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def apply(self) -> Game:
        pass

    @property
    @abstractmethod
    def hash(self):
        pass


class Walk(Action):
    def __init__(self, game: Game, pos_from: Position, pos_to: Position):
        self._pos_from = pos_from
        self._pos_to = pos_to
        self._game = game

    def apply(self) -> Game:
        game = deepcopy(self._game)
        game.board = game.board.move(self._pos_from, self._pos_to)
        marine_id = game.board.board[self._pos_to]
        game.marines[marine_id].gaze_direction = Direction.from_positions(self._pos_from, self._pos_to)
        return game

    def is_valid(self) -> bool:
        if not self._game.board.is_empty(self._pos_to):
            return False
        if not self._game.board.position_in_board(self._pos_to):
            return False
        return True

    @staticmethod
    def get_allowed(marine_id: MarineId, game: Game) -> Iterable[Action]:
        marine_pos = game.board.get_position(marine_id)
        if marine_pos is None:
            return []
        for new_pos in generate_movements(marine_pos):
            action = Walk(game, marine_pos, new_pos)
            if action.is_valid():
                yield Walk(game, marine_pos, new_pos)

    @property
    def hash(self):
        return hash(('WalkAction', self._pos_to, self._pos_to))


def get_allow_actions(marine_id: MarineId, game: Game) -> Iterable[Action]:
    return Walk.get_allowed(marine_id, game)
