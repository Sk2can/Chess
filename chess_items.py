from math import ceil

import pygame as pg
from game_config import *

pg.init()
font_obj = pg.font.Font(pg.font.get_default_font(), 15)


class Chessboard:
    def __init__(self, parent_surface: pg.Surface):
        self.board = pg.Surface((CELL_SIZE * CELL_QTY, CELL_SIZE * CELL_QTY))
        self.__screen = parent_surface
        self.__screen.blit(self.board,
                           (WINDOW_SIZE[0] - self.board.get_width(), WINDOW_SIZE[1] - self.board.get_height()))
        self.__draw_playboard()
        self.all_sprites.draw(self.__screen)
        pg.display.update()
        self.all_sprites.update()

    def __draw_playboard(self):
        self.all_sprites = pg.sprite.Group()
        for y in range(CELL_QTY):
            for x in range(CELL_QTY):
                # заполняем доску полями
                cell = pg.Surface((CELL_SIZE, CELL_SIZE))
                cell.fill(COLORS[(x + y) % 2])
                # Рисуем координаты полей
                if y == CELL_QTY - 1:
                    symbol = font_obj.render(ALPHABET[x + 1], 1, COLORS[x % 2])
                    cell.blit(symbol, (5, CELL_SIZE - 15))
                if x == CELL_QTY - 1:
                    symbol = font_obj.render(str(9 - (y + 1)), 1, COLORS[y % 2])
                    cell.blit(symbol, (CELL_SIZE - 15, 5))
                self.board.blit(cell, (x * CELL_SIZE, y * CELL_SIZE))
                #Размещаем фигуры на доске
                if y == 1:
                    pawn = Pawn(self.get_center_of_cell((x, y)), "b")
                    self.all_sprites.add(pawn)
                if y == 6:
                    pawn = Pawn(self.get_center_of_cell((x, y)), "w")
                    self.all_sprites.add(pawn)
        self.__screen.blit(self.board,
                           (WINDOW_SIZE[0] - self.board.get_width(), WINDOW_SIZE[1] - self.board.get_height()))

    def get_square_from_pos(self, pos):
        #Получаем координаты ячейки по пикселям
        y = ceil(pos[0] // 80)
        x = ceil(pos[1] // 80)
        return (x, y)

    def get_center_of_cell(self, coords):
        #вычисляем центр ячейки в пикселях по координатам ячейки
        x = int(((coords[0]) * CELL_SIZE) + CELL_SIZE/2)
        y = int(((coords[1]) * CELL_SIZE) + CELL_SIZE/2)
        return (x, y)

    def draw_figures(self):
        pass



class Figure(pg.sprite.Sprite):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False


class Pawn(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_pa.png").convert_alpha()
        else:
            self.image = pg.image.load("assets\/figures\/w_pa.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Rook(Figure):
    def __init__(self):
        super().__init__(self)
        if self.color == 'b':
            self.image = "assets\/figures\/b_ro.png"
        else:
            self.image = "assets\/figures\/w_ro.png"


class Bishop(Figure):
    def __init__(self):
        super().__init__(self)
        if self.color == 'b':
            self.image = "assets\/figures\/b_bi.png"
        else:
            self.image = "assets\/figures\/w_bi.png"


class Queen(Figure):
    def __init__(self):
        super().__init__(self)
        if self.color == 'b':
            self.image = "assets\/figures\/b_qu.png"
        else:
            self.image = "assets\/figures\/w_qu.png"


class King(Figure):
    def __init__(self):
        super().__init__(self)
        if self.color == 'b':
            self.image = "assets\/figures\/b_ki.png"
        else:
            self.image = "assets\/figures\/w_ki.png"


class Knight(Figure):
    def __init__(self):
        super().__init__(self)
        if self.color == 'b':
            self.image = "assets\/figures\/b_kn.png"
        else:
            self.image = "assets\/figures\/w_kn.png"