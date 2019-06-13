#!/usr/bin/env python
# -*- coding: utf-8 -*-

from game import game
from game import players
from game import board
from game import terminals


if __name__ == '__main__':
    expected_in_line = 4
    depth = 3
    players = [players.ConsolePlayer(board.RED), players.MiniMaxPlayer(board.YELLOW, terminals.combined_terminal, depth, expected_in_line)]
    game.game(players, expected_in_line, width=7, height=6)
