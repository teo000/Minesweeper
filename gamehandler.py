import pygame

from game_options import GameOptions
from minesweeper import Minesweeper, CellStatus

SQ_SIZE = 30

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


BTN_SIZE = 50
CTR_PADDING = 10
CTR_HEIGHT = 60
CTR_WIDTH = 60

HAPPY_PATH = "resources/images/happy.png"
DEAD_PATH = "resources/images/dead.png"
QUESTION_PATH = "resources/images/question_face.png"

GRAY = (200, 200, 200)

SQ_SIZE = 30
TOP_BAR_HEIGHT = 100


def load_and_scale_image(image_path):
    img = pygame.image.load(image_path)
    return pygame.transform.scale(img, (BTN_SIZE, BTN_SIZE))


class GameHandler:
    def __init__(self, game_options: GameOptions, is_timed=False, time_limit=None):
        self.is_timed = is_timed
        self.bombs_no = game_options.bombs_no
        self.grid_height = game_options.grid_height
        self.grid_width = game_options.grid_width
        width = self.grid_width * SQ_SIZE

        self.game = Minesweeper(self.grid_width, self.grid_height, SQ_SIZE, self.bombs_no, TOP_BAR_HEIGHT)
        self.reset_button = Button(HAPPY_PATH, width // 2 - BTN_SIZE,
                                   (TOP_BAR_HEIGHT - BTN_SIZE) // 2)
        self.menu_button = Button(QUESTION_PATH, width // 2,
                                  (TOP_BAR_HEIGHT - BTN_SIZE) // 2)
        self.bombs_count = BombsCount(CTR_PADDING, (TOP_BAR_HEIGHT - CTR_HEIGHT) // 2,
                                      CTR_WIDTH, CTR_HEIGHT)

        self.timer = Timer(width - CTR_PADDING - CTR_WIDTH, (TOP_BAR_HEIGHT - CTR_HEIGHT) // 2,
                           CTR_WIDTH, CTR_HEIGHT, count_backwards=is_timed, time_limit=time_limit)
        self.bombs_count.set_bombs_no(self.bombs_no)

        screen_width = self.grid_width * SQ_SIZE
        screen_height = self.grid_height * SQ_SIZE + TOP_BAR_HEIGHT

        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.return_to_menu = False

    def draw(self):
        self.screen.fill(GRAY)

        for row in self.game.squares:
            for square in row:
                self.screen.blit(IMAGES[square.status], square.position)

        self.reset_button.draw(self.screen)

        self.menu_button.draw(self.screen)
        self.bombs_count.draw(self.screen)
        self.timer.draw(self.screen)

    def process_left_click(self, mouse_x, mouse_y):
        if mouse_y > TOP_BAR_HEIGHT and not self.game.is_over:
            self.game.process_left_click(mouse_x, mouse_y)
        elif self.reset_button.is_clicked(mouse_x, mouse_y):
            self.timer.reset()
            self.bombs_count.set_bombs_no(self.bombs_no)
            self.game = Minesweeper(self.grid_width, self.grid_height, SQ_SIZE, self.bombs_no, TOP_BAR_HEIGHT)
            self.reset_button.img = load_and_scale_image(HAPPY_PATH)
        elif self.menu_button.is_clicked(mouse_x, mouse_y):
            self.return_to_menu = True

    def process_right_click(self, mouse_x, mouse_y):
        if mouse_y > TOP_BAR_HEIGHT and not self.game.is_over:
            self.game.process_right_click(mouse_x, mouse_y)
            self.bombs_count.set_bombs_no(self.bombs_no - self.game.flags_no)

    def game_loop(self):
        clock = pygame.time.Clock()

        while not self.return_to_menu:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.process_left_click(event.pos[0], event.pos[1])
                    if event.button == 3:
                        self.process_right_click(event.pos[0], event.pos[1])

            if self.is_timed and self.timer.time == 0:
                self.game.is_over = True

            if not self.game.is_over:
                self.timer.update()

            if self.game.is_over:
                self.reset_button.img = load_and_scale_image(DEAD_PATH)

            self.draw()

            pygame.display.flip()
            clock.tick(60)


class Button:
    def __init__(self, img_path, x, y):
        self.rect = pygame.Rect(x, y, BTN_SIZE, BTN_SIZE)
        self.img = load_and_scale_image(img_path)

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def is_clicked(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            print("btn clicked")
            return True


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
default_font = pygame.font.get_default_font()


class Counter:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(default_font, 28)
        self.surface = pygame.Surface((width, height))

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class BombsCount(Counter):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def set_bombs_no(self, bombs_no):
        self.surface.fill(BLACK)
        bombs_count = self.font.render(str(bombs_no), True, WHITE)
        rect = bombs_count.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(bombs_count, rect)


class Timer(Counter):
    def __init__(self, x, y, width, height, count_backwards=False, time_limit=None):
        super().__init__(x, y, width, height)
        self.initial_time = pygame.time.get_ticks()
        self.time_limit = time_limit + 1 if time_limit is not None else None
        self.get_current_time = self.count_backwards if count_backwards else self.count_forward
        self.time = self.get_current_time()

    def update(self):
        self.surface.fill(BLACK)
        self.time = self.get_current_time()
        timer_text = self.font.render(str(self.time), True, WHITE)
        rect = timer_text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(timer_text, rect)

    def count_forward(self):
        time = (pygame.time.get_ticks() - self.initial_time) // 1000
        if time > 999:
            time = 999
        return time

    def count_backwards(self):
        time = self.time_limit + (self.initial_time - pygame.time.get_ticks()) // 1000
        if time < 0:
            time = 0
        return time

    def reset(self):
        self.initial_time = pygame.time.get_ticks()
        self.time = self.get_current_time()
