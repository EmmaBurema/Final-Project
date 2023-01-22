import pygame
from pygame import gfxdraw

import sys
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input


class Board:
    board = []
    Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])

    OWNER_NONE = 0
    OWNER_USER = 1
    OWNER_COMPUTER = 2

    def __init__(self, BOARDSIZE):
        self.Boardsize = BOARDSIZE

    def updateBoard(self):
        for i in range(self.Boardsize):
            for i2 in range(self.Boardsize):
                # print(BOARDSIZE * i + i2)
                self.board.append(
                    self.Point(self.Boardsize, * i + i2, i2 * 100 + 100, i * 100 + 100, []))
        moves_done = []
        moves_done_persons = []
        boxes = [[i, i + 1, i + self.Boardsize, i + self.Boardsize + 1, self.OWNER_NONE] for i in range(0, 3)]
        boxes.extend([[i, i + 1, i + self.Boardsize, i + self.Boardsize + 1, self.OWNER_NONE] for i in range(4, 7)])
        boxes.extend([[i, i + 1, i + self.Boardsize, i + self.Boardsize + 1, self.OWNER_NONE] for i in range(8, 11)])
        score = [0, 0]  # user, computer
        is_user_turn = True