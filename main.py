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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
