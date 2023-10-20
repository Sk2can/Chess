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
        self.draw_playboard()
        self.all_sprites.draw(self.__screen)
        pg.display.update()
        self.all_sprites.update()

    def draw_playboard(self):
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
                # Размещаем фигуры на доске
                figure = POSITIONS[y][x]
                match figure:
                    case "b_ro":
                        rook = Rook(self.get_center_of_cell((x, y)), "b")
                        self.all_sprites.add(rook)
                    case "b_kn":
                        knight = Knight(self.get_center_of_cell((x, y)), "b")
                        self.all_sprites.add(knight)
                    case "b_bi":
                        bishop = Bishop(self.get_center_of_cell((x, y)), "b")
                        self.all_sprites.add(bishop)
                    case "b_qu":
                        queen = Queen(self.get_center_of_cell((x, y)), "b")
                        self.all_sprites.add(queen)
                    case "b_ki":
                        king = King(self.get_center_of_cell((x, y)), "b")
                        self.all_sprites.add(king)
                    case "w_ro":
                        rook = Rook(self.get_center_of_cell((x, y)), "w")
                        self.all_sprites.add(rook)
                    case "w_kn":
                        knight = Knight(self.get_center_of_cell((x, y)), "w")
                        self.all_sprites.add(knight)
                    case "w_bi":
                        bishop = Bishop(self.get_center_of_cell((x, y)), "w")
                        self.all_sprites.add(bishop)
                    case "w_qu":
                        queen = Queen(self.get_center_of_cell((x, y)), "w")
                        self.all_sprites.add(queen)
                    case "w_ki":
                        king = King(self.get_center_of_cell((x, y)), "w")
                        self.all_sprites.add(king)
                    case "b_pa":
                        pawn = Pawn(self.get_center_of_cell((x, y)), "b")
                        self.all_sprites.add(pawn)
                    case "w_pa":
                        pawn = Pawn(self.get_center_of_cell((x, y)), "w")
                        self.all_sprites.add(pawn)
        self.__screen.blit(self.board,
                           (WINDOW_SIZE[0] - self.board.get_width(), WINDOW_SIZE[1] - self.board.get_height()))

    def get_square_from_pos(self, pos):
        # Получаем координаты ячейки по пикселям
        y = ceil(pos[0] // 80)
        x = ceil(pos[1] // 80)
        return (x, y)

    def get_center_of_cell(self, coords):
        # вычисляем центр ячейки в пикселях по координатам ячейки
        x = int(((coords[0]) * CELL_SIZE) + CELL_SIZE / 2)
        y = int(((coords[1]) * CELL_SIZE) + CELL_SIZE / 2)
        return (x, y)

    def find_object(self, pos):
        for object in self.all_sprites:
            if self.get_square_from_pos(object.rect.center) == pos:
                return object
        


class Figure(pg.sprite.Sprite):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.square_pos = Chessboard.get_square_from_pos(self, pos)
        self.has_moved = False


class Pawn(Figure):
    def __init__(self, pos, color):
        Figure.__init__(self, pos, color)
        self.valid_moves = []
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_pa.png").convert_alpha()
        else:
            self.image = pg.image.load("assets\/figures\/w_pa.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))


    def get_valid_moves (self, chessboard):
        valid_moves = []
        if self.color == "b":
            pass
        if self.color == "w":
            pos = chessboard.get_square_from_pos(self.pos)
            y, x = pos[0], pos[1]
            if self.has_moved == False and POSITIONS[y - 2][x] == '':
                valid_moves.append((y-2, x))
            if POSITIONS[y - 1][x] == '':
                valid_moves.append((y - 1, x))
        return valid_moves

    def move(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.has_moved = True
        self.square_pos = Chessboard.get_square_from_pos(self, pos)
        self.rect.x += 80
        self.rect.y -= 80

class Rook(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_ro.png").convert_alpha()
        else:
            self.image = pg.image.load("assets\/figures\/w_ro.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Bishop(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_bi.png").convert_alpha()
        else:
            self.image = pg.image.load("assets\/figures\/w_bi.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Queen(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_qu.png").convert_alpha()
        else:
            self.image = pg.image.load("assets\/figures\/w_qu.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))


class King(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_ki.png").convert_alpha()
        else:
            self.image = pg.image.load("assets\/figures\/w_ki.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Knight(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_kn.png").convert_alpha()
        else:
            self.image = pg.image.load("assets\/figures\/w_kn.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
