from flat_matrix import FlatMatrix

EMPTY = 0
RED = 1
BLUE = 2


class Board(object):

    def __init__(self, width=5, height=5, state=None):
        if state:
            self.state = state
        else:
            self.state = FlatMatrix(width, height)

    def move(self, x, color, perform=True):
        state = self.state
        if x < state.height and state.get(x, state.height - 1) == EMPTY:
            if perform:
                y = state.height - 1
                while state.get(x, y) != EMPTY or y < 0:
                    y -= 1
                y += 1
                return state.set(x, y, color)
            return True
        return None if perform else False

    def run_terminal(self, terminal):
        return terminal(self)