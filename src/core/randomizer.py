import random


class Randomizer:

    def random(self):
        return random.random()

    def choice(self, seq):
        return random.choice(seq)

    def randint(self, a, b):
        return random.randint(a, b)
