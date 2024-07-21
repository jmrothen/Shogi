import pandas as pd
import math
import re


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


def clean_coord(position):
    if type(position) is str:
        return coord_to_pos(coord=position)
    else:
        return position


def is_pos(num):
    if num > 0:
        return True
    elif num < 0:
        return False
    else:
        return []


# take position, return the 0-index row column
def pos_to_xy(pos):
    pos = clean_coord(pos)
    row = math.floor((pos - 1) / 9)
    col = (pos - 1) % 9
    return [row, col]


# class for Pieces
class Piece:
    def __init__(self, color, role, pos, is_upgraded=False, is_alive=True):
        self.color = color
        self.role = role
        self.pos = clean_coord(pos)
        # self.image = image
        self.is_upgraded = is_upgraded
        self.is_alive = is_alive

    # add a simple function that prints the piece's traits
    def __str__(self):
        color_long = "Black" if self.color == 'b' else "White"
        upgraded_status = " promoted " if self.is_upgraded else ""
        match self.role:
            case 'p': role = "pawn"
            case 'r': role = "rook"
            case 'b': role = "bishop"
            case 'l': role = "lance"
            case 'n': role = "knight"
            case 's': role = "silver"
            case 'g': role = "gold"
            case 'k': role = "king"
        alive_status = f"at {pos_to_coord(self.pos)}" if self.is_alive else "dead"
        return f"{color_long} {upgraded_status}{self.role} {alive_status}"

    def legal_moves(self):
        direction = -9 if self.color == 'b' else 9
        moves = []

        if self.role == 'p' and not self.is_upgraded:
            moves.append(self.pos + direction)
        elif self.role == 'n':
            moves.extend([self.pos + direction * 2 - 1, self.pos + direction * 2 + 1])
        elif self.role == 'k':
            moves.extend([self.pos + i for i in [-1, 1, -10, -9, -8, 8, 9, 10]])
        elif self.role in ['g'] or (self.role in ['s', 'n', 'l', 'p'] and self.is_upgraded):
            if self.color == 'b':
                moves.extend([self.pos + i for i in [-1, 1, -10, -9, -8, 9]])
            elif self.color == 'w':
                moves.extend([self.pos + i for i in [1, -1, 10, 9, 8, -9]])
        elif self.role == 's':
            if self.color == 'b':
                moves.extend([self.pos + i for i in [-10, -9, -8, 8, 10]])
            elif self.color == 'w':
                moves.extend([self.pos + i for i in [10, 9, 8, -8, -10]])
        elif self.role == 'l':
            moves.extend([self.pos + direction * i for i in range(1, 10)])
        elif self.role in ['b', 'r', 'r+', 'b+']:
            for i in range(1, 10):
                if self.role in ['b', 'b+']:
                    moves.extend([self.pos + i * (-10), self.pos + i * (-8), self.pos + i * 10, self.pos + i * 8])
                if self.role in ['r', 'r+']:
                    moves.extend([self.pos + i * (-9), self.pos + i * (-1), self.pos + i * 1, self.pos + i * 9])
            if self.role in ['r+', 'b+']:
                moves.extend([self.pos + i for i in [-1, 1, -9, 9]])

        # Filter out-of-bounds moves
        moves = [move for move in moves if 1 <= move <= 81]
        return pd.DataFrame(moves)

    def kill(self):
        # swap colors
        if self.color == 'w':
            self.color = 'b'
        else:
            self.color = 'w'
        # move to dead
        self.is_alive = False

    def can_promote(self):
        if self.role in ['k', 'g']:
            return False
        return True

    def promote(self):
        if self.can_promote():
            self.is_upgraded = True
        else:
            ValueError("illegal move: cannot promote this piece")

    def place(self, pos):
        self.pos = pos
        self.is_alive = True

    def shorthand(self):
        match (self.role, self.is_upgraded):
            case (*a, False):
                out = ''.join(a)
            case (*a, True):
                out = ''.join(a) + '+'
            case _:
                out = "error"
        return out


# end class stuff


def create_piece_array():
    piece_types = [
        ('b', 'p', ['g9', 'g8', 'g7', 'g6', 'g5', 'g4', 'g3', 'g2', 'g1']),
        ('w', 'p', ['c9', 'c8', 'c7', 'c6', 'c5', 'c4', 'c3', 'c2', 'c1']),
        ('b', 'r', ['h2']),
        ('w', 'r', ['b8']),
        ('b', 'b', ['h8']),
        ('w', 'b', ['b2']),
        ('b', 'l', ['i1', 'i9']),
        ('w', 'l', ['a9', 'a1']),
        ('b', 'n', ['i8', 'i2']),
        ('w', 'n', ['a2', 'a8']),
        ('b', 's', ['i7', 'i3']),
        ('w', 's', ['a3', 'a7']),
        ('b', 'g', ['i6', 'i4']),
        ('w', 'g', ['a6', 'a4']),
        ('b', 'k', ['i5']),
        ('w', 'k', ['a5'])
    ]
    piece_array = [Piece(color, role, pos) for color, role, positions in piece_types for pos in positions]
    return piece_array


# function to check a pos (bool)
def check_pos(piece_array, pos):
    for i in piece_array:
        if i.pos == pos and i.is_alive:
            return True
    return False


# function to find what piece is at position (pos)
def get_occupier(piece_array, pos):
    for i in piece_array:
        if i.pos == pos and i.is_alive:
            return piece_array.index(i)


# function to perform a move
def move_piece(piece_array, piece, pos):
    # safety check for dead piece
    if not piece.is_alive:
        ValueError("illegal move: dead piece")

    # verify positional input is in the format we want
    pos = clean_coord(pos)

    # check if move is legal right off the bat
    if pos not in piece.legal_moves():
        ValueError("illegal move: not allowed")

    # check if this is a passing move which requires a pass-through check (Only happens for lances, rooks and bishops)
    if piece.role in ['r', 'b'] or (piece.role == 'l' and not piece.is_upgraded):
        # grab the directional movement value
        mod = pos - piece.pos

        # grab list of potential directional movement values
        new_mods = [i - piece.pos for i in piece.legal_moves()]

        # filter to directional movements with lower distance than move of interest, and in same polarity (pos/neg)
        new_mods = [i for i in new_mods if (abs(i) < abs(mod) and is_pos(i) == is_pos(mod))]

        # if are moves still remaining...
        if new_mods:
            # default case here is horizontal movement
            mod_rate = 1

            # we'll refine the exact directional movement
            if mod % 8 == 0 and piece.pos % 9 != 0:
                # positive slope diagonal
                mod_rate = 8
            elif mod % 9 == 0:
                # vertical
                mod_rate = 9
            elif mod % 10 == 0 and piece.pos % 9 != 1:
                # negative slope diagonal
                mod_rate = 10

            # first consider horizontal case ...
            new_mods2 = []
            if mod_rate == 1:
                # grab the pieces column
                if piece.pos % 9 == 0:
                    pcol = 9
                else:
                    pcol = piece.pos % 9
                # filter to pieces in the direction we're interested (positive or negative)
                if is_pos(mod):
                    # restrict to answers in the same row
                    new_mods2 = [i for i in new_mods if ((9 - pcol) >= i > 0)]
                elif not is_pos(mod):
                    # restrict to answers in the same row
                    new_mods2 = [i for i in new_mods if (1 - pcol) <= i < 0]
            # non-horizontal case
            else:
                # grab only the people in that line
                new_mods2 = [i for i in new_mods if i % mod_rate == 0]

            # if we still have items left...
            if new_mods2:
                # check each location, if its occupied, we error, otherwise continue
                for j in new_mods2:
                    relative_pos = piece.pos + j
                    if check_pos(piece_array, relative_pos):
                        ValueError("illegal move: blocked")

    # now we check if the position is occupied
    if check_pos(piece_array, pos):
        occupier = piece_array[get_occupier(piece_array, pos)]
        if occupier.color() == piece.color():
            ValueError("illegal move: friendly fire")
        else:
            occupier.kill()
            piece.place(pos=pos)
    else:
        piece.place(pos=pos)
