import sys

from src.player import Player

class Dealer(Player):

    def __init__(self, name):
        """Initialization."""
        if sys.version < '3':
            super(Dealer, self).__init__(name)
        else:
            super().__init__(name)
