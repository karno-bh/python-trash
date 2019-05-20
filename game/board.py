from flat_matrix import FlatMatrix

EMPTY = 0
RED = 1
BLUE = 3

# lower left corner is (0, 0) of board coordinate
# i.e. the board grows to north
NO_MOVE = (0,0)
NORTH = (0, 1)
EAST = (1, 0)
SOUTH = (0, -1)
WEST = (-1, 0)
NE = (1,1)
SE = (1, -1)
SW = (-1, -1)
NW = (-1, 1)

DIRECTIONS_PAIRS = [
    [EAST, WEST],
    [SE, NW],
    [SW, NE],
    [NORTH, SOUTH]
]


def invert_direction(direction):
    # type: (tuple[int, int]) -> tuple[int, int]
    return -direction[0], -direction[1]


class Board(object):

    def __init__(self, width=5, height=5, state=None):
        # type: (int, int, FlatMatrix) -> Board

        self.state = state or FlatMatrix(width, height)

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


__all__ = [
    'EMPTY', 'RED', 'BLUE',
    'NO_MOVE', 'NORTH', 'EAST', 'SOUTH', 'WEST', 'NE', 'SE', 'SW', 'NW', 'DIRECTIONS_PAIRS',
    'invert_direction',
    'Board',
]