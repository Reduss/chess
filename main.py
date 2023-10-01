import pygame

from enum import Enum
from typing import Tuple, List, Dict

# ==== CONSTS ====

INIT_DISPLAY_W = 1000
INIT_DISPLAY_H = 800

# TODO: set these
MIN_DISPLAY_W = None
MIN_DISPLAY_H = None

GRID_CELL_SIZE = 80

# Colors

BLACK: pygame.Color = pygame.Color(0, 0, 0)
WHITE: pygame.Color = pygame.Color(255, 255, 255)
GREY: pygame.Color = pygame.Color(128,128,128)
DARK_BROWN: pygame.Color = pygame.Color(179,95,51)
LIGHT_BROWN: pygame.Color = pygame.Color(241,208,165)

CELL_DARK = DARK_BROWN
CELL_LIGHT = LIGHT_BROWN

# Surfaces

SCREEN: pygame.Surface = pygame.display.set_mode([INIT_DISPLAY_W, INIT_DISPLAY_H], pygame.RESIZABLE)
PLAYING_AREA: pygame.Surface = pygame.Surface([GRID_CELL_SIZE * 8, GRID_CELL_SIZE * 8])


COORDS_X = ["a", "b", "c", "d", "e", "f", "g", "h"]
COORDS_Y = [8, 7, 6, 5, 4, 3, 2, 1]

GRID = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]


# ==== RENDER ====

def render_grid() -> None:
    x_pos = 0
    y_pos = 0
    for i in range(8):
        current_cell_color = CELL_LIGHT if i % 2 == 0 else CELL_DARK
        for j in range(8):
            pygame.draw.rect(PLAYING_AREA, current_cell_color, pygame.Rect(x_pos, y_pos, GRID_CELL_SIZE, GRID_CELL_SIZE))
            x_pos = x_pos + GRID_CELL_SIZE
            current_cell_color = CELL_DARK if current_cell_color == CELL_LIGHT else CELL_LIGHT
        y_pos = y_pos + GRID_CELL_SIZE
        x_pos = 0


def render_background():
    render_grid()
    
    
    # TODO: blit coordinates, set min size of the window, 
    #       render pieces, implement mouse controlls 
    
    
    SCREEN.fill(GREY)
    SCREEN.blit(PLAYING_AREA, get_centered_coords())

def get_centered_coords() -> Tuple[int, int]: 
    """Returns PLAYING_AREA's coords (of its' top-left corner) that will center it

    Returns:
        List[int, int]: coordinates for PLAYING_AREA
    """
    # TODO: check if it's realy centered (i have a feeling it's off by a px or so)
    return (
            int(SCREEN.get_width() / 2 - PLAYING_AREA.get_width() / 2), 
            int(SCREEN.get_height() / 2 - PLAYING_AREA.get_height() / 2)
        )


# TODO: pieces as enum + dictionary where values are functions that draw them?


# ==== LOGIC ====


def get_grid_matrix() -> list[list]:
    return []

# ==== MAIN LOOP ====

def start() -> bool:
    """
        Initializes the game
        
    Returns:
        bool: True if running
    """
    pygame.init()
    render_background()
    return True

def update():
    
    pygame.display.flip()

def main():
    running = start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                render_background()
        update()
    pygame.quit()

main()
