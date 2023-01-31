"""
            Main
            game
    board         player - this class doesn't exist yet
            compPlayer  userPlayer
                        speechRec

    Structure:
    The main loop will call upon the game class to run the game
    The game class will call upon 2 classes which are:
    - board class - which maneges the drawing of the board but also checking
        if moves are valid and counting the scores.
    - player class - which handles the input of both the computer and the user
        player
    The player class then will call upon or the user player or the computer player
    The computer player will calculate the best possible move to make to always win,
        sometimes the computer will even try to crash the game to win (try the board
        at a size of 2, you will be able to win of the computer).
    The user player will all upon the speech recogintion to make a move, this is done
        by the subclass that has been made for this.
    All the speech recognition does is use the microphone to hear what you are saying
        by using the google library to be able to interpert words.

*** FOR MARIJE - DELETE BEFORE HANDING IN ***
De player class bestaat nog niet, deze moet het "tekenen"/doorgeven van beide players
kunnen handelen.

Het lijkt alsof de compPlayer alleen met de best move functie aan de slag moet, maar
dat is volgens mij niet zo. Want hij decide op een of andere manier toch iets maar ik
kon de "usages van versie 1-5 niet vinden.

Dan momenteel staat de check moves nog in een aparte class, maar deze moet terug gezet
worden in de board class.

NOG NIET ALLE FUNCTIES VAN DE MAIN STAAN IN EEN CLASS!!!
***
"""

import pygame
from pygame.locals import *
from pygame import gfxdraw
import sys
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input

import speech_recognition as sr
import pyaudio


BOARDSIZE = 4

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

OWNER_NONE = 0
OWNER_USER = 1
OWNER_COMPUTER = 2

Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])
#Box = namedtuple("Box", ["p1", "p2", "p3", "p4", "owner"])

# initialize game engine
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 50)
score_font = pygame.font.SysFont('Arial', 30)
dot_font = pygame.font.SysFont('Arial', 15)

BOX_USER = myfont.render('U', True, BLUE)
BOX_COMPUTER = myfont.render('C', True, RED)
spoke1 = [(2, 6), (10, 11), (9, 13), (4, 5)]
spoke2 = [(1, 5), (6, 7), (10, 14), (8, 9)]

# set screen width/height and caption
size = BOARDSIZE * 100 + 100
SURF = pygame.display.set_mode((size, size))
pygame.display.set_caption("Dots and  Boxes")

# initialize clock. used later in the loop.
clock = pygame.time.Clock()

# the gameboard is stored as a list of points
# points contain their number, and the number of their connections
board = []


def get_best_move_v1(possible):
    # take random from possible moves
    return choice(possible)

def get_best_move_v2(possible):
    # check if there are any possible boxes
    for p_move in possible:
        if move_makes_box(*p_move):
            # this move can make a box - take it!
            return p_move
    # ok, so there weren't any box making moves
    # now lets just take a random move
    return choice(possible)

def get_best_move_v3(possible):
    # check if there are any possible boxes
    for p_move in possible:
        if move_makes_box(*p_move):
            # this move can make a box - take it!
            return p_move
    # ok, so there weren't any box making moves
    # now lets just take a random move
    # but, we want to make sure we don't give the user a box on the next turn
    for box in boxes:
        count, not_connections = count_connections_box(box)
        # note we are checking if len(possible) > 1 because
        # even if it is a bad move, we don't want to delete our only move

        if count == 2 and len(possible) > 1:
            # this box has 2 connections - we DO NOT want to make the third
            # connection, because that would allow the user to make the
            # last connection, claiming the box
            for p_move in possible:
                if p_move in not_connections:
                    possible.remove(p_move)

    return choice(possible)

def get_best_move_v5(possible):
    # check if there are any possible boxes
    for p_move in possible:
        if move_makes_box(*p_move):
            # this move can make a box - take it!
            return p_move
    # ok, so there weren't any box making moves
    # now lets just take a random move
    # but, we want to make sure we don't give the user a box on the next turn

    for box in boxes:
        count, not_connections = count_connections_box(box)
        # note we are checking if len(possible) > 2 because
        # even if it is a bad move, we don't want to delete our only move
        if count == 2 and len(possible) > 2:
            # this box has 2 connections - we DO NOT want to make the third
            # connection, because that would allow the user to make the
            # last connection, claiming the box
            # print(possible)
            for p_move in possible:
                if p_move in not_connections:
                    # print(p_move)
                    a, b = p_move
                    possible.remove((a, b))
                    possible.remove((b, a))

    # now, we want to prioritize any spoke moves
    for p_move in possible:
        a, b = p_move
        if (a, b) in spoke1 or (b, a) in spoke1:
            return p_move
    for p_move in possible:
        a, b = p_move
        if (a, b) in spoke2 or (b, a) in spoke2:
            return p_move

    return choice(possible)


def check_complete():
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
        sys.exit()

def move_makes_box(id1, id2):
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

def check_move_made_box(is_user, id1, id2):
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

def user_move():  # The user is asked to tell the computer what he/she wants to input
    try:
        #p1, p2 = map(int, input("What move do you want to make?").split(","))
        p1, p2 = map(int, listen().split(","))

    except ValueError:
        print("Invalid move.")
        user_move()
    else:
        if is_connection(p1, p2):
            print("Sorry, this move is already taken.")
            user_move()
        elif not is_valid(p1, p2):
            print("Invalid move.")
            user_move()
        else:
            is_box = move(True, p1, p2)
            check_complete()

            if is_box:
                print("You scored! Have another turn.")
                SURF.fill((255, 255, 255))
                disp_board()
                pygame.display.update()
                check_complete()
                user_move()

def listen():
    #   Using the laptop microphone as the source
    #   listens to what is said and stores in 'audio_text' variable
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Tell me your move")
        audio_text = r.listen(source)
        print("Got it, thanks")

        #   This bit is exception handling
        #   r (recognizer method) gives a request error when the API cannot be reached
    try:
        # using google speech recognition
        speech_input = r.recognize_google(audio_text)
        print("You said: " + speech_input)
        # p1, p2 = map(int, speech_input.split(","))
        return speech_input
    except ValueError:
        print("Invalid input format. Please enter two integers separated by a comma.")
        return None
    except:
        print("Sorry, could you repeat that?")
        return None


SURF.fill((255, 255, 255))
disp_board()
pygame.display.update()

# Maak loop functie in een van de classes


# Loop until the user clicks close button
while True:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # clear the screen before drawing
    SURF.fill((255, 255, 255))
    is_user_turn = True
    disp_board()
    pygame.display.update()
    user_move()
    disp_board()
    # display what was drawn
    pygame.display.update()
    # sleep(0.5)
    is_user_turn = False
    disp_board()
    pygame.display.update()
    sleep(0.5)
    decide_and_move()
    check_complete()
    # SURF.fill((255, 255, 255))
    # disp_board()
    # pygame.display.update()
    # sleep(0.5)
    # sleep(1.5)
    # run at 20 fps
    # clock.tick(20)
