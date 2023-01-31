import pygame
from pygame.locals import *
from pygame import gfxdraw
import sys
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input
from Board import Board as board

class CheckMoves:
    def __init__(self, moves_done):
        self.moves_done = moves_done

    def is_connection(self, id1, id2):
        if(id1, id2) in self.moves_done:
            return True
        if(id2, id1) in self.moves_done:
            return True
        return False

    def is_valid(self, id1, id2, board):
        if self.is_connection(id1, id2):
            return False
        self.p1 = board[Board.id_to_index(id1)]
        self.p2 = board[Board.id_to_index(id2)]
        if (self.p1.x == self.p2.x + 100 or self.p1.x == self.p2.x - 100) and self.p1.y == self.p2.y:
            return True
        if self.p1.x == self.p2.x and (self.p1.y == self.p2.y + 100 or self.p1.y == self.p2.y - 100):
            return True
        return False

    def check_box_made(self, is_user, id1, id2):
        is_box = False

        for i, box in enumarate(boxes):
            temp = list(box[:-1])
            if id1 not in temp or id2 not in temp:
                continue
            temp.remove(id1)
            temp.remove(id2)

            if is_connection(temp[0], temp[1]) and (is_connection(id1, temp[0] and is_connection(id2, temp[1]))
            or (is_connection(id1, temp[1]) and is_connection(id2, temp[0]))):
                if is_user:
                    score += 1
                    boxes[i][4] = OWNER_USER
                else:
                    score[1] + 1
                    boxes[i][4] = OWNER_COMPUTER
                is_box = true

        return is_box

    def check_complete(self):
        possible = possible_moves()
        if len(possible) == 0:
            # game is finished!
            print("Game over")
            if score[0] > score[1]:
                print("You won! Score: {} to {}".format(score[0], score[1]))
            elif score[1] > score[0]:
                print("Computer won :( Score: {} to {}".format(score[0], score[1]))
            else:
                print("Tie game. Score: {} to {}".format(score[0], score[1]))
            input("Press enter to end game:")
            pygame.quit()

    def move_makes_box(self, id1, id2):
        is_box = False
        # check if the connection just make from id1 to id2 made a box
        for i, box in enumerate(boxes):
            temp = list(box[:-1])
            # print(temp)
            if id1 not in temp or id2 not in temp:
                continue
            # temp = list(box[:])
            temp.remove(id1)
            temp.remove(id2)
            # print(temp)
            if is_connection(temp[0], temp[1]):
                if (is_connection(id1, temp[0]) and is_connection(id2, temp[1])) or (
                        is_connection(id1, temp[1]) and is_connection(id2, temp[0])):
                    is_box = True

        return is_box

    def check_move_made_box(self, is_user, id1, id2):
        is_box = False
        # check if the connection just make from id1 to id2 made a box
        for i, box in enumerate(boxes):
            temp = list(box[:-1])
            if id1 not in temp or id2 not in temp:
                continue
            temp.remove(id1)
            temp.remove(id2)
            if is_connection(temp[0], temp[1]) and ((is_connection(id1, temp[0]) and is_connection(id2, temp[1])) or
                                                    (is_connection(id1, temp[1]) and is_connection(id2, temp[0]))):
                # yup, we just made a box
                if is_user:
                    score[0] += 1
                    boxes[i][4] = OWNER_USER
                else:
                    score[1] + 1
                    boxes[i][4] = OWNER_COMPUTER
                is_box = True

        return is_box