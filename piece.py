from board import *


# class for Pieces
class Piece:
    def __init__(self, color, role, pos, is_upgraded=False, is_alive=True):
        self.color = color
        self.role = role
        self.pos = clean_coord(pos)
        # self.image = image
        self.is_upgraded = is_upgraded
        self.is_alive = is_alive

    """
    def __str__(self):
        return f"{self.color} {self.role} at {self.pos}"
    """

    def legal_moves(self):
        moves = pd.DataFrame([])
        # pawns
        if self.role == 'p' and not self.is_upgraded:
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 9])
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos + 9])
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # knights
        if self.role == 'n':
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 17, self.pos - 19])
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos + 17, self.pos + 19])
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # king
        if self.role == 'k':
            moves = pd.DataFrame([self.pos - 1, self.pos + 1,
                                  self.pos - 10, self.pos - 9,
                                  self.pos - 8, self.pos + 8,
                                  self.pos + 10, self.pos + 9])
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # golds
        if self.role in ['g'] or (self.role in ['s', 'n', 'l', 'p'] and self.is_upgraded):
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 1, self.pos + 1,
                                      self.pos - 10, self.pos - 9,
                                      self.pos - 8, self.pos + 9])
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos - 1, self.pos + 1,
                                      self.pos + 10, self.pos + 9,
                                      self.pos + 8, self.pos - 9])
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # silver
        if self.role == 's':
            if self.color == 'b':
                moves = pd.DataFrame([self.pos - 10, self.pos - 9,
                                      self.pos - 8, self.pos + 8,
                                      self.pos + 10])
            elif self.color == 'w':
                moves = pd.DataFrame([self.pos + 10, self.pos + 9,
                                      self.pos + 8, self.pos - 8,
                                      self.pos - 10])
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # lance
        if self.role == 'l':
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
            return moves

        # bishop
        if self.role == 'b':
            # nw
            nw = pd.DataFrame([self.pos - 10, self.pos - 20, self.pos - 30,
                               self.pos - 40, self.pos - 50, self.pos - 60,
                               self.pos - 70, self.pos - 80])
            # ne
            ne = pd.DataFrame([self.pos - 8, self.pos - 16, self.pos - 24,
                               self.pos - 32, self.pos - 40, self.pos - 48,
                               self.pos - 56, self.pos - 64])
            # se
            se = pd.DataFrame([self.pos + 10, self.pos + 20, self.pos + 30,
                               self.pos + 40, self.pos + 50, self.pos + 60,
                               self.pos + 70, self.pos + 80])
            # sw
            sw = pd.DataFrame([self.pos + 8, self.pos + 16, self.pos + 24,
                               self.pos + 32, self.pos + 40, self.pos + 48,
                               self.pos + 56, self.pos + 64])
            moves = pd.concat([nw, ne, se, sw], ignore_index=True)
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # rook
        if self.role == 'r':
            # north
            no = pd.DataFrame([self.pos - 9, self.pos - 18, self.pos - 27,
                               self.pos - 36, self.pos - 45, self.pos - 54,
                               self.pos - 63, self.pos - 72])
            # west
            we = pd.DataFrame([self.pos - 1, self.pos - 2, self.pos - 3,
                               self.pos - 4, self.pos - 5, self.pos - 6,
                               self.pos - 7, self.pos - 8])
            # east
            ea = pd.DataFrame([self.pos + 1, self.pos + 2, self.pos + 3,
                               self.pos + 4, self.pos + 5, self.pos + 6,
                               self.pos + 7, self.pos + 8])
            # south
            so = pd.DataFrame([self.pos + 9, self.pos + 18, self.pos + 27,
                               self.pos + 36, self.pos + 45, self.pos + 54,
                               self.pos + 63, self.pos + 72])
            moves = pd.concat([no, we, ea, so], ignore_index=True)
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # dragon (r+)
        if self.role == 'r' and self.is_upgraded:
            # north
            no = pd.DataFrame([self.pos - 9, self.pos - 18, self.pos - 27,
                               self.pos - 36, self.pos - 45, self.pos - 54,
                               self.pos - 63, self.pos - 72])
            # west
            we = pd.DataFrame([self.pos - 1, self.pos - 2, self.pos - 3,
                               self.pos - 4, self.pos - 5, self.pos - 6,
                               self.pos - 7, self.pos - 8])
            # east
            ea = pd.DataFrame([self.pos + 1, self.pos + 2, self.pos + 3,
                               self.pos + 4, self.pos + 5, self.pos + 6,
                               self.pos + 7, self.pos + 8])
            # south
            so = pd.DataFrame([self.pos + 9, self.pos + 18, self.pos + 27,
                               self.pos + 36, self.pos + 45, self.pos + 54,
                               self.pos + 63, self.pos + 72])
            dr = pd.DataFrame([self.pos + 10, self.pos - 10, self.pos + 8, self.pos - 8])
            # combine
            moves = pd.concat([no, we, ea, so, dr], ignore_index=True)
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

        # horse (b+)
        if self.role == 'b' and self.is_upgraded:
            # nw
            nw = pd.DataFrame([self.pos - 10, self.pos - 20, self.pos - 30,
                               self.pos - 40, self.pos - 50, self.pos - 60,
                               self.pos - 70, self.pos - 80])
            # ne
            ne = pd.DataFrame([self.pos - 8, self.pos - 16, self.pos - 24,
                               self.pos - 32, self.pos - 40, self.pos - 48,
                               self.pos - 56, self.pos - 64])
            # se
            se = pd.DataFrame([self.pos + 10, self.pos + 20, self.pos + 30,
                               self.pos + 40, self.pos + 50, self.pos + 60,
                               self.pos + 70, self.pos + 80])
            # sw
            sw = pd.DataFrame([self.pos + 8, self.pos + 16, self.pos + 24,
                               self.pos + 32, self.pos + 40, self.pos + 48,
                               self.pos + 56, self.pos + 64])
            # horse
            hr = pd.DataFrame([self.pos + 1, self.pos - 1, self.pos + 9, self.pos - 9])

            moves = pd.concat([nw, ne, se, sw, hr], ignore_index=True)
            moves = moves[moves[0] >= 1]
            moves = moves[moves[0] <= 81]
            return moves

    def kill(self):
        # swap colors
        if self.color == 'w':
            self.color = 'b'
        else:
            self.color = 'w'
        # move to dead
        self.is_alive = False

    def promote(self):
        self.is_upgraded = True

    def place(self, pos):
        self.pos = pos
        self.is_alive = True

    def shorthand(self):
        match (self.role, self.is_upgraded):
            case (*a, False):
                out = f"{a}"
            case (*a, True):
                out = f"{a}+"
            case _:
                out = "error"
        return out


# end class stuff


def create_piece_array():
    piece_array = [
        # pawns black
        Piece('b', 'p', 'g9'),
        Piece('b', 'p', 'g8'),
        Piece('b', 'p', 'g7'),
        Piece('b', 'p', 'g6'),
        Piece('b', 'p', 'g5'),
        Piece('b', 'p', 'g4'),
        Piece('b', 'p', 'g3'),
        Piece('b', 'p', 'g2'),
        Piece('b', 'p', 'g1'),
        # pawns white
        Piece('w', 'p', 'c9'),
        Piece('w', 'p', 'c8'),
        Piece('w', 'p', 'c7'),
        Piece('w', 'p', 'c6'),
        Piece('w', 'p', 'c5'),
        Piece('w', 'p', 'c4'),
        Piece('w', 'p', 'c3'),
        Piece('w', 'p', 'c2'),
        Piece('w', 'p', 'c1'),
        # rooks
        Piece('b', 'r', 'h2'),
        Piece('w', 'r', 'b8'),
        # bishops
        Piece('b', 'b', 'h8'),
        Piece('w', 'b', 'b2'),
        # lances
        Piece('b', 'l', 'i1'),
        Piece('b', 'l', 'i9'),
        Piece('w', 'l', 'a9'),
        Piece('w', 'l', 'a1'),
        # knights
        Piece('b', 'n', 'i8'),
        Piece('b', 'n', 'i2'),
        Piece('w', 'n', 'a2'),
        Piece('w', 'n', 'a8'),
        # silvers
        Piece('b', 's', 'i7'),
        Piece('b', 's', 'i3'),
        Piece('w', 's', 'a3'),
        Piece('w', 's', 'a7'),
        # gold
        Piece('b', 'g', 'i6'),
        Piece('b', 'g', 'i4'),
        Piece('w', 'g', 'a6'),
        Piece('w', 'g', 'a4'),
        # kings
        Piece('b', 'k', 'i5'),
        Piece('w', 'k', 'a5')
    ]
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
