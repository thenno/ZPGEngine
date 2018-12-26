#!/usr/bin/env python3

from core.ai import choose_command
from core.board import (
    Board,
    Position,
    print_board,
)
from core.randomizer import Randomizer
from core.marines import Marine
from core.actions import (
    applay_action,
    get_allow_actions,
)


def main():
    marines = {
        '1': Marine(name='1'),
        '2': Marine(name='2'),
    }
    board = Board(
        size=16,
        board={
            Position(0, 15): '1',
            Position(15, 0): '2',
        }
    )
    print_board(board)
    randomizer = Randomizer()
    while all(map(lambda x: x.alive, marines.values())):
        for player in marines.values():
            allow_actions = get_allow_actions(
                player=player.name,
                board=board,
            )
            allow_actions = list(allow_actions)
            command = choose_command(allow_actions, randomizer=randomizer)
            if command:
                board = applay_action(board, command)
                print_board(board)


if __name__ == '__main__':
    main()
