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

    def position_in_board(self, pos: Position) -> bool:
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
    print(' x' + ''.join(map(str, range(board.size))))
    print('y')
    for number, line in zip(range(board.size), printed_board):
        line_serialized = map(str, line)
        print(str(number).zfill(2) + ' ' + ''.join(line_serialized))
    print()


def get_distance(pos1, pos2) -> Distance:
    return Distance(
        abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y),
    )


def generate_movements(pos: Position, distance: Distance = Distance(1)) -> Iterable[Position]:
    for mx in range(-distance, distance + 1):
        for my in range(-distance, distance + 1):
            if mx == 0 and my == 0:
                continue
            new_pos = Position(mx + pos.x, my + pos.y)
            yield new_pos
