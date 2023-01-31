import pygame
from pygame.locals import *
from pygame import gfxdraw
import sys
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input

from speech_rec import Mic

class UserMoves:
    def __init__(self):
        self.p1
        self.p2


    def user_move(self):
        try:
            self.p1, self.p2 = map(int, input("What move do you want to make?").split(","))
            self.p1, self.p2 = map(int, listen().split(","))

        except ValueError:
            print("Move is not possible.")
            self.user_move();
        else:
            if connection(self.p1, self.p2):
                print("Not possible, this had already been taken.")
                self.user_move()
            elif not is_valid(self.p1, self.p2):
                print("Not possible, this move is invalid")
            else:
                self.is_box = move(True, self.p1, self.p2)
                check_complete()

                if is_box():
                    print("You scored! Have another Turn!")
                    SURF.fill((255, 255, 255))
                    disp_board()
                    pygame.display.update()
                    check_complete()
                    user_move()