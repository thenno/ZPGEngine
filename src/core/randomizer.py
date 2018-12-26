import random


class Randomizer(object):
    def random(self):
        return random.random()

    def choice(self, seq):
        return random.choice(seq)

    def randint(self, a, b):
        return random.randint(a, b)
