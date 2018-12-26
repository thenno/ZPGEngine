import copy
from typing import Dict, List, Any, Optional, Iterable, NewType, AnyStr


Distance = NewType('Distance', int)


class Position(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __str__(self):
        return 'Position(x={x};y={y})'.format(x=self.x, y=self.y)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y))


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
        return pos in self.board

    def get_position(self, name: AnyStr) -> Optional[Position]:
        for pos, n in self.board.items():
            if name == n:
                return pos
        return None


def print_board(board: Board):
    def generate_board(size: int) -> List[List]:
        replacer = '.'
        return [
            [replacer] * size for _ in range(size)
        ]
    # List
    printed_board = generate_board(board.size)
    for pos, name in board.board.items():
        printed_board[pos.y][pos.x] = name
    print(' x' + ''.join(map(str, range(board.size))))
    print('y')
    for number, line in zip(range(board.size), printed_board):
        line_serialized = map(str, line)
        print(str(number) + ' ' + ''.join(line_serialized))
    print()


def get_distance(pos1, pos2) -> Distance:
    return Distance(
        abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y),
    )


def generate_movements(board: Board, pos: Position) -> Iterable[Position]:
    for mx in range(-1, 2):
        for my in range(-1, 2):
            if mx == 0 and my == 0:
                continue
            new_pos = Position(mx + pos.x, my + pos.y)
            if not ((0 <= new_pos.x < board.size) and (0 <= new_pos.y < board.size)):
                continue
            if board.is_empty(new_pos):
                continue
            yield new_pos
