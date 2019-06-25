from board import *
from itertools import count
from player import *
from players import *
from terminals import *


def game(players, expected_in_line, width=7, height=6):
    # type: (list[Player], int, int, int) -> None
    replace = {
        EMPTY: '-',
        RED: 'r',
        YELLOW: 'y',
    }
    # board = Board(width, height)
    map00 = """
    - - - - - - -
    - - - - - - -
    - - - r - - -
    - - y y - - -
    - r y y y - -
    r r r y r - -
    """
    map01 = """
    - - - - - - -
    - - - - - - -
    - - - - - - -
    - - - y - - -
    - - - y y - -
    - - - r r - -
    """
    map02 = """
    - - - r - - -
    - r - y - - -
    - y - r - - -
    - r - y - - -
    - y - r y - -
    - r - y r y -
    """
    map03 = """
    - - - r - - -
    - r - y - - -
    - y - r - - -
    - r - y r - -
    - y - r y - -
    - r - y r y -
    """
    m = load_map(map02)
    board = Board(m.width, m.height, m)
    # board = Board()
    for step in count(0):
        print board.state.pretty_log(replace)
        win = winner(board, expected_in_line)
        if win != EMPTY:
            print "Game Over. {0} won".format(COLOR_NAMES[win])
            break
        else:
            print "No Winner"
            has_move = False
            last_row = board.state.height - 1
            for i in range(board.state.width):
                if board.state.get(i, last_row) == EMPTY:
                    has_move = True
                    break
            if not has_move:
                print "Game Over"
                break
        player = players[step % 2]
        color = player.color
        while True:
            column = player.move(board)
            new_state = board.move(column, color)
            if new_state is not None:
                break
            print "Invalid move, please select valid column"
        board = Board(state=new_state)


if __name__ == '__main__':
    expected_in_line = 4
    depth = 3
    players = [ConsolePlayer(RED), MiniMaxPlayer(YELLOW, combined_terminal, depth, expected_in_line)]
    game(players, expected_in_line, width=7, height=6)