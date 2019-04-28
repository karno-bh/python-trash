from board import *
from flat_matrix import *


def __walk_landscape(state):
    # type: (FlatMatrix) -> Generator[Tuple[int, int], None, None]
    for i in range(state.width):
        j = state.height - 1
        while j != -1:
            if state.get(i, j) != EMPTY:
                break
            j -= 1
        yield i, j
    pass


def winner(board, expected_in_line):
    # type: (Board, int) -> int
    indicators_length = len(DIRECTIONS_PAIRS)
    state_clone = FlatMatrix(
        board.state.width,
        board.state.height,
        [x << indicators_length for x in board.state.data]
    )
    max_horizontal = state_clone.width - 1
    max_vertical = state_clone.height - 1
    for i, j in __walk_landscape(state_clone):
        if j == -1:
            continue
        start_val = state_clone.get(i, j)
        start_real_val = start_val >> indicators_length
        for directions_idx in range(indicators_length):
            mask = 1 << directions_idx
            direction_already_checked = mask & start_val
            if direction_already_checked:
                continue
            directions = DIRECTIONS_PAIRS[directions_idx]
            collected_length = 1
            state_clone.set(i, j, start_val << indicators_length | mask, clone=False)
            for direction in directions:
                run_i = i
                run_j = j
                while True:
                    run_i += direction[0]
                    run_j += direction[1]
                    if run_i < 0 or run_i > max_horizontal or run_j < 0 or run_j > max_vertical:
                        break
                    inspected_element = state_clone.get(run_i, run_j)
                    real_inspected_el_val = inspected_element >> indicators_length
                    if start_real_val != real_inspected_el_val:
                        break
                    if inspected_element & mask:
                        raise RuntimeError("Direction had to be checked in previous iterations")
                    collected_length += 1
                    state_clone.set(run_i, run_j, inspected_element << indicators_length | mask, clone=False)
                    if collected_length == expected_in_line:
                        return real_inspected_el_val
    return EMPTY


def gainful_lines(board, expected_in_line):
    """
    Gainful line is a line that can grow till the maximal number of elements by one element on iteration
    :rtype: Dict
    """
    indicators_length = len(DIRECTIONS_PAIRS)
    state_clone = FlatMatrix(
        board.state.width,
        board.state.height,
        [x << indicators_length for x in board.state.data]
    )
    max_horizontal = state_clone.width - 1
    max_vertical = state_clone.height - 1
    result = {
        RED: {},
        BLUE: {}
    }
    for i, j in __walk_landscape(state_clone):
        j += 1
        if j > max_vertical:
            continue

        pass


def __test_walk_landscape():
    data = [
        1, 2, 1, 1,
        1, 0, 1, 2,
        2, 0, 0, 2,
    ]
    m = FlatMatrix(4, 3, data)
    print m
    for i, j in __walk_landscape(m):
        print i, j


def __test_win_state():
    data1 = [
        1, 0, 1, 1,
        1, 0, 1, 3,
        1, 0, 0, 3,
        0, 0, 0, 0,
    ]
    data2 = [
        1, 3, 1, 1,
        3, 1, 1, 3,
        3, 3, 1, 3,
        0, 0, 0, 0,
    ]
    m = FlatMatrix(4, 4, data1)
    print m
    b = Board(4, 4, m)
    v1 = winner(b, 4)
    print v1


if __name__ == '__main__':
    # __test_walk_landscape()
    __test_win_state()