from components.card import Card

class Hand(object):

    def __init__(self, cards=None):
        """Initialization."""
        self.active = True
        self.bet = 0
    
        if isinstance(cards, Card):
            cards = [cards,]
        
        self.cards = cards or []    
        self.totals = self.get_totals()

    def __str__(self):
        """Return a string representing this hand."""
        hand = [unicode(card).ljust(6, ' ') for card in self.cards]
        
        return ''.join(hand)

    def get_totals(self):
        """Calculate the total value of the hand."""
        total = sum([card.value for card in self.cards])
        totals = [total,]
        
        # Ace encountered; this means there are possibly two totals
        if [card for card in self.cards if card.value == 1]:
            totals.append(total + 10)      
            
        # Try to remove useless info when there is an Ace involved.
        if len(totals) > 1:
            if totals[1] > 21:
                total = (totals[0],)
            elif totals[1] == 21:
                total = (21,)
            else:
                total = (totals[0], totals[1],)
        else:
            total = (totals[0],)
        
        return total
    
    def set_totals(self):
        """Calculate and set the totals for this object."""
        self.totals = self.get_totals()
    
    def add_card(self, card):
        """Add a card to the deck and automatically update the totals."""
        self.cards.append(card)
        self.set_totals()

    def status(self):
        """Check for various hand statuses based off the total value."""
        if self.totals[0] > 21:
            self.active = False
            status = 'bust'
        else:
            for total in self.totals:
                if len(self.cards) == 2 and total == 21: 
                    status = 'blackjack'
                    self.active = False
                    break
                elif total == 21: 
                    status = '21'
                    self.active = False
                    break
                else:
                    status = 'active'

        return status
