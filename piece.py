from board import *


# class for Pieces
class Piece:
    def __init__(self, color, role, pos, image=None, is_upgraded=False, is_alive = True):
        self.color = color
        self.role = role
        if type(pos) is str:
            self.pos = coord_to_pos(pos)
        else:
            self.pos = pos
        self.image = image
        self.is_upgraded = is_upgraded
        self.status = is_alive
        

    """
    def __str__(self):
        return f"{self.color} {self.role} at {self.pos}"
    """

    def can_move(self):
        moves = pd.DataFrame([])
        # pawns
        if self.role == 'p':

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
        if self.role in ['g', 's+', 'n+', 'l+', 'p+']:
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
        if self.role == 'r+':
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
        if self.role == 'b+':
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

############################### START HERE
# function to find what piece is at position (pos)


# function to take a piece, and place it on board
def place_piece(piece, pos):
    global board
    if check_pos(pos) == 1:
        ValueError("position is occupied")


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
        board[piece.pos - 1] = 0
        piece.pos = pos
        board[pos - 1] = piece_dict[piece.role]
        if tcol == 'w':
            white_active.remove(tpiece)
            white_pocket.append(tpiece)
        elif tcol == 'b':
            black_active.remove(tpiece)
            black_pocket.append(tpiece)
        return 1
    else:
        return 0
