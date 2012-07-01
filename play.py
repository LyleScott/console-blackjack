
from src.board import Board

N_PLAYERS = 3
N_DECKS = 4

def main():
    board = Board(n_players=N_PLAYERS, n_decks=N_DECKS)

    while board.deal():
        print 'Dealing...'

        while board.turns:
            player = board.turns.popleft()
            player.myturn = True
            
            while player.active:
                print board.player_stats()
                msg = '? [H]it / [S]tand / [D]ouble Down'
                equal_cards = player.hand[0].face == player.hand[1].face 
                if len(player.hand) == 2 and equal_cards:
                    msg += ' / Sp[l]it'
                input = raw_input(msg + ': ')

                if input.lower() == 'h':
                    player.hand.append(board.shoe.get_card())
                elif input.lower() == 's':
                    player.active = False
                    break
                elif input.lower() == 'd':
                    pass

                player.calc_hand_status()

            player.myturn = False

    #print unicode(board)


if __name__ == '__main__':
    main()

