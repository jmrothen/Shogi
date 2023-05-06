import math
import re
import numpy as np
import pandas as pd
import pygame
from pygame.locals import *

######################################################
# PYGAME SECTION

# initialize
# pygame.init()

# make window
# screen = pygame.display.set_mode((800, 600))

# background image
# background = pygame.image.load('shogiboard.png')

#######################################################
# GENERAL FUNCTIONS

# simple board representation
# goal is the make accessing editing the board easy
# just a matter of accessing an index in a vector
board = np.repeat(0, 81)

# because the board is an array, we'll depict everything with integers
# therefore we need a map from piece name to number in board
# dictionary for piece representation in array
piece_dict = {
    'p': 1,
    'g': 2,
    's': 3,
    'l': 4,
    'n': 5,
    'r': 6,
    'b': 7,
    'k': 8,
    'p+': 9,
    's+': 10,
    'n+': 11,
    'l+': 12,
    'r+': 13,
    'b+': 14
}

# let's create a nice reference df so it's easy to visualize the board positions
boardref = pd.DataFrame([[1, 2, 3, 4, 5, 6, 7, 8, 9],
                         [10, 11, 12, 13, 14, 15, 16, 17, 18],
                         [19, 20, 21, 22, 23, 24, 25, 26, 27],
                         [28, 29, 30, 31, 32, 33, 34, 35, 36],
                         [37, 38, 39, 40, 41, 42, 43, 44, 45],
                         [46, 47, 48, 49, 50, 51, 52, 53, 54],
                         [55, 56, 57, 58, 59, 60, 61, 62, 63],
                         [64, 65, 66, 67, 68, 69, 70, 71, 72],
                         [73, 74, 75, 76, 77, 78, 79, 80, 81]], columns=['9', '8', '7', '6', '5', '4', '3', '2', '1'])
boardref.index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
# this is effectively a visual map for board to end result


# Shogi has active and inactive pieces, so lets create buckets for both
white_active = list([])
black_active = list([])
white_pocket = list([])
black_pocket = list([])


# this lets us move pieces between active and inactive (pocket)


# create a function that maps the board vector to a more visual df
def printb(board=board):
    # reformat into a dataframe
    pp = pd.DataFrame(np.array([
        board[0:9], board[9:18], board[18:27],
        board[27:36], board[36:45], board[45:54],
        board[54:63], board[63:72], board[72:81]
    ]))
    # add column names
    pp.columns = ['9', '8', '7', '6', '5', '4', '3', '2', '1']
    # add row names
    pp.index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # return data frame
    return pp


# let's create functions to map from a coordinate (a7) to a board vector position
def coord_to_pos(coord):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    l = re.search(r"[a-z]", coord).group(0)
    n = int(re.search(r"[0-9]", coord).group(0))
    row = letters.index(l) + 1
    col = 10 - n
    pos = (row - 1) * 9 + col
    return pos


# and a function that maps backward if ever needed
def pos_to_coord(pos):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    row = math.ceil(pos / 9)
    row = letters[row - 1]
    col = 10 - (pos % 9)
    return f"{row}{col}"


# create a way to evaluate if a position is empty or not
def check_pos(pos):
    global board
    # if the input is a coord, we map it to position
    if type(pos) == str:
        pos = coord_to_pos(pos)
    # check if a piece is in that position
    if board[pos - 1] != 0:
        return 1
    else:
        return 0


# class for Pieces
class Piece:
    def __init__(self, color, name, pos, image=None, is_upgraded=False):
        self.color = color
        self.name = name
        self.is_upgraded = is_upgraded
        self.image = image
        if type(pos) == str:
            self.pos = coord_to_pos(pos)
        else:
            self.pos = pos

    """
    def __str__(self):
        return f"{self.color} {self.name} at {self.pos}"
    """

    def can_move(self):
        # pawns
        if self.name == 'p':
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 9])
                moves = moves[moves[0] >= 1]
                moves = moves[moves[0] <= 81]
                return moves
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos + 9])
                moves = moves[moves[0] >= 1]
                moves = moves[moves[0] <= 81]
                return moves

        # knights
        if self.name == 'n':
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 17, self.pos - 19])
                moves = moves[moves[0] >= 1]
                moves = moves[moves[0] <= 81]
                return moves
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos + 17, self.pos + 19])
                moves = moves[moves[0] >= 1]
                moves = moves[moves[0] <= 81]
                return moves

        # king
        if self.name == 'k':
            moves = pd.DataFrame([self.pos - 1, self.pos + 1,
                                  self.pos - 10, self.pos - 9,
                                  self.pos - 8, self.pos + 8,
                                  self.pos + 10, self.pos + 9])
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # golds
        if self.name in ['g', 's+', 'n+', 'l+', 'p+']:
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 1, self.pos + 1,
                                      self.pos - 10, self.pos - 9,
                                      self.pos - 8, self.pos + 9])
                moves = moves[moves[0] >= 1]
                moves = moves[moves[0] <= 81]
                return moves
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos - 1, self.pos + 1,
                                      self.pos + 10, self.pos + 9,
                                      self.pos + 8, self.pos - 9])
                moves = moves[moves[0] >= 1]
                moves = moves[moves[0] <= 81]
                return moves

        # silver
        if self.name == 's':
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 10, self.pos - 9,
                                      self.pos - 8, self.pos + 8,
                                      self.pos + 10])
                moves = moves[moves[0] >= 1]
                moves = moves[moves[0] <= 81]
                return moves
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos + 10, self.pos + 9,
                                      self.pos + 8, self.pos - 8,
                                      self.pos - 10])
                moves = moves[moves[0] >= 1]
                moves = moves[moves[0] <= 81]
                return moves

        # # # # # # # following option need a loop check

        # lance
        if self.name == 'l':
            moves = []
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 9, self.pos - 18, self.pos - 27,
                                      self.pos - 36, self.pos - 45, self.pos - 60,
                                      self.pos - 70, self.pos - 80])
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos + 9, self.pos + 18, self.pos + 27,
                                      self.pos + 36, self.pos + 45, self.pos + 60,
                                      self.pos + 70, self.pos + 80])
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            for i in moves:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break

        # bishop
        if self.name == 'b':
            moves = []
            # nw
            nw = pd.DataFrame([self.pos - 10, self.pos - 20, self.pos - 30,
                               self.pos - 40, self.pos - 50, self.pos - 60,
                               self.pos - 70, self.pos - 80])
            nw = nw[nw[0] >= 1]
            nw = nw[nw[0] <= 81]
            for i in nw:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # ne
            ne = pd.DataFrame([self.pos - 8, self.pos - 16, self.pos - 24,
                               self.pos - 32, self.pos - 40, self.pos - 48,
                               self.pos - 56, self.pos - 64])
            ne = ne[ne[0] >= 1]
            ne = ne[ne[0] <= 81]
            for i in ne:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # se
            se = pd.DataFrame([self.pos + 10, self.pos + 20, self.pos + 30,
                               self.pos + 40, self.pos + 50, self.pos + 60,
                               self.pos + 70, self.pos + 80])
            se = se[se[0] >= 1]
            se = se[se[0] <= 81]
            for i in se:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # sw
            sw = pd.DataFrame([self.pos + 8, self.pos + 16, self.pos + 24,
                               self.pos + 32, self.pos + 40, self.pos + 48,
                               self.pos + 56, self.pos + 64])
            sw = sw[sw[0] >= 1]
            sw = sw[sw[0] <= 81]
            for i in sw:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            moves = pd.DataFrame(moves)
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # rook
        if self.name == 'r':
            moves = []
            # north
            no = pd.DataFrame([self.pos - 9, self.pos - 18, self.pos - 27,
                               self.pos - 36, self.pos - 45, self.pos - 54,
                               self.pos - 63, self.pos - 72])
            no = no[no[0] >= 1]
            no = no[no[0] <= 81]
            for i in no:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # west
            we = pd.DataFrame([self.pos - 1, self.pos - 2, self.pos - 3,
                               self.pos - 4, self.pos - 5, self.pos - 6,
                               self.pos - 7, self.pos - 8])
            we = we[we[0] >= 1]
            we = we[we[0] <= 81]
            for i in we:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # east
            ea = pd.DataFrame([self.pos + 1, self.pos + 2, self.pos + 3,
                               self.pos + 4, self.pos + 5, self.pos + 6,
                               self.pos + 7, self.pos + 8])
            ea = ea[ea[0] >= 1]
            ea = ea[ea[0] <= 81]
            for i in ea:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # south
            so = pd.DataFrame([self.pos + 9, self.pos + 18, self.pos + 27,
                               self.pos + 36, self.pos + 45, self.pos + 54,
                               self.pos + 63, self.pos + 72])
            so = so[so[0] >= 1]
            so = so[so[0] <= 81]
            for i in so:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            moves = pd.DataFrame(moves)
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # dragon (r+)
        if self.name == 'r+':
            moves = []
            # north
            no = pd.DataFrame([self.pos - 9, self.pos - 18, self.pos - 27,
                               self.pos - 36, self.pos - 45, self.pos - 54,
                               self.pos - 63, self.pos - 72])
            no = no[no[0] >= 1]
            no = no[no[0] <= 81]
            for i in no:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # west
            we = pd.DataFrame([self.pos - 1, self.pos - 2, self.pos - 3,
                               self.pos - 4, self.pos - 5, self.pos - 6,
                               self.pos - 7, self.pos - 8])
            we = we[we[0] >= 1]
            we = we[we[0] <= 81]
            for i in we:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # east
            ea = pd.DataFrame([self.pos + 1, self.pos + 2, self.pos + 3,
                               self.pos + 4, self.pos + 5, self.pos + 6,
                               self.pos + 7, self.pos + 8])
            ea = ea[ea[0] >= 1]
            ea = ea[ea[0] <= 81]
            for i in ea:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # south
            so = pd.DataFrame([self.pos + 9, self.pos + 18, self.pos + 27,
                               self.pos + 36, self.pos + 45, self.pos + 54,
                               self.pos + 63, self.pos + 72])
            so = so[so[0] >= 1]
            so = so[so[0] <= 81]
            for i in so:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # extra moves
            moves.append([self.pos + 10])
            moves.append([self.pos - 10])
            moves.append([self.pos + 8])
            moves.append([self.pos - 8])

            moves = pd.DataFrame(moves)
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # horse (b+)
        if self.name == 'b+':
            moves = []
            # nw
            nw = pd.DataFrame([self.pos - 10, self.pos - 20, self.pos - 30,
                               self.pos - 40, self.pos - 50, self.pos - 60,
                               self.pos - 70, self.pos - 80])
            nw = nw[nw[0] >= 1]
            nw = nw[nw[0] <= 81]
            for i in nw:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # ne
            ne = pd.DataFrame([self.pos - 8, self.pos - 16, self.pos - 24,
                               self.pos - 32, self.pos - 40, self.pos - 48,
                               self.pos - 56, self.pos - 64])
            ne = ne[ne[0] >= 1]
            ne = ne[ne[0] <= 81]
            for i in ne:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # se
            se = pd.DataFrame([self.pos + 10, self.pos + 20, self.pos + 30,
                               self.pos + 40, self.pos + 50, self.pos + 60,
                               self.pos + 70, self.pos + 80])
            se = se[se[0] >= 1]
            se = se[se[0] <= 81]
            for i in se:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # sw
            sw = pd.DataFrame([self.pos + 8, self.pos + 16, self.pos + 24,
                               self.pos + 32, self.pos + 40, self.pos + 48,
                               self.pos + 56, self.pos + 64])
            sw = sw[sw[0] >= 1]
            sw = sw[sw[0] <= 81]
            for i in sw:
                if check_pos(i) == 0:
                    moves.append(i)
                else:
                    # check color of piece here
                    # if same color, dont append,
                    # if different color, append
                    moves.append(i)
                    break
            # add some extra stuff
            moves.append([self.pos + 1])
            moves.append([self.pos - 1])
            moves.append([self.pos + 9])
            moves.append([self.pos - 9])
            moves = pd.DataFrame(moves)
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves


# function to initialize and place a piece
def drop_piece(color, name, pos):
    # grab active lists and board since we'll be editing them
    global white_active
    global black_active
    global board
    # coord to pos just in case
    if type(pos) == str:
        pos = coord_to_pos(pos)
    # check if position is taken
    if check_pos(pos) == 1:
        return -1
    else:
        # create a new piece and add it to the colors team
        newpiece = Piece(color, name, pos)
        if color == 'w':
            white_active.append(newpiece)
        elif color == 'b':
            black_active.append(newpiece)
    board[pos - 1] = piece_dict[name]
    return 1


# function to put board in the standard starting position
def board_init():
    global board
    board = np.repeat(0, 81)
    # pawns black
    drop_piece('b', 'p', 'g9')
    drop_piece('b', 'p', 'g8')
    drop_piece('b', 'p', 'g7')
    drop_piece('b', 'p', 'g6')
    drop_piece('b', 'p', 'g5')
    drop_piece('b', 'p', 'g4')
    drop_piece('b', 'p', 'g3')
    drop_piece('b', 'p', 'g2')
    drop_piece('b', 'p', 'g1')
    # pawns white
    drop_piece('w', 'p', 'c9')
    drop_piece('w', 'p', 'c8')
    drop_piece('w', 'p', 'c7')
    drop_piece('w', 'p', 'c6')
    drop_piece('w', 'p', 'c5')
    drop_piece('w', 'p', 'c4')
    drop_piece('w', 'p', 'c3')
    drop_piece('w', 'p', 'c2')
    drop_piece('w', 'p', 'c1')
    # rooks
    drop_piece('b', 'r', 'h2')
    drop_piece('w', 'r', 'b8')
    # bishops
    drop_piece('b', 'b', 'h8')
    drop_piece('w', 'b', 'b2')
    # lances
    drop_piece('b', 'l', 'i1')
    drop_piece('b', 'l', 'i9')
    drop_piece('w', 'l', 'a9')
    drop_piece('w', 'l', 'a1')
    # knights
    drop_piece('b', 'n', 'i8')
    drop_piece('b', 'n', 'i2')
    drop_piece('w', 'n', 'a2')
    drop_piece('w', 'n', 'a8')
    # silvers
    drop_piece('b', 's', 'i7')
    drop_piece('b', 's', 'i3')
    drop_piece('w', 's', 'a3')
    drop_piece('w', 's', 'a7')
    # gold
    drop_piece('b', 'g', 'i6')
    drop_piece('b', 'g', 'i4')
    drop_piece('w', 'g', 'a6')
    drop_piece('w', 'g', 'a4')
    # kings
    drop_piece('b', 'k', 'i5')
    drop_piece('w', 'k', 'a5')


# function to perform a move
def move_piece(piece, pos):
    global board

    if type(piece) == str:
        piece = coord_to_pos(piece)
    if type(piece) == int:
        for i in white_active + black_active:
            if i.pos == piece:
                piece = i
                break

    pcol = piece.color
    tcol = ''
    tpiece = ''

    # if the input is a coord, we map it to position
    if type(pos) == str:
        pos = coord_to_pos(pos)

    # first, check if move is possible
    if pos in piece.can_move().values:
        move = 1
        # check position
        # if you have a friend on that square, it says no
        if check_pos(pos) == 1:
            for i in white_active:
                if i.pos == pos:
                    tpiece = i
                    tcol = 'w'
                    break
            if tcol == '':
                for j in black_active:
                    if j.pos == pos:
                        tpiece = j
                        tcol = 'b'
                        break
            if tcol == pcol:
                move = 0
    else:
        move = 0

    # move piece there
    if move == 1:
        board[piece.pos-1] = 0
        piece.pos = pos
        board[pos - 1] = piece_dict[piece.name]
        if tcol == 'w':
            white_active.remove(tpiece)
            white_pocket.append(tpiece)
        elif tcol == 'b':
            black_active.remove(tpiece)
            black_pocket.append(tpiece)
        return 1
    else:
        return 0


board_init()
printb()
move_piece('g8', 'f8')
printb()

"""
# game loop or something
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    screen.fill((255, 255, 255))
    screen.blit(background, (200, 0))
    board_init()
    left, middle, right = pygame.mouse.get_pressed()
    if left:
        mpos = pygame.mouse.get_pos()
    pygame.display.update()
pygame.quit()
"""