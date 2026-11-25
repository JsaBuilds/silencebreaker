import pygame
import random
import time
from constants import MIN_ALERT_TIME, MAX_ALERT_TIME

############################################################################
#
# ChannelController: Controller for channel queueing and playback logic
#
############################################################################
class ChannelController(object):

    def __init__(self, n_channels):
        pygame.mixer.set_num_channels(n_channels)
        self.sounds = []

    # Redefine the number of channels allowed
    def set_num_channels(n_channels):
        pygame.mixer.set_num_channels(n_channels)

    # Attempt to queue a sound to an empty channel
    # Returns True if successful, False if not.
    def queued_to_channel(self, sound):
        channel = pygame.mixer.find_channel()
        if channel:
            channel.queue(sound)
            print(f"Playing new sound on channel {channel}")
            return True

        return False

    # Add a sound to the list of rotating active sounds
    def add_sound(self, sound):
        self.sounds.append(SoundTimer(sound))
        print(f"Added sound {sound} into rotation.")

    # Remove a sound to the list of rotating active sounds
    def remove_sound(self, sound):
        for soundtimer in self.sounds:
            if soundtimer.sound == sound:
                self.sounds.remove(soundtimer)
        print(f"Removed sound {sound} from rotation.")

    def play_sounds(self):
        # Sound object will have:
        for sound in self.sounds:
            sound.dec_timer()
            if sound.timer == 0 and self.queued_to_channel(sound.sound):
                print(f"Resetting timer of sound {sound.sound}")
                sound.reset_timer()

class SoundTimer(object):
    def __init__(self, sound):
        self.sound = sound
        self.timer = random.randint(MIN_ALERT_TIME, MAX_ALERT_TIME)

    def dec_timer(self):
        if self.timer > 0:
            self.timer -= 1

    def reset_timer(self):
        self.timer = random.randint(MIN_ALERT_TIME, MAX_ALERT_TIME)
        print(f"Sound timer is now at ~{self.timer / 60} seconds")