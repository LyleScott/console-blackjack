from src.player import Player
from src.deck import Deck
from src.shoe import Shoe


class Board(object):

    def __init__(self, n_players=1, n_decks=1):
        """Initialization."""
        self.players = []
        self.shoe = None

        self.generate_players(n_players)
        self.generate_shoe(n_decks)

    def generate_players(self, n_players):
        """Generate players for the board. (includes Dealer)"""
        self.players.append(Player(name='D0'))
        for i in xrange(n_players):
            name = 'P%d' % (i+1,)
            self.players.append(Player(name))

    def generate_shoe(self, n_decks):
        """Generate a shoe of cards from one or many decks."""
        cards = []
        for _ in xrange(n_decks):
            deck = Deck()
            cards.extend(deck.cards)
        self.shoe = Shoe(cards=cards)

    def deal(self):
        """Deal out two cards to each player."""
        for _ in xrange(2):
            for player in self.players:
                card = self.shoe.get_card()
                player.hand.append(card)

    def __str__(self):
        """String representation."""
        output = []
        output.append('\nSHOE:\n')
        output.append(unicode(self.shoe))
        output.append('\n\nPLAYERS:\n')
        for player in self.players:
            output.append(unicode(player)+'\n')
        return ''.join(output)
