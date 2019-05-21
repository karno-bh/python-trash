from board import *
from flat_matrix import *
import math


def __walk_landscape_with_gravity(state):
    # type: (FlatMatrix) -> Generator[Tuple[int, int], None, None]
    for i in range(state.width):
        # TODO j should not start from the maximal height. The maximal height should be specified in board
        j = state.height - 1
        while j != -1 and state.get(i, j) == EMPTY:
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
    for i, j in __walk_landscape_with_gravity(state_clone):
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
                    if state_clone.out_of_range(run_i, run_j):
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


def __score(i, j, expected_type, state, height_map):
    # type: (int, int, int, FlatMatrix, list[int]) -> float
    if state.out_of_range(i, j):
        return 0.0
    observed = state.get(i, j)
    if observed == expected_type:
        return 1.0
    if observed == EMPTY:
        return 1.0 / math.pow(2, j - height_map[i] + 1)
    return 0.0


def gainful_lines(board, expected_in_line):
    """
    Gainful line is a line that can grow till the maximal number of elements
    :rtype: Dict
    """
    indicators_length = len(DIRECTIONS_PAIRS)
    state_clone = FlatMatrix(
        board.state.width,
        board.state.height,
        [x for x in board.state.data]
    )
    max_horizontal = state_clone.width - 1
    max_vertical = state_clone.height - 1
    result = {
        RED: {},
        BLUE: {},
    }
    height_map = [j for i, j in __walk_landscape_with_gravity(state_clone)]

    for i in range(state_clone.width):
        j = max_vertical
        while j != -1 and state_clone.get(i, j) == EMPTY:
            for direction_pair in DIRECTIONS_PAIRS:
                for direction in DIRECTIONS_PAIRS:
                    neighbour_i = direction[0] + i
                    neighbour_j = direction[1] + j
                    if state_clone.out_of_range(neighbour_i, neighbour_j):
                        observed = state_clone.get(neighbour_i, neighbour_j)
                        if observed == EMPTY:
                            break
                    inv_direction = invert_direction(direction)
                    inv_neighbour_i, inv_neighbour_j = neighbour_i, neighbour_j
                    direction_score = inv_direction_score = -1.0
                    line_score = 1.0
                    possible_line_length = 1
                    while (direction_score != 0.0 and inv_direction_score != 0.0)\
                            or possible_line_length == expected_in_line:
                        next_neighbour_i = neighbour_i + direction[0]
                        next_neighbour_j = neighbour_j + direction[1]
                        next_inv_neighbour_i = inv_neighbour_i + inv_direction[0]
                        next_inv_neighbour_j = inv_neighbour_j + inv_direction[1]
                        score_next_neighbour = __score(
                            next_neighbour_i,
                            next_neighbour_j,
                            observed,
                            state_clone,
                            height_map
                        )
                        score_next_inv_neighbour = __score(
                            next_inv_neighbour_i,
                            next_inv_neighbour_j,
                            observed,
                            state_clone,
                            height_map
                        )
                        max_score = score_next_neighbour
                        next_is_max = True
                        if score_next_inv_neighbour > max_score:
                            max_score = score_next_inv_neighbour
                            next_is_max = False
                        if next_is_max:
                            neighbour_i = next_neighbour_i
                            neighbour_j = next_neighbour_j
                        else:
                            inv_neighbour_i = next_inv_neighbour_i
                            inv_neighbour_j = next_inv_neighbour_j











    # for i, j in __walk_landscape(state_clone):
    #     j += 1
    #     if j > max_vertical:
    #         continue
    #     for dummy_move in [RED, BLUE]:
    #         state_clone.set(i, j, dummy_move, clone=False)
    #         for directions in DIRECTIONS_PAIRS:
    #             real_length = 1
    #             heuristic_length = 1.0
    #             l_dir = directions[0]
    #             r_dir = directions[1]
    #             l_direction_val = 1.0
    #             r_direction_val = 1.0
    #             while real_length != expected_in_line and (l_direction_val or r_direction_val):
    #                 if l_direction_val:
    #
    #                     pass
    #                 if r_direction_val:
    #                     pass
    #
    #         pass
    #     state_clone.set(i, j, EMPTY, clone=False)
    #     pass


def __test_walk_landscape():
    data = [
        1, 2, 1, 1,
        1, 0, 1, 2,
        2, 0, 0, 2,
    ]
    m = FlatMatrix(4, 3, data)
    print m
    for i, j in __walk_landscape_with_gravity(m):
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
    v1 = winner(b, 3)
    print v1


if __name__ == '__main__':
    # __test_walk_landscape()
    __test_win_state()