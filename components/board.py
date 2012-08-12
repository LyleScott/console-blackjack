import string
import os

from collections import deque

import constants
from components.dealer import Dealer
from components.hand import Hand
from components.player import Player
from components.shoe import Shoe


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
                player.hands[0].add_card(card)

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
        lines = [unicode(player) for player in [self.dealer,] + self.players]
        return  '\n'.join(lines)

    def check_dealer_blackjack(self, print_stats=True):
        """Check if the dealer has blackjack."""
        hand = self.dealer.hands[0]
        if hand.status() == 'blackjack':
            if print_stats:
                self.dealer.current_hand = hand
                print(self.player_stats())
                print('\nDealer blackjack!')
                print('\n%s\n' % self.get_winners_and_losers())
            return True
        return False

    def play(self):
        """Manually step through gameplay as each player and automate the
        dealers hand.
        """
        while self.deal():
            print('Dealing...')

            # If the dealer is delt blackjack, everyone loses. :(
            if self.check_dealer_blackjack():
                continue

            for player in self.players:

                # A player can have multiple hands if they split...
                for hand in player.hands:

                    player.current_hand = hand
                    
                    print(self.player_stats())

                    while hand.active is True:

                        msg = '? [H]it / [S]tand'
                        
                        # Some games set a limit for which you have the option
                        # to double down. Enforce this if set.
                        can_double_down = (constants.CANT_DOUBLE_DOWN_AFTER < 0
                                           or hand.totals[0] <=  
                                           constants.CANT_DOUBLE_DOWN_AFTER)
                        if can_double_down is True:
                            msg += ' / [D]ouble Down'

                        face1 = hand.cards[0].face

                        # Give the option to split if the cards are the same.
                        if len(hand.cards) > 1:
                            face2 = hand.cards[1].face
                            if len(hand.cards) == 2 and face1 == face2:
                                msg += ' / Sp[l]it'

                        # Make the next move as per the user's decision.
                        userinput = raw_input('%s: ' % msg)
                        userinput = userinput.lower().strip()
                        if userinput == 'h':
                            hand.add_card(self.shoe.get_card())
                        elif userinput == 's':
                            break
                        elif userinput == 'd' and can_double_down is True:
                            pass
                        elif userinput == 'l':
                            split_card = hand.cards.pop()
                            player.hands.append(Hand(cards=split_card))
                            hand.set_totals()

                        print(self.player_stats())

                    player.current_hand = None

            # Automate the dealers hand since it has a specific set of rules.
            self.deal_dealers_hand()

            # Print the final players summary for this hand.
            print(self.player_stats())
            print('\n%s\n' % self.get_winners_and_losers())
            
            raw_input('hit any key to deal again...')

    def deal_dealers_hand(self):
        """Automate the dealer's hand."""
        hand = self.dealer.hands[0]
        self.dealer.current_hand = hand
        
        while True:
            totals = hand.totals
            print(totals)

            if len(totals) > 1 and totals[1] <= 21:
                total = totals[1]
            else:
                total = totals[0]

            if (constants.DEALERS_HITS_ON_17 and total > 17) or total >= 17:
                break

            hand.add_card(self.shoe.get_card())

    def get_winners_and_losers(self):
        """Print a list of players and their win/lose/push status."""
        totals = self.dealer.hands[0].totals
        if len(totals) > 1 and totals[1] <= 21:
            dealer_total = totals[1]
        else:
            dealer_total = totals[0]

        stats = []
        for player in self.players:
            for i, hand in enumerate(player.hands):
                totals = hand.totals

                if len(totals) > 1 and totals[1] <= 21:
                    total = totals[1]
                else:
                    total = totals[0]

                # Player's hand busted. (always a lose)
                # Player's hand is more than the dealer's hand.
                if total > 21 or (dealer_total <= 21 and dealer_total > total):
                    status = 'loser'

                # Player's hand is the same as the dealers hand.
                elif total == dealer_total:
                    status = 'push'

                # Dealer busted.
                # Player's hand is greater than the dealer's and didn't bust.
                elif dealer_total > 21 or total > dealer_total:
                    status = 'winner'

                # There exists a bug! Oh noes...
                else:
                    status = ('<unknown>: total: %d   dealer_total: %s' %
                              (total, dealer_total,))

                if len(player.hands) > 1:
                    name = '%s%s' % (player.name, string.ascii_lowercase[i],)
                else:
                    name = player.name
                name = name.ljust(3)

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
