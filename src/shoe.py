import random


class Shoe(object):
    # How many cards to print before a line break happens.
    linebreak_index = 5

    def __init__(self, cards=None):
        """Initialization."""
        self.cards = cards or []

    def shuffle(self):
        """Shuffle all cards in shoe."""
        random.shuffle(self.shoe)

    def get_card(self):
        """Get a card from the top of the deck."""
        return self.cards.pop()

    def __str__(self):
        """String representation."""
        output = []
        i = 0
        for card in self.cards:
            if i and i % self.linebreak_index == 0:
                output.append('\n')
            i += 1

            card = unicode(card).ljust(7, ' ')
            output.append(card)

        return ''.join(output)
