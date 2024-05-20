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

def drawGrid(window):
    # draw horizontal grid lines
    for row in range(1, ROWS):
        y = row * RECTANGLE_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    # draw vertical grid lines
    for col in range(1, COLS):
        x = col * RECTANGLE_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    # draw the border
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS) # use outline thickness for a hollow rectangle (not filled in)
    

def draw(window):
    window.fill(BACKGROUND_COLOR) # fill window w/ background color
    drawGrid(window)
    pygame.display.update() # update the window

def main(window):
    clock = pygame.time.Clock() # regulates speed of the loop
    run = True # game loop

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if we press the exit button
                run = False
                break

        draw(window)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)