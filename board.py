from itertools import product
from numpy import zeros
import pygame as pg

# Colors (RGB)
COLORS: dict[str, tuple[int, int, int]] = {
    "BLUE": (0, 0, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "ORANGE": (255, 165, 0)
}

class Board:
    """Game board"""

    def __init__(self, rows: int, columns: int, square_size: int):
        self.ROWS: int = rows
        self.COLUMNS: int = columns
        self.SQUARE_SIZE: int = square_size
        self.WIDTH: int = self.COLUMNS * self.SQUARE_SIZE
        self.HEIGHT: int = (self.ROWS + 1) * self.SQUARE_SIZE
        self.CIRCLE_RADIUS: int = int(self.SQUARE_SIZE / 2 - 5)
        self.SIZE: tuple[int, int] = (self.WIDTH, self.HEIGHT)

        self.board = zeros((self.ROWS, self.COLUMNS))

    def drop_piece(self, row: int | None, col: int, piece: int):
        self.board[row][col] = piece

    def is_valid(self, col: int) -> bool:
        return self.board[self.ROWS - 1][col] == 0 # Check if at least one row is empty

    def get_next_open_row(self, col: int) -> int | None:
        for r in range(self.ROWS):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece: int) -> bool | None:
        # Check horizontal locations
        for col, row in product(range(self.COLUMNS - 3), range(self.ROWS)):
            if self.board[row][col] == piece and self.board[row][col + 1] == piece and self.board[row][col + 2] == piece and self.board[row][col + 3] == piece:
                return True
        # Check vertical locations
        for col, row in product(range(self.COLUMNS), range(self.ROWS - 3)):
            if self.board[row][col] == piece and self.board[row + 1][col] == piece and self.board[row + 2][col] == piece and self.board[row + 3][col] == piece:
                return True
        # Check diagonal locations
        for col, row in product(range(self.COLUMNS - 3), range(self.ROWS - 3)):
            if self.board[row][col] == piece and self.board[row + 1][col + 1] == piece and self.board[row + 2][col + 2] == piece and self.board[row + 3][col + 3] == piece:
                return True
        for col, row in product(range(self.COLUMNS - 3), range(3, self.ROWS)):
            if self.board[row][col] == piece and self.board[row - 1][col + 1] == piece and self.board[row - 2][col + 2] == piece and self.board[row - 3][col + 3] == piece:
                return True

    def update(self, screen: pg.Surface):
        for c in range(self.COLUMNS):
            for r in range(self.ROWS):
                pg.draw.rect(screen, COLORS["BLUE"], (c * self.SQUARE_SIZE, r * self.SQUARE_SIZE + self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                pg.draw.circle(screen, COLORS["BLACK"], (int((c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), int(r * self.SQUARE_SIZE + self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.CIRCLE_RADIUS)
        for c in range(self.COLUMNS):
            for r in range(self.ROWS):
                if self.board[r][c] == 1:
                    pg.draw.circle(screen, COLORS["RED"], (int((c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.HEIGHT - int(r * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.CIRCLE_RADIUS)
                elif self.board[r][c] == 2:
                    pg.draw.circle(screen, COLORS["YELLOW"], (int((c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.HEIGHT - int(r * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.CIRCLE_RADIUS)
        pg.display.update()