import pygame

# Health Bar that can be applied to any entity containing health, max_health, and a rect attributes
class UpgradeBar(pygame.sprite.Sprite):
    """Responsible for updating the experience bar on the bottom of the screen."""
    def __init__(self, player):
        super().__init__()

        self.player = player

        self.display_surface = pygame.display.get_surface()
        self.ds_width = self.display_surface.get_width()
        self.ds_height = self.display_surface.get_height()
        self.ds_hw = self.ds_width // 2
        self.ds_hh = self.ds_height // 2

        # Inner bar
        # Uses screen value for scaling resolution
        self.inner_bar_height = int(self.display_surface.get_height() * 0.05)
        self.inner_bar_width = int(self.display_surface.get_width() * 0.8)
        self.inner_image = pygame.Surface((self.inner_bar_width, self.inner_bar_height))
        self.inner_image.fill((0, 175, 200))
        self.inner_rect = self.inner_image.get_rect()
        self.inner_rect.midbottom = (
            self.ds_hw, self.ds_height - (self.ds_height // 50)
        )

        # Outer bar
        # Uses screen value for scaling resolution
        self.outer_bar_height = int(self.display_surface.get_height() * 0.07)
        self.outer_bar_width = int(self.display_surface.get_width() * 0.81)
        self.outer_image = pygame.Surface((self.outer_bar_width, self.outer_bar_height))
        self.outer_image.fill((0, 125, 140))
        self.outer_rect = self.outer_image.get_rect()
        self.outer_rect.center = self.inner_rect.center

    def draw(self):
        """
        Draw the bar on the screen.
        :return:
        """
        # Outer bar
        self.display_surface.blit(self.outer_image, self.outer_rect)

        # Resize inner bar
        new_width = self.inner_rect.width * (self.player.upgrades.xp / self.player.upgrades.xp_til_next_level)
        self.inner_image = pygame.transform.scale(self.inner_image, (new_width, self.inner_bar_height))
        self.inner_image.fill((0, 175, 200))  # Shows up as black without this if bar was 0 width
        self.display_surface.blit(self.inner_image, self.inner_rect)
