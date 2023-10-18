import pygame as pg
from game_config import *
from chess_items import *


if __name__ == '__main__':
    clock = pg.time.Clock()
    pg.display.set_caption(WINDOW_TITLE)
    pg.display.set_icon(pg.image.load(WINDOW_ICON_PATH))
    screen = pg.display.set_mode(WINDOW_SIZE)
    chessboard = Chessboard(screen)

    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False