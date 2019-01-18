#!/usr/bin/env python3

from copy import deepcopy

from core.ai import choose_command
from core.game import Game
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
                Position(0, 5): 'x',
                Position(1, 5): 'x',
                Position(2, 5): 'x',
                Position(3, 5): 'x',
                Position(4, 5): 'x',
                Position(5, 5): 'x',
                Position(8, 5): 'x',
                Position(10, 5): 'x',
                Position(11, 5): 'x',
                Position(12, 5): 'x',
                Position(13, 5): 'x',
            },
        ),
        memory={
            MarineId('1'): [],
            MarineId('2'): [],
        },
        goals={
            MarineId('1'): [],
            MarineId('2'): [],
        }
    )
    print_board(game.board)
    randomizer = Randomizer()
    while all(map(lambda x: x.alive, game.marines.values())):
        for marine_id in game.marines.keys():
            print(marine_id)
            allow_commands = {
                action.to_command()
                for action in get_allow_actions(
                    marine_id=marine_id,
                    game=game,
                )
            }
            position = game.board.get_position(marine_id)
            mask = game.board.get_fov_mask(position)
            fov = game.board.get_view(mask)
            command = choose_command(
                commands=allow_commands,
                fov=fov,
                randomizer=randomizer,
                goals=game.goals,
            )
            if command in allow_commands:
                game = command.to_action(game=game).apply()
                print_board(game.board)
                print_board(game.board, mask=mask)
            print(game.marines[marine_id].gaze_direction)
            input()


if __name__ == '__main__':
    main()
