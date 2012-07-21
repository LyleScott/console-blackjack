import random

from src.deck import Deck

class Shoe(object):

    # How many cards to print before a line break happens.
    linebreak_index = 10 

    def __init__(self, n_decks=None):
        """Initialization."""
        self.cards = []
        for i in range(n_decks):
            cards = Deck().cards
            self.cards.extend(cards)

        self.cut()

    def shuffle(self):
        """Shuffle all cards in shoe."""
        random.shuffle(self.shoe)

    def cut(self):
        """Cut the deck."""
        stop = len(self.cards)
        start = int(stop * .75)
        index = random.randint(start, stop)
        section1 = self.cards[:index]
        section2 = self.cards[index:stop]
        self.cards = section2 + section1

    def get_card(self):
        """Get a card from the top of the deck."""
        if not self.cards:
            return None
        return self.cards.pop()

    def __str__(self):
        """String representation."""
        output = []
        i = 0
        for card in self.cards:
            if i and i % self.linebreak_index == 0:
                output.append('\n')
            i += 1

            card = card.ljust(7, ' ')
            output.append(card)

        return ''.join(output)

