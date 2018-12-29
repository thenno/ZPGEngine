from typing import Iterable
from core.randomizer import Randomizer
from core.actions import Action


def choose_command(actions: Iterable[Action], randomizer: Randomizer) -> Action:
    return randomizer.choice(actions)
