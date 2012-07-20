from collections import deque


from src.dealer import Dealer
from src.hand import Hand
from src.player import Player
from src.shoe import Shoe


class Board(object):

    def __init__(self, n_players=1, n_decks=1):
        """Initialization."""
        self.players = []
        self.generate_players(n_players)
        self.shoe = Shoe(n_decks=n_decks)
        self.turns = deque()

    def generate_players(self, n_players):
        """Generate players for the board. (includes Dealer)"""
        self.dealer = Dealer(name='D0')
        for i in range(n_players):
            name = 'P%d' % (i+1)
            self.players.append(Player(name))

    def deal(self):
        """Deal out two cards to each player."""
        # There probably aren't enough cards for a new game.
        if len(self.shoe.cards) < len(self.players) * 4:
            return False

        # Initialize dealer/player attributes to start a new hand.
        for player in self.players + [self.dealer,]:
            player.hands = [Hand(),]
            player.active = True

        # Deal each player a round of cards.
        for _ in range(2):
            for player in self.players + [self.dealer,]:
                self.turns.append(player) 
                card = self.shoe.get_card()
                player.hands[0].cards.append(card)

        # Check for dealer backjack.
        status = self.dealer.hands[0].status()
        if status and status == 'blackjack':
            self.turns = deque()
        else:
            # Move the dealer from first position to last position.
            self.turns.append(self.dealer)

        return True

    def player_stats(self):
        """Print each players stats; name, total, hand, status, etc."""
        lines = [str(player) for player in [self.dealer,] + self.players]
        return  '\n'.join(lines)
    
    def play(self):
        """TODO"""
        while self.deal():
            print('Dealing...')
            
            for player in self.players + [self.dealer,]:
                player.myturn = True
                
                for hand in player.get_active_hands():
                    
                    while hand.status() == 'active':
                    
                        print(self.player_stats())
    
                        msg = '? [H]it / [S]tand / [D]ouble Down'
                        face1 = hand.cards[0].face
                        
                        if len(hand.cards) > 1:
                            face2 = hand.cards[1].face
                            if len(hand.cards) == 2 and face1 == face2:
                                msg += ' / Sp[l]it'
                            
                        userinput = input('%s: ' % msg)
        
                        if userinput.lower().strip() == 'h':
                            hand.cards.append(self.shoe.get_card())
                        elif userinput.lower().strip() == 's':
                            hand.active = False
                            break
                        elif userinput.lower().strip() == 'd':
                            pass
                        elif userinput.lower().strip() == 'l':
                            split_card = hand.cards.pop()
                            player.hands.append(Hand(cards=split_card))

                player.myturn = False
            
            print(self.get_winners_and_losers())
            
    def get_winners_and_losers(self):
        dealer_total = self.dealer.hands[0].get_totals()[0]
        stats = []
        for player in self.players:
            for hand in player.hands:
                totals = hand.get_totals()
                
                if len(totals) > 1 and totals[1] < 21:
                    total = totals[1]
                else:
                    total = totals[0]
    
                if total > 21:
                    status = 'lose'
                elif total == dealer_total:
                    status = 'push'
                elif total <= 21 and total > dealer_total:
                    status = 'winner'
                else:
                    status = 'WTF'
                
                stats.append('%s -- %s' % (player.name, status,))
            
        return '\n'.join(stats)

    def __str__(self):
        """String representation."""
        output = []
        output.append('\nSHOE:\n')
        output.append(self.shoe)
        output.append('\n\nPLAYERS:\n')
        output.append(self.player_stats())
        
        return ''.join(output)
