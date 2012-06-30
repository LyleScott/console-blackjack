
class Player(object):

    def __init__(self, name, hand=None):
        """Initialization."""
        self.name = name
        self.hand = hand or []

    def __str__(self):
        """String representation."""
        hand = ''.join([unicode(card).ljust(6, ' ') for card in self.hand])

        values = [card.value for card in self.hand]
        total = sum(values)
        if 1 in values:
            total = '%s/%s' % (total, total+10,)

        total = str(total).ljust(5, ' ')
        return '%s --> (%s) %s' % (self.name, total, hand,)
