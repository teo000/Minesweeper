import pygame
import pygame_menu

import game_options
from gamehandler import GameHandler


def menu_loop():
    def submit_onclick():
        game_handler = GameHandler(game_options.MEDIUM)
        game_handler.game_loop()
        pygame.display.set_mode((500, 500))

    def timed_mode_onclick():
        timer_input.hide()
        not_timed_mode.show()
        timed_mode.hide()

    def not_timed_mode_onclick():
        timer_input.show()
        not_timed_mode.hide()
        timed_mode.show()

    def select_difficulty(selected_value, difficulty):
        if difficulty == 'Custom':
            lines_input.show()
            columns_input.show()
            bombs_input.show()
        else:
            lines_input.hide()
            columns_input.hide()
            bombs_input.hide()

    pygame.init()
    surface = pygame.display.set_mode((500, 500))

    menu = pygame_menu.Menu('Minesweeper', 500, 500,
                            theme=pygame_menu.themes.THEME_DEFAULT)
    pygame.display.set_caption("Minesweeper")
    icon_image = pygame.image.load('resources/images/bomb.png')
    pygame.display.set_icon(icon_image)

    items = [('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('Custom', 'Custom')]

    menu.add.selector(
        title='Difficulty:\t',
        items=items,
        onreturn=select_difficulty,
        onchange=select_difficulty
    )

    lines_input = menu.add.text_input("Lines: ", input_type=pygame_menu.locals.INPUT_INT, input_underline='_',
                                      maxchar=3)
    lines_input.hide()
    columns_input = menu.add.text_input("Columns: ", input_type=pygame_menu.locals.INPUT_INT, input_underline='_',
                                        maxchar=3)
    columns_input.hide()
    bombs_input = menu.add.text_input("Bombs: ", input_type=pygame_menu.locals.INPUT_INT, input_underline='_',
                                      maxchar=5)
    bombs_input.hide()

    not_timed_mode = menu.add.button("Not Timed Mode", not_timed_mode_onclick)
    timed_mode = menu.add.button("Timed Mode", timed_mode_onclick)
    timed_mode.hide()
    timer_input = menu.add.text_input("Timer: ", input_type=pygame_menu.locals.INPUT_INT, input_underline='_',
                                      maxchar=4)
    timer_input.hide()

    # error_label = menu.add.label()

    menu.add.button('Submit', submit_onclick, background_color=(47, 48, 51), font_color=(255, 255, 255))

    menu.mainloop(surface)

    pygame.quit()
