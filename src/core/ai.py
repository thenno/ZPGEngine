from core.randomizer import Randomizer
from core.actions import Command, Commands
from core.game import MarineKnowledge


def choose_command(commands: Commands, knowledge: MarineKnowledge, randomizer: Randomizer) -> Command:
    return randomizer.choice(list(commands))
