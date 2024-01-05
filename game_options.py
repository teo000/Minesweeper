
class GameOptions:
    def __init__(self, grid_width, grid_height, bombs_no):
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

