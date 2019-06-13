from board import *
from flat_matrix import *
import math


def walk_landscape_with_gravity(state):
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
    for i, j in walk_landscape_with_gravity(state_clone):
        if j == -1:
            continue
        start_val = state_clone.get(i, j)
        start_real_val = start_val >> indicators_length
        for directions_idx in range(indicators_length):
            mask = 1 << directions_idx
            direction_already_checked = mask & start_val
            if direction_already_checked:
                # print "checked debug"
                continue
            directions = DIRECTIONS_PAIRS[directions_idx]
            collected_length = 1
            # temp_val = start_val << indicators_length | mask
            temp_val = start_val | mask
            state_clone.set(i, j, temp_val, clone=False)
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
                    # state_clone.set(run_i, run_j, inspected_element << indicators_length | mask, clone=False)
                    state_clone.set(run_i, run_j, inspected_element | mask, clone=False)
                    if collected_length == expected_in_line:
                        return real_inspected_el_val
    return EMPTY


def __score(i, j, expected_type, state, height_map, expected_in_line):
    # type: (int, int, int, FlatMatrix, list[int], int) -> float
    if state.out_of_range(i, j):
        return 0.0
    observed = state.get(i, j)
    if observed == expected_type:
        return 1.0
    if observed == EMPTY:
        return 1.0 / math.pow(expected_in_line, j - height_map[i])
    return 0.0


def __construct_key(i1, j1, i2, j2):
    # type: (int, int, int, int) -> str
    if (i1 != i2 and i2 < i1) or j2 < j1:
        i1, i2 = i2, i1
        j1, j2 = j2, j1
    return "{0}_{1}__{2}_{3}".format(i1, j1, i2, j2)


def gainful_lines(board, expected_in_line):
    # type: (Board, int) -> dict[int, dict[str, list[float]]]
    """
    Gainful line is a line that can grow till the maximal number of elements
    :rtype: Dict
    """
    state_clone = FlatMatrix(
        board.state.width,
        board.state.height,
        [x for x in board.state.data]
    )
    max_vertical = state_clone.height - 1
    result = {
        RED: {},
        YELLOW: {},
    }
    height_map = [j for i, j in walk_landscape_with_gravity(state_clone)]

    for i in range(state_clone.width):
        j = max_vertical
        while j != -1 and state_clone.get(i, j) == EMPTY:
            for direction_pair in DIRECTIONS_PAIRS:
                for direction in direction_pair:
                    neighbour_i = direction[0] + i
                    neighbour_j = direction[1] + j
                    if state_clone.out_of_range(neighbour_i, neighbour_j):
                        continue
                    observed = state_clone.get(neighbour_i, neighbour_j)
                    if observed == EMPTY:
                        continue
                    inv_direction = invert_direction(direction)
                    inv_neighbour_i, inv_neighbour_j = neighbour_i, neighbour_j
                    line_values = [1.0]
                    while len(line_values) != expected_in_line:
                        next_neighbour_i = neighbour_i + direction[0]
                        next_neighbour_j = neighbour_j + direction[1]
                        next_inv_neighbour_i = inv_neighbour_i + inv_direction[0]
                        next_inv_neighbour_j = inv_neighbour_j + inv_direction[1]
                        direction_score = __score(next_neighbour_i, next_neighbour_j, observed,
                                                  state_clone, height_map, expected_in_line)
                        inv_direction_score = __score(next_inv_neighbour_i, next_inv_neighbour_j, observed,
                                                      state_clone, height_map, expected_in_line)
                        if direction_score == 0.0 and inv_direction_score == 0.0:
                            break

                        max_score = direction_score
                        if inv_direction_score > max_score:
                            max_score = inv_direction_score
                            inv_neighbour_i = next_inv_neighbour_i
                            inv_neighbour_j = next_inv_neighbour_j
                        else:
                            neighbour_i = next_neighbour_i
                            neighbour_j = next_neighbour_j
                        line_values.append(max_score)

                    if len(line_values) == expected_in_line:
                        values = result[observed]
                        key = __construct_key(neighbour_i, neighbour_j, inv_neighbour_i, inv_neighbour_j)
                        if key not in values:
                            values[key] = line_values
            j -= 1

    return result


def score_from_gainful_lines(lines_per_player):
    # type: (dict[int, dict[str, list[float]]]) -> dict[int, float]
    result = {}
    for player, player_lines in lines_per_player.iteritems():
        player_result = 0.0
        for line_coord, line_values in player_lines.iteritems():
            line_sum = sum(line_values)
            player_result += math.pow(line_sum, 2)
        result[player] = player_result
    return result


def score_from_win(winner):
    # type: (int) -> dict[int, float]
    empiric_winner_score = 100000.0
    result = {
        RED: 0.0,
        YELLOW: 0.0,
    }
    if not winner:
        return result
    result[winner] = empiric_winner_score
    return result


def combined_terminal(board, expected_in_line):
    # type: (Board, int) -> dict[int, float]
    win_state = winner(board, expected_in_line)
    if win_state:
        return score_from_win(win_state)
    return score_from_gainful_lines(gainful_lines(board, expected_in_line))

def __test_walk_landscape():
    data = [
        1, 2, 1, 1,
        1, 0, 1, 2,
        2, 0, 0, 2,
    ]
    m = FlatMatrix(4, 3, data)
    print m
    for i, j in walk_landscape_with_gravity(m):
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

def __test_win_state_2():
    data = [
        1,1,1,0,1,0,3,
        0,0,3,0,0,0,3,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
    ]
    m = FlatMatrix(7,6, data)
    print m
    b = Board(6,7,m)
    v1 = winner(b,4)
    print v1

def __text_gainful_lines():
    data1 = [
        1, 0, 1, 1,
        1, 0, 1, 3,
        1, 0, 0, 3,
        0, 0, 0, 0,
    ]
    m = FlatMatrix(4, 4, data1)
    print m
    b = Board(4,4,m)
    lines = gainful_lines(b, 4)
    print lines
    from_gainful_lines_score = score_from_gainful_lines(lines)
    print from_gainful_lines_score


def __load_map(map):
    print map
    lines = 0
    rows = 0
    first_line = True
    acc = []
    for line in map.splitlines():
        line = line.strip()
        if line:
            lines += 1
            row_vals = []
            for row in line.split(" "):
                row = row.strip()
                if row:
                    v = EMPTY
                    if row == 'r':
                        v = RED
                    elif row == 'y':
                        v = YELLOW
                    row_vals.append(v)
            if first_line:
                rows = len(row_vals)
            elif len(row_vals) != rows:
                raise Exception('Number of rows not equal to first line')
            acc += row_vals

    m = FlatMatrix(rows, lines, acc)
    print m

    flip_m = FlatMatrix(rows, lines)
    jj = 0
    for j in range(lines - 1, -1, -1):
        for i in  range(rows):
            v = m.get(i, j)
            flip_m.set(i, jj, v, clone=False)
        jj += 1

    print flip_m
    return flip_m

    pass

def __test_win_state_3():
    map = """
        - - - - - - -
        - - - r y - -
        - r y y y - -
        - y r y r - -
        - r y r y - -
        r r r y r - -
    """
    m = __load_map(map)
    b = Board(m.width, m.height, m)
    w = winner(b, 4)
    print w


if __name__ == '__main__':
    # __test_walk_landscape()
    # __test_win_state()
    # __text_gainful_lines()
    # __test_win_state_2()
    # __load_map()
    __test_win_state_3()