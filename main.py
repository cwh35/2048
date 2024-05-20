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

    def setPosition(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECTANGLE_HEIGHT)
            self.col = math.ceil(self.x / RECTANGLE_WIDTH)
        else:
            self.row = math.floor(self.y / RECTANGLE_HEIGHT)
            self.col = math.floor(self.x / RECTANGLE_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

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

def getRandomPosition(tiles):
    row = None
    col = None
    while True:
        # pick a random position
        row = random.randrange(0, ROWS) # generate up to ROWS - 1
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col

def moveTiles(window, tiles, clock, direction):
    updated = True
    blocks = set() # which tiles have already merged in a movement

    if direction == "left":
        sortFunction = lambda x: x.col
        reverse = False # start with the largest column elements, furthest to the right
        delta = (-MOVE_VELOCITY, 0) # how much we need to move the tiles
        boundaryCheck = lambda tile: tile.col == 0 # check if the tile is at the boundary
        getNextTile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}") # get the next tile in the direction we are moving
        mergeCheck = lambda tile, nextTile: tile.x > nextTile.x + MOVE_VELOCITY # check if the tiles can merge
        moveCheck = lambda tile, nextTile: tile.x > nextTile.x + RECTANGLE_WIDTH + MOVE_VELOCITY # check if the tiles can move
        ceil = True # round up when moving to left
    elif direction == "right":
        sortFunction = lambda x: x.col
        reverse = True 
        delta = (MOVE_VELOCITY, 0) # how much we need to move the tiles
        boundaryCheck = lambda tile: tile.col == COLS - 1 # check if the tile is at the boundary
        getNextTile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}") # get the next tile in the direction we are moving
        mergeCheck = lambda tile, nextTile: tile.x < nextTile.x - MOVE_VELOCITY # check if the tiles can merge
        moveCheck = lambda tile, nextTile: tile.x + RECTANGLE_WIDTH + MOVE_VELOCITY < nextTile.x # check if the tiles can move
        ceil = False # round down when moving to right
    elif direction == "up":
        sortFunction = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VELOCITY) # how much we need to move the tiles
        boundaryCheck = lambda tile: tile.row == 0 # check if the tile is at the boundary
        getNextTile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}") # get the next tile in the direction we are moving
        mergeCheck = lambda tile, nextTile: tile.y > nextTile.y + MOVE_VELOCITY # check if the tiles can merge
        moveCheck = lambda tile, nextTile: tile.y > nextTile.y + RECTANGLE_HEIGHT + MOVE_VELOCITY # check if the tiles can move
        ceil = True # round up when moving up
    elif direction == "down":
        sortFunction = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VELOCITY) # how much we need to move the tiles
        boundaryCheck = lambda tile: tile.row == ROWS - 1 # check if the tile is at the boundary
        getNextTile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}") # get the next tile in the direction we are moving
        mergeCheck = lambda tile, nextTile: tile.y < nextTile.y - MOVE_VELOCITY # check if the tiles can merge
        moveCheck = lambda tile, nextTile: tile.y + RECTANGLE_HEIGHT + MOVE_VELOCITY < nextTile.y # check if the tiles can move
        ceil = False # round down when moving down

    while updated:
        clock.tick(FPS)
        updated = False
        sortedTiles = sorted(tiles.values(), key=sortFunction, reverse=reverse)

        for i, tile in enumerate(sortedTiles): # get index of tile and tile object itself
            if boundaryCheck(tile):
                continue
            
            nextTile = getNextTile(tile) # tile in the way of which we want to move
            if not nextTile:
                tile.move(delta)
            elif tile.value == nextTile.value and tile not in blocks and nextTile not in blocks:
                if mergeCheck(tile, nextTile): # are we in the process of merging?
                    tile.move(delta)
                else:
                    nextTile.value *= 2
                    sortedTiles.pop(i)
                    blocks.add(nextTile)
            elif moveCheck(tile, nextTile):
                tile.move(delta)
            else: 
                continue

            tile.setPosition(ceil)
            updated = True

        updateTiles(window, tiles, sortedTiles)

    endMove(tiles)

def endMove(tiles):
    if len(tiles) == 16:
        return "lost"
    
    row, col = getRandomPosition(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def updateTiles(window, tiles, sortedTiles):
    tiles.clear()
    for tile in sortedTiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)

def generateTiles():
    tiles = {}

    for _ in range(2):
        row, col = getRandomPosition(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles

def main(window):
    clock = pygame.time.Clock() # regulates speed of the loop
    run = True # game loop

    tiles = generateTiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if we press the exit button
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveTiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    moveTiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    moveTiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    moveTiles(window, tiles, clock, "down")

        draw(window, tiles)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)