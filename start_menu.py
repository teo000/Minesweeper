import pygame
import pygame_menu
import game_options
from gamehandler import GameHandler

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500


def menu_loop():
    def submit_onclick():
        difficulty = difficulty_selector.get_value()[0][1]
        is_timed = timed_mode.is_visible()
        time_limit = timer_input.get_value() if is_timed else None
        validation_error = check_valid_timer(is_timed, time_limit)
        if validation_error is not None:
            show_validation_error(validation_error)
            return

        if difficulty == game_options.CUSTOM:
            lines = lines_input.get_value()
            columns = columns_input.get_value()
            bombs = bombs_input.get_value()
            validation_error = check_valid_options(lines, columns, bombs)
            if validation_error is not None:
                show_validation_error(validation_error)
                return
            difficulty = game_options.GameOptions(columns, lines, bombs)

        game_handler = GameHandler(difficulty, is_timed, time_limit)
        game_handler.game_loop()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def check_valid_options(lines, columns, bombs):
        if lines <= 0:
            return 'Enter a valid number of lines'
        if lines > 30:
            return 'Lines should be less than 30'
        if columns <= 0:
            return 'Enter a valid number of columns'
        if columns > 64:
            return 'Columns should be less than 64'
        if bombs <= 0:
            return 'There must be more at least one bomb'
        if bombs > lines * columns:
            return f'Bombs should be less than {lines * columns}'
        return None

    def show_validation_error(message):
        error_label.set_title(message)
        error_label.show()

    def check_valid_timer(is_timed, time_limit):
        if not is_timed:
            return None
        if time_limit <= 0:
            return 'Time limit must be positive'
        return None

    def timed_mode_onclick():
        timer_input.hide()
        not_timed_mode.show()
        timed_mode.hide()

    def not_timed_mode_onclick():
        timer_input.show()
        not_timed_mode.hide()
        timed_mode.show()

    def select_difficulty(selected_value, difficulty):
        if difficulty == game_options.CUSTOM:
            lines_input.show()
            columns_input.show()
            bombs_input.show()
        else:
            lines_input.hide()
            columns_input.hide()
            bombs_input.hide()

    pygame.init()

    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    menu = pygame_menu.Menu('Minesweeper', SCREEN_WIDTH, SCREEN_HEIGHT,
                            theme=pygame_menu.themes.THEME_DEFAULT)
    pygame.display.set_caption("Minesweeper")
    icon_image = pygame.image.load('resources/images/bomb.png')
    pygame.display.set_icon(icon_image)

    items = [
        ('Easy', game_options.EASY),
        ('Medium', game_options.MEDIUM),
        ('Hard', game_options.HARD),
        ('Custom', game_options.CUSTOM)
    ]

    difficulty_selector = menu.add.selector(
        title='Difficulty:\t',
        items=items,
        onreturn=select_difficulty,
        onchange=select_difficulty
    )

    lines_input = menu.add.text_input('Lines: ',
                                      input_type=pygame_menu.locals.INPUT_INT,
                                      input_underline='_',
                                      maxchar=3)
    lines_input.hide()
    columns_input = (
        menu.add.text_input('Columns: ',
                            input_type=pygame_menu.locals.INPUT_INT,
                            input_underline='_',
                            maxchar=3)
    )
    columns_input.hide()
    bombs_input = menu.add.text_input('Bombs: ',
                                      input_type=pygame_menu.locals.INPUT_INT,
                                      input_underline='_',
                                      maxchar=5)
    bombs_input.hide()

    not_timed_mode = menu.add.button('Not Timed Mode',
                                     not_timed_mode_onclick)
    timed_mode = menu.add.button('Timed Mode', timed_mode_onclick)
    timed_mode.hide()
    timer_input = menu.add.text_input('Time limit (s): ',
                                      input_type=pygame_menu.locals.INPUT_INT,
                                      input_underline='_',
                                      maxchar=3)
    timer_input.hide()

    error_label = menu.add.label('Error: ', font_color=(255, 50, 50))
    error_label.hide()

    menu.add.button('Submit', submit_onclick,
                    background_color=(47, 48, 51), font_color=(255, 255, 255))

    menu.mainloop(surface)

    pygame.quit()
