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
    # map = """
    # - - - - - - -
    # - - - r y - -
    # - - y y y - -
    # - - r y r - -
    # - - y r y - -
    # r r r y r - -
    # """
    # map = """
    # - - - - - - - - - -
    # - - - - - - - - - -
    # - - - - - - - - - -
    # - - - - - - - - - -
    # - - - - - - - - - -
    # - - - - - - - - - -
    # - - - - r - - - - -
    # - - - - y - - - - -
    # - - - y y - y - - -
    # - - - r y - y y - -
    # r - - y r r r y - -
    # r r - y r y r r y r
    # """
    # state = load_map(map)
    # board = Board(state.width, state.height, state)
    # board = Board(10,12)
    board = Board(width, height)
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
        # gain_lines = gainful_lines(board, expected_in_line)
        # print gain_lines
        # score = score_from_gainful_lines(gain_lines)
        # print score
        player = players[step % 2]
        color = player.color
        while True:
            column = player.move(board)
            new_state = board.move(column, color)
            if new_state is not None:
                break
            print "Invalid move, please select valid column"
        board = Board(state=new_state)