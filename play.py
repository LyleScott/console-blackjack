
from src.board import Board

N_PLAYERS = 3

def main():
    board = Board(n_players=N_PLAYERS, n_decks=1)

    while board.shoe.cards and [i for i in xrange(N_PLAYERS) if board.players[i].active]:
        board.deal()

        while board.turns:
            player = board.turns.popleft()
            player.myturn = True
            
            while player.active:
                print board.player_stats()
                input = raw_input('[H]it / [S]tand / [D]ouble Down? ')

                if input.lower() == 'h':
                    player.hand.append(board.shoe.get_card())
                elif input.lower() == 's':
                    player.active = False
                    break
                elif input.lower() == 'd':
                    pass

                player.calc_hand_status()

            player.myturn = False

    print unicode(board)


if __name__ == '__main__':
    main()

