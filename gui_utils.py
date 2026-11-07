import pygame

def mouse_down(x, y, x2, y2):
    mouse = pygame.mouse.get_pos()
    return (mouse[0] >= x and mouse[0] <= x2 and \
           mouse[1] <= y2 and mouse[1] >= y)