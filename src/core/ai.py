from typing import Iterable

from core.randomizer import Randomizer
from core.actions import Action
from core.board import Position


def choose_action(actions: Iterable[Action], position: Position, fov, randomizer: Randomizer) -> Action:
    return randomizer.choice(list(actions))
