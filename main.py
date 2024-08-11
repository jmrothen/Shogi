import time

from board import *
import sys
import pygame
from pygame.locals import *

# Initialize the game
pygame.init()

#####################
# Set up the screen #
#####################

# screen parameters
screen_height = 1000
screen_width = 1300

# board parameters
board_height = round(.9 * screen_height)
board_width = board_height

# calculate the cell size
cell_size = board_width // 9

# calculate the gaps at top and bottom of the screen
height_gap_top, height_gap_bot = adjusted_half_gap(screen_height, board_height)

# calculate the area to the left of board where pockets will be
width_gap = round((screen_width - board_width) * .9)  # w2

# calculate pocket-size
pocket_width = board_height // 3  # w3 = h3
pocket_height = pocket_width

# calculate the gap between edge of screen and pocket
pocket_gap = (width_gap - pocket_width) // 2

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shogi Board')

# Colors
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
WHITE = (255, 255, 255)
IVORY = (255, 255, 240)
GRAY = (128, 128, 128)


##########################
# Function to draw board #
##########################


# Function to draw the Shogi board


def draw_shogi_board_pygame(pa=None, save_path=None):
    # reference global variables
    global selected_piece
    global se_pos
    global error_text
    if not pa:
        global piece_array
    else:
        piece_array = pa

    # Fill background
    screen.fill(BEIGE)

    if selected_piece is not None:
        # we will change the color of each cell which the selected piece can move to
        if piece_array[selected_piece].is_alive:
            for i in filter_moves(piece_array, selected_piece):
                row, col = i
                pygame.draw.rect(screen, (255, 204, 204),
                                 (width_gap + col * cell_size + 1, height_gap_top + row * cell_size + 1, cell_size - 1,
                                  cell_size - 1), 0)
        else:
            for i in legal_drops(piece_array, selected_piece):
                row, col = i
                pygame.draw.rect(screen, (255, 204, 204),
                                 (width_gap + col * cell_size + 1, height_gap_top + row * cell_size + 1, cell_size - 1,
                                  cell_size - 1), 0)

    # Draw the game board
    pygame.draw.rect(screen, BLACK, (width_gap, height_gap_top, board_height, board_width), 3)
    for i in range(1, 9):
        pygame.draw.line(screen, BLACK, (width_gap, height_gap_top + i * cell_size),
                         (width_gap + board_height, height_gap_top + i * cell_size), 1)
        pygame.draw.line(screen, BLACK, (width_gap + i * cell_size, height_gap_top),
                         (width_gap + i * cell_size, height_gap_top + board_height), 1)

    # make every third line thicker (to represent the 3x3 squares)
    for i in range(1, 9):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (width_gap, height_gap_top + i * cell_size),
                             (width_gap + board_height, height_gap_top + i * cell_size), 2)
            pygame.draw.line(screen, BLACK, (width_gap + i * cell_size, height_gap_top),
                             (width_gap + i * cell_size, height_gap_top + board_height), 2)

    # Draw the pockets for captured pieces
    pygame.draw.rect(screen, IVORY, (pocket_gap, height_gap_top, pocket_width, pocket_height), 0)
    pygame.draw.rect(screen, IVORY,
                     (pocket_gap, height_gap_top + board_height - pocket_height, pocket_width, pocket_height), 0)

    # Draw the pocket outlines
    pygame.draw.rect(screen, BLACK, (pocket_gap, height_gap_top, pocket_width, pocket_height), 2)
    pygame.draw.rect(screen, BLACK,
                     (pocket_gap, height_gap_top + board_height - pocket_height, pocket_width, pocket_height), 2)

    # Default font for our text rendering
    font = pygame.font.SysFont(None, 30)

    # Draw the color label for each pocket above the pocket
    for i, color in enumerate(['White', 'Black']):
        text = font.render(color, True, BLACK)
        text_rect = text.get_rect(center=(pocket_gap + pocket_width // 2, height_gap_top - cell_size // 7))
        screen.blit(text, text_rect if i == 0 else text.get_rect(center=(pocket_gap + pocket_width // 2,
                                                                         height_gap_top + board_height + cell_size // 7)))

    # Add labels for columns above the board
    for i in [9, 8, 7, 6, 5, 4, 3, 2, 1]:
        text = font.render(str(i), True, BLACK)
        text_rect = text.get_rect(
            center=(width_gap + (9 - i) * cell_size + cell_size // 2, height_gap_top - cell_size // 7))
        screen.blit(text, text_rect)

    # Add labels for rows to the left of the board
    for i, letter in enumerate('abcdefghi', start=1):
        text = font.render(letter, True, BLACK)
        text_rect = text.get_rect(
            center=(width_gap - cell_size // 9, height_gap_top + (i - 1) * cell_size + cell_size // 2))
        screen.blit(text, text_rect)

    # Draw the pieces
    # We'll track dead pieces separately to draw them in pockets later
    dead_pieces = {'w': [], 'b': []}

    # cycle through pieces
    for index, i in enumerate(piece_array):
        # if the piece is selected, we'll draw it at the mouse position
        if selected_piece and index == selected_piece:
            text = pygame.font.SysFont(None, 50).render(i.shorthand(), True, BLACK) if i.color == 'b' \
                else pygame.font.SysFont(None, 50).render(i.shorthand(), True, GRAY)
            text_rect = text.get_rect(center=(se_pos[0], se_pos[1]))
            screen.blit(text, text_rect)
        # for all other pieces, we'll draw them at their current position
        elif i.is_alive:
            row, col = i.pos
            text = pygame.font.SysFont(None, 50).render(i.shorthand(), True, BLACK) if i.color == 'b' \
                else pygame.font.SysFont(None, 50).render(i.shorthand(), True, GRAY)
            text_rect = text.get_rect(center=(width_gap + col * cell_size + cell_size // 2,
                                              height_gap_top + row * cell_size + cell_size // 2))
            screen.blit(text, text_rect)
        # dead pieces are stored for next step
        elif not i.is_alive:
            dead_pieces[i.color].append(i.shorthand())

    # Count occurrences of each piece type in the dead-list
    piece_counts = {'w': {}, 'b': {}}
    for j in dead_pieces:
        for i in dead_pieces[j]:
            if i in piece_counts[j]:
                piece_counts[j][i] += 1
            else:
                piece_counts[j][i] = 1

    # Draw the dead pieces
    for j in dead_pieces:
        for index, i in enumerate(dead_pieces[j]):
            # make sure we adjust our pixel offset to the correct pocket
            if j == 'w':
                y_offset = height_gap_top
            else:
                y_offset = height_gap_top + board_height - pocket_height

            # map the piece role to a position in the pocket
            positions = {
                'p': (pocket_gap + pocket_width // 4, y_offset + pocket_height // 4),
                'l': (pocket_gap + pocket_width // 2, y_offset + pocket_height // 4),
                'n': (pocket_gap + 3 * pocket_width // 4, y_offset + pocket_height // 4),
                's': (pocket_gap + pocket_width // 4, y_offset + pocket_height // 2),
                'g': (pocket_gap + 3 * pocket_width // 4, y_offset + pocket_height // 2),
                'b': (pocket_gap + pocket_width // 4, y_offset + 3 * pocket_height // 4),
                'r': (pocket_gap + 3 * pocket_width // 4, y_offset + 3 * pocket_height // 4)
            }

            # adjust the piece according to its color
            text = pygame.font.SysFont(None, 50).render(i, True, BLACK) if j == 'b' \
                else pygame.font.SysFont(None, 50).render(i, True, GRAY)
            text_rect = text.get_rect(center=positions[i])
            screen.blit(text, text_rect)

            # Add a count subscript if there are multiple pieces of the same type in pocket
            if piece_counts[j][i] > 1:
                count_text = pygame.font.SysFont(None, 20).render(str(piece_counts[j][i]), True, BLACK)
                count_rect = count_text.get_rect(center=(positions[i][0], positions[i][1] + 20))
                screen.blit(count_text, count_rect)

    # Draw error text
    if error_text:
        # place the error text, in red, at the bottom of the screen below the board
        text = pygame.font.SysFont(None, 20).render(str(error_text), True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, height_gap_top + board_height + 25))
        screen.blit(text, text_rect)

    # write text on the left of screen, between pockets, to indicate whose turn it is
    player_color = 'Black' if active_color == 'b' else 'White'
    text = pygame.font.SysFont(None, 40).render(f"{player_color}'s turn", True, BLACK)
    text_rect = text.get_rect(center=(pocket_gap + pocket_width // 2, height_gap_top + board_height // 2))
    screen.blit(text, text_rect)
    # draw a light red arrow pointing to the current player
    if player_color == 'White':
        pygame.draw.polygon(screen, (255, 100, 100),
                            [(pocket_gap + pocket_width // 2, height_gap_top + board_height // 2 - 50),
                             (pocket_gap + pocket_width // 2 - 20, height_gap_top + board_height // 2 - 20),
                             (pocket_gap + pocket_width // 2 + 20, height_gap_top + board_height // 2 - 20)])
    elif player_color == 'Black':
        pygame.draw.polygon(screen, (255, 100, 100),
                            [(pocket_gap + pocket_width // 2, height_gap_top + board_height // 2 + 50),
                             (pocket_gap + pocket_width // 2 - 20, height_gap_top + board_height // 2 + 20),
                             (pocket_gap + pocket_width // 2 + 20, height_gap_top + board_height // 2 + 20)])

    # Update the display
    pygame.display.flip()

    # Save the screen to a file
    if save_path:
        pygame.image.save(screen, save_path)


# initial game-loop variables
selected_piece = None  # index of the clicked piece
piece_array = create_piece_array()  # array of pieces
error_text = None  # possible error text that I might draw on screen if needed
se_pos = [None, None]  # tracked for selected piece to follow mouse
active_color = 'b'  # black goes first
check_flag = False


def handle_input(input_event):
    global selected_piece
    global se_pos
    global error_text
    global piece_array
    global active_color
    global check_flag

    if input_event.type == QUIT:
        pygame.quit()
        sys.exit()

    elif input_event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        x2 = x - width_gap
        y2 = y - height_gap_top
        # if the click is on the board...
        if 0 <= x2 < board_width and 0 <= y2 < board_height:
            col = x2 // cell_size
            row = y2 // cell_size
            position = [row, col]

            # If there is a piece selected...
            if selected_piece is not None:

                # if it's coming from pocket, we'll try to drop it rather than use the move command
                if not piece_array[selected_piece].is_alive:
                    try:

                        # Check if the drop is legal
                        if position not in legal_drops(piece_array, selected_piece):
                            raise ValueError("illegal move: not a legal drop")

                        # consider the case where the player is in check
                        if check_flag:
                            safe_moves = check_safe_moves(piece_array, active_color)
                            for s in safe_moves:
                                if s[0] == selected_piece and s[1] == position:
                                    piece_array = move_piece(piece_array, index=selected_piece, coord=position, drop=True)
                                    selected_piece = None
                                    se_pos = None
                                    active_color = 'w' if active_color == 'b' else 'b'
                                    error_text = None
                                    check_flag = False  # remove the check!
                                    break
                            if selected_piece is not None:
                                raise ValueError("illegal move: piece cannot stop check")

                        # if the player is not in check, we can just drop the piece!
                        else:
                            piece_array = move_piece(piece_array, index=selected_piece, coord=position, drop=True)
                            selected_piece = None
                            se_pos = None
                            active_color = 'w' if active_color == 'b' else 'b'
                            error_text = None

                    # catch the error and reset the selected piece if something fails
                    except ValueError as e:
                        error_text = e
                        selected_piece = None
                        se_pos = None

                # if the piece is alive, we'll try to move it
                else:
                    try:
                        # first, check if the move would put the king in check (illegal)
                        if not is_safe_king_move(piece_array, selected_piece, position):
                            raise ValueError("illegal move: puts king in check")

                        # next, check if the move is legal in general
                        if position not in filter_moves(piece_array, selected_piece):
                            raise ValueError("illegal move: not a legal move")

                        # if the player is in check, we need to check if the move will stop the check
                        if check_flag:

                            # consider all the safe moves available to the player
                            safe_moves = check_safe_moves(piece_array, active_color)
                            for s in safe_moves:
                                if s[0] == selected_piece and position == s[1]:
                                    piece_array = move_piece(piece_array, index=selected_piece, coord=position)
                                    selected_piece = None
                                    se_pos = None
                                    active_color = 'w' if active_color == 'b' else 'b'
                                    error_text = None
                                    check_flag = False  # remove the check!
                                    break

                            # if the piece+move were not found in the safe_move list, toss error
                            if selected_piece is not None:
                                raise ValueError("illegal move: move does not stop check")

                        # if not in check, just go ahead and make the move!
                        else:
                            piece_array = move_piece(piece_array, index=selected_piece, coord=position)
                            selected_piece = None
                            se_pos = None
                            active_color = 'w' if active_color == 'b' else 'b'
                            error_text = None

                    except ValueError as e:
                        error_text = e
                        selected_piece = None
                        se_pos = None

            # if there is no piece selected, we'll try to select one
            else:
                try:
                    # check if there's a piece where we clicked
                    if check_pos(piece_array, coord=position):

                        # get the index of the piece in the piece_array
                        occ_index = get_occupier(piece_array, coord=position)
                        occ = piece_array[occ_index]

                        # first, check if that piece is the active player's piece
                        if occ.color == active_color:

                            # if the player is in check, we need to check if the piece can stop the check
                            if check_flag:

                                # grab the safe moves available to the player
                                safe_moves = check_safe_moves(piece_array, active_color)

                                # check if the piece clicked is one of the pieces in safe_moves
                                for c in safe_moves:
                                    piece_index = c[0]

                                    # if it can, we'll select it
                                    if occ_index == piece_index:
                                        selected_piece = occ_index
                                        se_pos = pygame.mouse.get_pos()
                                        error_text = False
                                        break

                                # if piece could not stop check, toss error
                                if selected_piece is None:
                                    error_text = "illegal move: piece cannot stop check"

                            else:
                                selected_piece = occ_index
                                se_pos = pygame.mouse.get_pos()
                                error_text = None

                        # if not our piece, toss error
                        else:
                            error_text = "illegal move: not your piece"

                    # If no piece there, just continue

                except ValueError as e:
                    error_text = e

        # next, we want to check if the click was in the top or bottom pocket
        elif pocket_gap <= x <= pocket_gap + pocket_width:
            # Determine pocket color
            if height_gap_top <= y <= height_gap_top + pocket_height:
                pocket = 'w'
            elif height_gap_top + board_height - pocket_height <= y <= height_gap_top + board_height:
                pocket = 'b'
            else:
                pocket = None

            # Continue if pocket color matches active color
            if pocket == active_color and selected_piece is None:
                # Adjust coordinates relative to pocket
                x -= pocket_gap
                y -= height_gap_top if pocket == 'w' else height_gap_top + board_height - pocket_height

                if 0 <= x < pocket_width and 0 <= y < pocket_height:
                    col, row = x // (pocket_width // 3), y // (pocket_height // 3)
                    pocket_position = (row, col)
                    print(pocket_position)

                    # Map pocket position to piece type
                    piece_map = {
                        (0, 0): 'p', (0, 1): 'l', (0, 2): 'n',
                        (1, 0): 's', (1, 2): 'g',
                        (2, 0): 'b', (2, 2): 'r'
                    }
                    piece = piece_map.get(pocket_position)
                    selected_piece = get_dead_piece(piece_array, pocket, piece)
                    se_pos = pygame.mouse.get_pos()
        else:
            selected_piece = None
            se_pos = None

    if input_event.type == MOUSEMOTION:
        if selected_piece:
            se_pos = pygame.mouse.get_pos()


# Run the game loop
while True:
    for event in pygame.event.get():
        if is_in_checkmate(piece_array, active_color):
            time.sleep(5)
            pygame.quit()
            sys.exit()
        elif is_in_check(piece_array, active_color):
            check_flag = True
        else:
            check_flag = False
        handle_input(event)

        draw_shogi_board_pygame()
