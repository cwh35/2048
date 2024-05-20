import pygame
import random
import math

pygame.init() # initializing the features we need

# constant definitions
FPS = 60 # frames per second, how quickly the game is running
WIDTH, HEIGHT = 800, 800 # window size, square
ROWS, COLS = 4, 4 # number of rows and columns in the grid

RECTANGLE_HEIGHT = HEIGHT // ROWS # height of each rectangle
RECTANGLE_WIDTH = WIDTH // COLS # width of each rectangle

OUTLINE_COLOR = (187, 173, 160) # color of the outline of the grid
OUTLINE_THICKNESS = 10 # thickness of the outline of the grid
BACKGROUND_COLOR = (205, 192, 180) # color of the background of the grid
FONT_COLOR = (119, 110, 101) # color of the font of the numbers


FONT = pygame.font.SysFont("comicsans", 60, bold=True) # setting font
MOVE_VELOCITY = 20 # 20 pixels per second

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # setting the window size
pygame.display.set_caption("2048") # setting title