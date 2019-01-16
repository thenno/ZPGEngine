#!/usr/bin/env python3

from core.ai import choose_action
from core.game import Game, Memory
from core.board import (
    Board,
    Position,
    Direction,
    print_board,
    get_field_of_view,
    print_fov_board,
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
            print(marine_id)
            allow_actions = {
                action.hash: action
                for action in get_allow_actions(
                    marine_id=marine_id,
                    game=game,
                )
            }
            action = choose_action(
                list(allow_actions.values()),
                randomizer=randomizer,
            )
            if action and action.hash in allow_actions:
                game = action.apply()
                p = game.board.get_position(marine_id)
                fov = list(get_field_of_view(p, game.board))
                print_board(game.board)
                print_fov_board(game.board, fov)
            print(game.marines[marine_id].gaze_direction)
            input()


if __name__ == '__main__':
    main()
