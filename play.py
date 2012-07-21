import platform
import sys

from src.board import Board

N_PLAYERS = 3
N_DECKS = 1

def check_version():
    """Python 3 required to run this!"""
    pyversion = platform.python_version()
    v = int(pyversion[0])
    if v < 3:
        print('You need Python 3.x to run this.')
        sys.exit(-2)

def main():
    """Let's get it on..."""
    board = Board(n_players=N_PLAYERS, n_decks=N_DECKS)
    board.play()


if __name__ == '__main__':
    check_version()
    main()
