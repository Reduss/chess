from typing import List, Tuple

import pygame
from pygame.event import Event

import render
import game_logic

# TODO: need a better way to proccess all the events in main()


def handle(even_list: List[Event]):
    #switch case to call different handlers
    pass

def handle_mouse(event: Event):
    # find which cell has been clicked
    # check if there is a piece in that cell
    # handle if true, return if false
    
    if click_inside_grid():
        pos = render.get_chess_notation_from_pos(pygame.mouse.get_pos())
        print(pos)
        piece = list(filter(lambda p: p.position == pos, game_logic.INGAME_PIECES))
        
        # TODO: thefactor the copy-paste
        if piece:
            for p in game_logic.INGAME_PIECES:
                if p is not piece[0]: 
                    p.is_focused = False
            f = not piece[0].is_focused 
            piece[0].is_focused = f
        else:
            for p in game_logic.INGAME_PIECES:
                p.is_focused = False
    else:
        print("Click outside the grid")

def click_inside_grid():
    if render.get_chess_notation_from_pos(pygame.mouse.get_pos()) != "":
        return True
    return False

