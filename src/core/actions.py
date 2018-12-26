from typing import NewType, Tuple, Iterable, AnyStr

from core.board import Board, generate_movements

Action = NewType('Action', str)
ActionParams = NewType('ActionParams', tuple)
Command = NewType('Command', Tuple[Action, ActionParams])
WALK = Action('walk')
ATTACK = Action('attack')


def applay_action(board: Board, command: Command):
    action, params = command
    if action == WALK:
        return board.move(*params)


def get_allow_actions(board: Board, player: AnyStr) -> Iterable[Command]:
    player_pos = board.get_position(player)
    if player_pos is None:
        return []
    for new_pos in generate_movements(board, player_pos):
        yield Command((
            WALK, ActionParams((player_pos, new_pos)),
        ))
