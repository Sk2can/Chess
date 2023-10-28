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
        self.init_figures()
        self.all_sprites.draw(self.__screen)
        self.flag_sprites = pg.sprite.Group()
        pg.display.update()
        self.flags_mas = []
        self.all_sprites.update()
        self.current_color = TURN

    def init_figures(self):
        self.all_sprites = pg.sprite.Group()
        for y in range(CELL_QTY):
            for x in range(CELL_QTY):
                figure = POSITIONS[x][y]
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

    def update(self, screen):
        self.draw_playboard()
        self.flag_sprites = pg.sprite.Group()
        self.flag_sprites.draw(screen)
        self.all_sprites.draw(screen)
        pg.display.update()

    def reset(self, screen):
        SELECTED_PIECE = None
        self.flag_sprites = pg.sprite.Group()
        self.draw_playboard()
        self.flag_sprites.draw(screen)
        self.all_sprites.draw(screen)
        pg.display.update()

    def draw_playboard(self):
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
        self.__screen.blit(self.board,
                           (WINDOW_SIZE[0] - self.board.get_width(), WINDOW_SIZE[1] - self.board.get_height()))

    def get_square_from_pos(self, pos):
        # Получаем координаты ячейки по пикселям
        y = ceil(pos[0] // 80)
        x = ceil(pos[1] // 80)
        return (y, x)

    def get_center_of_cell(self, coords):
        # вычисляем центр ячейки в пикселях по координатам ячейки
        x = int(((coords[0]) * CELL_SIZE) + CELL_SIZE / 2)
        y = int(((coords[1]) * CELL_SIZE) + CELL_SIZE / 2)
        return (y, x)

    def find_object(self, pos, last_figure):
        for object in self.all_sprites:
            if len(self.flags_mas) != 0 and last_figure.color == self.current_color:
                return last_figure
            if self.get_square_from_pos(object.rect.center) == pos:
                return object

    def find_object_on_coords(self, pos):
        for object in self.all_sprites:
            if object.square_pos == pos:
                return object


class Flag(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(FLAG).convert_alpha()
        self.pos = Chessboard.get_center_of_cell(self, pos)
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))


class Figure(pg.sprite.Sprite):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.color = color
        self.square_pos = Chessboard.get_square_from_pos(self, pos)
        self.foo = list(self.square_pos)
        self.foo[0], self.foo[1] = self.foo[1], self.foo[0]
        self.square_pos = tuple(self.foo)
        self.has_moved = False
        self.valid_moves = []


class Pawn(Figure):
    def __init__(self, pos, color):
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_pa.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_pa.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.name = "_pa"

    def get_valid_moves(self, chessboard):
        valid_moves = []
        if self.color == "b":
            pos = chessboard.get_square_from_pos((self.pos[1], self.pos[0]))
            y, x = pos[0], pos[1]
            if self.has_moved == False and POSITIONS[y + 2][x] == '':
                valid_moves.append((y + 2, x))
            if POSITIONS[y + 1][x] == '':
                valid_moves.append((y + 1, x))
            try:
                if POSITIONS[y + 1][x - 1] != '' and POSITIONS[y + 1][x - 1][0] == "w":
                    valid_moves.append((y + 1, x - 1))
            except IndexError:
                pass
            try:
                if POSITIONS[y + 1][x + 1] != '' and POSITIONS[y + 1][x + 1][0] == "w":
                    valid_moves.append((y + 1, x + 1))
            except IndexError:
                pass
        if self.color == "w":
            pos = chessboard.get_square_from_pos((self.pos[1], self.pos[0]))
            y, x = pos[0], pos[1]
            if self.has_moved == False and POSITIONS[y - 2][x] == '':
                valid_moves.append((y - 2, x))
            if POSITIONS[y - 1][x] == '':
                valid_moves.append((y - 1, x))
            try:
                if POSITIONS[y - 1][x - 1] != '' and POSITIONS[y - 1][x - 1][0] == "b":
                    valid_moves.append((y - 1, x - 1))
            except IndexError:
                pass
            try:
                if POSITIONS[y - 1][x + 1] != '' and POSITIONS[y - 1][x + 1][0] == "b":
                    valid_moves.append((y - 1, x + 1))
            except IndexError:
                pass
        return valid_moves

    def draw_valid_moves(self, chessboard, screen):
        chessboard.flag_sprites = pg.sprite.Group()
        self.valid_moves = self.get_valid_moves(chessboard)
        for flag_pos in self.valid_moves:
            chessboard.flag_sprites.add(Flag(flag_pos))
            chessboard.flags_mas.append(flag_pos)
        chessboard.flag_sprites.draw(screen)
        pg.display.update()

    def move(self, new_pos, chessboard, SELECTED_PIECE):
        if POSITIONS[new_pos[0]][new_pos[1]] != '' and POSITIONS[new_pos[0]][new_pos[1]][0] != self.color:
            self.attack(chessboard.find_object_on_coords(new_pos), new_pos)
        n = self.square_pos[0] - new_pos[0]
        self.has_moved = True
        self.rect.y -= 80 * n
        self.square_pos = new_pos
        self.pos = chessboard.get_center_of_cell(self.square_pos)
        if self.color == 'w' and self.square_pos[0] == 0 or self.color == 'b' and self.square_pos[0] == 7:
            self.kill()
            SELECTED_PIECE.name = "_qu"
            queen = Queen(chessboard.get_center_of_cell((self.square_pos[0], self.square_pos[1])), self.color)
            chessboard.all_sprites.add(queen)
        self.valid_moves = []

    def attack(self, attacked_figure, new_pos):
        attacked_figure.kill()
        n = self.square_pos[1] - new_pos[1]
        self.rect.x -= 80 * n


class Rook(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_ro.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_ro.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.name = "_ro"

    def get_valid_moves(self, chessboard):
        valid_moves = []
        pos = chessboard.get_square_from_pos((self.pos[1], self.pos[0]))
        y, x = pos[0], pos[1]
        cond1, cond2, cond3, cond4 = False, False, False, False
        for i in range(1, 8):
            try:
                if cond1 == False:
                    if POSITIONS[y + i][x] == '' :
                        valid_moves.append((y + i, x))
                    elif POSITIONS[y + i][x][0] == self.color:
                        cond1 = True
                    elif POSITIONS[y + i][x][0] != self.color:
                        valid_moves.append((y + i, x))
                        cond1 = True
            except IndexError:
                pass

            try:
                if cond2 == False:
                    if POSITIONS[y - i][x] == '':
                        valid_moves.append((y - i, x))
                    elif POSITIONS[y - i][x][0] == self.color:
                        cond2 = True
                    elif POSITIONS[y - i][x][0] != self.color:
                        valid_moves.append((y - i, x))
                        cond2 = True
            except IndexError:
                pass

            try:
                if cond3 == False:
                    if POSITIONS[y][x + i] == '':
                        valid_moves.append((y, x + i))
                    elif POSITIONS[y][x + i][0] == self.color:
                        cond3 = True
                    elif POSITIONS[y][x + i][0] != self.color:
                        valid_moves.append((y, x + i))
                        cond3 = True
            except IndexError:
                pass

            try:
                if cond4 == False:
                    if POSITIONS[y][x - i] == '':
                        valid_moves.append((y, x - i))
                    elif POSITIONS[y][x - i][0] == self.color:
                        cond4 = True
                    elif POSITIONS[y][x - i][0] != self.color:
                        valid_moves.append((y, x - i))
                        cond4 = True
            except IndexError:
                pass
        return valid_moves

    def draw_valid_moves(self, chessboard, screen):
        chessboard.flag_sprites = pg.sprite.Group()
        self.valid_moves = self.get_valid_moves(chessboard)
        for flag_pos in self.valid_moves:
            chessboard.flag_sprites.add(Flag(flag_pos))
            chessboard.flags_mas.append(flag_pos)
        chessboard.flag_sprites.draw(screen)
        pg.display.update()

    def move(self, new_pos, chessboard, SELECTED_PIECE):
        is_attack = False
        if POSITIONS[new_pos[0]][new_pos[1]] != '' and POSITIONS[new_pos[0]][new_pos[1]][0] != self.color:
            self.attack(chessboard.find_object_on_coords(new_pos), new_pos)
            is_attack = True
        n = self.square_pos[0] - new_pos[0]
        m = self.square_pos[1] - new_pos[1]
        self.has_moved = True
        if is_attack == False:
            self.rect.y -= 80 * n
            self.rect.x -= 80 * m
        self.square_pos = new_pos
        self.pos = chessboard.get_center_of_cell(self.square_pos)
        self.valid_moves = []

    def attack(self, attacked_figure, new_pos):
        attacked_figure.kill()
        n = self.square_pos[0] - new_pos[0]
        m = self.square_pos[1] - new_pos[1]
        self.rect.y -= 80 * n
        self.rect.x -= 80 * m



class Bishop(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_bi.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_bi.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))


class Queen(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_qu.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_qu.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))


class King(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_ki.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_ki.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))


class Knight(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_kn.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_kn.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
