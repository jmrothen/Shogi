from board import *
import sys
import pygame
from pygame.locals import *

# Initialize the game
pygame.init()

# Set up the screen
screen_width = 1300
screen_height = 1000
board_width = 900
board_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shogi Board')

# Colors
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
WHITE = (255, 255, 255)
IVORY = (255, 255, 240)


# Function to draw the Shogi board
def draw_shogi_board_pygame(piece_array=None, save_path=None):
    if not piece_array:
        piece_array = create_piece_array()

    # Fill background
    screen.fill(BEIGE)

    # Draw grid lines
    cell_size = board_width // 9
    for i in range(11):
        pygame.draw.line(screen, BLACK, (i * cell_size, 100), (i * cell_size, screen_height))
        pygame.draw.line(screen, BLACK, (100, i * cell_size), (board_width+100, i * cell_size))

    # Draw the extra space divided into three squares
    square_height = (screen_height - 100) // 3
    for i in range(1, 4):
        pygame.draw.rect(screen, BLACK, (board_width+100, (i-1) * square_height+100, screen_width-board_width, square_height), 1)

    # Font for text
    font = pygame.font.SysFont(None, 14)

    # Add labels for columns above the board
    col_labels = list(range(1, 10))[::-1]
    for i, label in enumerate(col_labels):
        text = font.render(str(label), True, BLACK)
        screen.blit(text, (i * cell_size + cell_size // 2, 0 - 20 + 100))  # Adjusted y-coordinate

    # Add labels for rows to the left of the board
    row_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'][::-1]
    for i, label in enumerate(row_labels):
        text = font.render(label, True, BLACK)
        screen.blit(text, (0 - 20 + 100, i * cell_size + cell_size // 2))  # Adjusted x-coordinate

    # Place pieces on the board
    for piece in piece_array:
        if piece.is_alive:
            row, col = pos_to_xy(piece.pos)
            text = font.render(piece.shorthand(), True, BLACK)
            screen.blit(text, (col * cell_size + cell_size // 2, (8 - row) * cell_size + cell_size // 2))

    # Update the display
    pygame.display.flip()

    # Save the screen to a file
    if save_path:
        pygame.image.save(screen, save_path)


# Example usage
draw_shogi_board_pygame()

# Main loop (for demonstration purposes)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
