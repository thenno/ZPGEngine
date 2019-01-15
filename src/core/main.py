#!/usr/bin/env python3

from core.ai import choose_action
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
            print(marine_id)
            allow_actions = {
                action.hash: action
                for action in get_allow_actions(
                    marine_id=marine_id,
                    game=game,
                )
            }
            action = choose_action(list(allow_actions.values()), randomizer=randomizer)
            if action and action.hash in allow_actions:
                game = action.apply()
                print_board(game.board)
            print(game.marines[marine_id].gaze_direction)
            input()


if __name__ == '__main__':
    main()
