from board import *
from player import *


class ConsolePlayer(Player):

    def __init__(self, color):
        super(ConsolePlayer, self).__init__(color)

    def move(self, board):  # type: (Board) -> int
        color_name = COLOR_NAMES.get(self.color) or 'Unknown'
        return int(input("You are {0}, please select a column: ".format(color_name)))


__all__= ['ConsolePlayer']