import copy
import dataclasses
from typing import Dict, List, Any, Optional, Iterable, NewType, AnyStr


Distance = NewType('Distance', int)


@dataclasses.dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Direction:
    x: int
    y: int

    @staticmethod
    def from_positions(pos1: Position, pos2: Position):
        x = pos2.x - pos1.x
        y = pos2.y - pos1.y
        x = 0 if x == 0 else x // abs(x)
        y = 0 if y == 0 else y // abs(y)
        return Direction(x, y)


class Board(object):

    def __init__(self, size, board: Dict[Position, Any]=None) -> None:
        if board is None:
            board = {}
        self.board = board
        self.size = size

    def move(self, pos1: Position, pos2: Position):
        if pos1 == pos2:
            return self
        board = copy.deepcopy(self.board)
        board[pos2] = board[pos1]
        del board[pos1]
        return Board(size=self.size, board=board)

    def is_empty(self, pos: Position) -> bool:
        return not bool(self.board.get(pos))

    def get_position(self, name: AnyStr) -> Optional[Position]:
        for pos, n in self.board.items():
            if name == n:
                return pos
        return None

    def is_position_in_board(self, pos: Position) -> bool:
        if (0 <= pos.x < self.size) and (0 <= pos.y < self.size):
            return True
        return False


def print_board(board: Board):
    def generate_board(size: int) -> List[List]:
        replacer = '.'
        return [
            [replacer] * size for _ in range(size)
        ]
    printed_board = generate_board(board.size)
    for pos, name in board.board.items():
        printed_board[pos.y][pos.x] = name
    print(' x ' + ''.join(map(str, range(board.size))))
    print('y')
    for number, line in zip(range(board.size), printed_board):
        line_serialized = map(str, line)
        print(str(number).zfill(2) + ' ' + ''.join(line_serialized))
    print()


def print_fov_board(board: Board, fov):
    for j in range(board.size):
        line = []
        for i in range(board.size):
            if Position(i, j) in fov:
                line.append(board.board.get(Position(i, j), '.'))
            else:
                line.append('?')
        print(line)
    print()


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
    """

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


def get_field_of_view(pos_from: Position, board: Board) -> Iterable[Position]:
    def is_visible(position: Position) -> bool:
        line = list(get_line_of_view(pos_from, position))
        for i, pos_for_check in enumerate(line):
            if i not in (0, len(line) - 1) and not board.is_empty(pos_for_check):
                return False
        return True

    positions = generate_movements(pos_from, distance=Distance(5))
    for pos in positions:
        if not board.is_position_in_board(pos):
            continue
        if is_visible(pos):
            yield pos
