import pygame
from pygame.locals import *
from pygame import gfxdraw
import sys
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input

from Board import Board
from Player import move

class Game:
    def __init__(self, player1, player2, BOARDSIZE):
        self.boardsize = BOARDSIZE
        self.size = self.broadsize * 100 + 100
        self.SURF = pygame.display.set_mode((self.size, self.size))
        self.board = Board(self.boardsize)
        self.is_user_turn
        self.player1 = player1
        self.player2 = player2

    def gameLoop(self):
        self.SURF.fill((255, 255, 255))
        self.board.disp_board()
        pygame.display.update()

        while True:
            # write event handlers here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # clear the screen before drawing
            self.SURF.fill((255, 255, 255))
            self.is_user_turn = True
            self.board.disp_board()
            pygame.display.update()
            self.player1.move()
            self.board.disp_board()
            # display what the turn that plyer 1 made
            pygame.display.update()
            self.is_user_turn = False
            self.board.disp_board()
            pygame.display.update()
            sleep(0.5)
            self.player2.move()         #used to be decide and move (AI player)
            self.board.check_complete()
            #Probeer uit te commenten
            self.SURF.fill((255, 255, 255))
            self.board.disp_board()
            pygame.display.update()
            sleep(0.5)