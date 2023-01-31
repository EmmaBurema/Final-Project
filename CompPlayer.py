import pygame
from random import choice
from Board import Board

class CompPlayer:
    def __init__(self, board, score):
        self.Board = board
        self.spoke1 = [(2, 6), (10, 11), (9, 13), (4, 5)]
        self.spoke2 = [(1, 5), (6, 7), (10, 14), (8, 9)]
        self.score = score
        self.is_valid = Board.is_valid

        self.not_connections = []


    def possible_moves(self):
        possible = []

        for a in range(1, len(self.Board)):
            for b in list(range(1, len(self.Board))):
                if b == a:
                    continue
                if not self.BoardClass.is_valid(a, b, self.Board):
                    continue
                possible.append((a, b))
            return possible

    def count_connections_box(self, box):
        # count how many lines are in the boxes
        count = 0
        if self.BoardClass.is_connection(box[0], box[1]):
            count += 1
        else:
            self.not_connections.append((box[0], box[1]))
            self.not_connections.append((box[1], box[0]))

        if self.BoardClass.is_connection(box[1], box[3]):
            count += 1
        else:
            self.not_connections.append((box[1], box[3]))
            self.not_connections.append((box[3], box[1]))

        if self.BoardClass.is_connection(box[2], box[3]):
            count += 1
        else:
            self.not_connections.append((box[2], box[3]))
            self.not_connections.append((box[3], box[2]))

        if self.BoardClass.is_connection(box[2], box[0]):
            count += 1
        else:
            self.not_connections.append((box[2], box[0]))
            self.not_connections.append((box[0], box[2]))

        return (count, self.BoardClass.not_connections)

    def get_best_move(self, possible):
        # checking for possible boxes
        self.valid = possible[:]
        for p_move in possible:
            if self.move_makes_box(*p_move):    #if it can close a box, do so
                return p_move
        removed = []
        # Making random move without giving oponent a box to close
        for box in self.boxes:
            count, self.not_connections = self.count_connections_box(box)
            if count == 2:      # two connections >> so don't make another
                for p_move in possible:
                    if p_move in self.not_connections:
                        a, b = p_move
                        removed.extend([(a, b), (b, a)])
                        possible.remove((a, b))
                        possible.remove((b, a))
        if len(possible) > 0:       # prioritizing the spoke moves
            for p_move in possible:
                a, b = p_move
                if (a, b) in self.spoke1 or (b, a) in self.spoke1:
                    return p_move
            for p_move in possible:
                a, b = p_move
                if (a, b) in self.spoke2 or (b, a) in self.spoke2:
                    return p_move
            # If everything is whack, just do something random
            return choice(possible)
        else:   # nothing left in possible
            # have to give human a box :(
            # keep prioritizing spoke moves
            for p_move in removed:
                a, b = p_move
                if (a, b) in self.spoke1 or (b, a) in self.spoke1:
                    return p_move
            for p_move in removed:
                a, b = p_move
                if (a, b) in self.spoke2 or (b, a) in self.spoke2:
                    return p_move
            # again, something random
            return choice(removed)

    def decide_and_move(self):
        # Do a random move
        possible = self.possible_moves()
        my_choice = self.get_best_move(possible)
        is_box = self.move(False, my_choice[0], my_choice[1])

        if is_box:
            self.score[1] += 1
            self.SURF.fill((255, 255, 255))
            self.board.disp_board()
            pygame.display.update()
            self.check_complete()
            self.decide_and_move()