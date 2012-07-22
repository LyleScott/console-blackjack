from src.board import Board

N_PLAYERS = 3
N_DECKS = 4

def main():
    """Let's get it on..."""
    board = Board(n_players=N_PLAYERS, n_decks=N_DECKS)
    board.play()


if __name__ == '__main__':
    main()
