from typing import Iterable
from core.actions import Command
from core.randomizer import Randomizer


def choose_command(actions: Iterable[Command], randomizer: Randomizer):
    return randomizer.choice(actions)
