import pygame

from gamehandler import GameHandler
from minesweeper import Minesweeper, CellStatus

pygame.init()

GRID_WIDTH, GRID_HEIGHT = 15, 20
MAX_SQ_WIDTH, MAX_SQ_HEIGHT = 50, 50
SQ_SIZE = 30
BOMBS_NO = 40
TOP_BAR_HEIGHT = 100

SCREEN_WIDTH = SQ_SIZE * GRID_WIDTH
SCREEN_HEIGHT = SQ_SIZE * GRID_HEIGHT + TOP_BAR_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Minesweeper")

IMG_PATHS = {
    CellStatus.UNKNOWN: 'resources/images/blank_cell.png',
    CellStatus.ONE: 'resources/images/one.png',
    CellStatus.TWO: 'resources/images/two.png',
    CellStatus.THREE: 'resources/images/three.png',
    CellStatus.FOUR: 'resources/images/four.png',
    CellStatus.FIVE: 'resources/images/five.png',
    CellStatus.SIX: 'resources/images/six.png',
    CellStatus.SEVEN: 'resources/images/seven.png',
    CellStatus.EIGHT: 'resources/images/eight.png',
    CellStatus.BOMB: 'resources/images/bomb.png',
    CellStatus.BOOM: 'resources/images/boom.png',
    CellStatus.SAFE: 'resources/images/gray_cell.png',
    CellStatus.FLAGGED: 'resources/images/flag.png',
}

IMAGES = {}

for cell_status in CellStatus:
    img = pygame.image.load(IMG_PATHS[cell_status])
    scaled_img = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))
    IMAGES[cell_status] = scaled_img


game_handler = GameHandler(screen, SCREEN_WIDTH, TOP_BAR_HEIGHT, GRID_WIDTH, GRID_HEIGHT, SQ_SIZE, BOMBS_NO)
clock = pygame.time.Clock()

running = True

while running:
    game = game_handler.game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                game_handler.process_left_click(event.pos[0], event.pos[1])
            if event.button == 3:
                game_handler.process_right_click(event.pos[0], event.pos[1])


    screen.fill(GRAY)
    game_handler.draw()

    for row in game.squares:
        for square in row:
            screen.blit(IMAGES[square.status], square.position)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
