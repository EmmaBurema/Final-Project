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

