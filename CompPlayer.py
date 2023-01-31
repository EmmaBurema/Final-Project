import pygame
from pygame.locals import *
from pygame import gfxdraw
import sys
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input

from CheckMoves import CheckMoves

from main import is_connection


class CompPlayer:
    def __init__(self, board, score):
        self.Board = board
        self.spoke1 = [(2, 6), (10, 11), (9, 13), (4, 5)]
        self.spoke2 = [(1, 5), (6, 7), (10, 14), (8, 9)]
        self.score = score


    def possible_moves(self):
        possible = []

        for a in range(1, len(self.Board)):
            for b in list(range(1, len(self.Board))):
                if b == a:
                    continue
                if not is_valid(a, b):
                    continue
                possible.append((a, b))
            return possible

    def count_connections_box(self, box):
        count = 0
        not_connections = []

        if is_connection(box[0], box[1]):
            count += 1
        else:
            not_connections.append((box[0], box[1]))
            not_connections.append((box[1], box[0]))

        if is_connection(box[1], box[3]):
            count += 1
        else:
            not_connections.append((box[1], box[3]))
            not_connections.append((box[3], box[1]))

        if is_connection(box[2], box[3]):
            count += 1
        else:
            not_connections.append((box[2], box[3]))
            not_connections.append((box[3], box[2]))

        if is_connection(box[2], box[0]):
            count += 1
        else:
            not_connections.append((box[2], box[0]))
            not_connections.append((box[0], box[2]))

        return (count, not_connections)

    def get_best_move(self, possible):
        self.valid = possible[:]
        for p_move in possible:
            if move_makes_box(*p_move):
                return p_move
        removed = []
        for box in boxes:
            count, not_connections = self.count_connections_box(box)
            if count == 2:
                for p_move in possible:
                    if p_move in not_connections:
                        a, b = p_move
                        removed.extend([(a, b), (b, a)])
                        possible.remove((a, b))
                        possible.remove((b, a))
        if len(possible) > 0:
            for p_move in possible:
                a, b = p_move
                if (a, b) in spoke1 or (b, a) in spoke1:
                    return p_move
            for p_move in possible:
                a, b = p_move
                if (a, b) in spoke2 or (b, a) in spoke2:
                    return p_move
            return choice(possible)
        else:
            for p_move in removed:
                a, b = p_move
                if (a, b) in spoke1 or (b, a) in spoke1:
                    return p_move
            for p_move in removed:
                a, b = p_move
                if (a, b) in spoke2 or (b, a) in spoke2:
                    return p_move
            return choice(removed)

    def decide_and_move(self):
        # randomly pick a valid move
        possible = possible_moves()
        my_choice = get_best_move(possible)
        # print(my_choice)
        is_box = move(False, my_choice[0], my_choice[1])

        if is_box:
            self.score[1] += 1
            self.SURF.fill((255, 255, 255))
            disp_board()
            pygame.display.update()
            check_complete()
            decide_and_move()