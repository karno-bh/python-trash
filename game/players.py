from board import *
from player import *
import random
from terminals import *


class ConsolePlayer(Player):

    def __init__(self, color):
        super(ConsolePlayer, self).__init__(color)

    def move(self, board):  # type: (Board) -> int
        color_name = COLOR_NAMES.get(self.color) or 'Unknown'
        return int(input("You are {0}, please select a column: ".format(color_name))) - 1


class UIPlayer(Player):

    def __init__(self, color, moving_callback):
        super(UIPlayer, self).__init__(color)
        self.moving_callback = moving_callback
        self.my_state = 'waiting'

    def move(self, board):
        if self.my_state == 'waiting':
            self.my_state = 'playing'
            return -1
        if self.my_state == 'playing':
            column = self.moving_callback()
            if column == -1:
                return -1
            self.my_state = 'waiting'
            return column

class MiniMaxPlayer(Player):

    def __init__(self, color, combined_terminal, depth, expected_in_line):
        # type: (int, callable[[Board], dict[int, float]], int, int) -> None
        super(MiniMaxPlayer, self).__init__(color)
        if not combined_terminal:
            raise AttributeError("No terminal provided")
        self.game_terminal = combined_terminal
        self.depth = depth
        self.expected_in_line = expected_in_line

    def move(self, board):  # type: (Board) -> int
        min_max_move_score = self.__min_max_move(board, self.color, float('-inf'), float('+inf'), 0, -1)
        return min_max_move_score[1]

    def __is_terminal(self, board, current_depth):
        # type: (Board, int) -> tuple[bool, int]
        if current_depth == self.depth:
            return True, 0
        has_move = False
        for i, j in walk_landscape_with_gravity(board.state):
            if j != board.state.height:
                has_move = True
                break
        if not has_move:
            return True, 0
        won_player = winner(board, self.expected_in_line)
        if won_player:
            return True, won_player
        return False, 0

    def __score_map_to_score(self, score_map, depth):
        # type: (dict[int, float], int) -> float
        if self.color == RED:
            score = score_map[RED] - score_map[YELLOW]
        else:
            score = score_map[YELLOW] - score_map[RED]
        depth_correction = 0 if depth == 0 else 1 / depth
        if score > 0:
            return score + depth_correction
        return score - depth_correction

    def __min_max_move(self, board, playing_for, alpha, beta, current_depth, parent_move):
        # type: (Board, int, float, float, int, int) -> tuple[float, int]
        terminal_state = self.__is_terminal(board, current_depth)
        if terminal_state[0]:
            won_player = terminal_state[1]
            if won_player:
                winner_score = score_from_win(won_player)
                return self.__score_map_to_score(winner_score, current_depth), parent_move
            heuristic = self.game_terminal(board, self.expected_in_line)
            return self.__score_map_to_score(heuristic, 0), parent_move
        playing_indexes = [x for x in range(board.state.width)]
        random.shuffle(playing_indexes)
        height_map = [x for x in walk_landscape_with_gravity(board.state)]
        max_player = playing_for == self.color
        ret_column = -1
        val = float(max_player and '-inf' or '+inf')
        for index in playing_indexes:
            column, row = height_map[index]
            if row == board.state.height:
                continue
            moved_state = board.move(column, playing_for)
            moved_board = Board(state=moved_state)
            child_score = self.__min_max_move(moved_board, opponent(playing_for), alpha, beta, current_depth + 1, column)[0]
            if max_player:
                if child_score > val:
                    val = child_score
                    ret_column = column
                alpha = max(alpha, val)
            else:
                if child_score < val:
                    val = child_score
                    ret_column = column
                beta = min(beta, val)
            if alpha > beta:
                break
        return val, ret_column


__all__= ['ConsolePlayer', 'MiniMaxPlayer']