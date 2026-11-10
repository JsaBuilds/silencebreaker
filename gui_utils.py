import pygame


'''
Mouse calls
'''

def mouse_hover(x, y, x2, y2):
    mouse = pygame.mouse.get_pos()
    return (mouse[0] >= x and mouse[0] <= x2 and \
           mouse[1] <= y2 and mouse[1] >= y)

def lmb_pressed():
    return pygame.mouse.get_pressed()[0]

def rmb_pressed():
    return pygame.mouse.get_pressed()[2]

def mmb_pressed():
    return pygame.mouse.get_pressed()[1]