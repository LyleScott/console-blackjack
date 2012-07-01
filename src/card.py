
class Card(object):

    # Map some values to representface cards to a 
    facemap = {1 : 'A',
               11: 'J',
               12: 'Q',
               13: 'K',}


    def __init__(self, suit, value):
        """Initialization."""
        self.suit = suit
        self.value = value
        self.rawvalue = value
        if self.value > 10:
            self.face = self.facemap[self.value]
            self.value = 10
        elif value == 1:
            self.face = self.facemap[self.value]
        else:
            self.face = value

    def __str__(self):
        """String representation."""
        return '%s-%s' % (self.suit, self.face,)
