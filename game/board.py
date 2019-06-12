from flat_matrix import FlatMatrix

EMPTY = 0
RED = 1
YELLOW = 3

COLOR_NAMES = {
    EMPTY: 'Empty',
    RED: 'Red',
    YELLOW: 'Yellow',
}

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


def opponent(color):
    # type: (int) -> int
    if color == RED:
        return YELLOW
    return RED

class Board(object):

    def __init__(self, width=7, height=6, state=None):
        # type: (int, int, FlatMatrix) -> Board

        self.state = state or FlatMatrix(width, height)

    def move(self, x, color, perform=True):
        state = self.state
        if x >= 0 and x < state.width and state.get(x, state.height - 1) == EMPTY:
            if perform:
                y = state.height - 1
                while state.get(x, y) == EMPTY and y >= 0:
                    y -= 1
                y += 1
                return state.set(x, y, color)
            return True
        return None if perform else False


__all__ = [
    'EMPTY', 'RED', 'YELLOW', 'COLOR_NAMES',
    'NO_MOVE', 'NORTH', 'EAST', 'SOUTH', 'WEST', 'NE', 'SE', 'SW', 'NW', 'DIRECTIONS_PAIRS',
    'invert_direction', 'opponent',
    'Board',
]