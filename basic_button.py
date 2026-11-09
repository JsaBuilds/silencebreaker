'''
Generic Button class
'''

import pygame
from constants import FONT_LARGE, BUTTON_PADDING, BLACK, GREY, WHITE, BUTTON_CLICK_TIME, SCREEN_SIZE, LIGHT_GREY

BUTTON_EDGE_ROUNDING = 10 # Width of the ellipses that smooth out the sides of the buttons

screen = pygame.display.set_mode(SCREEN_SIZE)

class Button(object):
    def __init__(self, x, y, w, h, text):

        # Positioning and dimensions
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h

        # Text rendering / sizing
        self.text = text.replace(".mp3", "").replace(".wav", "").replace(".ogg", "").replace(".m4a", "")
        self.fontsize = FONT_LARGE
        self.font_type = pygame.font.SysFont("Liberation Serif", self.fontsize, bold=True) # bigfont
        self.font_y_offset = 0

        # Adjust text size to fit within button
        while self.font_type.size(self.text)[0] > (self.w - (2 * BUTTON_PADDING)):
            self.fontsize -= 1
            self.font_y_offset += 0.5
            self.font_type = pygame.font.SysFont("Liberation Serif", self.fontsize, bold=True)

        self.font = self.font_type.render(self.text, True, BLACK)
        self.font_y_offset = (self.h - self.font_type.size(self.text)[1]) / 2

        # State variables
        self.clicked = False
        self.clicktime = 0
        self.is_pressed = False

    # Draw button and text
    def display(self, button_color):
        border_padding = self.h / 10
        
        # Draw the base of the button
        pygame.draw.rect(screen, GREY, pygame.Rect((self.x + 5, self.y), (self.w - 10, self.h)))
        pygame.draw.ellipse(screen, GREY, pygame.Rect((self.x, self.y), (10, self.h)))
        pygame.draw.ellipse(screen, GREY, pygame.Rect((self.x + self.w - 10, self.y), (10, self.h)))
        
        # Draw the button interior
        pygame.draw.rect(screen, button_color, pygame.Rect((self.x + border_padding + 5, self.y + border_padding), 
                                                           (self.w - border_padding*2 - 10, self.h - border_padding*2)))
        pygame.draw.ellipse(screen, button_color, pygame.Rect((self.x + border_padding, self.y + border_padding), 
                                                              (10, self.h - border_padding*2)))
        pygame.draw.ellipse(screen, button_color, pygame.Rect((self.x + self.w - 10 - border_padding, self.y + border_padding), 
                                                              (10, self.h - border_padding*2)))

        # Draw the text
        screen.blit(self.font, (self.x + BUTTON_PADDING, self.y + self.font_y_offset))

    # Get mouse clicked input
    def get_input(self):
        mouse = pygame.mouse.get_pos()
        get_click = pygame.mouse.get_pressed()

        # Mouse on top of button
        if mouse[0] >= self.x and mouse[0] <= self.x2 and \
           mouse[1] <= self.y2 and mouse[1] >= self.y:

            # If clicked button, toggle activate/deactivate.
            if get_click == (True, False, False) and not self.clicked:
                self.clicked = True
                self.clicktime = BUTTON_CLICK_TIME
                self.is_pressed = not self.is_pressed

    # Control the delay between clicks.
    def reduce_clicktime(self):
        if self.clicked and self.clicktime > 0:
            self.clicktime -= 1

            if self.clicktime == 0:
                self.clicked = False
                self.release_action()

    # Special function to be performed when button is pressed.
    def pressed_action(self):
        pass

    # Action performed when button is released
    def release_action(self):
        self.is_pressed = False

    def update(self):
        button_color = GREY
        
        # Check if mouse is over button
        self.get_input()
        self.reduce_clicktime()

        if self.is_pressed:
            button_color = LIGHT_GREY
            self.pressed_action()
        #else:
            #self.is_pressed_timer = 0

        # Draw button and text
        self.display(button_color)
