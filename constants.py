'''
Global constants used across modules
'''

# Screen Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_MARGIN = 150

# Button dimensions
BUTTON_PADDING = 10
BUTTON_HEIGHT = 32
BUTTON_GAP = BUTTON_HEIGHT + 6 # Vertical gap between buttons on screen
BUTTON_EDGE_ROUNDING = 10 # Width of the ellipses that smooth out the sides of the buttons


# Refresh rate
FRAMERATE = 60
MINUTE = 60 * FRAMERATE

# Font Sizes
FONT_SMALL = 16
FONT_LARGE = 32



# Max and min seconds between alert time
MAX_ALERT_TIME = 300 * FRAMERATE # 5 minutes
MIN_ALERT_TIME = 1 * FRAMERATE  # 1 second

# Colors
WHITE = (255, 255, 255)
LIGHT_GREY = (180, 180, 180)
GREY = (127, 127, 127)
DARK_GREY = (90, 90, 90)
BLACK = (0, 0, 0)

BUTTON_CLICK_TIME = 10
