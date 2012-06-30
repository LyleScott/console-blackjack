
from src.board import Board

def main():
    board = Board(n_players=3, n_decks=1)
    board.deal()
    print unicode(board)

if __name__ == '__main__':
    main()