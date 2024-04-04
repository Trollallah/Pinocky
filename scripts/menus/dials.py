import pygame
import os
from scripts.utilities.scale import scale_singleton as scale
from scripts.utilities.enums import GameState


class Dials:
    """
    The Dials class is for settings that can be changed..
    UNFINISHED.
    """
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.default_image = pygame.image.load((os.path.join('assets', 'temp.png'))).convert()
        self.font = pygame.font.SysFont('arial', 36, bold=False, italic=False)
        self.textsurf = self.font.render("Space bar to go back.", True, 'black')

        if not scale.scale:
            self.default = self.default_image
        else:
            self.default = pygame.transform.scale(self.default_image, self.display_surface.get_size())

    def game_loop(self, is_running):
        """
        Dials logic run every frame.
        :param is_running:
        :return: running, state
        """
        running = is_running
        state = GameState.DIALS

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Keydown events handling
            if event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    state = GameState.MENU

        self.draw()

        return running, state

    def draw(self):
        """
        Draw the Dials screen.
        :return:
        """
        self.display_surface.blit(self.default, (0, 0))
        self.display_surface.blit(self.textsurf, (self.display_surface.get_width() // 2, (self.display_surface.get_height() // 2) + 100))
