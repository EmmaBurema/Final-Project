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

size = BOARDSIZE * 100 + 100
SURF = pygame.display.set_mode((size, size))
pygame.display.set_caption("Dots and  Boxes")
clock = pygame.time.Clock()