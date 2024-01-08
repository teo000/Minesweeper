
class GameOptions:
    def __init__(self, grid_width, grid_height, bombs_no):
        """
            Initializes the GameOptions instance with grid dimensions and
            bomb count.

            Parameters:
            - grid_width (int): The width of the game grid.
            - grid_height (int): The height of the game grid.
            - bombs_no (int): The number of bombs in the game.
        """
        self.bombs_no = bombs_no
        self.grid_height = grid_height
        self.grid_width = grid_width


EASY = GameOptions(
    bombs_no=10,
    grid_height=8,
    grid_width=8
)

MEDIUM = GameOptions(
    bombs_no=40,
    grid_height=16,
    grid_width=16
)

HARD = GameOptions(
    bombs_no=99,
    grid_height=16,
    grid_width=30
)

CUSTOM = None
