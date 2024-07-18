import numpy as np
import pandas as pd
import math
import re

board = np.repeat(0, 81)

# because the board is an array, we'll depict everything with integers
# therefore we need a map from piece name to number in board
# dictionary for piece representation in array
piece_dict = {
    'p': 1, 'g': 2, 's': 3, 'l': 4, 'n': 5, 'r': 6, 'b': 7,
    'k': 8, 'p+': 9, 's+': 10, 'n+': 11, 'l+': 12, 'r+': 13, 'b+': 14
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
                         [73, 74, 75, 76, 77, 78, 79, 80, 81]],
                        columns=['9', '8', '7', '6', '5', '4', '3', '2', '1'])
boardref.index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


# this is effectively a visual map for board to end result


# Shogi has active and inactive pieces, so lets create buckets for both


# this lets us move pieces between active and inactive (pocket)


# create a function that maps the board vector to a more visual df
def printb(board_print =board):
    # reformat into a dataframe
    pp = pd.DataFrame(np.array([
        board_print[0:9], board_print[9:18], board_print[18:27],
        board_print[27:36], board_print[36:45], board_print[45:54],
        board_print[54:63], board_print[63:72], board_print[72:81]
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
    letter = re.search(r"[a-z]", coord).group(0)
    number = int(re.search(r"[0-9]", coord).group(0))
    row = letters.index(letter) + 1
    col = 10 - number
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
    if type(pos) is str:
        pos = coord_to_pos(pos)
    # check if a piece is in that position
    if board[pos - 1] != 0:
        return 1
    else:
        return 0
