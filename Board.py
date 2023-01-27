import pygame
from pygame import gfxdraw

import sys
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input

from UserPlayer import UserMoves
from CompPlayer import CompPlayer


class Board:
    def __init__(self, BOARDSIZE):
        self.Boardsize = BOARDSIZE
        self.size = self.BOARDSIZE * 100 + 100

        self.board = []
        self.Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])

        self.OWNER_NONE = 0
        self.OWNER_USER = 1
        self.OWNER_COMPUTER = 2

        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        self.SURF = pygame.display.set_mode((self.size, self.size))

        self.myfont = pygame.font.SysFont('Arial', 50)
        self.score_font = pygame.font.SysFont('Arial', 30)
        self.dot_font = pygame.font.SysFont('Arial', 15)

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

    def id_to_index(self, _id):
        for i in range(len(self.board)):
            if self.board[i].id == _id:
                return i
        return -1

    def dispay_board(self):
        # first lets draw the score at the top
        score_user = self.score_font.render("USER: {}".format(self.score[0]), True, self.BLUE)
        w, h = self.score_font.size("USER: {}".format(self.score[0]))
        self.SURF.blit(self.score_user, (self.size // 2 - w - 10, 10))
        score_comp = self.score_font.render("AI: {}".format(self.score[1]), True, self.RED)
        w2, h2 = self.score_font.size("AI: {}".format(self.score[1]))
        self.SURF.blit(score_comp, (self.size // 2 + 10, 10))
        if self.is_user_turn:
            # pygame.draw.circle(SURF, BLUE, (size // 2 - w - 20, 10 + h // 2), 7, 0)
            gfxdraw.filled_circle(self.SURF, self.size // 2 - w - 20, 10 + h // 2, 7, self.BLUE)
            gfxdraw.aacircle(self.SURF, self.size // 2 - w - 20, 10 + h // 2, 7, self.BLUE)
        else:
            # pygame.draw.circle(SURF, RED, (size // 2 + w2 + 20, 10 + h2 // 2), 7, 0)
            gfxdraw.filled_circle(self.SURF, self.size // 2 + w2 + 20, 10 + h2 // 2, 7, self.RED)
            gfxdraw.aacircle(self.SURF, self.size // 2 + w2 + 20, 10 + h2 // 2, 7, self.RED)
        for i, move in enumerate(self.moves_done):
            p1 = self.board[self.id_to_index(move[0])]
            p2 = self.board[self.id_to_index(move[1])]
            thickness = 3 if move == self.moves_done[-1] else 1
            if self.moves_done_persons[i]:
                pygame.draw.line(self.SURF, self.BLUE, (p1.x, p1.y), (p2.x, p2.y), thickness)
            else:
                pygame.draw.line(self.SURF, self.RED, (p1.x, p1.y), (p2.x, p2.y), thickness)
            # for partner_id in point.partners:
            #     partner = board[id_to_index(partner_id)]
            #     pygame.draw.line(SURF, BLACK, (point.x, point.y), (partner.x, partner.y))
            # print(partner)
        for i, point in enumerate(self.board):
            # pygame.draw.circle(SURF, BLACK, (point.x, point.y), 5, 0)
            gfxdraw.filled_circle(self.SURF, point.x, point.y, 5, self.BLACK)
            gfxdraw.aacircle(self.SURF, point.x, point.y, 5, self.BLACK)
            dot_num = self.dot_font.render(str(i), True, self.BLACK)
            self.SURF.blit(dot_num, (point.x + 10, point.y - 20))
        for box in self.boxes:
            x1 = self.board[self.id_to_index(box[0])].x
            y1 = self.board[self.id_to_index(box[0])].y
            if box[4] == self.OWNER_USER:
                text_width, text_height = self.myfont.size("U")
                self.SURF.blit(self.BOX_USER, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))
            elif box[4] == self.OWNER_COMPUTER:
                text_width, text_height = self.myfont.size("C")
                self.SURF.blit(self.BOX_COMPUTER, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))

    def gameLoop(self):
        self.SURF.fill((255, 255, 255))
        user_turn = True
        self.disp_board()
        pygame.display.update()
        UserMoves.user_move()
        self.display_board()
        pygame.display.update()
        CompPlayer.decide_and_move()