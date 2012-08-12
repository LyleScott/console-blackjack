# -*- coding: utf-8
from __future__ import unicode_literals

import random

from components.card import Card

class Deck(object):

    # How many cards to print before a line break happens.
    linebreak_index = 5

    # Map the suit to a textual representation.
    #suits = {'heart':   '\u2665',
    #         'diamond': '\u2666',
    #         'club':    '\u2667',
    #         'spade':   '\u2664',}
    suits = {'heart':   '♥',
             'diamond': '♦',
             'club':    '♧',
             'spade':   '♤',}


    def __init__(self, name='Deck', cards=None):
        """Initialization."""
        self.name = name
        self.cards = cards
        if not cards:
            self.generate_deck()

    def generate_deck(self, shuffled=True):
        """Generate a deck of 52 unshuffled cards."""
        self.cards = []
        for suit in self.suits.values():
            for value in range(1, 14):
                card = Card(suit, value)
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
