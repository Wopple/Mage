MOVE = 0
ATTACK = 1

class Plan(object):
    def __init__(self, character):
        self.character = character
        self.actions = []
