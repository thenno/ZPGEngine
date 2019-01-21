from typing import Optional, Set, List, Dict

from core.board import Board, Position
from core.game_objects import Marine, Wall, GameObject
from core.game import GameId


def print_board(board: Board, objects: Dict[GameId, GameObject], mask: Optional[Set[Position]] = None):
    def generate_board(size: int) -> List[List]:
        replacer = '.'
        return [
            [replacer] * size for _ in range(size)
        ]
    printed_board = generate_board(board.size)
    for pos, name in board.board.items():
        if isinstance(objects[name], Marine):
            printed_board[pos.y][pos.x] = 'm'
        elif isinstance(objects[name], Wall):
            printed_board[pos.y][pos.x] = '#'
    if mask is not None:
        for y in range(board.size):
            for x in range(board.size):
                if Position(x, y) not in mask:
                    printed_board[y][x] = '?'
    print(' x ' + ''.join(map(str, range(board.size))))
    print('y')
    for number, line in zip(range(board.size), printed_board):
        line_serialized = map(str, line)
        print(str(number).zfill(2) + ' ' + ''.join(line_serialized))
    print()
