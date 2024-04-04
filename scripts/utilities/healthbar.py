import pygame


class HealthBar(pygame.sprite.Sprite):
    """
    Health Bar that can be applied to any entity containing health, max_health, and a rect attributes.
    """
    def __init__(self, entity):
        super().__init__()

        self.entity = entity

        self.display_surface = pygame.display.get_surface()

        self.bar_height = (self.entity.rect.height // 10)
        self.bar_width = self.entity.rect.width * (self.entity.health / self.entity.max_health)
        self.image = pygame.Surface((self.bar_width, self.bar_height))
        self.image.fill((175, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            self.entity.rect.midbottom[0], self.entity.rect.midbottom[1] + (self.entity.rect.height // 10))

    def draw(self):
        """Draw the healthbar."""
        new_width = self.entity.rect.width * (self.entity.health / self.entity.max_health)
        self.image = pygame.transform.scale(self.image, (new_width, self.bar_height))
        self.display_surface.blit(self.image, self.rect)
