import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Dimensions and refresh rate
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_MARGIN = 150
BUTTON_PADDING = 10
BUTTON_HEIGHT = 32
FRAMERATE = 60
MINUTE = 60 * FRAMERATE

# Font Sizes
FONT_SMALL = 16
FONT_LARGE = 32

BUTTON_GAP = 38

# Max and min seconds between alert time
MAX_ALERT_TIME = 300 * FRAMERATE # 5 minutes
MIN_ALERT_TIME = 1 * FRAMERATE  # 1 second

# Colors
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
DARK_GREY = (90, 90, 90)
BLACK = (0, 0, 0)

# Fonts
csfont = pygame.font.SysFont("comicsans", FONT_SMALL, bold=True)
bigfont = pygame.font.SysFont("Liberation Serif", FONT_LARGE, bold=True)


clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)

# Generic button
class ClickButton(object):
    def __init__(self, x, y, w, h, text):

        # Text
        self.text = text
        self.font = bigfont.render(text, True, BLACK)

        # Positioning and dimensions
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h
        
        # State variables
        self.clicked = False
        self.play = False
        self.clicktime = 0
        self.play_timer = 0

    def display(self, button_color, scroll_offset):
        # Draw button and text
        pygame.draw.rect(screen, button_color, pygame.Rect((self.x, self.y + scroll_offset), (self.w, self.h)))
        screen.blit(self.font, (self.x + BUTTON_PADDING, self.y - 4 + scroll_offset))

    def get_input(self, scroll_offset):
        mouse = pygame.mouse.get_pos()
        get_click = pygame.mouse.get_pressed()

        # Mouse on top of button
        if mouse[0] >= self.x and mouse[0] <= self.x2 and \
           mouse[1] <= (self.y2 + scroll_offset) and mouse[1] >= (self.y + scroll_offset):

            # If clicked button, toggle activate/deactivate.
            if get_click == (True, False, False) and not self.clicked:
                self.clicked = True
                self.clicktime = 10
                self.play = not self.play

    # Special function to be performed when button is pressed.
    def on_play(self):
        pass

    def update(self, scroll_offset):
        button_color = GREY
        
        # Check if mouse is over button
        self.get_input(scroll_offset)

        # Code to control the delay between clicks.
        if self.clicked and self.clicktime > 0:
            self.clicktime -= 1

            if self.clicktime == 0:
                self.clicked = False

        if self.play:
            button_color = WHITE
            self.on_play()
        else:
            self.play_timer = 0

        # Draw button and text
        self.display(button_color, scroll_offset)


# Sound button
class SoundButton(ClickButton):

    def __init__(self, x, y, directory, sound):
        super().__init__(x, y, (SCREEN_WIDTH / 2) - (BUTTON_PADDING / 2) - SCREEN_MARGIN, BUTTON_HEIGHT, sound)

        # Sound
        self.sound = pygame.mixer.Sound("%s/%s" % (directory, sound))
        self.font = bigfont.render(sound.replace(".mp3", "").replace(".wav", "").replace(".ogg", ""), True, BLACK)

    def on_play(self):
        if self.play_timer > 0:
            self.play_timer -= 1

        else:
            self.sound.play()
            self.play_timer = random.randint(MIN_ALERT_TIME, MAX_ALERT_TIME)


# Tab button (switching between button folders)
class TabButton(ClickButton):

    def __init__(self, x, y, text):
        super().__init__(x, y, SCREEN_MARGIN - (4 * BUTTON_PADDING), BUTTON_HEIGHT, text)
        self.switched = False

    def get_input(self, current_tab):
        mouse = pygame.mouse.get_pos()
        get_click = pygame.mouse.get_pressed()
        current = current_tab

        # Mouse on top of button
        if mouse[0] >= self.x and mouse[0] <= self.x2 and \
           mouse[1] <= self.y2 and mouse[1] >= self.y:

            # If clicked button, toggle activate/deactivate.
            if get_click == (True, False, False) and not self.clicked:
                self.clicked = True
                self.clicktime = 10
                self.play = True
                current = self.text

        return current

    def update(self, current_tab):
        button_color = GREY
        
        # Check if mouse is over button
        current = self.get_input(current_tab)

        if current != self.text:
            self.play = False
            self.switched = False

        # Code to control the delay between clicks.
        if self.clicked and self.clicktime > 0:
            self.clicktime -= 1

            if self.clicktime == 0:
                self.clicked = False

        if self.play:
            button_color = WHITE
            self.on_play()

        # Draw button and text
        self.display(button_color, 0)
        return current

    def on_play(self):
        if not self.switched:
            self.switched = True


if __name__ == "__main__":

    #
    # Initialization
    #
    done = False

    count = 0
    scroll = 0

    master_dict = {}
    buttons = []
    tab_buttons = {}
    subdir_button_names = []
    current = "alerts"

    #
    # Directory search and load sounds.
    #
    for root, dirs, files in os.walk('alerts'):

        count = 0
        ypos = 0

        print(root)
        subdir_button_names.append(root)
        #if len(dirs) > 0:
            #subdir_button_names.append(root)
            #for subdir in dirs:
                #subdir_button_names.append(subdir)
        master_dict[root] = []

        for file in files:
            if file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".ogg"):
                xpos = SCREEN_MARGIN
                if count % 2 != 0:
                    xpos = (SCREEN_WIDTH / 2) + (BUTTON_PADDING / 2)
                elif count > 0:
                    ypos += 1

                # Add new button for the folder.
                print("New file: \'%s\' added to tab \'%s\'" % (file, root))
                master_dict[root].append(SoundButton(xpos, ypos * (BUTTON_HEIGHT + BUTTON_PADDING), root, file))
                count += 1

    #
    # Create tab buttons
    #
    count = 1
    for subdir in subdir_button_names:
        tab_buttons[subdir] = TabButton(SCREEN_WIDTH - SCREEN_MARGIN + (2 * BUTTON_PADDING), \
                                        count * (BUTTON_HEIGHT + BUTTON_PADDING), subdir)
        count += 1

    tab_buttons["alerts"].play = True

    #
    # Main loop
    #
    while not done:

        #
        # Control and input
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                
                # Press 'A' key to activate every button at once!
                if event.key == pygame.K_a:
                    for button in master_dict[current]:
                        button.play = True

                # Press 'Q' key to deactivate every button.
                elif event.key == pygame.K_q:
                    for button in master_dict[current]:
                        button.play = False

                # Use right and left arrow keys to add/subtract 1 minute from max alert time.
                elif event.key == pygame.K_RIGHT:
                    MAX_ALERT_TIME += MINUTE

                elif event.key == pygame.K_LEFT and (MAX_ALERT_TIME - MINUTE) > MIN_ALERT_TIME:
                    MAX_ALERT_TIME -= MINUTE

            # Scroll through the buttons. (The 'scroll' variable is an
            # offset that is added to the buttons' original positions
            # to alter where they are.)
            elif event.type == pygame.MOUSEWHEEL:
                
                scroll += (event.y * FRAMERATE)

                # Check to make sure we're not scrolling offscreen. Undo bad
                # scrolling if we did.
                #if scroll > BUTTON_GAP or (scroll + (count * BUTTON_GAP) + BUTTON_GAP) < SCREEN_HEIGHT:
                #    scroll -= (event.y * FRAMERATE)

        # Use continuous key polling for speedy interval change.
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            MAX_ALERT_TIME += 8

        elif pressed [pygame.K_DOWN] and (MAX_ALERT_TIME - 8) > MIN_ALERT_TIME:
            MAX_ALERT_TIME -= 8

        #
        # Display and sound
        #
        screen.fill(BLACK)

        # Draw buttons
        for key, buttons in master_dict.items():

            if current == key:
                for button in buttons:
                    button.update(scroll)

        # Draw side windows.
        pygame.draw.rect(screen, DARK_GREY, pygame.Rect((0, 0), (SCREEN_MARGIN - BUTTON_PADDING, SCREEN_HEIGHT)))
        pygame.draw.rect(screen, DARK_GREY, pygame.Rect((SCREEN_WIDTH - SCREEN_MARGIN + BUTTON_PADDING, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)))

        # Delay display
        max_delay_s = float(MAX_ALERT_TIME) / 60.00
        delay_frames = csfont.render("%d frames" % MAX_ALERT_TIME, True, BLACK)
        delay_seconds = csfont.render("(%.2f s)" % max_delay_s, True, BLACK)
        screen.blit(csfont.render("Maximum Delay:", True, BLACK), (10, 10))
        screen.blit(delay_frames, (10, 10 + FONT_SMALL))
        screen.blit(delay_seconds, (10, 10 + (2 * FONT_SMALL)))

        # Draw tab buttons
        tabs_text = csfont.render("Tabs:", True, BLACK)
        screen.blit(tabs_text, (SCREEN_WIDTH - SCREEN_MARGIN + (2 * BUTTON_PADDING), 10))
        for key, button in tab_buttons.items():
            current = button.update(current)

        pygame.display.flip()
        clock.tick(FRAMERATE)