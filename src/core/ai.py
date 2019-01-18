from typing import Iterable

from core.randomizer import Randomizer
from core.actions import Action, Command
from core.board import Position


def choose_command(commands: Iterable[Action], goals, fov, randomizer: Randomizer) -> Command:
    return randomizer.choice(list(commands))
