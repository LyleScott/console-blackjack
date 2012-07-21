import string
import os

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

    def player_stats(self, clear_screen=True):
        """Print each players stats; name, total, hand, status, etc."""
        if clear_screen:
            os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        lines = [str(player) for player in [self.dealer,] + self.players]
        return  '\n'.join(lines)
    
    def play(self):
        """Play the game."""
        while self.deal():
            print('Dealing...')
            
            for player in self.players + [self.dealer,]:
                
                for hand in player.hands:
                    
                    player.current_hand = hand
                    
                    print(self.player_stats())
                    
                    while hand.active is True:
                        
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
                            break
                        elif userinput.lower().strip() == 'd':
                            pass
                        elif userinput.lower().strip() == 'l':
                            split_card = hand.cards.pop()
                            player.hands.append(Hand(cards=split_card))
                            
                        print(self.player_stats())
                            
                    player.current_hand = None
                    
            print('\n%s\n' % self.get_winners_and_losers())
            input('hit any key to deal again...')
            
    def get_winners_and_losers(self):
        """Print a list of players and their win/lose/push status."""
        dealer_total = self.dealer.hands[0].get_totals()[0]
        stats = []
        for i, player in enumerate(self.players):
            for hand in player.hands:
                totals = hand.get_totals()
                
                if len(totals) > 1 and totals[1] < 21:
                    total = totals[1]
                else:
                    total = totals[0]
    
                if total > 21 or total < dealer_total:
                    status = 'loser'
                elif total == dealer_total:
                    status = 'push'
                elif total <= 21 and total > dealer_total:
                    status = 'winner'
                else:
                    status = '<unknown>'
                
                if len(player.hands) > 1:
                    name = '%s%s' % (player.name, string.ascii_lowercase[i],)
                else:
                    name = player.name
                
                stats.append('%s -- %s' % (name, status,))
            
        return '\n'.join(stats)

    def __str__(self):
        """String representation."""
        output = []
        output.append('\nSHOE:\n')
        output.append(self.shoe)
        output.append('\n\nPLAYERS:\n')
        output.append(self.player_stats())
        
        return ''.join(output)
