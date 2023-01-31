"""
Sources:
https://github.com/coderkalyan/dots-boxes-py/blob/master/dots_boxes.py
dotsandboxes.org
https://blog.devgenius.io/dots-and-boxes-game-in-python-22058a187a84
chat.openai.com
https://replit.com/@SharkCoding/Dots-and-Boxes-Pygame?embed=true#pyproject.toml
https://mail.python.org/pipermail/tutor/2002-June/014765.html

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
