from abc import ABCMeta, abstractmethod
from board import *


class Player(object):
    __metaclass__ = ABCMeta

    def __init__(self, color):
        if color != RED and color != YELLOW:
            raise
        self.color = color

    @abstractmethod
    def move(self, board):
        # type: (Board) -> int
        pass


__all__ = ['Player']