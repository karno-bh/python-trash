from board import *
from itertools import count
from player import *
from players import *
from terminals import *


def game(players, expected_in_line):
    # type: (list[Player], int) -> Nones
    board = Board()
    for step in count(0):
        print board.state
        win = winner(board, expected_in_line)
        print win
        gain_lines = gainful_lines(board, expected_in_line)
        # print gain_lines
        score = score_from_gainful_lines(gain_lines)
        print score
        player = players[step % 2]
        color = player.color
        column = player.move(board)
        new_state = board.move(column, color)
        board = Board(state=new_state)


if __name__ == '__main__':
    players = [ConsolePlayer(RED), ConsolePlayer(YELLOW)]
    game(players, 4)