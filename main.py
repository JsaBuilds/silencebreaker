import pygame
import random
import glob
import os
from channelcontroller import ChannelController
from file_utils import open_dir_dialogue, load_settings, update_settings
from gui_utils import mouse_hover, lmb_pressed
from constants import *
from basic_button import Button

pygame.init()
pygame.mixer.init()


# Fonts
csfont = pygame.font.SysFont("comicsans", FONT_SMALL, bold=True)
bigfont = pygame.font.SysFont("Liberation Serif", FONT_LARGE, bold=True)


clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)


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

        #else:
            #self.sound.play()
            #self.reset_timer()

    def release_action(self):
        pass


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

    def __init__(self, x, y, text, function):
        super().__init__(x, y, SCREEN_MARGIN - (3 * BUTTON_PADDING), BUTTON_HEIGHT, text)
        self.function = function

    def pressed_action(self):
        self.is_pressed = False
        sounds_dir = open_dir_dialogue(SOUNDS_DIR) # TODO: make independent of this global constant
        settings["alert_dir"] = sounds_dir
        update_settings(settings, SETTINGS_PATH)

#############################################################
#
# ButtonInitializer: Handles button initialization on startup
#
#############################################################
class ButtonInitializer(object):

    def __init__(self):
        pass

    # TODO: make this work for the base directory as well.
    def create_sound_button(soundfile_dir, soundfile, sounds_dict):
        tab_name = os.path.basename(soundfile_dir)
        print("New file: \'%s\' added to tab \'%s\'" % (soundfile, tab_name))
        sounds_dict[tab_name].append(SoundButton(xpos, ypos * (BUTTON_HEIGHT + BUTTON_PADDING), soundfile_dir, soundfile))


if __name__ == "__main__":

    #
    # Initialization
    #
    done = False

    scroll = 0

    SETTINGS_PATH = os.path.expanduser("~/.silencebreaker/settings.json")
    SOUNDS_DIR = None

    settings = load_settings(SETTINGS_PATH)

    # Create channel controller (default settings: 4 channels)
    n_channels = 4
    if settings["n_channels"] > 0:
        n_channels = settings["n_channels"]
    
    chnl_ctrl = ChannelController(n_channels)

    #
    # Directory search and load sounds.
    #
    if settings["alert_dir"] == None:
        SOUNDS_DIR = open_dir_dialogue("~/Music")
        settings["alert_dir"] = SOUNDS_DIR
        update_settings(settings, SETTINGS_PATH)
    else:
        SOUNDS_DIR = os.path.expanduser(settings["alert_dir"])


    alert_buttons = {}
    tab_buttons = {}
    current = "alerts"
    tab_count = 0
    for root, dirs, files in os.walk(SOUNDS_DIR):

        alerts_in_tab = 0
        ypos = 0

        print(f"Looking at directory {root}")
        tab_name = os.path.basename(root)
        if tab_name == '':
            tab_name = "Sounds"

        print("Tab name: \'%s\'" % tab_name)
        tab_buttons[tab_name] = TabButton(SCREEN_WIDTH - SCREEN_MARGIN + (2 * BUTTON_PADDING), \
                                                     (tab_count + 1) * (BUTTON_HEIGHT + BUTTON_PADDING), tab_name)
        alert_buttons[tab_name] = []
        tab_count += 1

        for file in files:
            if file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".ogg"):
                xpos = SCREEN_MARGIN
                if alerts_in_tab % 2 != 0:
                    xpos = (SCREEN_WIDTH / 2) + (BUTTON_PADDING / 2)
                elif alerts_in_tab > 0:
                    ypos += 1

                # Add new button for the folder.
                print("New file: \'%s\' added to tab \'%s\'" % (file, tab_name))
                alert_buttons[tab_name].append(SoundButton(xpos, ypos * (BUTTON_HEIGHT + BUTTON_PADDING), root, file))
                alerts_in_tab += 1

    tab_buttons[os.path.basename(SOUNDS_DIR)].is_pressed = True


    alerts_dir_button = MenuButton(BUTTON_PADDING, 200, "Select alerts folder", "Selects it")
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
                    #for button in alert_buttons[current]:
                    #    button.play = True
                    for key, buttons in alert_buttons.items():
                        for button in buttons:
                            if current == key:
                                button.play = True

                # Press 'Q' key to deactivate every button.
                elif event.key == pygame.K_q:
                    #for button in alert_buttons[current]:
                    #    button.play = False
                    for key, buttons in alert_buttons.items():
                        for button in buttons:
                            if current == key:
                                button.play = False

                # Use right and left arrow keys to add/subtract 1 minute from max alert time.
                elif event.key == pygame.K_RIGHT:
                    MAX_ALERT_TIME += MINUTE

                elif event.key == pygame.K_LEFT and (MAX_ALERT_TIME - MINUTE) > MIN_ALERT_TIME:
                    MAX_ALERT_TIME -= MINUTE

            # Scroll through the buttons. (The 'scroll' variable is an offset that is added 
            # to the buttons' original positions to alter where they are.)
            elif event.type == pygame.MOUSEWHEEL:
                
                scroll += (event.y * FRAMERATE)

                # Check to make sure we're not scrolling offscreen. Undo bad
                # scrolling if we did.
                #if scroll > BUTTON_GAP or (scroll + (alerts_in_tab * BUTTON_GAP) + BUTTON_GAP) < SCREEN_HEIGHT:
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
        for key, buttons in alert_buttons.items():
            for button in buttons:
                if current == key:
                    button.update(scroll)

                if button.timer_up() and chnl_ctrl.queued_to_channel(button.sound):
                    button.reset_timer()



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

        alerts_dir_button.update()

        pygame.display.flip()
        clock.tick(FRAMERATE)