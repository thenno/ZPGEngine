from typing import Iterable, Set, NewType
from copy import deepcopy
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from core.board import Position, generate_movements, Direction
from core.game import Game, GameId
from core.game_objects import Marine
from core.errors import BaseCoreError


class Command(metaclass=ABCMeta):

    @abstractmethod
    def to_action(self, game: Game) -> 'Action':
        pass


Commands = NewType('Commands', Set[Command])


class Action(metaclass=ABCMeta):

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def to_command(self) -> Command:
        pass

    @abstractmethod
    def apply(self) -> Game:
        pass


@dataclass(frozen=True)
class CommandWalk(Command):
    pos_from: Position
    pos_to: Position

    def to_action(self, game: Game) -> Action:
        return Walk(game=game, pos_to=self.pos_to, pos_from=self.pos_from)


class Walk(Action):
    def __init__(self, game: Game, pos_from: Position, pos_to: Position):
        self._pos_from = pos_from
        self._pos_to = pos_to
        self._game = game

    def apply(self) -> Game:
        game = deepcopy(self._game)
        game.board = game.board.move(self._pos_from, self._pos_to)
        game_id = game.board.board[self._pos_to]
        game.memory[game_id].way.append(self._pos_from)
        marine_obj = deepcopy(game.objects[game_id])
        if not isinstance(marine_obj, Marine):
            raise BaseCoreError('There is not marine by id %s', game_id)
        marine_obj.gaze_direction = Direction.from_positions(self._pos_from, self._pos_to)
        game.objects[game_id] = marine_obj
        return game

    def is_valid(self) -> bool:
        if not self._game.board.is_empty(self._pos_to):
            return False
        if not self._game.board.is_position_in_board(self._pos_to):
            return False
        return True

    @staticmethod
    def get_allowed(game_id: GameId, game: Game) -> Iterable[Action]:
        marine_pos = game.board.get_position(game_id)
        if marine_pos is None:
            return []
        for new_pos in generate_movements(marine_pos):
            action = Walk(game, marine_pos, new_pos)
            if action.is_valid():
                yield Walk(game, marine_pos, new_pos)

    def to_command(self) -> CommandWalk:
        return CommandWalk(pos_from=self._pos_from, pos_to=self._pos_to)


def get_allow_actions(game_id: GameId, game: Game) -> Iterable[Action]:
    return Walk.get_allowed(game_id, game)
