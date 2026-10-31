import pygame

############################################################################
#
# ChannelController: Controller for channel queueing and playback logic
#
############################################################################
class ChannelController(object):

    def __init__(self, n_channels):
        pygame.mixer.set_num_channels(n_channels)

    # Redefine the number of channels allowed
    def set_num_channels(n_channels):
        pygame.mixer.set_num_channels(n_channels)

    # Attempt to queue a sound to an empty channel
    # Returns True if successful, False if not.
    def queued_to_channel(self, sound):
        channel = pygame.mixer.find_channel()
        if channel:
            channel.queue(sound)
            return True

        return False