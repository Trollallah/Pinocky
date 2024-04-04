import os
import pygame

from scripts.pickups.pickup import Pickup
from scripts.utilities.enums import Pickups
from scripts.utilities.scale import scale_singleton as scale


class PickupGroup(pygame.sprite.Group):
    """Manages pickups' data and spawning."""
    def __init__(self):
        pygame.sprite.Group.__init__(self)

        self.display_surface = pygame.display.get_surface()

        self.xp_small_image = pygame.image.load(os.path.join("assets", "pickups", "shoe_low.png")).convert_alpha()
        self.xp_large_image = pygame.image.load(os.path.join("assets", "pickups", "shoe_high.png")).convert_alpha()
        if scale.scale:
            self.xp_small_image = pygame.transform.scale(self.xp_small_image, (scale.r1440(self.xp_small_image.get_width()), self.xp_small_image.get_height()))
            self.xp_large_image = pygame.transform.scale(self.xp_large_image,
                                                (scale.r1440(self.xp_large_image.get_width()), self.xp_large_image.get_height()))

        self.pickup_data = {
            Pickups.XP_SMALL: [Pickups.XP_SMALL, 1, self.xp_small_image],
            Pickups.XP_BIG: [Pickups.XP_BIG, 15, self.xp_large_image]
        }

        # List to check if pickup is XP for player pickup radius
        # Non XP pickups need to be "stepped on"
        self.xp_list = [Pickups.XP_SMALL, Pickups.XP_BIG]

    def spawn_pickup(self, center, pickup_type):
        """
        Spawns a pickup of the pickup_type provided in parameter.
        :param center:
        :param pickup_type:
        :return:
        """
        data = self.pickup_data[pickup_type]
        self.add(Pickup(center, data[0], data[1], data[2]))

    def draw_with_offset(self, offset):
        """
        Draws the pickup in relation to player position.
        :param offset:
        :return:
        """
        for pickup in self.sprites():
            offset_pos = pickup.rect.centerx - offset[0], pickup.rect.centery - offset[1]
            self.display_surface.blit(pickup.image, offset_pos)
