import pygame


class EndScreen(pygame.sprite.Sprite):
    """
    Displays the end screen and presents player with stats and options to exit or main menu.
    This class could definitely be rewritten in a less hacky way.
    """
    def __init__(self, game, player, game_timer):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.display_surface = pygame.display.get_surface()
        self.ds_w = self.display_surface.get_width()
        self.ds_hw = self.ds_w // 2
        self.ds_h = self.display_surface.get_height()
        self.ds_hh = self.ds_h // 2

        self.gamover = False
        self.top_text = "Congratulations!"
        self.middle_text = "You lasted: " + game_timer.timer_text
        self.bottom_text = "Score: " + str(player.score)

        self.text_size = 54
        self.font = pygame.font.SysFont('arial', self.text_size, bold=False, italic=False)

        self.top_surf = self.font.render(self.top_text, False, 'black')
        self.middle_surf = self.font.render(self.middle_text, False, 'black')
        self.bottom_surf = self.font.render(self.bottom_text, False, 'black')

        self.top_rect = self.top_surf.get_rect()
        self.middle_rect = self.middle_surf.get_rect()
        self.bottom_rect = self.bottom_surf.get_rect()

        self.menu_button_text = "Menu"
        self.exit_button_text = "Exit"

        self.menu_button_surf = self.font.render(self.menu_button_text, False, 'green')
        self.exit_button_surf = self.font.render(self.exit_button_text, False, 'red')

        #self.menu_button_surf.fill((25, 175, 175))
        #self.exit_button_surf.fill((175, 200, 200))

        self.menu_rect = self.menu_button_surf.get_rect()
        self.exit_rect = self.exit_button_surf.get_rect()

        self.image = pygame.Surface((self.ds_hw * 1.5, self.ds_hh * 1.5))
        self.rect = self.image.get_rect()
        self.rect.center = (self.ds_hw, self.ds_hh)
        self.image.fill((255, 255, 255))

        self.quarter = self.image.get_height() // 5

        self.rect_list = [self.top_rect, self.middle_rect, self.bottom_rect, self.menu_rect]
        for i, rect in enumerate(self.rect_list):
            rect.centerx = self.rect.midtop[0]
            rect.centery = self.rect.midtop[1] + self.quarter * (i + 1)

        self.exit_rect.centerx = self.rect_list[3].centerx
        self.exit_rect.centery = self.rect_list[3].centery
        self.exit_rect.centerx += self.rect.width // 6
        self.rect_list[3].centerx -= self.rect.width // 6

        self.menu = False
        self.exit = False

    def draw(self):
        """
        Draw the screen.
        :return:
        """
        self.image.fill((100, 145, 165))
        self.image.set_alpha((8))
        self.display_surface.blit(self.image, self.rect)
        self.display_surface.blit(self.top_surf, self.rect_list[0])
        self.display_surface.blit(self.middle_surf, self.rect_list[1])
        self.display_surface.blit(self.bottom_surf, self.rect_list[2])
        self.display_surface.blit(self.menu_button_surf, self.rect_list[3])
        self.display_surface.blit(self.exit_button_surf, self.exit_rect)

    def select_option(self, mouse_pos):
        """
        Uses the mouse position to determine which button was selected.
        :param mouse_pos:
        :return:
        """
        if self.exit_rect.collidepoint(mouse_pos):
            self.exit = True
        elif self.menu_rect.collidepoint(mouse_pos):
            self.menu = True
        else:
            self.exit = False
            self.menu = False
