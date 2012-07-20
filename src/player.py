
from collections import deque

class Player(object):
    
    HAND_STATUS_WIDTH = 9
    HAND_TOTAL_WIDTH = 5

    def __init__(self, name):
        """Initialization."""
        self.name = name
        self.hands = deque()
        self.current_hand = 0
        self.myturn = False
        
    def get_active_hands(self):
        return [hand for hand in self.hands if hand.status() == 'active']

    def __str__(self):
        """String representation."""

        output = []

        for i in range(len(self.hands)):
            if self.myturn and i == self.current_hand:
                prefix = '*'
            else:
                prefix = ' '

            is_dealer = not type(self) == Player
            if not is_dealer or self.myturn:
                hand = self.hands[i]
                hand_status = self.hands[i].status().ljust(self.HAND_STATUS_WIDTH)
                totals = hand.get_totals()
                total = '/'.join(map(str, totals)).ljust(self.HAND_TOTAL_WIDTH)
            else:
                hand = '%s    ??' % self.hands[i].cards[0]
                hand_status = '?' * self.HAND_STATUS_WIDTH
                total = '?' * self.HAND_TOTAL_WIDTH 
                
            output.append('%s%s --> [%s] (%s) %s' % (self.name, prefix,
                                                     hand_status, total, hand,))

        return '\n'.join(output)
