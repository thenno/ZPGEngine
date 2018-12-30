#!/usr/bin/env python3

from core.ai import choose_command
from core.game import Game, Memory
from core.board import (
    Board,
    Position,
    Direction,
    print_board,
)
from core.randomizer import Randomizer
from core.marines import Marine, MarineId
from core.actions import (
    get_allow_actions,
)


def main():
    game = Game(
        marines={
            MarineId('1'): Marine(
                name=MarineId('1'),
                gaze_direction=Direction(-1, -1),
            ),
            MarineId('2'): Marine(
                name=MarineId('2'),
                gaze_direction=Direction(1, 1),
            ),
        },
        board=Board(
            size=16,
            board={
                Position(0, 15): '1',
                Position(15, 0): '2',
            },
        ),
        memory=Memory(
            {
                MarineId('1'): [],
                MarineId('2'): [],
            },
        ),
    )
    print_board(game.board)
    randomizer = Randomizer()
    while all(map(lambda x: x.alive, game.marines.values())):
        for marine_id in game.marines.keys():
            allow_actions = get_allow_actions(
                marine_id=marine_id,
                game=game,
            )
            allow_actions = list(allow_actions)
            command = choose_command(allow_actions, randomizer=randomizer)
            if command and command.is_valid():
                game = command.apply()
                print_board(game.board)


if __name__ == '__main__':
    main()
