import math
import re

import numpy as np
import pandas as pd
import pygame
from pygame.locals import *

######################################################
# PYGAME SECTION

# initialize
# pygame.init()

# make window
# screen = pygame.display.set_mode((800, 600))

# background image
# background = pygame.image.load('shogiboard.png')

#######################################################
# GENERAL FUNCTIONS

# simple board representation
# goal is the make accessing editing the board easy
# just a matter of accessing an index in a vector



board_init()
printb()
move_piece('g8', 'f8')
printb()

"""
# game loop or something
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    screen.fill((255, 255, 255))
    screen.blit(background, (200, 0))
    board_init()
    left, middle, right = pygame.mouse.get_pressed()
    if left:
        mpos = pygame.mouse.get_pos()
    pygame.display.update()
pygame.quit()
"""