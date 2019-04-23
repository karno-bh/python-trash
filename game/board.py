from flat_matrix import FlatMatrix

EMPTY = 0
RED = 1
BLUE = 2


class Board(object):

    def __init__(self, width=5, height=5):
        self.state = FlatMatrix(width, height)

    def can_move(self, x, y):
        return True