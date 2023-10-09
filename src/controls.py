from typing import List, Tuple, Union

import pygame
from pygame.event import Event

import render
import game_logic


# TODO: need a better way to proccess all the events in main()

# TODO: is there a good way to manage focus?


def handle(even_list: List[Event]):
    # TODO: switch case to call different handlers ? 
    pass

def handle_mouse(event: Event):
    
    # if outside the grid
    #   unfocus all
    # if inside
    #   if on piece
    #       piece.focus = not piece.focus
    #       unfocus the other ones
    #   elif not on piece
    #       unfocus all
    
    if click_is_inside_grid():
        pos = render.get_chess_notation_from_pos(pygame.mouse.get_pos())
        print(pos)
        piece = list(filter(lambda p: p.position == pos, game_logic.INGAME_PIECES))
        
        # TODO: refactor the copy-paste
        if piece:
            unfocus_all_pieces_except(piece[0])
            piece[0].is_focused = not piece[0].is_focused
            if is_Movable(piece[0]):
                game_logic.find_move(piece[0])
        else:
            unfocus_all_pieces_except()
    else:
        unfocus_all_pieces_except(None)
        print("Click outside the grid. All pieced have been unfocused")

def handle_focused_piece(pc: game_logic.Piece):
    # calculate possible moves
    # render them
    # if the following click is inside possile move cells, 
    #   change the position of the piece to that cell
    # else unfocus the piece
    # unfocus the piece
    
    pass

# TODO: check other conditions
def is_Movable(pc: game_logic.Piece):
    return pc.is_focused and not pc.is_taken

def unfocus_all_pieces_except(pc: Union[game_logic.Piece, None] = None):
    for p in game_logic.INGAME_PIECES:
        if pc is p:
            continue
        p.is_focused = False

def click_is_inside_grid():
    if render.get_chess_notation_from_pos(pygame.mouse.get_pos()) != "":
        return True
    return False

