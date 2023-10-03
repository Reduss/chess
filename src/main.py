import pygame
from enum import Enum
from typing import Tuple, List, Dict
from controls import handle_mouse

import render
import game_logic


# ==== MAIN LOOP ====

def start():
    pygame.init()
    pygame.display.set_caption("Chess")
    
    game_logic.init()
    render.render()
    
    
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
                render.render()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse(event)
                render.render()
            update()
    pygame.quit()

main()