import pandas as pd
import math
import re
import copy


# create a function break a gap into two equal-ish parts
def adjusted_half_gap(dimension_one, dimension_two):
    if dimension_one - dimension_two % 2 == 0:
        return (dimension_one - dimension_two) / 2, (dimension_one - dimension_two) / 2
    else:
        return math.ceil((dimension_one - dimension_two) / 2), math.floor((dimension_one - dimension_two) / 2)


# let's create functions to map from a coordinate (a7) to a board vector position


def is_pos(num):
    if num > 0:
        return True
    elif num < 0:
        return False
    else:
        return []


# class for Pieces
class Piece:
    def __init__(self, color, role, pos, is_upgraded=False, is_alive=True):
        self.color = color
        self.role = role
        self.pos = pos
        # self.image = image
        self.is_upgraded = is_upgraded
        self.is_alive = is_alive

    # option to print the long for of the piece name
    def long_name(self):
        role = ""
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
        return role

    # add a simple function that prints the piece's traits
    def __str__(self):
        color_long = "Black" if self.color == 'b' else "White"
        upgraded_status = " promoted " if self.is_upgraded else ""
        role = self.long_name()
        alive_status = f"at {self.pos}" if self.is_alive else "dead"
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
        self.is_upgraded = False
        self.pos = [9, 9]

    def can_promote(self):
        return False if (self.role in ['k', 'g'] or self.is_upgraded) else True

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
        ('b', 'p', [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8]]),
        ('w', 'p', [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8]]),
        ('b', 'r', [[7, 7]]),
        ('w', 'r', [[1, 1]]),
        ('b', 'b', [[7, 1]]),
        ('w', 'b', [[1, 7]]),
        ('b', 'l', [[8, 0], [8, 8]]),
        ('w', 'l', [[0, 0], [0, 8]]),
        ('b', 'n', [[8, 1], [8, 7]]),
        ('w', 'n', [[0, 1], [0, 7]]),
        ('b', 's', [[8, 2], [8, 6]]),
        ('w', 's', [[0, 2], [0, 6]]),
        ('b', 'g', [[8, 3], [8, 5]]),
        ('w', 'g', [[0, 3], [0, 5]]),
        ('b', 'k', [[8, 4]]),
        ('w', 'k', [[0, 4]])
    ]
    piece_array = [Piece(color, role, pos, False, True) for color, role, positions in piece_types for pos in positions]
    return piece_array


# function to check a pos (bool)
def check_pos(piece_array, coord=None):
    location = coord
    for i in piece_array:
        if i.pos == location and i.is_alive:
            return True
    return False


# function to find what piece is at position (pos)
def get_occupier(piece_array, coord=None):
    location = coord
    for i, piece in enumerate(piece_array):
        if piece.pos == location:
            return i


def filter_moves(piece_array, index):
    piece = piece_array[index]
    moves_out = piece.legal_moves().copy()
    to_remove = []
    for j in moves_out:
        # check if this is a passing move which requires a pass-through check
        if piece.role in ['r', 'b'] or (piece.role == 'l' and not piece.is_upgraded):
            # find out the direction of the move in questions
            x_dir = j[0] - piece.pos[0]
            y_dir = j[1] - piece.pos[1]

            # if the move is vertical or horizontal, we can check for pieces in the way
            if x_dir == 0:  # horizontal move
                direction = 1 if is_pos(y_dir) else -1
                for i in range(1, abs(y_dir)):
                    if check_pos(piece_array, coord=[piece.pos[0], piece.pos[1] + i * direction]):
                        to_remove.append(j)
                        break
            elif y_dir == 0:  # vertical move
                direction = 1 if is_pos(x_dir) else -1
                for i in range(1, abs(x_dir)):
                    if check_pos(piece_array, coord=[piece.pos[0] + i * direction, piece.pos[1]]):
                        to_remove.append(j)
                        break
            else:  # diagonal move
                direction_x = 1 if is_pos(x_dir) else -1
                direction_y = 1 if is_pos(y_dir) else -1
                for i in range(1, abs(x_dir)):
                    if check_pos(piece_array, coord=[piece.pos[0] + i * direction_x, piece.pos[1] + i * direction_y]):
                        to_remove.append(j)
                        break
        # now we check if the position is occupied by a friendly piece
        if check_pos(piece_array, coord=j):
            occupier = piece_array[get_occupier(piece_array, coord=j)]
            if occupier.color == piece.color:
                to_remove.append(j)
    for q in to_remove:
        if q in moves_out:
            moves_out.remove(q)
    return moves_out


# function to perform a move
def move_piece(piece_array, index, coord=None, drop=False):
    location = coord
    piece_array_test = copy.deepcopy(piece_array)
    piece = piece_array_test[index]

    if not location:
        raise ValueError("illegal move: no target location specified")

    if not drop:
        # safety check for dead piece
        if not piece.is_alive:
            raise ValueError("illegal move: dead piece")

        # check if move is legal right off the bat
        if location not in piece.legal_moves():
            raise ValueError("illegal move: not allowed")

        if location not in filter_moves(piece_array_test, index):
            raise ValueError("illegal move: pieces in the way")

    # now we check if the position is occupied
    if check_pos(piece_array_test, coord=location):
        occupier = piece_array_test[get_occupier(piece_array_test, coord=location)]
        occupier.kill()
        piece.place(pos=location)
    else:
        piece.place(pos=location)
    return copy.deepcopy(piece_array_test)


# function to grab the index of the first dead piece of a certain color and role
def get_dead_piece(piece_array, color, role):
    for i in piece_array:
        if not i.is_alive and i.color == color and i.role == role:
            return piece_array.index(i)
    return None


# function which compiles every possible move for a player
def all_possible_moves(piece_array, color):
    moves = []
    for i in piece_array:
        if i.color == color and i.is_alive:
            moves.extend([(piece_array.index(i), x) for x in i.legal_moves()])
    return moves


# function to check if a player is in check
def is_in_check(piece_array, color):
    king_index = 38 if color == 'b' else 39
    king_pos = piece_array[king_index].pos

    enemy_color = 'w' if color == 'b' else 'b'
    for i in piece_array:
        if i.color == enemy_color and i.is_alive:
            if king_pos in filter_moves(piece_array, piece_array.index(i)):
                return True
    return False


# function to check if a player is in checkmate
def is_in_checkmate(piece_array, color):
    if is_in_check(piece_array, color):
        king_index = 38 if color == 'b' else 39
        for i in filter_moves(piece_array, king_index):
            new_array = move_piece(piece_array, king_index, coord=i)
            if not is_in_check(new_array, color):
                return False
        for j in piece_array:
            if j.color == color and j.is_alive:
                for i in filter_moves(piece_array, piece_array.index(j)):
                    new_array = move_piece(piece_array, piece_array.index(j), coord=i)
                    if not is_in_check(new_array, color):
                        return False
        return True
    else:
        return False


# make sure that the move doesn't put the player in check
def is_safe_king_move(piece_array, index, coord=None, drop=False):
    color = piece_array[index].color
    new_piece_array = move_piece(piece_array, index, coord=coord, drop=drop)
    return not is_in_check(new_piece_array, color)


def legal_drops(piece_array, index):
    piece_array_test = piece_array.copy()
    piece = piece_array_test[index]

    # for every possible coordinate...
    possible_coord = [[i, j] for i in range(9) for j in range(9)]
    to_remove = []

    # remove occupied coordinates
    for i in piece_array_test:
        if i.is_alive and i != piece:
            to_remove.append(i.pos)

    # check for pieces having no further moves
    for i in possible_coord:
        # test the move
        test_array = move_piece(piece_array_test, index, coord=i, drop=True)

        # get the future moves which would be possible for the piece in this new location
        # NOTE, this only cares above legal moves, not the filtered ones
        future_moves = test_array[index].legal_moves()

        # if there are no future moves, remove the coordinate from the list
        if not future_moves:
            to_remove.append(i)

    # if we're a pawn, remove columns which already contain a pawn of the same color
    if piece.role == 'p':
        # check for columns with pawns already in them
        pawn_columns = []
        for j in piece_array_test:
            if j.role == 'p' and j.color == piece.color and j.is_alive:
                # remove all possible coordinates in the same column as this pawn
                pawn_columns.append(j.pos[1])

        # loop through those columns and remove them from the possible coordinates
        for i in possible_coord:
            if i[1] in pawn_columns:
                to_remove.append(i)

        # also, we need to make sure that the pawn does not cause checkmate when placed
        for i in possible_coord:
            enemy_color = 'w' if piece.color == 'b' else 'b'
            test_array = move_piece(piece_array_test, index, coord=i, drop=True)
            if is_in_checkmate(test_array, enemy_color):
                to_remove.append(i)

    to_remove = list(set(tuple(coord) for coord in to_remove))
    possible_coord = [coord for coord in possible_coord if tuple(coord) not in to_remove]

    return possible_coord


# create a function which supplies all possible piece - move combinations that bring the player out of check
def check_safe_moves(piece_array, color, drop=False):
    safe_moves = []
    if drop:
        for i in piece_array:
            if i.color == color and not i.is_alive:
                for j in legal_drops(piece_array, piece_array.index(i)):
                    if is_safe_king_move(piece_array, piece_array.index(i), coord=j, drop=True):
                        safe_moves.append((piece_array.index(i), j))
    else:
        for i in piece_array:
            if i.color == color and i.is_alive:
                for j in filter_moves(piece_array, piece_array.index(i)):
                    if is_safe_king_move(piece_array, piece_array.index(i), coord=j):
                        safe_moves.append((piece_array.index(i), j))
    return safe_moves


def check_promoting_move(piece_array, index, color=None, coord=None):
    # grab active piece
    piece_array_test = copy.deepcopy(piece_array)
    piece = piece_array_test[index]
    if not color:
        color = piece.color

    # check old and new locations to see if piece is a
    old_pos = piece.pos
    new_pos = coord

    if not piece.can_promote():
        return False  # piece cannot promote

    if color == 'b':
        if old_pos[0] <= 2 or new_pos[0] <= 2:
            return True
        else:
            return False
    else:
        if old_pos[0] >= 6 or new_pos[0] >= 6:
            return True
        else:
            return False
