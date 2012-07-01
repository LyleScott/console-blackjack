from collections import deque

from src.player import Player
from src.shoe import Shoe


class Board(object):

    def __init__(self, n_players=1, n_decks=1):
        """Initialization."""
        self.players = {}
        self.generate_players(n_players)
        self.shoe = Shoe(n_decks=n_decks)
        self.turns = deque()

    def generate_players(self, n_players):
        """Generate players for the board. (includes Dealer)"""
        self.players[0] = Player(name='D0')
        for i in xrange(n_players):
            index = i + 1
            name = 'P%d' % (index,)
            self.players[index] = Player(name)

    def deal(self):
        """Deal out two cards to each player."""
        # There probably aren't enough cards for a new game.
        if len(self.shoe.cards) < len(self.players) * 4:
            return

        # Deal each player a round of cards.
        for _ in xrange(2):
            for player_index in sorted(self.players.keys()):
                self.turns.append(self.players[player_index]) 
                card = self.shoe.get_card()
                self.players[player_index].hand.append(card)

        # Check for dealer backjack.
        dealer = self.turns.popleft()
        dealer.calc_hand_status()
        if dealer.status == 'blackjack!':
            self.turns = []
        else:
            # Move the dealer from first position to last position.
            self.turns.append(dealer)

    def player_stats(self):
        """Print each players stats; name, total, hand, status, etc."""
        lines = [unicode(self.players[i]) for i in self.players.keys()]
        return  '\n'.join(lines)

    def __str__(self):
        """String representation."""
        output = []
        output.append('\nSHOE:\n')
        output.append(unicode(self.shoe))
        output.append('\n\nPLAYERS:\n')
        output.append(self.player_stats())
        return ''.join(output)
