import copy
import dataclasses
from typing import (
    Dict,
    Optional,
    Iterable,
    NewType,
    Set,
)

from core.game_objects import GameId
from core.errors import BaseCoreError


Distance = NewType('Distance', int)


@dataclasses.dataclass(frozen=True)
class Position:
    x: int
    y: int


FOV = NewType('FOV', Dict[Position, Optional[GameId]])
PositionMask = NewType('PositionMask', Set[Position])


@dataclasses.dataclass(frozen=True)
class Direction:
    x: int
    y: int

    @staticmethod
    def from_positions(pos1: Position, pos2: Position) -> 'Direction':
        x = pos2.x - pos1.x
        y = pos2.y - pos1.y
        x = 0 if x == 0 else x // abs(x)
        y = 0 if y == 0 else y // abs(y)
        return Direction(x, y)


class Board(object):

    def __init__(self, size, board: Dict[Position, GameId]=None):
        if board is None:
            board = {}
        self.board = board
        self.size = size

    def move(self, pos1: Position, pos2: Position) -> 'Board':
        if pos1 == pos2:
            return self
        board = copy.deepcopy(self.board)
        board[pos2] = board[pos1]
        del board[pos1]
        return Board(size=self.size, board=board)

    def is_empty(self, pos: Position) -> bool:
        return not bool(self.board.get(pos))

    def get_position(self, game_id: GameId) -> Position:
        for pos, n in self.board.items():
            if game_id == n:
                return pos
        raise BaseCoreError('There is nothing by id {0}'.format(game_id))

    def is_position_in_board(self, pos: Position) -> bool:
        if (0 <= pos.x < self.size) and (0 <= pos.y < self.size):
            return True
        return False

    def get_view(self, mask: Set[Position]) -> FOV:
        return FOV({
            position: self.board.get(position)
            for position in mask
        })

    def get_fov_mask(self, position: Position) -> PositionMask:
        def is_visible(pos_to: Position) -> bool:
            line = list(get_line_of_view(position, pos_to))
            for i, pos_for_check in enumerate(line):
                if i not in (0, len(line) - 1) and not self.is_empty(pos_for_check):
                    return False
            return True

        positions = generate_movements(position, distance=Distance(5))
        result = set()
        for pos in positions:
            if not self.is_position_in_board(pos):
                continue
            if is_visible(pos):
                result.add(pos)
        return PositionMask(result)


def get_distance(pos1, pos2) -> Distance:
    return Distance(
        max(abs(pos1.x - pos2.x), abs(pos1.y - pos2.y)),
    )


def generate_movements(pos: Position, distance: Distance = Distance(1)) -> Iterable[Position]:
    for mx in range(-distance, distance + 1):
        for my in range(-distance, distance + 1):
            new_pos = Position(mx + pos.x, my + pos.y)
            yield new_pos


def get_line_of_view(pos1: Position, pos2: Position) -> Iterable[Position]:
    """
    Bresenham's line algorithm

    There may be some problems, check it again and add tests
    """

    # TODO: check it again and add tests
    delta_x = abs(pos2.x - pos1.x)
    delta_y = abs(pos2.y - pos1.y)
    if delta_x > delta_y:
        a1, b1, a2, b2 = pos1.x, pos1.y, pos2.x, pos2.y
    else:
        a1, b1, a2, b2 = pos1.y, pos1.x, pos2.y, pos2.x
    delta_a = abs(a2 - a1)
    delta_b = abs(b2 - b1)
    error = 0.0
    delta_err = delta_b / delta_a if delta_a != 0 else 0
    b = b1
    direction = b2 - b1
    if direction > 0:
        direction = 1
    if direction < 0:
        direction = -1
    if a1 < a2:
        range_a = range(a1, a2 + 1)
    else:
        range_a = range(a2, a1 + 1)[::-1]
    for a in range_a:
        if delta_x > delta_y:
            yield Position(a, b)
        else:
            yield Position(b, a)
        error = error + delta_err
        if error >= 0.5:
            b = b + direction
            error = error - 1.0
