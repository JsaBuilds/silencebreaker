'''
Generic Button class
'''

import pygame
import random
#from constants import FONT_LARGE, BLACK, GREY, LIGHT_GREY, \
#                      SCREEN_SIZE, BUTTON_PADDING, BUTTON_EDGE_ROUNDING, BUTTON_CLICK_TIME
from constants import *

from gui_utils import mouse_hover, lmb_pressed

pygame.mixer.init()
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
        pass # If the button stays in the pressed state once clicked, put its action here.


    # Action performed when button is released
    def release_action(self):
        self.is_pressed = False
        # If the button releases immediately, put its action here.


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


# Sound button
class SoundButton(Button):

    def __init__(self, x, y, directory, sound):
        super().__init__(x, y, (SCREEN_WIDTH / 2) - (BUTTON_PADDING / 2) - SCREEN_MARGIN, BUTTON_HEIGHT, sound)

        # Delay before playing sound (initialized to a random duration)
        self.sound_timer = random.randint(MIN_ALERT_TIME, MAX_ALERT_TIME)

        # Sound
        self.sound = pygame.mixer.Sound("%s/%s" % (directory, sound))

    def reset_timer(self):
        self.sound_timer = random.randint(MIN_ALERT_TIME, MAX_ALERT_TIME)

    def timer_up(self):
        return self.sound_timer == 0

    def pressed_action(self):
        if self.sound_timer > 0:
            self.sound_timer -= 1

        else:
            #self.sound.play()
            self.reset_timer()

    def release_action(self):
        if self.is_pressed:
            self.sound.play()



# Tab button (switching between button folders)
class TabButton(Button):

    def __init__(self, x, y, text):
        super().__init__(x, y, SCREEN_MARGIN - (3 * BUTTON_PADDING), BUTTON_HEIGHT, text)
        self.switched = False

    def get_input(self, current_tab):
        #mouse = pygame.mouse.get_pos()
        get_click = pygame.mouse.get_pressed()
        current = current_tab

        # Mouse on top of button
        if mouse_hover(self.x, self.y, self.x2, self.y2):

            # If clicked button, toggle activate/deactivate.
            if get_click == (True, False, False) and not self.clicked:
                self.clicked = True
                self.clicktime = BUTTON_CLICK_TIME
                self.is_pressed = True
                current = self.text

        return current

    def pressed_action(self):
        if not self.switched:
            self.switched = True

    def release_action(self):
            pass

    def update(self, current_tab):
        button_color = GREY
        
        # Check if mouse is over button
        current = self.get_input(current_tab)

        if current != self.text:
            self.is_pressed = False
            self.switched = False

        self.reduce_clicktime()

        if self.is_pressed:
            button_color = LIGHT_GREY
            self.pressed_action()

        self.display(button_color)
        return current


class MenuButton(Button):

    def __init__(self, x, y, text, function, *args):
        super().__init__(x, y, SCREEN_MARGIN - (3 * BUTTON_PADDING), BUTTON_HEIGHT, text)
        self.function = function
        self.args = args
        #print("Arguments: ")
        #print(enumerate(self.args))

    def release_action(self):
        self.is_pressed = False
        self.function(*self.args)