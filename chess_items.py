from math import ceil

import pyautogui
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

    def is_the_game_over(self):
        chessboard = self
        b_moves = 0
        w_moves = 0
        for piece in self.all_sprites:
            if piece.color == "w":
                final_moves = piece.get_valid_moves(chessboard)
                final_moves = piece.forbidden_move_ban(final_moves, chessboard)
                w_moves += len(final_moves)
            if piece.color == "b":
                final_moves = piece.get_valid_moves(chessboard)
                final_moves = piece.forbidden_move_ban(final_moves, chessboard)
                b_moves += len(final_moves)
            if b_moves and w_moves !=0:
                break
        if b_moves == 0:
            return "w"
        if w_moves == 0:
            return "b"
    def print(self):
        figures = {'': '', 'b_ki': '♔', 'b_qu': '♕', 'b_ro': '♖', 'b_bi': '♗', 'b_kn': '♘', 'b_pa': '♙',
                   'w_ki': '♚', 'w_qu': '♛', 'w_ro': '♜', 'w_bi': '♝', 'w_kn': '♞', 'w_pa': '♟︎'}
        for y in range(8):
            line = ""
            for x in range(8):
                if str(figures[POSITIONS[y][x]]) == '':
                    line += ' '
                    continue
                line += (str(figures[POSITIONS[y][x]]))
            print(line)
        print()

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

    def border_check(self, coords):
        if (coords[0] <= 7 and coords[0] >= 0) and (coords[1] <= 7 and coords[1] >= 0):
            return True
        return False

    def is_checked(self, chessboard, is_fake):
        flag = False
        kings_pos = []
        for i in range(0, 8):
            for j in range(0, 8):
                if POSITIONS[i][j] == "w_ki" or POSITIONS[i][j] == "b_ki":
                    kings_pos.append((i, j))
        for figure in chessboard.all_sprites:
            moves = figure.get_valid_moves(chessboard)
            if kings_pos[0] in moves:
                for king in chessboard.all_sprites:
                    if king.square_pos == kings_pos[0]:
                        if is_fake == False:
                            king.image = pg.image.load(f"assets\/figures\/{king.color}_ki_checked.png")
                        return king.color
            if kings_pos[1] in moves:
                for king in chessboard.all_sprites:
                    if king.square_pos == kings_pos[1]:
                        if is_fake == False:
                            king.image = pg.image.load(f"assets\/figures\/{king.color}_ki_checked.png")
                        return king.color
        if flag == False:
            for king in chessboard.all_sprites:
                if king.square_pos in kings_pos:
                    king.image = pg.image.load(f"assets\/figures\/{king.color}_ki.png")

    def forbidden_move_ban(self, valid_moves, chessboard):
        kings_pos = {"w" : (-1,-1), "b" : (-1,-1)}
        for i in range(0, 8):
            for j in range(0, 8):
                if POSITIONS[i][j] == "w_ki":
                    kings_pos["w"] = (i,j)
                if POSITIONS[i][j] == "b_ki":
                    kings_pos["b"] = (i,j)

        # название фигуры, которая совершает фиктивный ход
        current_figure = POSITIONS[self.square_pos[0]][self.square_pos[1]]
        # ее изначальная позиция
        default_pos = (self.square_pos[0], self.square_pos[1])
        attacking_moves = []
        banned_moves = []
        attacking_piece = None
        # совершает каждый возможный ход фиктивно
        for move in valid_moves:
            # делает ход в массиве доски
            POSITIONS[self.square_pos[0]][self.square_pos[1]] = ''
            # значальное значение ячейки на которую ходят
            default_figure = POSITIONS[move[0]][move[1]]
            # помещают в нее текущую фигуру
            POSITIONS[move[0]][move[1]] = current_figure
            # узнаем есть ли на клетке для хода вражеская фигура
            for piece in chessboard.all_sprites:
                if kings_pos["w"] in piece.get_valid_moves(chessboard) and piece.color == "b":
                    attacking_piece = piece
                    break
                if kings_pos["b"] in piece.get_valid_moves(chessboard) and piece.color == "w":
                    attacking_piece = piece
                    break
            # находим объект фигуры которой ходим и совершаем фиктивный ход
            for piece in chessboard.all_sprites:
                if piece.square_pos == default_pos:
                    current_piece = piece
                    piece.square_pos = move
                    break
            if current_piece.name == "_ki":
                kings_pos = {"w": (-1, -1), "b": (-1, -1)}
                for i in range(0, 8):
                    for j in range(0, 8):
                        if POSITIONS[i][j] == "w_ki":
                            kings_pos["w"] = (i, j)
                        if POSITIONS[i][j] == "b_ki":
                            kings_pos["b"] = (i, j)
            for figure in chessboard.all_sprites:
                moves = figure.get_valid_moves(chessboard)
                if figure.color == "b":
                    if kings_pos["w"] in moves and piece.color !="b":
                        banned_moves.append(move)
                        #добавление запрещенных ходов

                if figure.color == "w" and piece.color !="w":
                    if kings_pos["b"] in moves:
                        banned_moves.append(move)
                        # добавление запрещенных ходов

            # востанавливаем поле в состояние до фиктивных ходов
            current_piece.square_pos = default_pos
            POSITIONS[default_pos[0]][default_pos[1]] = current_figure
            POSITIONS[move[0]][move[1]] = default_figure
        # удаляем забаненые ходы
        if attacking_piece != None and attacking_piece.square_pos in banned_moves and self.name != "_ki":
            banned_moves.remove(attacking_piece.square_pos)
        for move in banned_moves:
            try:
                valid_moves.remove(move)
            except ValueError:
                pass
        return valid_moves


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
            if POSITIONS[y + 1][x] == '':
                valid_moves.append((y + 1, x))
                if self.has_moved == False and POSITIONS[y + 2][x] == '':
                    valid_moves.append((y + 2, x))
            if self.border_check((y + 1, x - 1)):
                if POSITIONS[y + 1][x - 1] != '' and POSITIONS[y + 1][x - 1][0] == "w":
                    valid_moves.append((y + 1, x - 1))
            if self.border_check((y + 1, x + 1)):
                if POSITIONS[y + 1][x + 1] != '' and POSITIONS[y + 1][x + 1][0] == "w":
                    valid_moves.append((y + 1, x + 1))
        if self.color == "w":
            pos = chessboard.get_square_from_pos((self.pos[1], self.pos[0]))
            y, x = pos[0], pos[1]
            if POSITIONS[y - 1][x] == '':
                valid_moves.append((y - 1, x))
                if self.has_moved == False and POSITIONS[y - 2][x] == '':
                    valid_moves.append((y - 2, x))
            if self.border_check((y - 1, x - 1)):
                if POSITIONS[y - 1][x - 1] != '' and POSITIONS[y - 1][x - 1][0] == "b":
                    valid_moves.append((y - 1, x - 1))
            if self.border_check((y - 1, x + 1)):
                if POSITIONS[y - 1][x + 1] != '' and POSITIONS[y - 1][x + 1][0] == "b":
                    valid_moves.append((y - 1, x + 1))
        return valid_moves

    def draw_valid_moves(self, chessboard, screen):
        chessboard.flag_sprites = pg.sprite.Group()
        self.valid_moves = self.get_valid_moves(chessboard)
        self.valid_moves = self.forbidden_move_ban(self.valid_moves, chessboard)
        print(self.valid_moves)
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
            if self.border_check((y + i, x)):
                if cond1 == False:
                    if POSITIONS[y + i][x] == '':
                        valid_moves.append((y + i, x))
                    elif POSITIONS[y + i][x][0] == self.color:
                        cond1 = True
                    elif POSITIONS[y + i][x][0] != self.color:
                        valid_moves.append((y + i, x))
                        cond1 = True
            if self.border_check((y - i, x)):
                if cond2 == False:
                    if POSITIONS[y - i][x] == '':
                        valid_moves.append((y - i, x))
                    elif POSITIONS[y - i][x][0] == self.color:
                        cond2 = True
                    elif POSITIONS[y - i][x][0] != self.color:
                        valid_moves.append((y - i, x))
                        cond2 = True
            if self.border_check((y, x + i)):
                if cond3 == False:
                    if POSITIONS[y][x + i] == '':
                        valid_moves.append((y, x + i))
                    elif POSITIONS[y][x + i][0] == self.color:
                        cond3 = True
                    elif POSITIONS[y][x + i][0] != self.color:
                        valid_moves.append((y, x + i))
                        cond3 = True
            if self.border_check((y, x - i)):
                if cond4 == False:
                    if POSITIONS[y][x - i] == '':
                        valid_moves.append((y, x - i))
                    elif POSITIONS[y][x - i][0] == self.color:
                        cond4 = True
                    elif POSITIONS[y][x - i][0] != self.color:
                        valid_moves.append((y, x - i))
                        cond4 = True
        # здесь должен быть метод бана ходов приводящих к шаху
        return valid_moves

    def draw_valid_moves(self, chessboard, screen):
        chessboard.flag_sprites = pg.sprite.Group()
        self.valid_moves = self.get_valid_moves(chessboard)
        self.valid_moves = self.forbidden_move_ban(self.valid_moves, chessboard)
        print(self.valid_moves)
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
        self.name = "_bi"

    def get_valid_moves(self, chessboard):
        valid_moves = []
        pos = chessboard.get_square_from_pos((self.pos[1], self.pos[0]))
        y, x = pos[0], pos[1]
        cond1, cond2, cond3, cond4 = False, False, False, False
        for i in range(1, 8):
            if self.border_check((y + i, x + i)):
                if cond1 == False:
                    if POSITIONS[y + i][x + i] == '':
                        valid_moves.append((y + i, x + i))
                    elif POSITIONS[y + i][x + i][0] == self.color:
                        cond1 = True
                    elif POSITIONS[y + i][x + i][0] != self.color:
                        valid_moves.append((y + i, x + i))
                        cond1 = True
            if self.border_check((y - i, x - i)):
                if cond2 == False:
                    if POSITIONS[y - i][x - i] == '':
                        valid_moves.append((y - i, x - i))
                    elif POSITIONS[y - i][x - i][0] == self.color:
                        cond2 = True
                    elif POSITIONS[y - i][x - i][0] != self.color:
                        valid_moves.append((y - i, x - i))
                        cond2 = True
            if self.border_check((y - i, x + i)):
                if cond3 == False:
                    if POSITIONS[y - i][x + i] == '':
                        valid_moves.append((y - i, x + i))
                    elif POSITIONS[y - i][x + i][0] == self.color:
                        cond3 = True
                    elif POSITIONS[y - i][x + i][0] != self.color:
                        valid_moves.append((y - i, x + i))
                        cond3 = True
            if self.border_check((y + i, x - i)):
                if cond4 == False:
                    if POSITIONS[y + i][x - i] == '':
                        valid_moves.append((y + i, x - i))
                    elif POSITIONS[y + i][x - i][0] == self.color:
                        cond4 = True
                    elif POSITIONS[y + i][x - i][0] != self.color:
                        valid_moves.append((y + i, x - i))
                        cond4 = True
        # здесь должен быть метод бана ходов приводящих к шаху
        return valid_moves

    def draw_valid_moves(self, chessboard, screen):
        chessboard.flag_sprites = pg.sprite.Group()
        self.valid_moves = self.get_valid_moves(chessboard)
        self.valid_moves = self.forbidden_move_ban(self.valid_moves, chessboard)
        print(self.valid_moves)
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


class Queen(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_qu.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_qu.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.name = "_qu"

    def get_valid_moves(self, chessboard):
        valid_moves = []
        pos = chessboard.get_square_from_pos((self.pos[1], self.pos[0]))
        y, x = pos[0], pos[1]
        cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8 = False, False, False, False, False, False, False, False
        for i in range(1, 8):
            if self.border_check((y + i, x)):
                if cond1 == False:
                    if POSITIONS[y + i][x] == '':
                        valid_moves.append((y + i, x))
                    elif POSITIONS[y + i][x][0] == self.color:
                        cond1 = True
                    elif POSITIONS[y + i][x][0] != self.color:
                        valid_moves.append((y + i, x))
                        cond1 = True
            if self.border_check((y - i, x)):
                if cond2 == False:
                    if POSITIONS[y - i][x] == '':
                        valid_moves.append((y - i, x))
                    elif POSITIONS[y - i][x][0] == self.color:
                        cond2 = True
                    elif POSITIONS[y - i][x][0] != self.color:
                        valid_moves.append((y - i, x))
                        cond2 = True
            if self.border_check((y, x + i)):
                if cond3 == False:
                    if POSITIONS[y][x + i] == '':
                        valid_moves.append((y, x + i))
                    elif POSITIONS[y][x + i][0] == self.color:
                        cond3 = True
                    elif POSITIONS[y][x + i][0] != self.color:
                        valid_moves.append((y, x + i))
                        cond3 = True
            if self.border_check((y, x - i)):
                if cond4 == False:
                    if POSITIONS[y][x - i] == '':
                        valid_moves.append((y, x - i))
                    elif POSITIONS[y][x - i][0] == self.color:
                        cond4 = True
                    elif POSITIONS[y][x - i][0] != self.color:
                        valid_moves.append((y, x - i))
                        cond4 = True
            if self.border_check((y + i, x + i)):
                if cond5 == False:
                    if POSITIONS[y + i][x + i] == '':
                        valid_moves.append((y + i, x + i))
                    elif POSITIONS[y + i][x + i][0] == self.color:
                        cond5 = True
                    elif POSITIONS[y + i][x + i][0] != self.color:
                        valid_moves.append((y + i, x + i))
                        cond5 = True
            if self.border_check((y - i, x - i)):
                if cond6 == False:
                    if POSITIONS[y - i][x - i] == '':
                        valid_moves.append((y - i, x - i))
                    elif POSITIONS[y - i][x - i][0] == self.color:
                        cond6 = True
                    elif POSITIONS[y - i][x - i][0] != self.color:
                        valid_moves.append((y - i, x - i))
                        cond6 = True
            if self.border_check((y - i, x + i)):
                if cond7 == False:
                    if POSITIONS[y - i][x + i] == '':
                        valid_moves.append((y - i, x + i))
                    elif POSITIONS[y - i][x + i][0] == self.color:
                        cond7 = True
                    elif POSITIONS[y - i][x + i][0] != self.color:
                        valid_moves.append((y - i, x + i))
                        cond7 = True
            if self.border_check((y + i, x - i)):
                if cond8 == False:
                    if POSITIONS[y + i][x - i] == '':
                        valid_moves.append((y + i, x - i))
                    elif POSITIONS[y + i][x - i][0] == self.color:
                        cond8 = True
                    elif POSITIONS[y + i][x - i][0] != self.color:
                        valid_moves.append((y + i, x - i))
                        cond8 = True
        # здесь должен быть метод бана ходов приводящих к шаху
        return valid_moves

    def draw_valid_moves(self, chessboard, screen):
        chessboard.flag_sprites = pg.sprite.Group()
        self.valid_moves = self.get_valid_moves(chessboard)
        self.valid_moves = self.forbidden_move_ban(self.valid_moves, chessboard)
        print(self.valid_moves)
        for flag_pos in self.valid_moves:
            chessboard.flag_sprites.add(Flag(flag_pos))
            chessboard.flags_mas.append(flag_pos)
        chessboard.flag_sprites.draw(screen)
        pg.display.update()

    def move(self, new_pos, chessboard, SELECTED_PIECE):
        is_attack = False
        if POSITIONS[new_pos[0]][new_pos[1]] != '' and POSITIONS[new_pos[0]][new_pos[1]][0] != self.color:
            self.attack(chessboard.find_object_on_coords(new_pos), new_pos, chessboard)
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

    def attack(self, attacked_figure, new_pos, chessboard):
        attacked_figure.kill()
        n = self.square_pos[0] - new_pos[0]
        m = self.square_pos[1] - new_pos[1]
        self.rect.y -= 80 * n
        self.rect.x -= 80 * m


class King(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_ki.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_ki.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.short_rook = None
        self.long_rook = None
        self.castling_piece = None
        self.name = "_ki"

    def get_valid_moves(self, chessboard):
        valid_moves = []
        pos = chessboard.get_square_from_pos((self.pos[1], self.pos[0]))
        y, x = pos[0], pos[1]
        if self.border_check((y + 1, x + 1)):
            if POSITIONS[y + 1][x + 1] == '':
                valid_moves.append((y + 1, x + 1))
            elif POSITIONS[y + 1][x + 1][0] != self.color:
                valid_moves.append((y + 1, x + 1))
        if self.border_check((y - 1, x - 1)):
            if POSITIONS[y - 1][x - 1] == '':
                valid_moves.append((y - 1, x - 1))
            elif POSITIONS[y - 1][x - 1][0] != self.color:
                valid_moves.append((y - 1, x - 1))
        if self.border_check((y - 1, x + 1)):
            if POSITIONS[y - 1][x + 1] == '':
                valid_moves.append((y - 1, x + 1))
            elif POSITIONS[y - 1][x + 1][0] != self.color:
                valid_moves.append((y - 1, x + 1))
        if self.border_check((y + 1, x - 1)):
            if POSITIONS[y + 1][x - 1] == '':
                valid_moves.append((y + 1, x - 1))
            elif POSITIONS[y + 1][x - 1][0] != self.color:
                valid_moves.append((y + 1, x - 1))
        if self.border_check((y - 1, x)):
            if POSITIONS[y - 1][x] == '':
                valid_moves.append((y - 1, x))
            elif POSITIONS[y - 1][x][0] != self.color:
                valid_moves.append((y - 1, x))
        if self.border_check((y, x + 1)):
            if POSITIONS[y][x + 1] == '':
                valid_moves.append((y, x + 1))
            elif POSITIONS[y][x + 1][0] != self.color:
                valid_moves.append((y, x + 1))
        if self.border_check((y + 1, x)):
            if POSITIONS[y + 1][x] == '':
                valid_moves.append((y + 1, x))
            elif POSITIONS[y + 1][x][0] != self.color:
                valid_moves.append((y + 1, x))
        if self.border_check((y, x - 1)):
            if POSITIONS[y][x - 1] == '':
                valid_moves.append((y, x - 1))
            elif POSITIONS[y][x - 1][0] != self.color:
                valid_moves.append((y, x - 1))
        # рокировка
        for rook in chessboard.all_sprites:
            if rook.name == "_ro" and rook.color == self.color:
                if rook.has_moved == True:
                    continue
                if rook.square_pos[1] == 7:
                    self.short_rook = rook
                    self.castling_piece = rook
                if rook.square_pos[1] == 0:
                    self.long_rook = rook
                    self.castling_piece = rook
        if self.border_check((y, x - 2)):
            if (POSITIONS[y][x - 2] == '' and POSITIONS[y][x - 3] == '' and POSITIONS[y][x - 1] == '' and
                    self.has_moved == False and self.long_rook != None):
                valid_moves.append((y, x - 2))
        if self.border_check((y, x + 2)):
            if POSITIONS[y][x + 2] == '' and POSITIONS[y][
                x + 1] == '' and self.has_moved == False and self.short_rook != None:
                valid_moves.append((y, x + 2))
        return valid_moves

    def draw_valid_moves(self, chessboard, screen):
        chessboard.flag_sprites = pg.sprite.Group()
        self.valid_moves = self.get_valid_moves(chessboard)
        self.valid_moves = self.forbidden_move_ban(self.valid_moves, chessboard)
        print(self.valid_moves)
        for flag_pos in self.valid_moves:
            chessboard.flag_sprites.add(Flag(flag_pos))
            chessboard.flags_mas.append(flag_pos)
        chessboard.flag_sprites.draw(screen)
        pg.display.update()

    def move(self, new_pos, chessboard, SELECTED_PIECE):
        is_attack = False
        is_castling = False
        if POSITIONS[new_pos[0]][new_pos[1]] != '' and POSITIONS[new_pos[0]][new_pos[1]][0] != self.color:
            self.attack(chessboard.find_object_on_coords(new_pos), new_pos, chessboard)
            is_attack = True
        if self.square_pos[1] - new_pos[1] == 2 or self.square_pos[1] - new_pos[1] == -2:
            is_castling = True
        n = self.square_pos[0] - new_pos[0]
        m = self.square_pos[1] - new_pos[1]
        self.has_moved = True
        if is_attack == False:
            self.rect.y -= 80 * n
            self.rect.x -= 80 * m
        if is_castling:
            if m == -2:
                POSITIONS[self.short_rook.square_pos[0]][self.short_rook.square_pos[1]] = ''
                POSITIONS[self.short_rook.square_pos[0]][
                    self.short_rook.square_pos[1] - 2] = self.short_rook.color + self.short_rook.name
                self.short_rook.move((self.short_rook.square_pos[0], self.short_rook.square_pos[1] - 2), chessboard,
                                     SELECTED_PIECE)
            if m == 2:
                POSITIONS[self.long_rook.square_pos[0]][self.long_rook.square_pos[1]] = ''
                POSITIONS[self.long_rook.square_pos[0]][
                    self.long_rook.square_pos[1] + 3] = self.long_rook.color + self.long_rook.name
                self.long_rook.move((self.long_rook.square_pos[0], self.long_rook.square_pos[1] + 3), chessboard,
                                    SELECTED_PIECE)
        self.square_pos = new_pos
        self.pos = chessboard.get_center_of_cell(self.square_pos)
        self.valid_moves = []

    def attack(self, attacked_figure, new_pos, chessboard):
        attacked_figure.kill()
        n = self.square_pos[0] - new_pos[0]
        m = self.square_pos[1] - new_pos[1]
        self.rect.y -= 80 * n
        self.rect.x -= 80 * m


class Knight(Figure):
    def __init__(self, pos, color):
        pg.sprite.Sprite.__init__(self)
        Figure.__init__(self, pos, color)
        if self.color == 'b':
            self.image = pg.image.load("assets\/figures\/b_kn.png")
        else:
            self.image = pg.image.load("assets\/figures\/w_kn.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.name = "_kn"

    def get_valid_moves(self, chessboard):
        valid_moves = []
        pos = chessboard.get_square_from_pos((self.pos[1], self.pos[0]))
        y, x = pos[0], pos[1]
        if self.border_check((y - 2, x - 1)):
            if POSITIONS[y - 2][x - 1] == '' or POSITIONS[y - 2][x - 1][0] != self.color:
                valid_moves.append((y - 2, x - 1))
        if self.border_check((y - 2, x + 1)):
            if POSITIONS[y - 2][x + 1] == '' or POSITIONS[y - 2][x + 1][0] != self.color:
                valid_moves.append((y - 2, x + 1))
        if self.border_check((y + 2, x - 1)):
            if POSITIONS[y + 2][x - 1] == '' or POSITIONS[y + 2][x - 1][0] != self.color:
                valid_moves.append((y + 2, x - 1))
        if self.border_check((y + 2, x + 1)):
            if POSITIONS[y + 2][x + 1] == '' or POSITIONS[y + 2][x + 1][0] != self.color:
                valid_moves.append((y + 2, x + 1))
        if self.border_check((y - 1, x - 2)):
            if POSITIONS[y - 1][x - 2] == '' or POSITIONS[y - 1][x - 2][0] != self.color:
                valid_moves.append((y - 1, x - 2))
        if self.border_check((y - 1, x + 2)):
            if POSITIONS[y - 1][x + 2] == '' or POSITIONS[y - 1][x + 2][0] != self.color:
                valid_moves.append((y - 1, x + 2))
        if self.border_check((y + 1, x - 2)):
            if POSITIONS[y + 1][x - 2] == '' or POSITIONS[y + 1][x - 2][0] != self.color:
                valid_moves.append((y + 1, x - 2))
        if self.border_check((y + 1, x + 2)):
            if POSITIONS[y + 1][x + 2] == '' or POSITIONS[y + 1][x + 2][0] != self.color:
                valid_moves.append((y + 1, x + 2))
        return valid_moves

    def draw_valid_moves(self, chessboard, screen):
        chessboard.flag_sprites = pg.sprite.Group()
        self.valid_moves = self.get_valid_moves(chessboard)
        self.valid_moves = self.forbidden_move_ban(self.valid_moves, chessboard)
        print(self.valid_moves)
        for flag_pos in self.valid_moves:
            chessboard.flag_sprites.add(Flag(flag_pos))
            chessboard.flags_mas.append(flag_pos)
        chessboard.flag_sprites.draw(screen)
        pg.display.update()

    def move(self, new_pos, chessboard, SELECTED_PIECE):
        is_attack = False
        if POSITIONS[new_pos[0]][new_pos[1]] != '' and POSITIONS[new_pos[0]][new_pos[1]][0] != self.color:
            self.attack(chessboard.find_object_on_coords(new_pos), new_pos, chessboard)
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

    def attack(self, attacked_figure, new_pos, chessboard):
        attacked_figure.kill()
        n = self.square_pos[0] - new_pos[0]
        m = self.square_pos[1] - new_pos[1]
        self.rect.y -= 80 * n
        self.rect.x -= 80 * m
