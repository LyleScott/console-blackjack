
from src.card import Card

class Hand(object):

    def __init__(self, cards=None):
        """Initialization."""
        
        if isinstance(cards, Card):
            cards = [cards,]
        
        self.cards = cards or []

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

    def status(self):
        """Check for various hand statuses based off the total value."""
        totals = self.get_totals()

        for total in totals:
            if ((total > 21 and len(totals) == 1) or
                (totals[0] > 21 and totals[1] > 21)):
                status = 'bust'
            elif len(self.cards) == 2 and total == 21: 
                status = 'blackjack'
                break
            elif total == 21: 
                status = '21'
                break
            else:
                status = 'active'

        return status

    def __str__(self):
        """Return a string representing this hand."""
        hand = [str(card).ljust(6, ' ') for card in self.cards]
        return ''.join(hand)
