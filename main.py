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
    Board         Player
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
"""

from Game import Game
from UserPlayer import UserMoves as HumanPlayer
from CompPlayer import CompPlayer as AIPlayer

boardsize = 4

game = Game(HumanPlayer(), AIPlayer(), boardsize)
game.run()