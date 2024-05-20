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

class Tile:
    COLORS = [
        # these colors are from the actual 2048 game
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECTANGLE_WIDTH
        self.y = row * RECTANGLE_HEIGHT

    def getColor(self):
        # get correct color based on the value of the tile
        colorIndex = int(math.log2(self.value)) - 1
        color = self.COLORS[colorIndex]

        return color

    def draw(self, window):
        # draw the rectangle of the tile, then draw the text on top of the tile
        color = self.getColor()
        pygame.draw.rect(window, color, (self.x, self.y, RECTANGLE_WIDTH, RECTANGLE_HEIGHT))

        # this creates a surface that contains the text
        text = FONT.render(str(self.value), 1, FONT_COLOR) # 1 is for anti-aliasing
        # where we want to put the text
        window.blit(
            text, 
            (
            self.x + (RECTANGLE_WIDTH / 2 - text.get_width() / 2),
            self.y + (RECTANGLE_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def setPosition(self):
        pass

    def move(self, delta):
        pass

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
    

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR) # fill window w/ background color

    for tile in tiles.values():
        tile.draw(window)

    drawGrid(window)
    pygame.display.update() # update the window

def main(window):
    clock = pygame.time.Clock() # regulates speed of the loop
    run = True # game loop

    tiles = {
        "00": Tile(4, 0, 0),
        "20": Tile(128, 2, 0),
        "02": Tile(64, 0, 2),
    }

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if we press the exit button
                run = False
                break

        draw(window, tiles)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)