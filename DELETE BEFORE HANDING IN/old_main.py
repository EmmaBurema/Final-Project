"""
gfx draw why??
less global variables, make use of classes and functions
crashed>


Dots and Boxes Solver
Version 7:
Computer tries to complete as many Boxes as Possible,
while avoiding putting in the 3rd line on a box(as this would
allow the next player to complete that box, therefore, getting the point.)
Also, tries to play spoke pattern to make sure large
"chains" do not form, as this can give the user an advantage.
New: When computer is forced to sacrifice a cell, it should analyze and
figure out which sacrifice would give the user the least points.
Notes:
* User goes first (so program can mathematically win)
"""

import pygame
from pygame import gfxdraw
import sys
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input

import speech_recognition as sr


FieldLength = 4

Black = (0, 0, 0)
Red = (255, 0, 0)
Blue = (0, 0, 255)

NoOne = 0
OwnedByUser = 1
OwnedByComputer = 2

Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])
# Box = namedtuple("Box", ["p1", "p2", "p3", "p4", "owner"])

# initialize game engine
pygame.init()
pygame.font.init()
LetterFont = pygame.font.SysFont('Arial', 50)
ScoreFont = pygame.font.SysFont('Arial', 30)
idFont = pygame.font.SysFont('Arial', 15)

UsersBox = LetterFont.render('U', True, Blue)
ComputersBox = LetterFont.render('C', True, Red)
Middle1 = [(2, 6), (10, 11), (9, 13), (4, 5)]
Middle2 = [(1, 5), (6, 7), (10, 14), (8, 9)]

# set screen width/height and caption
Length = FieldLength * 100 + 100
Search = pygame.display.set_mode((Length, Length))
pygame.display.set_caption("Dots and  Boxes vs. AI")

# initialize Seconds. used later in the loop.
Seconds = pygame.time.Clock()

# the gameField is stoRed as a list of points
# points contain their number, and the number of their connections
Field = []

for i in range(FieldLength):
    for i2 in range(FieldLength):
        # print(FieldLength * i + i2)
        Field.append(
            Point(FieldLength * i + i2, i2 * 100 + 100, i * 100 + 100, []))
LinesUsed = []
LinesUsed_persons = []
Boxes = [[i, i + 1, i + FieldLength, i + FieldLength + 1, NoOne] for i in range(0, 3)]
Boxes.extend([[i, i + 1, i + FieldLength, i + FieldLength + 1, NoOne] for i in range(4, 7)])
Boxes.extend([[i, i + 1, i + FieldLength, i + FieldLength + 1, NoOne] for i in range(8, 11)])
Score = [0, 0]  # user, computer
is_user_turn = True


# print(Boxes)
def id_to_index(_id):
    for i in range(len(Field)):
        if Field[i].id == _id:
            return i
    return -1

# print(Field)
def DisplayField():
    # first lets draw the Score at the top
    Score_user = ScoreFont.render("USER: {}".format(Score[0]), True, Blue)
    w, h = ScoreFont.size("USER: {}".format(Score[0]))
    Search.blit(Score_user, (Length // 2 - w - 10, 10))
    Score_comp = ScoreFont.render("AI: {}".format(Score[1]), True, Red)
    w2, h2 = ScoreFont.size("AI: {}".format(Score[1]))
    Search.blit(Score_comp, (Length // 2 + 10, 10))
    if is_user_turn:
        # pygame.draw.circle(Search, Blue, (Length // 2 - w - 20, 10 + h // 2), 7, 0)
        gfxdraw.filled_circle(Search, Length // 2 - w - 20, 10 + h // 2, 7, Blue)
        gfxdraw.aacircle(Search, Length // 2 - w - 20, 10 + h // 2, 7, Blue)
    else:
        # pygame.draw.circle(Search, Red, (Length // 2 + w2 + 20, 10 + h2 // 2), 7, 0)
        gfxdraw.filled_circle(Search, Length // 2 + w2 + 20, 10 + h2 // 2, 7, Red)
        gfxdraw.aacircle(Search, Length // 2 + w2 + 20, 10 + h2 // 2, 7, Red)
    for i, Move in enumerate(LinesUsed):
        p1 = Field[id_to_index(Move[0])]
        p2 = Field[id_to_index(Move[1])]
        thickness = 3 if Move == LinesUsed[-1] else 1
        if LinesUsed_persons[i]:
            pygame.draw.line(Search, Blue, (p1.x, p1.y), (p2.x, p2.y), thickness)
        else:
            pygame.draw.line(Search, Red, (p1.x, p1.y), (p2.x, p2.y), thickness)
        # for partner_id in point.partners:
        #     partner = Field[id_to_index(partner_id)]
        #     pygame.draw.line(Search, Black, (point.x, point.y), (partner.x, partner.y))
        # print(partner)
    for i, point in enumerate(Field):
        # pygame.draw.circle(Search, Black, (point.x, point.y), 5, 0)
        gfxdraw.filled_circle(Search, point.x, point.y, 5, Black)
        gfxdraw.aacircle(Search, point.x, point.y, 5, Black)
        dot_num = idFont.render(str(i), True, Black)
        Search.blit(dot_num, (point.x + 10, point.y - 20))
    for box in Boxes:
        x1 = Field[id_to_index(box[0])].x
        y1 = Field[id_to_index(box[0])].y
        if box[4] == OwnedByUser:
            text_width, text_height = LetterFont.size("U")
            Search.blit(UsersBox, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))
        elif box[4] == OwnedByComputer:
            text_width, text_height = LetterFont.size("C")
            Search.blit(ComputersBox, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))


def IsConnected(id1, id2):  # SPEECH?
    if (id1, id2) in LinesUsed:
        return True
    if (id2, id1) in LinesUsed:
        return True
    return False


def IsValid(id1, id2):
    if IsConnected(id1, id2):
        return False
    p1 = Field[id_to_index(id1)]
    p2 = Field[id_to_index(id2)]
    if (p1.x == p2.x + 100 or p1.x == p2.x - 100) and p1.y == p2.y:
        return True
    if p1.x == p2.x and (p1.y == p2.y + 100 or p1.y == p2.y - 100):
        return True
    return False
    # return ((id1, id2) not in LinesUsed and (id2, id1) not in LinesUsed) and (id2 == id1 + 1 or id2 == id1 - 1 or id2
    # == id1 + FieldLength or id2 == id1 - FieldLength)


def Move(is_user, id1, id2):  # SPEECH?
    # connects id1 and id2
    # depends on somebody else to check if Move is valid
    Field[id_to_index(id1)].partners.append(id2)
    Field[id_to_index(id2)].partners.append(id1)
    LinesUsed.append((id1, id2))
    LinesUsed_persons.append(is_user)
    return check_Move_made_box(is_user, id1, id2)


def Possible_Moves():
    Possible = []
    for a in range(1, len(Field)):
        for b in list(range(1, len(Field))):
            if b == a:
                continue
            if not IsValid(a, b):
                continue
            Possible.append((a, b))
    return Possible


def CountConnectionsBox(box):
    # counts the number of lines that exist inside given box
    # note - this is the points on the box itself, NOT an index to the box
    count = 0
    not_connections = []
    if IsConnected(box[0], box[1]):
        count += 1
    else:
        not_connections.append((box[0], box[1]))
        not_connections.append((box[1], box[0]))
    if IsConnected(box[1], box[3]):
        count += 1
    else:
        not_connections.append((box[1], box[3]))
        not_connections.append((box[3], box[1]))
    if IsConnected(box[2], box[3]):
        count += 1
    else:
        not_connections.append((box[2], box[3]))
        not_connections.append((box[3], box[2]))
    if IsConnected(box[2], box[0]):
        count += 1
    else:
        not_connections.append((box[2], box[0]))
        not_connections.append((box[0], box[2]))

    return (count, not_connections)


def get_best_Move_v1(Possible):
    # take random from Possible Moves
    return choice(Possible)


def get_best_Move_v2(Possible):
    # check if there are any Possible Boxes
    for p_Move in Possible:
        if Move_makes_box(*p_Move):
            # this Move can make a box - take it!
            return p_Move
    # ok, so there weren't any box making Moves
    # now lets just take a random Move
    return choice(Possible)


def get_best_Move_v3(Possible):
    # check if there are any Possible Boxes
    for p_Move in Possible:
        if Move_makes_box(*p_Move):
            # this Move can make a box - take it!
            return p_Move
    # ok, so there weren't any box making Moves
    # now lets just take a random Move
    # but, we want to make sure we don't give the user a box on the next turn
    for box in Boxes:
        count, not_connections = CountConnectionsBox(box)
        # note we are checking if len(Possible) > 1 because
        # even if it is a bad Move, we don't want to delete our only Move

        if count == 2 and len(Possible) > 1:
            # this box has 2 connections - we DO NOT want to make the third
            # connection, because that would allow the user to make the
            # last connection, claiming the box
            for p_Move in Possible:
                if p_Move in not_connections:
                    Possible.remove(p_Move)

    return choice(Possible)


def get_best_Move_v5(Possible):
    # check if there are any Possible Boxes
    for p_Move in Possible:
        if Move_makes_box(*p_Move):
            # this Move can make a box - take it!
            return p_Move
    # ok, so there weren't any box making Moves
    # now lets just take a random Move
    # but, we want to make sure we don't give the user a box on the next turn

    for box in Boxes:
        count, not_connections = CountConnectionsBox(box)
        # note we are checking if len(Possible) > 2 because
        # even if it is a bad Move, we don't want to delete our only Move
        if count == 2 and len(Possible) > 2:
            # this box has 2 connections - we DO NOT want to make the third
            # connection, because that would allow the user to make the
            # last connection, claiming the box
            # print(Possible)
            for p_Move in Possible:
                if p_Move in not_connections:
                    # print(p_Move)
                    a, b = p_Move
                    Possible.remove((a, b))
                    Possible.remove((b, a))

    # now, we want to prioritize any spoke Moves
    for p_Move in Possible:
        a, b = p_Move
        if (a, b) in Middle1 or (b, a) in Middle1:
            return p_Move
    for p_Move in Possible:
        a, b = p_Move
        if (a, b) in Middle2 or (b, a) in Middle2:
            return p_Move

    return choice(Possible)


def get_best_Move(Possible):
    # check if there are any Possible Boxes
    valid = Possible[:]
    for p_Move in Possible:
        if Move_makes_box(*p_Move):
            # this Move can make a box - take it!
            return p_Move
    # ok, so there weren't any box making Moves
    # now lets just take a random Move
    # but, we want to make sure we don't give the user a box on the next turn
    removed = []
    for box in Boxes:
        # print(box)
        count, not_connections = CountConnectionsBox(box)
        # note we are checking if len(Possible) > 2 because
        # even if it is a bad Move, we don't want to delete our only Move
        if count == 2:
            # this box has 2 connections - we DO NOT want to make the third
            # connection, because that would allow the user to make the
            # last connection, claiming the box
            # print(Possible)
            for p_Move in Possible:
                if p_Move in not_connections:
                    # print(p_Move)
                    a, b = p_Move
                    removed.extend([(a, b), (b, a)])
                    Possible.remove((a, b))
                    Possible.remove((b, a))

    # now, we want to prioritize any spoke Moves
    if len(Possible) > 0:
        for p_Move in Possible:
            a, b = p_Move
            if (a, b) in Middle1 or (b, a) in Middle1:
                return p_Move
        for p_Move in Possible:
            a, b = p_Move
            if (a, b) in Middle2 or (b, a) in Middle2:
                return p_Move

        # last resort: just pick a random Move
        return choice(Possible)
    else:
        # now if we have nothing left in Possible, that means we didn't have anything "safe"
        # to play this turn
        # at this point, we are forced to let the user Score
        # but still, we want to prioritize the spoke Moves
        for p_Move in removed:
            a, b = p_Move
            if (a, b) in Middle1 or (b, a) in Middle1:
                return p_Move
        for p_Move in removed:
            a, b = p_Move
            if (a, b) in Middle2 or (b, a) in Middle2:
                return p_Move

        # last resort: just pick a random Move
        return choice(removed)


def decide_and_Move():
    # randomly pick a valid Move
    Possible = Possible_Moves()
    my_choice = get_best_Move(Possible)
    # print(my_choice)
    is_box = Move(False, my_choice[0], my_choice[1])

    if is_box:
        Score[1] += 1
        Search.fill((255, 255, 255))
        DisplayField()
        pygame.display.update()
        check_complete()
        decide_and_Move()


def check_complete():
    Possible = Possible_Moves()
    if len(Possible) == 0:
        # game is finished!
        print("Game over")
        if Score[0] > Score[1]:
            print("You won! Score: {} to {}".format(Score[0], Score[1]))
        elif Score[1] > Score[0]:
            print("Computer won :( Score: {} to {}".format(Score[0], Score[1]))
        else:
            print("Tie game. Score: {} to {}".format(Score[0], Score[1]))
        input("Press enter to end game:")
        pygame.quit()
        sys.exit()


def Move_makes_box(id1, id2):
    is_box = False
    # check if the connection just make from id1 to id2 made a box
    for i, box in enumerate(Boxes):
        temp = list(box[:-1])
        # print(temp)
        if id1 not in temp or id2 not in temp:
            continue
        # temp = list(box[:])
        temp.remove(id1)
        temp.remove(id2)
        # print(temp)
        if IsConnected(temp[0], temp[1]):
            if (IsConnected(id1, temp[0]) and IsConnected(id2, temp[1])) or (
                    IsConnected(id1, temp[1]) and IsConnected(id2, temp[0])):
                is_box = True

    return is_box


def check_Move_made_box(is_user, id1, id2):
    is_box = False
    # check if the connection just make from id1 to id2 made a box
    for i, box in enumerate(Boxes): # box counts for every i
        temp = list(box[:-1])
        if id1 not in temp or id2 not in temp:
            continue
        temp.remove(id1)
        temp.remove(id2)
        if IsConnected(temp[0], temp[1]) and ((IsConnected(id1, temp[0]) and IsConnected(id2, temp[1])) or
                                                (IsConnected(id1, temp[1]) and IsConnected(id2, temp[0]))):
            # yup, we just made a box
            if is_user:
                Score[0] += 1
                Boxes[i][4] = OwnedByUser
            else:
                Score[1] + 1
                Boxes[i][4] = OwnedByComputer
            is_box = True

    return is_box


def UserMove():  # The user is asked to tell the computer what he/she wants to input
    try:
        #p1, p2 = map(int, input("What Move do you want to make?").split(","))
        response = listen()
        if isinstance(response, str):
            p1, p2 = map(int, response.split(","))
        else:
            print("Invalid Move.")
            UserMove()
            return

    except ValueError:
        print("Invalid Move.")
        UserMove()
    else:
        if IsConnected(p1, p2):
            print("Sorry, this Move is already taken.")
            UserMove()
        elif not IsValid(p1, p2):
            print("Invalid Move.")
            UserMove()
        else:
            is_box = Move(True, p1, p2)
            check_complete()

            if is_box:
                print("You Scored! Have another turn.")
                Search.fill((255, 255, 255))
                DisplayField()
                pygame.display.update()
                check_complete()
                UserMove()


def listen():
    #   Using the laptop microphone as the source
    #   listens to what is said and stores in 'audio_text' variable
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Tell me your Move")
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


Search.fill((255, 255, 255))
DisplayField()
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
    Search.fill((255, 255, 255))
    is_user_turn = True
    DisplayField()
    pygame.display.update()
    UserMove()
    DisplayField()
    # display what was drawn
    pygame.display.update()
    # sleep(0.5)
    is_user_turn = False
    DisplayField()
    pygame.display.update()
    sleep(0.5)
    decide_and_Move()
    check_complete()
    Search.fill((255, 255, 255))
    DisplayField()
    pygame.display.update()
    sleep(0.5)
    # sleep(1.5)
    # run at 20 fps
    # Seconds.tick(20)