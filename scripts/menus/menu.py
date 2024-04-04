import pygame
import os
from scripts.utilities.scale import scale_singleton as scale
from scripts.utilities.enums import GameState


class Menu:
    """The menu is the default screen the game loads and allows the player to pick other game states."""
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        # Create menu
        # All initial image sizes must be 720P compatible
        self.default_image = pygame.image.load((os.path.join('assets', 'main_menu', 'main_menu_default.png'))).convert()
        self.play_image = pygame.image.load((os.path.join('assets', 'main_menu', 'main_,menu_play.png'))).convert()
        self.settings_image = pygame.image.load(
            (os.path.join('assets', 'main_menu', 'main_,menu_settings.png'))).convert()
        self.exit_image = pygame.image.load((os.path.join('assets', 'main_menu', 'main_menu_exit.png'))).convert()
        self.button_width = 240
        self.button_height = 75
        self.button_x = 515
        self.button_y_play = 390
        self.button_y_dials = 500
        self.button_y_exit = 600
        if not scale.scale:
            self.default = self.default_image
            self.play = self.play_image
            self.settings = self.settings_image
            self.exit = self.exit_image
            self.play_rect = pygame.Rect(self.button_x, self.button_y_play, self.button_width, self.button_height)
            self.dials_rect = pygame.Rect(self.button_x, self.button_y_dials, self.button_width, self.button_height)
            self.exit_rect = pygame.Rect(self.button_x, self.button_y_exit, self.button_width, self.button_height)
        else:
            self.default = pygame.transform.scale(self.default_image, self.display_surface.get_size())
            self.play = pygame.transform.scale(self.play_image, self.display_surface.get_size())
            self.settings = pygame.transform.scale(self.settings_image, self.display_surface.get_size())
            self.exit = pygame.transform.scale(self.exit_image, self.display_surface.get_size())
            self.play_rect = pygame.Rect(scale.r1440(self.button_x), scale.r1440(self.button_y_play), scale.r1440(self.button_width),
                                         scale.r1440(self.button_height))
            self.dials_rect = pygame.Rect(scale.r1440(self.button_x), scale.r1440(self.button_y_dials), scale.r1440(self.button_width),
                                          scale.r1440(self.button_height))
            self.exit_rect = pygame.Rect(scale.r1440(self.button_x), scale.r1440(self.button_y_exit), scale.r1440(self.button_width),
                                         scale.r1440(self.button_height))
        self.num_to_show = 0  # 0-default 1-play 2-dials 3-exit
        self.menu_tuple = (self.default, self.play, self.settings, self.exit)

    def menu_to_show(self) -> pygame.Surface:
        """
        Due to strange menu image design where button states are included as different menu images instead of buttons
        added onto the menu image, the entire menu image needs to be swapped to display the correct "button" selected.
        :return: pygame.Surface
        """
        match self.num_to_show:
            case 0:
                return self.menu_tuple[0]
            case 1:
                return self.menu_tuple[1]
            case 2:
                return self.menu_tuple[2]
            case 3:
                return self.menu_tuple[3]

    def game_loop(self, is_running: bool):
        """
        Logic for menu and returns correct game state from selected menu button.
        :param is_running:
        :return: running, state
        """
        running = is_running
        state = GameState.MENU

        mouse_pos = pygame.mouse.get_pos()

        if self.play_rect.collidepoint(mouse_pos):
            self.num_to_show = 1
        elif self.dials_rect.collidepoint(mouse_pos):
            self.num_to_show = 2
        elif self.exit_rect.collidepoint(mouse_pos):
            self.num_to_show = 3
        else:
            self.num_to_show = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Keydown events handling
            if event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                match self.num_to_show:
                    #case 0: pass
                    case 1: state = GameState.GAME
                    case 2: state = GameState.DIALS
                    case 3: running = False

        return running, state
