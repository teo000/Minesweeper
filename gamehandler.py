import pygame

from minesweeper import Minesweeper, CellStatus

RESET_BTN_SIZE = 50


class GameHandler:
    def __init__(self, screen, width, top_bar_height, grid_width, grid_height, sq_size, bombs_no):
        self.bombs_no = bombs_no
        self.sq_size = sq_size
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.top_bar_height = top_bar_height
        self.game = Minesweeper(self.grid_width, self.grid_height, self.sq_size, self.bombs_no, top_bar_height)
        self.reset_button = ResetButton(screen, (width - RESET_BTN_SIZE) // 2, (top_bar_height - RESET_BTN_SIZE) // 2)

    def draw(self):
        self.reset_button.draw()

    def process_left_click(self, mouse_x, mouse_y):
        if mouse_y > self.top_bar_height and not self.game.is_over:
            self.game.process_left_click(mouse_x, mouse_y)
        elif self.reset_button.is_clicked(mouse_x, mouse_y):
            self.game = Minesweeper(self.grid_width, self.grid_height, self.sq_size, self.bombs_no, self.top_bar_height)


HAPPY_PATH = "resources/images/happy.png"
DEAD_PATH = "resources/images/dead.png"

img = pygame.image.load(HAPPY_PATH)
happy_img = pygame.transform.scale(img, (RESET_BTN_SIZE, RESET_BTN_SIZE))

class ResetButton:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.happy_rect = happy_img.get_rect(topleft=(x, y))

    def draw(self):
        self.screen.blit(happy_img, self.happy_rect)

    def is_clicked(self, mouse_x, mouse_y):
        if self.happy_rect.collidepoint(mouse_x, mouse_y):
            print("reset btn clicked")
            return True
