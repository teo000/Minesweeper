import pygame

from minesweeper import Minesweeper

BTN_SIZE = 50
CTR_PADDING = 10
CTR_HEIGHT = 60
CTR_WIDTH = 100

HAPPY_PATH = "resources/images/happy.png"
DEAD_PATH = "resources/images/dead.png"
QUESTION_PATH = "resources/images/question_face.png"


def load_and_scale_image(image_path):
    img = pygame.image.load(image_path)
    return pygame.transform.scale(img, (BTN_SIZE, BTN_SIZE))


class GameHandler:
    def __init__(self, screen, width, top_bar_height, grid_width, grid_height, sq_size, bombs_no):
        self.bombs_no = bombs_no
        self.sq_size = sq_size
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.top_bar_height = top_bar_height

        self.game = Minesweeper(self.grid_width, self.grid_height, self.sq_size, self.bombs_no, top_bar_height)
        self.reset_button = Button(screen, HAPPY_PATH, width // 2 - BTN_SIZE,
                                   (top_bar_height - BTN_SIZE) // 2)
        self.customize_button = Button(screen, QUESTION_PATH, width // 2,
                                       (top_bar_height - BTN_SIZE) // 2)
        self.bombs_count = BombsCount(screen, CTR_PADDING, (top_bar_height - CTR_HEIGHT) // 2,
                                      CTR_WIDTH, CTR_HEIGHT)

        self.timer = Timer(screen, width - CTR_PADDING - CTR_WIDTH, (top_bar_height - CTR_HEIGHT) // 2,
                           CTR_WIDTH, CTR_HEIGHT)
        self.bombs_count.set_bombs_no(bombs_no)

    def draw(self):
        self.reset_button.draw()
        self.customize_button.draw()
        self.bombs_count.draw()
        self.timer.update()
        self.timer.draw()

    def process_left_click(self, mouse_x, mouse_y):
        if mouse_y > self.top_bar_height and not self.game.is_over:
            self.game.process_left_click(mouse_x, mouse_y)
        elif self.reset_button.is_clicked(mouse_x, mouse_y):
            self.game = Minesweeper(self.grid_width, self.grid_height, self.sq_size, self.bombs_no, self.top_bar_height)
            self.timer.reset()
        elif self.customize_button.is_clicked(mouse_x, mouse_y):
            pass

    def process_right_click(self, mouse_x, mouse_y):
        if mouse_y > self.top_bar_height:
            self.game.process_right_click(mouse_x, mouse_y)
            self.bombs_count.set_bombs_no(self.bombs_no - self.game.flags_no)


class Button:
    def __init__(self, screen, img_path, x, y):
        self.screen = screen
        self.rect = pygame.Rect(x, y, BTN_SIZE, BTN_SIZE)
        self.img = load_and_scale_image(img_path)

    def draw(self):
        self.screen.blit(self.img, self.rect)

    def is_clicked(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            print("btn clicked")
            return True


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
default_font = pygame.font.get_default_font()


class Counter:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(default_font, 36)
        self.surface = pygame.Surface((width, height))

    def draw(self):
        self.screen.blit(self.surface, self.rect)


class BombsCount(Counter):
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)

    def set_bombs_no(self, bombs_no):
        self.surface.fill(BLACK)
        bombs_count = self.font.render(str(bombs_no), True, WHITE)
        rect = bombs_count.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(bombs_count, rect)


class Timer(Counter):
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)
        self.counts_up = True
        self.initial_time = pygame.time.get_ticks()

    def update(self):
        self.surface.fill(BLACK)
        time = (pygame.time.get_ticks() - self.initial_time) // 1000
        if time > 999:
            time = 999
        timer_text = self.font.render(str(time), True, WHITE)
        rect = timer_text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(timer_text, rect)

    def reset(self):
        self.initial_time = pygame.time.get_ticks()
