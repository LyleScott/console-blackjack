
class Player(object):

    def __init__(self, name, hand=None):
        """Initialization."""
        self.name = name
        self.hand = hand or []
        self.active = True
        self.status = ''
        self.totals = []
        self.myturn = False

    def calc_hand_total(self):
        """Calculate the total value of the hand."""
        values = [card.value for card in self.hand]
        self.totals = [sum(values),]
        if 1 in values:
            self.totals = [self.totals[0], self.totals[0] + 10]

    def calc_hand_status(self):
        """Check for various hand statuses based off the total value."""
        self.calc_hand_total()
        for total in self.totals:
            self.status = ''

            # Bust.
            if ((total > 21 and len(self.totals) == 1) or
                (self.totals[0] > 21 and self.totals[1] > 21)):
                self.status = 'bust!'
                self.active = False

            # Blackjack.
            elif len(self.hand) == 2 and total == 21:
                self.status = 'blackjack!'
                self.active = False

            # 21
            elif total == 21:
                self.status = '21!'
                self.active = False

    def printable_hand(self):
        """Return a printable string representing this players hand."""
        hand = [unicode(card).ljust(6, ' ') for card in self.hand]
        return ''.join(hand)

    def __str__(self):
        """String representation."""

        if self.myturn:
            prefix = '*'
        else:
            prefix = ' '

        self.calc_hand_status()

        total = '/'.join(map(str, self.totals))
        total = total.ljust(5, ' ')

        return '%s%s --> (%s) %s %s' % (self.name, prefix, total,
                                        self.printable_hand(), self.status)

