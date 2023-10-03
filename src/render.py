import pygame
from enum import Enum
from typing import Tuple, List, Dict
import math

from game_logic import PieceType, GRID_N, Piece, INGAME_PIECES, Team

# ==== CONSTS ====

INIT_DISPLAY_W = 1000
INIT_DISPLAY_H = 800

# TODO: set these
MIN_DISPLAY_W = None
MIN_DISPLAY_H = None

CELL_SIZE = 80

# Colors

BLACK: pygame.Color = pygame.Color(0, 0, 0)
WHITE: pygame.Color = pygame.Color(255, 255, 255)
GREY: pygame.Color = pygame.Color(128,128,128)
DARK_BROWN: pygame.Color = pygame.Color(179,95,51)
LIGHT_BROWN: pygame.Color = pygame.Color(241,208,165)
LIGHT_GREEN: pygame.Color = pygame.Color(88,232,88, 128)
TRANSPARENT: pygame.Color = pygame.Color(0 , 0, 0, 0)

CELL_DARK = DARK_BROWN
CELL_LIGHT = LIGHT_BROWN
CELL_HIGHLIGHT = LIGHT_GREEN

# Pieces

# Surfaces

SCREEN: pygame.Surface = pygame.display.set_mode([INIT_DISPLAY_W, INIT_DISPLAY_H], pygame.RESIZABLE)
GRID: pygame.Surface = pygame.Surface([CELL_SIZE * 8, CELL_SIZE * 8])
PIECES_SURFACE: pygame.Surface = pygame.Surface([CELL_SIZE * 8, CELL_SIZE * 8], pygame.SRCALPHA)
HINTS_SURFACE: pygame.Surface = pygame.Surface([CELL_SIZE * 8, CELL_SIZE * 8], pygame.SRCALPHA)

# NOTICE: all coordinates is in chess notation
COORDS_X = ["a", "b", "c", "d", "e", "f", "g", "h"]
COORDS_Y = [8, 7, 6, 5, 4, 3, 2, 1]

# Typography

pygame.font.init()
FONT = pygame.font.Font(None, 32)


# ==== RENDER ====

def render_cell(surface: pygame.Surface, coord: str, color: pygame.Color):
    # e4
    pygame.draw.rect(surface, color, pygame.Rect(get_pos_from_chess_notation(coord)[0], get_pos_from_chess_notation(coord)[1], 
                                                      CELL_SIZE, CELL_SIZE))

def highlight_cell(cell_coord: str):
    render_cell(HINTS_SURFACE, cell_coord, CELL_HIGHLIGHT)

def get_pos_from_chess_notation(pos_in_chess : str) -> List[int]:
    return [COORDS_X.index(pos_in_chess[0]) * CELL_SIZE,COORDS_Y.index(int(pos_in_chess[1])) * CELL_SIZE]

def get_chess_notation_from_pos(coordinates: Tuple[int, int]) -> str:
    # floor(x / CELL_SIZE) => the number of the cell 
    # 50 / 80
    if(not position_inside_grid(coordinates)):
        print("click outside the grid")
        return ""
    
    
    cell_num_x = math.floor((coordinates[0] - get_playarea_coords()[0]) / CELL_SIZE)
    cell_num_y = math.floor((coordinates[1] - get_playarea_coords()[1]) / CELL_SIZE)
    print(f"x: {cell_num_x}, y: {cell_num_y}")
    return f"{COORDS_X[cell_num_x]}{COORDS_Y[cell_num_y]}"

def position_inside_grid(coordinates: Tuple[int, int]) -> bool:
    #disp_w, disp_h = pygame.display.get_surface().get_size()
    
    #center_x = disp_w // 2
    #center_y = disp_h // 2
    
    #dist_to_check = render.CELL_SIZE * 4
    
    grid_top_left_cord = get_playarea_coords()
    grid_bottom_right_cord = [grid_top_left_cord[0] + CELL_SIZE * 8, grid_top_left_cord[1] + CELL_SIZE * 8]
    
    if coordinates[0] < grid_top_left_cord[0] or coordinates[0] > grid_bottom_right_cord[0]:
        return False
    elif coordinates[1] < grid_top_left_cord[1] or coordinates[1] > grid_bottom_right_cord[1]:
        return False
    return True

def render_grid() -> None:
    """Renders the board
    """
    x_pos = 0
    y_pos = 0
    for i in range(8):
        current_cell_color = CELL_LIGHT if i % 2 == 0 else CELL_DARK
        for j in range(8):
            pygame.draw.rect(GRID, current_cell_color, pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE))
            x_pos = x_pos + CELL_SIZE
            current_cell_color = CELL_DARK if current_cell_color == CELL_LIGHT else CELL_LIGHT
        y_pos = y_pos + CELL_SIZE
        x_pos = 0

def render_grid_new():
    x_pos = 0
    y_pos = 0
    for y_ind, y_coord in enumerate(COORDS_Y):
        current_cell_color = CELL_LIGHT if y_ind % 2 == 0 else CELL_DARK
        for x_ind, x_coord in enumerate(COORDS_X):
            render_cell(GRID, x_coord + str(y_coord), current_cell_color)
            x_pos = x_pos + CELL_SIZE
            current_cell_color = CELL_DARK if current_cell_color == CELL_LIGHT else CELL_LIGHT
        y_pos = y_pos + CELL_SIZE
        x_pos = 0

def render_coords() -> None:
    """
        Renderds board coordinates
    """
    y_pos_y = 0
    x_pos_x = 0
    print(y_pos_y)
    for cord1, cord2 in zip(COORDS_Y, COORDS_X):
        txt_y = FONT.render(str(cord1), True, BLACK)
        GRID.blit(txt_y, (0, y_pos_y))
        
        txt_x = FONT.render(cord2, True, BLACK)
        GRID.blit(txt_x, (x_pos_x + CELL_SIZE - txt_x.get_size()[0], CELL_SIZE * 8 - txt_x.get_size()[1]))
        x_pos_x += CELL_SIZE
        y_pos_y += CELL_SIZE

def render():
    """
        Renders everything
    """
    
    # TODO: set min size of the window, 
    #       implement mouse controls 
    blit_background()
    render_dynamic_assets()
    blit_dynamic()
    
    #render_grid()
    #SCREEN.fill(GREY)
    #render_grid_new()
    #render_coords()
    #render_possible_moves(Piece(PieceType.ROOK, Team.BLACK, position=f"{'a2'}"))
    #render_pieces()
    #SCREEN.blit(GRID, get_playarea_coords())
    #print("RENDER: render.render() called")

def blit_background():
    SCREEN.fill(GREY)
    render_grid_new()
    render_coords()
    
    PIECES_SURFACE.fill(TRANSPARENT)
    HINTS_SURFACE.fill(TRANSPARENT)

    SCREEN.blit(GRID, get_playarea_coords())
    #PIECES_SURFACE.fill(WHITE)
    #PIECES_SURFACE.blit(SCREEN, (10, 10))


"""
    rener order
        static
            fill screen
            render grid and coords
            blit GRID
        dyn
            fill pieces
            fill hints
            
            render pices
            render hints
            
            blit those
"""

def render_dynamic_assets():
    render_pieces()

def blit_dynamic():
    SCREEN.blit(HINTS_SURFACE, get_playarea_coords())
    SCREEN.blit(PIECES_SURFACE, get_playarea_coords())


def get_playarea_coords() -> Tuple[int, int]: 
    """Returns GRID's coords (of its' top-left corner) that will center it

    Returns:
        List[int, int]: coordinates for GRID
    """
    # TODO: check if it's realy centered (i have a feeling it's off by a px or so)
    return (
            int(SCREEN.get_width() / 2 - GRID.get_width() / 2), 
            int(SCREEN.get_height() / 2 - GRID.get_height() / 2)
        )

def render_pieces():
    for p in INGAME_PIECES:
        render_piece(p)

def render_piece(pc: Piece):
    try:
        sprite = pygame.image.load(rf"assets/{pc.team.value}_{pc.type.value}.png")
        sprite = pygame.transform.scale(sprite, (CELL_SIZE, CELL_SIZE))
        x, y = get_pos_from_chess_notation(pc.position)
        PIECES_SURFACE.blit(sprite, (x,y))
        if pc.is_focused:
            render_focus(pc)
    except pygame.error as e:
        print(f"Coudn't render a piece sprite: {e}")

def render_focus(pc: Piece):
    render_possible_moves(pc)

def render_possible_moves(pc: Piece):
    highlight_cell(pc.position)
    print(f"REDNER: render_possible_moves() called on cell {pc.position}")

# TODO: pieces as enum + dictionary where values are functions that draw them?
