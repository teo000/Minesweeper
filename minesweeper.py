import random
from enum import Enum
from math import trunc


class CellStatus(Enum):
    UNKNOWN = -1,
    SAFE = 0
    ONE = 1,
    TWO = 2,
    THREE = 3,
    FOUR = 4,
    FIVE = 5,
    SIX = 6,
    SEVEN = 7,
    EIGHT = 8,
    BOMB = 9,
    BOOM = 10
    FLAGGED = 11


class Square:
    def __init__(self, position, status: CellStatus):
        self.position = position
        self.status = status

class Minesweeper:
    def __init__(self, grid_width, grid_height, sq_size, bombs_no):
        self.BOMBS_NO = bombs_no
        self.SQ_SIZE = sq_size
        self.GRID_HEIGHT = grid_height
        self.GRID_WIDTH = grid_width
        # squares_pos = self.init_squares_pos()
        # self.squares_status = [[CellStatus.UNKNOWN for _ in range(grid_width)] for _ in range(grid_height)]
        self.squares = [[Square((j * self.SQ_SIZE, i * self.SQ_SIZE), CellStatus.UNKNOWN)
                         for i in range(grid_width)] for j in range(grid_height)]
        # self.bombs = self.generate_bombs()

    def init_squares_pos(self):
        squares = []
        for i in range(self.GRID_HEIGHT):
            for j in range(self.GRID_WIDTH):
                position = (
                    j * self.SQ_SIZE,
                    i * self.SQ_SIZE,
                )
                squares.append(position)
        return squares

    def generate_bombs(self):
        pass

    def process_click(self, mouse_x, mouse_y):
        line, col = trunc(mouse_x/self.SQ_SIZE), trunc(mouse_y/self.SQ_SIZE)
        print(f'square {line}, {col} was clicked')
        self.squares[line][col].status = CellStatus.SAFE
            # random.randint(1, 10)



