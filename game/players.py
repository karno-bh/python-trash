from board import *
from player import *


class ConsolePlayer(Player):

    def __init__(self, color):
        super(ConsolePlayer, self).__init__(color)

    def move(self, board):  # type: (Board) -> int
        color_name = COLOR_NAMES.get(self.color) or 'Unknown'
        return int(input("You are {0}, please select a column: ".format(color_name)))


class MiniMaxPlayer(Player):

    def __init__(self, color, win_terminal, score_terminal):
        super(MiniMaxPlayer, self).__init__(color)
        if not (win_terminal and score_terminal):
            raise AttributeError("Not all terminals are not provided")
        self.win_terminal = win_terminal
        self.score_terminal = score_terminal

    def move(self, board):  # type: (Board) -> int
        pass


__all__= ['ConsolePlayer']