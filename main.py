import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Fonts
csfont = pygame.font.SysFont("comicsans", 8, bold=True)
bigfont = pygame.font.SysFont("Liberation Serif", 32, bold=True)

# Screen size and refresh rate
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FRAMERATE = 60

BUTTON_GAP = 38

# Max and min seconds between alert time
MAX_ALERT_TIME = 300 * FRAMERATE # 5 minutes
MIN_ALERT_TIME = 1 * FRAMERATE  # 1 second

# Colors
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)


class Button(object):
    def __init__(self, y, sound):

        # Sound
        self.sound = pygame.mixer.Sound("alerts/%s" % sound)
        self.text = bigfont.render(sound, True, BLACK)
        
        # Positioning and dimensions
        self.x = (SCREEN_WIDTH / 2) - ((len(sound) * 32) / 2)
        self.y = y
        self.w = len(sound) * 32
        self.h = 32
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h
        
        # State variables
        self.clicked = False
        self.play = False
        self.clicktime = 0
        self.alert_timer = 0


    # Count down the alert timer. When it hits zero,
    # play the sound effect and reset to a random time within 
    # the range [MIN_ALERT_TIME, MAX_ALERT_TIME]
    def play_alert(self):
        if self.alert_timer > 0:
            self.alert_timer -= 1

        else:
            self.sound.play()
            self.alert_timer = random.randint(MIN_ALERT_TIME, MAX_ALERT_TIME)


    # Main functionality for Button. Draws the button, checks for mouse
    # clicks, and updates position based on the scroll_offset (used for
    # mouse wheel scrolling).
    def draw(self, scroll_offset):
        button_color = GREY
        mouse = pygame.mouse.get_pos()
        get_click = pygame.mouse.get_pressed()

        # Check if mouse is over button
        if mouse[0] >= self.x and mouse[0] <= self.x2 and \
           mouse[1] <= (self.y2 + scroll_offset) and mouse[1] >= (self.y + scroll_offset):

            # If clicked button, toggle activate/deactivate.
            if get_click == (True, False, False) and not self.clicked:
                self.clicked = True
                self.clicktime = 10
                self.play = not self.play

        # Code to control the delay between clicks.
        if self.clicked and self.clicktime > 0:
            self.clicktime -= 1

            if self.clicktime == 0:
                self.clicked = False

        if self.play:
            button_color = WHITE
            self.play_alert()
        else:
            self.alert_timer = 0

        # Draw button and text
        pygame.draw.rect(screen, button_color, pygame.Rect((self.x, self.y + scroll_offset), (self.w, self.h)))
        screen.blit(self.text, (self.x + self.h / 4, self.y - 6 + scroll_offset))


if __name__ == "__main__":

    done = False

    pos = 0
    scroll = 0
    buttons = []

    # Import all button sounds and fill out the list.
    directory = os.fsencode("alerts/")
    for file in os.listdir(directory):

        filename = os.fsdecode(file)
        if filename.endswith(".mp3") or filename.endswith(".wav") or filename.endswith(".ogg"):

            print("%d) %s" % (pos, filename))

            # Add new button at a y-position below the last one.
            buttons.append(Button(pos * BUTTON_GAP, filename))
            pos += 1

    # Main loop
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            
            elif event.type == pygame.KEYDOWN:
                
                # Press 'A' key to activate every button at once!
                if event.key == pygame.K_a:
                    for button in buttons:
                        button.play = True

                # Press 'Q' key to deactivate every button.
                elif event.key == pygame.K_q:
                    for button in buttons:
                        button.play = False

            # Scroll through the buttons. (The 'scroll' variable is an
            # offset that is added to the buttons' original positions
            # to alter where they are.)
            elif event.type == pygame.MOUSEWHEEL:
                
                scroll += (event.y * FRAMERATE)

                # Check to make sure we're not scrolling offscreen. Undo bad
                # scrolling if we did.
                if scroll > BUTTON_GAP or (scroll + (pos * BUTTON_GAP) + BUTTON_GAP) < SCREEN_HEIGHT:
                    scroll -= (event.y * FRAMERATE)

        screen.fill(BLACK)

        # Draw buttons
        for button in buttons:
            button.draw(scroll)

        pygame.display.flip()
        clock.tick(FRAMERATE)