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
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coords = chessboard.get_square_from_pos(pg.mouse.get_pos())
                    if chessboard.current_color == "w":
                        SELECTED_PIECE = chessboard.find_object(chessboard.get_square_from_pos(pg.mouse.get_pos()),
                                                                chessboard, SELECTED_PIECE)
                        if ((SELECTED_PIECE == None and len(chessboard.flags_mas) != 0) or
                                SELECTED_PIECE == None and len(chessboard.flags_mas) == 0 or
                                (
                                        len(chessboard.flags_mas) != 0 and SELECTED_PIECE != None and coords not in chessboard.flags_mas) or
                                SELECTED_PIECE.color == "b"):
                            chessboard.reset(screen)
                            chessboard.flags_mas = []
                            break
                        if SELECTED_PIECE != None and coords in SELECTED_PIECE.valid_moves:
                            SELECTED_PIECE = chessboard.find_object(
                                chessboard.get_square_from_pos(SELECTED_PIECE.rect.center), chessboard, SELECTED_PIECE)
                            old_pos = chessboard.get_square_from_pos(SELECTED_PIECE.rect.center)
                            new_pos = chessboard.get_square_from_pos(pg.mouse.get_pos())
                            if new_pos not in SELECTED_PIECE.valid_moves:
                                chessboard.reset(screen)
                                chessboard.flags_mas = []
                                break
                            POSITIONS[old_pos[0]][old_pos[1]] = ''
                            POSITIONS[new_pos[0]][new_pos[1]] = SELECTED_PIECE.color + SELECTED_PIECE.name
                            SELECTED_PIECE.move(new_pos)
                            chessboard.update(screen)
                            if SELECTED_PIECE.color == "w":
                                chessboard.current_color = "b"
                            else:
                                chessboard.current_color = "w"
                            chessboard.flags_mas = []
                            continue
                        if POSITIONS[coords[0]][coords[1]] != '':
                            SELECTED_PIECE.draw_valid_moves(chessboard, screen, SELECTED_PIECE)
                        if POSITIONS[coords[0]][coords[1]] == '' and SELECTED_PIECE != None:
                            SELECTED_PIECE = None
                            chessboard.update(screen)
                    if chessboard.current_color == "b":
                        SELECTED_PIECE = chessboard.find_object(chessboard.get_square_from_pos(pg.mouse.get_pos()),
                                                                chessboard, SELECTED_PIECE)
                        if ((SELECTED_PIECE == None and len(chessboard.flags_mas) != 0) or
                                SELECTED_PIECE == None and len(chessboard.flags_mas) == 0 or
                                (
                                        len(chessboard.flags_mas) != 0 and SELECTED_PIECE != None and coords not in chessboard.flags_mas) or
                                SELECTED_PIECE.color == "w"):
                            chessboard.reset(screen)
                            chessboard.flags_mas = []
                            break
                        if SELECTED_PIECE != None and coords in SELECTED_PIECE.valid_moves:
                            SELECTED_PIECE = chessboard.find_object(
                                chessboard.get_square_from_pos(SELECTED_PIECE.rect.center), chessboard, SELECTED_PIECE)
                            old_pos = chessboard.get_square_from_pos(SELECTED_PIECE.rect.center)
                            new_pos = chessboard.get_square_from_pos(pg.mouse.get_pos())
                            if new_pos not in SELECTED_PIECE.valid_moves:
                                chessboard.reset(screen)
                                chessboard.flags_mas = []
                                break
                            POSITIONS[old_pos[0]][old_pos[1]] = ''
                            POSITIONS[new_pos[0]][new_pos[1]] = SELECTED_PIECE.color + SELECTED_PIECE.name
                            SELECTED_PIECE.move(new_pos)
                            chessboard.update(screen)
                            if SELECTED_PIECE.color == "b":
                                chessboard.current_color = "w"
                            else:
                                chessboard.current_color = "b"
                            chessboard.flags_mas = []
                            continue
                        if POSITIONS[coords[0]][coords[1]] != '':
                            SELECTED_PIECE.draw_valid_moves(chessboard, screen, SELECTED_PIECE)
                        if POSITIONS[coords[0]][coords[1]] == '' and SELECTED_PIECE != None:
                            SELECTED_PIECE = None
                            chessboard.update(screen)

            chessboard.draw_playboard()
            chessboard.all_sprites.draw(screen)
