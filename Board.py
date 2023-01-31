import pygame
from pygame import gfxdraw

from collections import namedtuple
from builtins import input


class Board:
    def __init__(self, board_size):
        self.boardsize = board_size
        self.size = self.boardsize * 100 + 100

        self.board = []
        self.Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])

        self.OWNER_NONE = 0
        self.OWNER_USER = 1
        self.OWNER_COMPUTER = 2

        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        self.SURF = pygame.display.set_mode((self.size, self.size))

        self.my_font = pygame.font.SysFont('Arial', 50)
        self.score_font = pygame.font.SysFont('Arial', 30)
        self.dot_font = pygame.font.SysFont('Arial', 15)
        self.BOX_USER = self.my_font.render('U', True, self.BLUE)
        self.BOX_COMPUTER = self.my_font.render('C', True, self.RED)

        self.moves_done = []
        self.moves_done_persons = []
        self.score = [0, 0]  # user, computer
        self.is_user_turn = False
        self.score_user = 0
        self.boxes = []

    def update_board(self, is_user_turn):
        for i in range(self.boardsize):
            for i2 in range(self.boardsize):
                self.board.append(
                    self.Point(self.boardsize * i + i2, i2 * 100 + 100, i * 100 + 100, []))
        self.moves_done = []
        self.moves_done_persons = []
        self.boxes = [[i, i + 1, i + self.boardsize, i + self.boardsize + 1, self.OWNER_NONE] for i in range(0, 3)]
        self.boxes.extend([[i, i + 1, i + self.boardsize, i + self.boardsize + 1, self.OWNER_NONE] for i in range(4, 7)])
        self.boxes.extend([[i, i + 1, i + self.boardsize, i + self.boardsize + 1, self.OWNER_NONE] for i in range(8, 11)])
        self.score = [0, 0]  # user, computer
        self.is_user_turn = True
        return is_user_turn

    def id_to_index(self, _id):
        for i in range(len(self.board)):
            if self.board[i].id == _id:
                return i
        return -1

    def display_board(self):
        self.score_user = self.score_font.render("USER: {}".format(self.score[0]), True, self.BLUE)
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
                text_width, text_height = self.my_font.size("U")
                self.SURF.blit(self.BOX_USER, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))
            elif box[4] == self.OWNER_COMPUTER:
                text_width, text_height = self.my_font.size("C")
                self.SURF.blit(self.BOX_COMPUTER, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))

    def is_connection(self, id1, id2):
        if(id1, id2) in self.moves_done:
            return True
        if(id2, id1) in self.moves_done:
            return True
        return False

    def is_valid(self, id1, id2, board):
        if self.is_connection(id1, id2):
            return False
        p1 = board[Board.id_to_index(self, id1)]
        p2 = board[Board.id_to_index(self, id2)]
        if (p1.x == p2.x + 100 or p1.x == p2.x - 100) and p1.y == p2.y:
            return True
        if p1.x == p2.x and (p1.y == p2.y + 100 or p1.y == p2.y - 100):
            return True
        return False

    def check_box_made(self, is_user, id1, id2):
        self.is_box = False

        for i, box in enumerate(self.boxes):
            temp = list(box[:-1])
            if id1 not in temp or id2 not in temp:
                continue
            temp.remove(id1)
            temp.remove(id2)

            if self.is_connection(temp[0], temp[1]) and (self.is_connection(id1, temp[0] and self.is_connection(id2, temp[1]))
            or (self.is_connection(id1, temp[1]) and self.is_connection(id2, temp[0]))):
                if is_user:
                    self.score += 1
                    self.boxes[i][4] = self.OWNER_USER
                else:
                    self.score[1] + 1
                    self.boxes[i][4] = self.OWNER_COMPUTER
                is_box = True

        return is_box

    def check_complete(self):
        possible = self.possible_moves()
        if len(possible) == 0:
            # game is finished!
            print("Game over")
            if self.score[0] > self.score[1]:
                print("You won! Score: {} to {}".format(self.score[0], self.score[1]))
            elif self.score[1] > self.score[0]:
                print("Computer won :( Score: {} to {}".format(self.score[0], self.score[1]))
            else:
                print("Tie game. Score: {} to {}".format(self.score[0], self.score[1]))
            input("Press enter to end game:")
            pygame.quit()

    def move_makes_box(self, id1, id2):
        is_box = False
        # check if the connection just make from id1 to id2 made a box
        for i, box in enumerate(self.boxes):
            temp = list(box[:-1])
            # print(temp)
            if id1 not in temp or id2 not in temp:
                continue
            # temp = list(box[:])
            temp.remove(id1)
            temp.remove(id2)
            # print(temp)
            if self.is_connection(temp[0], temp[1]):
                if (self.is_connection(id1, temp[0]) and self.is_connection(id2, temp[1])) or (
                        self.is_connection(id1, temp[1]) and self.is_connection(id2, temp[0])):
                    is_box = True

        return is_box

    def check_move_made_box(self, is_user, id1, id2):
        is_box = False
        # check if the connection just make from id1 to id2 made a box
        for i, box in enumerate(self.boxes):
            temp = list(box[:-1])
            if id1 not in temp or id2 not in temp:
                continue
            temp.remove(id1)
            temp.remove(id2)
            if self.is_connection(temp[0], temp[1]) and ((self.is_connection(id1, temp[0]) and self.is_connection(id2, temp[1])) or
                                                    (self.is_connection(id1, temp[1]) and self.is_connection(id2, temp[0]))):
                # yup, we just made a box
                if is_user:
                    self.score[0] += 1
                    self.boxes[i][4] = self.OWNER_USER
                else:
                    self.score[1] + 1
                    self.boxes[i][4] = self.OWNER_COMPUTER
                is_box = True

        return is_box