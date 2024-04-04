import pygame
from scripts.utilities.scale import scale_singleton as scale


class Window:
    """
    Class that stores data about the window. Useful for resolution.
    1440p works, but doesn't feel as good as 720p. Uncomment lines 30-32 to enable
    """
    def __init__(self):

        # Create window
        pygame.display.set_caption('Pinocky')
        self.USER_DISPLAY_WIDTH = pygame.display.Info().current_w
        self.USER_DISPLAY_HEIGHT = pygame.display.Info().current_h

        # Resolutions
        self.WIN_720P_WIDTH = 1280
        self.WIN_720P_HEIGHT = 720
        self.WIN_1440P_WIDTH = 2560
        self.WIN_1440P_HEIGHT = 1440

        # Set default resolution
        self.WIN_DEFAULT = (self.WIN_720P_WIDTH, self.WIN_720P_HEIGHT)
        self.window_dimensions = self.WIN_DEFAULT
        scale.scale = False  # Flag to denote whether images need to be scaled. Only for doubling

        # Create scaling
        # Only 720P and 1440P currently in scope
        """if self.USER_DISPLAY_WIDTH >= 1440:  # and USER_DISPLAY_WIDTH <= WIN_1440P_WIDTH:
            self.window_dimensions = (self.WIN_1440P_WIDTH, self.WIN_1440P_HEIGHT)
            scale.scale = True"""

        self.window_surface = pygame.display.set_mode(
            self.window_dimensions)  # Allows 1:2 scaling for 1440p MAYBE add a 1080 later

