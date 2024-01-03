import pygame

from minesweeper import Minesweeper, CellStatus

pygame.init()


GRID_WIDTH, GRID_HEIGHT = 15, 15
MAX_SQ_WIDTH, MAX_SQ_HEIGHT = 50, 50
SQ_SIZE = 50
BOMBS_NO = 15

SCREEN_WIDTH = SQ_SIZE * GRID_WIDTH
SCREEN_HEIGHT = SQ_SIZE * GRID_WIDTH

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 250)

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


clock = pygame.time.Clock()


game = Minesweeper(GRID_WIDTH, GRID_HEIGHT, SQ_SIZE, BOMBS_NO)
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                game.process_click(event.pos[0], event.pos[1])

    screen.fill((255, 255, 255))

    for row in game.squares:
        for square in row:
            screen.blit(IMAGES[square.status], square.position)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
