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
        self.pos = pos_to_xy(pos)
        # self.image = image
        self.is_upgraded = is_upgraded
        self.is_alive = is_alive

    # add a simple function that prints the piece's traits
    def __str__(self):
        color_long = "Black" if self.color == 'b' else "White"
        upgraded_status = " promoted " if self.is_upgraded else ""
        match self.role:
            case 'p':
                role = "pawn"
            case 'r':
                role = "rook"
            case 'b':
                role = "bishop"
            case 'l':
                role = "lance"
            case 'n':
                role = "knight"
            case 's':
                role = "silver"
            case 'g':
                role = "gold"
            case 'k':
                role = "king"
        alive_status = f"at {pos_to_coord(self.pos)}" if self.is_alive else "dead"
        return f"{color_long} {upgraded_status}{self.role} {alive_status}"

    def legal_moves(self):
        moves = []
        new_moves = []
        direction = -1 if self.color == 'b' else 1

        if self.role == 'p' and not self.is_upgraded:
            new_moves = [(direction, 0)]

        elif self.role == 'n':
            new_moves = [(direction * 2, 1), (direction * 2, -1)]

        elif self.role == 'k':
            new_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        elif self.role in ['g'] or (self.role in ['s', 'n', 'l', 'p'] and self.is_upgraded):
            new_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (direction, 1), (direction, -1)]

        elif self.role == 's':
            new_moves = [(direction, 0), (direction, 1), (direction, -1), (-direction, 1), (-direction, -1)]

        elif self.role == 'l':
            new_moves = [(direction * i, 0) for i in range(1, 9)]

        elif self.role == 'r':
            new_moves = ([(0, i) for i in range(1, 9)] +
                         [(0, -i) for i in range(1, 9)] +
                         [(i, 0) for i in range(1, 9)] +
                         [(-i, 0) for i in range(1, 9)])
            if self.is_upgraded:
                new_moves.extend([(1, 1), (-1, 1), (1, -1), (-1, -1)])

        elif self.role == 'b':
            new_moves = ([(i, i) for i in range(1, 9)] +
                         [(i, -i) for i in range(1, 9)] +
                         [(-i, i) for i in range(1, 9)] +
                         [(-i, -i) for i in range(1, 9)])
            if self.is_upgraded:
                new_moves.extend([(0, 1), (1, 0), (0, -1), (-1, 0)])

        for i in new_moves:
            x_change = i[0]
            y_change = i[1]
            moves.append(([self.pos[0] + x_change, self.pos[1] + y_change]))

        # Remove entries with x or y < 0 or > 8
        moves = [i for i in moves if 0 <= i[0] <= 8 and 0 <= i[1] <= 8]

        return moves

    def kill(self):
        # swap colors
        if self.color == 'w':
            self.color = 'b'
        else:
            self.color = 'w'
        # move to dead
        self.is_alive = False
        self.pos = [9, 9]

    def can_promote(self):
        return False if self.role in ['k', 'g'] else True

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
def check_pos(piece_array, coord=None, pos=None):
    location = coord if coord else pos_to_xy(clean_coord(pos))
    for i in piece_array:
        if i.pos == location and i.is_alive:
            return True
    return False


# function to find what piece is at position (pos)
def get_occupier(piece_array, coord=None, pos=None):
    location = coord if coord else pos_to_xy(clean_coord(pos))
    for i in piece_array:
        if i.pos == location and i.is_alive:
            return piece_array.index(i)


# function to perform a move
def move_piece(piece_array, index, coord=None, pos=None):
    location = coord if coord else pos_to_xy(clean_coord(pos))
    piece = piece_array[index]

    if not location:
        raise ValueError("illegal move: no target location specified")

    # safety check for dead piece
    if not piece.is_alive:
        raise ValueError("illegal move: dead piece")

    # check if move is legal right off the bat
    if location not in piece.legal_moves():
        raise ValueError("illegal move: not allowed")

    # check if this is a passing move which requires a pass-through check (Only happens for lances, rooks and bishops)
    if piece.role in ['r', 'b'] or (piece.role == 'l' and not piece.is_upgraded):
        # find out the direction of the move
        x_dir = location[0] - piece.pos[0]
        y_dir = location[1] - piece.pos[1]
        if x_dir == 0:  # vertical move
            direction = 1 if is_pos(y_dir) else -1
            for i in range(1, abs(y_dir)):
                if check_pos(piece_array, coord=[piece.pos[0], piece.pos[1] + i * direction]):
                    raise ValueError("illegal move: passing through a piece")
        elif y_dir == 0:  # horizontal move
            direction = 1 if is_pos(x_dir) else -1
            for i in range(1, abs(x_dir)):
                if check_pos(piece_array, coord=[piece.pos[0] + i * direction, piece.pos[1]]):
                    raise ValueError("illegal move: passing through a piece")
        else:  # diagonal move
            direction_x = 1 if is_pos(x_dir) else -1
            direction_y = 1 if is_pos(y_dir) else -1
            for i in range(1, abs(x_dir)):
                if check_pos(piece_array, coord=[piece.pos[0] + i * direction_x, piece.pos[1] + i * direction_y]):
                    raise ValueError("illegal move: passing through a piece")

    # now we check if the position is occupied
    if check_pos(piece_array, coord=location):
        occupier = piece_array[get_occupier(piece_array, coord=location)]
        if occupier.color == piece.color:
            raise ValueError("illegal move: friendly fire")
        else:
            occupier.kill()
            piece.place(pos=location)
    else:
        piece.place(pos=location)
    return piece_array


# function to grab the index of the first dead piece of a certain color and role
def get_dead_piece(piece_array, color, role):
    for i in piece_array:
        if not i.is_alive and i.color == color and i.role == role:
            return piece_array.index(i)
    return None
