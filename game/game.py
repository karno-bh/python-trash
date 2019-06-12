from board import *
from itertools import count
from player import *
from players import *
from terminals import *


def game(players, expected_in_line):
    # type: (list[Player], int) -> Nones
    replace = {
        EMPTY: '-',
        RED: 'r',
        YELLOW: 'y',
    }
    board = Board()
    for step in count(0):
        print board.state.pretty_log(replace)
        win = winner(board, expected_in_line)
        if win != 0:
            print "Game Over. Winner is {0}".format(COLOR_NAMES[win])
            break
        else:
            print "No Winner"
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