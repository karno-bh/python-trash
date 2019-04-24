#!/usr/bin/env python
# -*- coding: utf-8 -*-

from game import FlatMatrix


class Game(object):

    def __init__(self):
        print "Constructing a Game Class"

    def run(self):
        print "Running Game"


def main():
    m_ex = FlatMatrix(3,4)
    print m_ex
    m_ex.set(1,1,2)
    print m_ex
    game = Game()
    game.run()


if __name__ == '__main__':
    main()