class Marine(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    @property
    def alive(self):
        return True

    def __str__(self):
        return self.name
