import pygame as pg


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


class Board():
    def __init__(self):
        pass


if __name__ == '__main__':
    pg.init()
    clock = pg.time.Clock()
    FPS = 60
    WINDOW_SIZE = (640, 640)
    BLACK_CELL = (181, 136, 99)
    WHITE_CELL = (240, 217, 181)
    COLORS = [WHITE_CELL, BLACK_CELL]
    CELL_QTY = 8
    CELL_SIZE = 80
    alphabet = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}
    screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption('Chess game')
    programIcon = pg.image.load("assets\/figures\Black_king.png")
    pg.display.set_icon(programIcon)
    font_obj = pg.font.Font(pg.font.get_default_font(), 15)

    for y in range(CELL_QTY):
        for x in range(CELL_QTY):
            pg.draw.rect(screen, COLORS[(x + y) % 2], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if y == CELL_QTY - 1:
                symbol = font_obj.render(alphabet[x + 1], 1, COLORS[x % 2])
                screen.blit(symbol, (x * CELL_SIZE + 3, y * CELL_SIZE + 65))
            if x == CELL_QTY - 1:
                symbol = font_obj.render(str(9 - (y + 1)), 1, COLORS[y % 2])
                screen.blit(symbol, (x * CELL_SIZE + 67, y * CELL_SIZE + 5))

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
        pg.display.update()
        clock.tick(FPS)
