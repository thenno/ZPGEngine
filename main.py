#!/usr/bin/env python3

from core.ai import choose_command
from core.game import (
    Game,
    GameId,
)
from core.board import (
    Board,
    Position,
    Direction,
)
from core.viewer import print_board
from core.randomizer import Randomizer
from core.game_objects import (
    Marine,
    MarineId,
    Wall,
)
from core.actions import (
    Commands,
    get_allow_actions,
)
from core.memory import Memory


def main():
    game = Game(
        board=Board(
            size=16,
            board={
                Position(0, 15): GameId(1),
                Position(15, 0): GameId(2),
                Position(0, 5): GameId(3),
                Position(1, 5): GameId(4),
                Position(2, 5): GameId(5),
                Position(3, 5): GameId(6),
                Position(4, 5): GameId(7),
                Position(5, 5): GameId(8),
                Position(8, 5): GameId(9),
                Position(10, 5): GameId(10),
                Position(11, 5): GameId(11),
                Position(12, 5): GameId(12),
                Position(13, 5): GameId(13),
            },
        ),
        memory={
            GameId(1): Memory(
                way=[],
                enemies={},
            ),
            GameId(2): Memory(
                way=[],
                enemies={},
            ),
        },
        objects={
            GameId(1): Marine(
                name=MarineId('1'),
                gaze_direction=Direction(-1, -1),
            ),
            GameId(2): Marine(
                name=MarineId('2'),
                gaze_direction=Direction(1, 1),
            ),
            GameId(3): Wall(),
            GameId(4): Wall(),
            GameId(5): Wall(),
            GameId(6): Wall(),
            GameId(7): Wall(),
            GameId(8): Wall(),
            GameId(9): Wall(),
            GameId(10): Wall(),
            GameId(11): Wall(),
            GameId(12): Wall(),
            GameId(13): Wall(),
        }
    )
    print_board(game.board, objects=game.objects)
    randomizer = Randomizer()
    marines = {
        game_id: obj
        for game_id, obj in game.objects.items()
        if obj.is_under_control
    }
    while all(map(lambda x: x.is_alive, marines.values())):
        for game_id in marines.keys():
            print(game_id)
            allow_commands = Commands({
                action.to_command()
                for action in get_allow_actions(
                    game_id=game_id,
                    game=game,
                )
            })
            knowledge = game.get_marine_knowledge(game_id)
            command = choose_command(
                commands=allow_commands,
                knowledge=knowledge,
                randomizer=randomizer,
            )
            if command in allow_commands:
                game = command.to_action(game=game).apply()
                print_board(game.board, objects=game.objects)
                print_board(game.board, objects=game.objects, mask=knowledge.mask)
            print(marines[game_id].gaze_direction)
            print('Memory: ', game.memory[game_id])
            input()


if __name__ == '__main__':
    main()
