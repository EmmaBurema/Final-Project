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

    SURF = pygame.display.set_mode((size, size))

    myfont = pygame.font.SysFont('Arial', 50)
    score_font = pygame.font.SysFont('Arial', 30)
    dot_font = pygame.font.SysFont('Arial', 15)

    def __init__(self, BOARDSIZE):
        self.Boardsize = BOARDSIZE
        size = self.BOARDSIZE * 100 + 100

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
            if board[i].id == _id:
                return i
        return -1

    def disp_board(self):
        # first lets draw the score at the top
        score_user = self.score_font.render("USER: {}".format(self.score[0]), True, BLUE)
        w, h = self.score_font.size("USER: {}".format(self.score[0]))
        SURF.blit(self.score_user, (self.size // 2 - w - 10, 10))
        score_comp = score_font.render("AI: {}".format(score[1]), True, RED)
        w2, h2 = score_font.size("AI: {}".format(score[1]))
        SURF.blit(score_comp, (size // 2 + 10, 10))
        if is_user_turn:
            # pygame.draw.circle(SURF, BLUE, (size // 2 - w - 20, 10 + h // 2), 7, 0)
            gfxdraw.filled_circle(SURF, size // 2 - w - 20, 10 + h // 2, 7, BLUE)
            gfxdraw.aacircle(SURF, size // 2 - w - 20, 10 + h // 2, 7, BLUE)
        else:
            # pygame.draw.circle(SURF, RED, (size // 2 + w2 + 20, 10 + h2 // 2), 7, 0)
            gfxdraw.filled_circle(SURF, size // 2 + w2 + 20, 10 + h2 // 2, 7, RED)
            gfxdraw.aacircle(SURF, size // 2 + w2 + 20, 10 + h2 // 2, 7, RED)
        for i, move in enumerate(moves_done):
            p1 = board[id_to_index(move[0])]
            p2 = board[id_to_index(move[1])]
            thickness = 3 if move == moves_done[-1] else 1
            if moves_done_persons[i]:
                pygame.draw.line(SURF, BLUE, (p1.x, p1.y), (p2.x, p2.y), thickness)
            else:
                pygame.draw.line(SURF, RED, (p1.x, p1.y), (p2.x, p2.y), thickness)
            # for partner_id in point.partners:
            #     partner = board[id_to_index(partner_id)]
            #     pygame.draw.line(SURF, BLACK, (point.x, point.y), (partner.x, partner.y))
            # print(partner)
        for i, point in enumerate(board):
            # pygame.draw.circle(SURF, BLACK, (point.x, point.y), 5, 0)
            gfxdraw.filled_circle(SURF, point.x, point.y, 5, BLACK)
            gfxdraw.aacircle(SURF, point.x, point.y, 5, BLACK)
            dot_num = dot_font.render(str(i), True, BLACK)
            SURF.blit(dot_num, (point.x + 10, point.y - 20))
        for box in boxes:
            x1 = board[id_to_index(box[0])].x
            y1 = board[id_to_index(box[0])].y
            if box[4] == OWNER_USER:
                text_width, text_height = myfont.size("U")
                SURF.blit(BOX_USER, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))
            elif box[4] == OWNER_COMPUTER:
                text_width, text_height = myfont.size("C")
                SURF.blit(BOX_COMPUTER, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))