from board import *
import sys
import pygame
from pygame.locals import *

# Initialize the game
pygame.init()

# Set up the screen
# screen parameters
screen_height = 1000
screen_width = 1300

# board parameters
board_height = round(.9 * screen_height)
board_width = board_height

# calculate the cell size
cell_size = board_width // 9


# create a function break a gap into two equal-ish parts
def adjusted_half_gap(dimension_one, dimension_two):
    if dimension_one - dimension_two % 2 == 0:
        return (dimension_one - dimension_two) / 2, (dimension_one - dimension_two) / 2
    else:
        return math.ceil((dimension_one - dimension_two) / 2), math.floor((dimension_one - dimension_two) / 2)


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


# Function to draw the Shogi board
def draw_shogi_board_pygame(pa=None, save_path=None):
    global selected_piece
    global se_pos

    if not pa:
        global piece_array
    else:
        piece_array = pa

    # Fill background
    screen.fill(BEIGE)

    # Draw the board
    pygame.draw.rect(screen, BLACK, (width_gap, height_gap_top, board_height, board_width), 3)
    for i in range(1, 9):
        pygame.draw.line(screen, BLACK, (width_gap, height_gap_top + i * cell_size),
                         (width_gap + board_height, height_gap_top + i * cell_size), 1)
        pygame.draw.line(screen, BLACK, (width_gap + i * cell_size, height_gap_top),
                         (width_gap + i * cell_size, height_gap_top + board_height), 1)

    # make every third line thicker
    for i in range(1, 9):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (width_gap, height_gap_top + i * cell_size),
                             (width_gap + board_height, height_gap_top + i * cell_size), 2)
            pygame.draw.line(screen, BLACK, (width_gap + i * cell_size, height_gap_top),
                             (width_gap + i * cell_size, height_gap_top + board_height), 2)

    # Draw the pockets
    pygame.draw.rect(screen, IVORY, (pocket_gap, height_gap_top, pocket_width, pocket_height), 0)
    pygame.draw.rect(screen, IVORY,
                     (pocket_gap, height_gap_top + board_height - pocket_height, pocket_width, pocket_height), 0)

    # Draw the pocket outlines
    pygame.draw.rect(screen, BLACK, (pocket_gap, height_gap_top, pocket_width, pocket_height), 2)
    pygame.draw.rect(screen, BLACK,
                     (pocket_gap, height_gap_top + board_height - pocket_height, pocket_width, pocket_height), 2)

    # Font for text
    font = pygame.font.SysFont(None, 30)

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

    dead_pieces = {'w': [], 'b': []}
    # Draw the pieces
    for index, i in enumerate(piece_array):
        if selected_piece and index == selected_piece:
            text = pygame.font.SysFont(None, 50).render(i.shorthand(), True, BLACK) if i.color == 'b' else pygame.font.SysFont(None, 50).render(i.shorthand(), True, GRAY)
            text_rect = text.get_rect(center=(se_pos[0], se_pos[1]))
            screen.blit(text, text_rect)
        elif i.is_alive:
            row, col = i.pos
            text = pygame.font.SysFont(None, 50).render(i.shorthand(), True, BLACK) if i.color == 'b' else pygame.font.SysFont(None, 50).render(i.shorthand(), True, GRAY)
            text_rect = text.get_rect(center=(width_gap + col * cell_size + cell_size // 2,
                                              height_gap_top + row * cell_size + cell_size // 2))
            screen.blit(text, text_rect)
        elif not i.is_alive:
            dead_pieces[i.color].append(i.shorthand())

    # Count occurrences of each piece type in the pocket
    piece_counts = {'w': {}, 'b': {}}
    for j in dead_pieces:
        for i in dead_pieces[j]:
            if i in piece_counts[j]:
                piece_counts[j][i] += 1
            else:
                piece_counts[j][i] = 1

    # Draw the pieces
    for j in dead_pieces:
        for index, i in enumerate(dead_pieces[j]):
            if j == 'w':
                y_offset = height_gap_top
            else:
                y_offset = height_gap_top + board_height - pocket_height

            positions = {
                'p': (pocket_gap + pocket_width // 4, y_offset + pocket_height // 4),
                'l': (pocket_gap + pocket_width // 2, y_offset + pocket_height // 4),
                'n': (pocket_gap + 3 * pocket_width // 4, y_offset + pocket_height // 4),
                's': (pocket_gap + pocket_width // 4, y_offset + pocket_height // 2),
                'g': (pocket_gap + 3 * pocket_width // 4, y_offset + pocket_height // 2),
                'b': (pocket_gap + pocket_width // 4, y_offset + 3 * pocket_height // 4),
                'r': (pocket_gap + 3 * pocket_width // 4, y_offset + 3 * pocket_height // 4)
            }

            # if the pocket is white, we'll draw the pieces in gray

            text = pygame.font.SysFont(None, 50).render(i, True, BLACK) if j == 'b' else pygame.font.SysFont(None, 50).render(i, True, GRAY)
            text_rect = text.get_rect(center=positions[i])
            screen.blit(text, text_rect)

            # Draw the count if there are multiple pieces of the same type
            if piece_counts[j][i] > 1:
                count_text = pygame.font.SysFont(None, 20).render(str(piece_counts[j][i]), True, BLACK)
                count_rect = count_text.get_rect(center=(positions[i][0], positions[i][1] + 20))
                screen.blit(count_text, count_rect)

    # Update the display
    pygame.display.flip()

    # Save the screen to a file
    if save_path:
        pygame.image.save(screen, save_path)


# initial safety variables
selected_piece = None  # index of the clicked piece
piece_array = create_piece_array()  # array of pieces
error_text = None  # possible error text that I might draw on screen if needed
se_pos = [None, None]  # tracked for selected piece to follow mouse
active_color = 'b'  # black goes first


def handle_input(input_event):
    global selected_piece
    global se_pos
    global error_text
    global piece_array
    global active_color

    if input_event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif input_event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        print(x, y)
        x2 = x - width_gap
        y2 = y - height_gap_top
        if 0 <= x2 < board_width and 0 <= y2 < board_height:
            x, y = x2, y2
            col = x // cell_size
            row = y // cell_size
            position = [row, col]
            print(position)
            if selected_piece:
                # if it's coming from pocket, we'll try to drop it rather than use the move command
                if not piece_array[selected_piece].is_alive:
                    try:
                        piece_array[selected_piece].place(position)
                        selected_piece = None
                        se_pos = None
                        active_color = 'w' if active_color == 'b' else 'b'
                    except ValueError as e:
                        error_text = e
                        selected_piece = None
                        se_pos = None
                else:
                    try:
                        piece_array = move_piece(piece_array, index=selected_piece, coord=position)
                        selected_piece = None
                        se_pos = None
                        active_color = 'w' if active_color == 'b' else 'b'
                    except ValueError as e:
                        # if it doesn't work, we'll just reset the selected piece
                        error_text = e
                        selected_piece = None
                        se_pos = None
            else:
                if check_pos(piece_array, coord=position):
                    if piece_array[get_occupier(piece_array, coord=position)].color == active_color:
                        selected_piece = get_occupier(piece_array, coord=position)
                        se_pos = pygame.mouse.get_pos()

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


    if input_event.type == MOUSEMOTION:
        if selected_piece:
            se_pos = pygame.mouse.get_pos()


# Run the game loop
while True:
    for event in pygame.event.get():
        handle_input(event)
        draw_shogi_board_pygame()
