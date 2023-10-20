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
                    # print("Координаты клика: " + str(pg.mouse.get_pos()))
                    # print("Номер клетки: " + str(chessboard.get_square_from_pos(pg.mouse.get_pos())))
                    # print("Координаты центра клетки: " + str(
                    #     chessboard.get_center_of_cell(coords)))
                    # print("Фигура: " + str(POSITIONS[coords[0]][coords[1]]))

                    if SELECTED_PIECE != None:
                        figure = POSITIONS[coords[0]][coords[1]]
                        new_pos = chessboard.get_square_from_pos(pg.mouse.get_pos())
                        if new_pos not in SELECTED_PIECE.valid_moves:
                            SELECTED_PIECE = None
                            break
                        SELECTED_PIECE.move(new_pos)
                        POSITIONS[coords[1]][coords[0]] = ''
                        POSITIONS[new_pos[1]][new_pos[0]] = figure
                        if SELECTED_PIECE.color == "w":
                            TURN = "b"
                        else:
                            TURN = "w"
                        print(*POSITIONS, sep='\n')
                        print(SELECTED_PIECE.rect)

                        continue

                    if POSITIONS[coords[0]][coords[1]] == "w_pa":
                        pawn = chessboard.find_object(chessboard.get_square_from_pos(pg.mouse.get_pos()))
                        pawn.valid_moves = Pawn.get_valid_moves(pawn, chessboard)
                        pawn.move(pawn.valid_moves[0])
                        POSITIONS[coords[0]][coords[1]] = ''
                        POSITIONS[pawn.valid_moves[0][0]][pawn.valid_moves[0][1]] = 'w_pa'

                        chessboard.draw_playboard()
                        chessboard.all_sprites.draw(screen)
                        pg.display.update()
            # print(pawn.square_pos)
            # print(str(Pawn.get_valid_moves(pawn, chessboard)) + "\n")