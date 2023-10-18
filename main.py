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
    WINDOW_SIZE = (700, 700)
    pg.display.set_mode(WINDOW_SIZE)

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
        clock.tick(FPS)
