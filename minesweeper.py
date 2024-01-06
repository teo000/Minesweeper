import random
from enum import Enum


class CellStatus(Enum):
    UNKNOWN = -1
    SAFE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    BOMB = 9
    BOOM = 10
    FLAGGED = 11


class Direction(Enum):
    UP = (0, -1)
    UP_RIGHT = (1, -1)
    RIGHT = (1, 0)
    DOWN_RIGHT = (1, 1)
    DOWN = (0, 1)
    DOWN_LEFT = (-1, 1)
    LEFT = (-1, 0)
    UP_LEFT = (-1, -1)


class Square:
    def __init__(self, position, status: CellStatus, is_bomb):
        self.position = position
        self.status = status
        self.is_bomb = is_bomb

    def toggle_flag(self):
        if self.status == CellStatus.UNKNOWN:
            self.status = CellStatus.FLAGGED
        elif self.status == CellStatus.FLAGGED:
            self.status = CellStatus.UNKNOWN


class Minesweeper:
    def __init__(self, grid_width, grid_height, sq_size, bombs_no, top_bar_height):
        self.BOMBS_NO = bombs_no
        self.SQ_SIZE = sq_size
        self.GRID_HEIGHT = grid_height
        self.GRID_WIDTH = grid_width
        self.top_bar_height = top_bar_height
        self.bombs = self.generate_bombs()
        self.squares = [[Square((j * self.SQ_SIZE, i * self.SQ_SIZE + self.top_bar_height), CellStatus.UNKNOWN, self.bombs[i][j])
                         for j in range(grid_width)] for i in range(grid_height)]
        self.is_over = False
        self.flags_no = 0

    def generate_bombs(self):
        bombs_pos = random.sample(
            [(i, j) for i in range(self.GRID_HEIGHT) for j in range(self.GRID_WIDTH)],
            self.BOMBS_NO
        )
        bombs = [[False for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        for pos in bombs_pos:
            bombs[pos[0]][pos[1]] = True

        for i in range(self.GRID_HEIGHT):
            for j in range(self.GRID_WIDTH):
                if bombs[i][j]:
                    print("X", end="   ")
                else:
                    print("0", end="   ")
            print()

        return bombs

    def process_left_click(self, mouse_x, mouse_y):
        clicked_square, line, col = self.get_clicked_square(mouse_x, mouse_y)
        if clicked_square is None:
            return
        print(f'square {line}, {col} was clicked')

        if clicked_square.is_bomb:
            self.is_over = True
            self.reveal_bombs()
            clicked_square.status = CellStatus.BOOM
        else:
            bombs_no = self.compute_bombs_near(line, col)
            if bombs_no > 0:
                clicked_square.status = CellStatus(bombs_no)
            else:
                clicked_square.status = CellStatus.SAFE
                # visited = [[False for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
                # self.reveal_safe_cells(line, col, visited)
                self.reveal_safe_cells(line, col)

    def process_right_click(self, mouse_x, mouse_y):
        clicked_square, line, col = self.get_clicked_square(mouse_x, mouse_y)
        if clicked_square is None:
            return
        print(f'square {line}, {col} was right clicked')
        if clicked_square.status == CellStatus.UNKNOWN:
            clicked_square.status = CellStatus.FLAGGED
            self.flags_no += 1
        elif clicked_square.status == CellStatus.FLAGGED:
            clicked_square.status = CellStatus.UNKNOWN
            self.flags_no -= 1

    def get_clicked_square(self, mouse_x, mouse_y):
        col, line = mouse_x // self.SQ_SIZE, (mouse_y - self.top_bar_height) // self.SQ_SIZE
        if line < 0:
            return None, None, None
        return self.squares[line][col], line, col

    def compute_bombs_near(self, x, y):
        bombs_no = 0
        for dir in Direction:
            if (0 <= x+dir.value[0] < self.GRID_HEIGHT and 0 <= y + dir.value[1] < self.GRID_WIDTH
                    and self.squares[x + dir.value[0]][y + dir.value[1]].is_bomb):
                bombs_no += 1
        return bombs_no

    # def reveal_safe_cells(self, x, y, visited):
    #     visited[x][y] = True
    #     for dir in Direction:
    #         if (0 <= x + dir.value[0] < self.GRID_HEIGHT and 0 <= y + dir.value[1] < self.GRID_WIDTH and
    #                 not visited[x + dir.value[0]][y + dir.value[1]]):
    #             neighbour = self.squares[x + dir.value[0]][y + dir.value[1]]
    #             bombs_no = self.compute_bombs_near(x + dir.value[0], y + dir.value[1])
    #             if not neighbour.is_bomb:
    #                 neighbour.status = CellStatus(bombs_no)
    #                 if bombs_no == 0:
    #                     self.reveal_safe_cells(x + dir.value[0], y + dir.value[1], visited)

    def reveal_safe_cells(self, x, y):
        visited = [[False for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        stack = [(x, y)]

        while len(stack) > 0:
            x, y = stack.pop()
            visited[x][y] = True

            for dir in Direction:
                new_x, new_y = x + dir.value[0], y + dir.value[1]

                if (0 <= new_x < self.GRID_HEIGHT and 0 <= new_y < self.GRID_WIDTH and
                        not visited[new_x][new_y]):
                    neighbour = self.squares[new_x][new_y]
                    bombs_no = self.compute_bombs_near(new_x, new_y)

                    if not neighbour.is_bomb:
                        neighbour.status = CellStatus(bombs_no)
                        if bombs_no == 0:
                            stack.append((new_x, new_y))

    def reveal_bombs(self):
        for line in self.squares:
            for square in line:
                if square.is_bomb:
                    square.status = CellStatus.BOMB
