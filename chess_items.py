import pygame as pg
from game_config import *

pg.init()
font_obj = pg.font.Font(pg.font.get_default_font(), 15)
board = pg.Surface((CELL_SIZE * CELL_QTY, CELL_SIZE * CELL_QTY))

class Chessboard:
    def __init__(self, parent_surface: pg.Surface, cell_qty: int = CELL_QTY, cell_size : int = CELL_SIZE):
        self.__screen = parent_surface
        self.__screen.blit(board, (WINDOW_SIZE[0] - board.get_width(), WINDOW_SIZE[1] - board.get_height()))
        self.__draw_playboard(cell_qty,cell_size)
        pg.display.update()

    def __draw_playboard(self, cell_qty, cell_size):
        for y in range(CELL_QTY):
            for x in range(CELL_QTY):
                cell = pg.Surface((CELL_SIZE, CELL_SIZE))
                cell.fill(COLORS[(x + y) % 2])
                if y == CELL_QTY - 1:
                    symbol = font_obj.render(ALPHABET[x + 1], 1, COLORS[x % 2])
                    cell.blit(symbol, (5, CELL_SIZE - 15))
                if x == CELL_QTY - 1:
                    symbol = font_obj.render(str(9 - (y + 1)), 1, COLORS[y % 2])
                    cell.blit(symbol, (CELL_SIZE - 15, 5))
                board.blit(cell, (x * CELL_SIZE, y * CELL_SIZE))
        self.__screen.blit(board, (WINDOW_SIZE[0] - board.get_width(), WINDOW_SIZE[1] - board.get_height()))

class Figure(object):
    def __init__(self):
        pass


class Pawn(Figure):
    def __init__(self):
        pass


class Rook(Figure):
    def __init__(self):
        pass


class Bishop(Figure):
    def __init__(self):
        pass


class Queen(Figure):
    def __init__(self):
        pass


class King(Figure):
    def __init__(self):
        pass


class Knight(Figure):
    def __init__(self):
        pass