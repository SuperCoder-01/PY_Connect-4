from math import floor
import pygame as pg
from board import Board, COLORS
pg.init()

# Setup
turn = 0
pg.display.set_caption("Connect 4")
Font = pg.font.SysFont("arial", 75)
running: bool = True

board: Board = Board(6, 7, 90)
screen = pg.display.set_mode(board.SIZE)

board.update(screen)
pg.display.update()

# Main game loop
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

        # Mouse events
        if event.type == pg.MOUSEMOTION:
            pg.draw.rect(screen, COLORS["BLACK"], (0, 0, board.WIDTH, board.SQUARE_SIZE))
            posX = event.pos[0]
            if turn == 0:
                pg.draw.circle(screen, COLORS["RED"], (posX, int(board.SQUARE_SIZE / 2)), board.CIRCLE_RADIUS)
            else:
                pg.draw.circle(screen, COLORS["YELLOW"], (posX, int(board.SQUARE_SIZE / 2)), board.CIRCLE_RADIUS)

        pg.display.update()

        if event.type == pg.MOUSEBUTTONDOWN:
            pg.draw.rect(screen, COLORS["BLACK"], (0, 0, board.WIDTH, board.SQUARE_SIZE))
            posX = event.pos[0]
            col = int(floor(posX / board.SQUARE_SIZE))
            if turn == 0: # Player 1's turn
                if board.is_valid(col):
                    row = board.get_next_open_row(col)
                    board.drop_piece(row, col, 1)

                    # Check for win
                    if board.winning_move(1):
                        label = Font.render("Red wins!", True, COLORS["RED"])
                        screen.blit(label, (40, 10))
                        running = False
                        continue
            elif board.is_valid(col): # Player 2's turn
                row: int | None = board.get_next_open_row(col)
                board.drop_piece(row, col, 2)
                # Check for win
                if board.winning_move(2):
                    label = Font.render("Yellow wins!", True, COLORS["YELLOW"])
                    screen.blit(label, (40, 10))
                    running = False
                    continue

            # Check for draw
            for col in range(board.COLUMNS):
                if board.get_next_open_row(col) is not None:
                    break
            else:
                label = Font.render("It's a draw", True, COLORS["ORANGE"])
                screen.blit(label, (40, 10))
                running = False

            board.update(screen)
            turn += 1
            turn %= 2

# Game ended
pg.time.wait(3000)