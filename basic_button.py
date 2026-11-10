'''
Generic Button class
'''

import pygame
from constants import FONT_LARGE, BLACK, GREY, LIGHT_GREY, \
                      SCREEN_SIZE, BUTTON_PADDING, BUTTON_EDGE_ROUNDING, BUTTON_CLICK_TIME

from gui_utils import mouse_hover, lmb_pressed


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
    def display(self, button_color, y_offset=0):
        border_padding = self.h / 10
        
        # Draw the base of the button
        pygame.draw.rect(screen, GREY, pygame.Rect((self.x + 5, self.y + y_offset), (self.w - 10, self.h)))
        pygame.draw.ellipse(screen, GREY, pygame.Rect((self.x, self.y + y_offset), (10, self.h)))
        pygame.draw.ellipse(screen, GREY, pygame.Rect((self.x + self.w - 10, self.y + y_offset), (10, self.h)))
        
        # Draw the button interior
        pygame.draw.rect(screen, button_color, pygame.Rect((self.x + border_padding + 5, self.y + border_padding + y_offset), 
                                                           (self.w - border_padding*2 - 10, self.h - border_padding*2)))
        pygame.draw.ellipse(screen, button_color, pygame.Rect((self.x + border_padding, self.y + border_padding + y_offset), 
                                                              (10, self.h - border_padding*2)))
        pygame.draw.ellipse(screen, button_color, pygame.Rect((self.x + self.w - 10 - border_padding, self.y + border_padding + y_offset), 
                                                              (10, self.h - border_padding*2)))

        # Draw the text
        screen.blit(self.font, (self.x + BUTTON_PADDING, self.y + self.font_y_offset + y_offset))


    # Get mouse input
    def get_input(self, y_offset=0):

        # Mouse on top of button
        if mouse_hover(self.x, self.y + y_offset, self.x2, self.y2 + y_offset):

            # If clicked button, toggle activate/deactivate.
            if lmb_pressed() and not self.clicked:
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


    # Primary button functionality
    def update(self, y_offset=0):
        button_color = GREY
        
        self.get_input(y_offset)
        self.reduce_clicktime()

        if self.is_pressed:
            button_color = LIGHT_GREY
            self.pressed_action()

        # Draw button and text
        self.display(button_color, y_offset)
