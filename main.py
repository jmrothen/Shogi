import math

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

    # Draw the pieces
    for index, i in enumerate(piece_array):
        if selected_piece and index == selected_piece:
            text = pygame.font.SysFont(None, 50).render(i.shorthand(), True, BLACK)
            text_rect = text.get_rect(center=(se_pos[0], se_pos[1]))
            screen.blit(text, text_rect)
        elif i.is_alive:
            row, col = i.pos
            text = pygame.font.SysFont(None, 50).render(i.shorthand(), True, BLACK)
            text_rect = text.get_rect(center=(width_gap + col * cell_size + cell_size // 2,
                                              height_gap_top + row * cell_size + cell_size // 2))
            screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # Save the screen to a file
    if save_path:
        pygame.image.save(screen, save_path)


# Example usage
# draw_shogi_board_pygame()

# initial safety variables
selected_piece = None  # index of the clicked piece
piece_array = create_piece_array()  # array of pieces
error_text = None  # possible error text that i might draw on screen if needed
se_pos = None  # tracked for selected piece to follow mouse



def handle_input(event):
    global selected_piece
    global se_pos
    global error_text
    global piece_array

    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        print(x, y)
        x -= width_gap
        y -= height_gap_top
        if 0 <= x < board_width and 0 <= y < board_height:
            col = x // cell_size
            row = y // cell_size
            position = [row, col]
            print(position)
            if selected_piece:
                try:
                    piece_array = move_piece(piece_array, index=selected_piece, coord=position)
                    selected_piece = None
                    se_pos = None
                except ValueError as e:
                    # if it doesn't work, we'll just reset the selected piece
                    error_text = e
                    selected_piece = None
                    se_pos = None
            else:
                if check_pos(piece_array, coord=position):
                    selected_piece = get_occupier(piece_array, coord=position)
                    se_pos = pygame.mouse.get_pos()
    if event.type == MOUSEMOTION:
        if selected_piece:
            se_pos = pygame.mouse.get_pos()


# Run the game loop
while True:
    for event in pygame.event.get():
        handle_input(event)
        draw_shogi_board_pygame()
