from typing import Set

from core.randomizer import Randomizer
from core.actions import Command, Commands, CommandWalk
from core.game import MarineKnowledge
from core.board import FOV


def choose_command(commands: Commands, knowledge: MarineKnowledge, randomizer: Randomizer) -> Command:
    # simplify implementation
    # we don't have anything except Walk
    commands = Commands(set(filter(lambda x: isinstance(x, CommandWalk), commands)))
    command = _choose_walk(commands, knowledge, randomizer)  # type: ignore
    return command


def _choose_walk(commands: Set[CommandWalk], knowledge: MarineKnowledge, randomizer: Randomizer) -> CommandWalk:
    commands = list(commands)
    if len(commands) == 1:
        return commands[0]
    for command in commands:
        if command.pos_to not in knowledge.memory.way:
            return command
    return randomizer.choice(commands)


def _is_enemy_in_fov(fov: FOV):
    return False
