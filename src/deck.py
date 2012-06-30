import random

from src.card import Card


class Deck(object):

    # How many cards to print before a line break happens.
    linebreak_index = 5

    # Map the suit to a textual representation.
    suits = {'heart': 
                 {'black': u'\u2661',
                  'red': u'\u2665'},
             'diamond':
                 {'black': u'\u2666',
                  'red': u'\u2662'},
             'club':
                 {'black': u'\u2663',
                  'red': u'\u2667'},
             'spade':
                 {'black': u'\u2660',
                  'red': u'\u2664'},}


    def __init__(self, name='Deck', cards=None):
        """Initialization."""
        self.name = name
        self.cards = cards
        if not cards:
            self.generate_deck()

    def generate_deck(self, shuffled=True):
        """Generate a deck of 52 unshuffled cards."""
        self.cards = []
        for colorcodes in self.suits.values():
            for color in colorcodes:
                for value in xrange(1, 14):
                    card = Card(colorcodes[color], value)
                    self.cards.append(card)
                    if shuffled:
                        self.shuffle_deck()

    def shuffle_deck(self):
        """Shuffle the deck in place."""
        random.shuffle(self.cards)

    def __str__(self):
        """String representation."""
        output = []
        i = 0 
        for card in self.cards:
            if i and i % self.linebreak_index == 0:
                output.append('\n')
            i += 1

            card = str(card).ljust(7, ' ')
            output.append(card)
            
        return ''.join(output)
