from collections import deque

class Player(object):
    
    HAND_STATUS_WIDTH = 9
    HAND_TOTAL_WIDTH = 5

    def __init__(self, name):
        """Initialization."""
        self.name = name
        self.hands = deque()
        self.current_hand = None

    def __str__(self):
        """String representation."""
        output = []

        for hand in self.hands:
            if hand == self.current_hand:
                prefix = '*'
            else:
                prefix = ' '

            is_dealer = not type(self) == Player
            if not is_dealer or hand == self.current_hand:
                hand_status = hand.status().ljust(self.HAND_STATUS_WIDTH)
                total = '/'.join(map(str, hand.totals))
                total = total.ljust(self.HAND_TOTAL_WIDTH)
            else:
                hand = '%s    ??' % hand.cards[0]
                hand_status = '?' * self.HAND_STATUS_WIDTH
                total = '?' * self.HAND_TOTAL_WIDTH 
                
            output.append('%s%s --> [%s] (%s) %s' % (self.name, prefix,
                                                     hand_status, total, hand,))

        return '\n'.join(output)
