import pygame


class CameraGroup(pygame.sprite.Group):
    """Class to allow for z ordering as well as offset value pushing."""
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.display_surface_width = self.display_surface.get_width()
        self.display_surface_height = self.display_surface.get_height()
        self.half_width = self.display_surface_width // 2
        self.half_height = self.display_surface_height // 2

        self.map = None
        self.pickup_group = None

    def add_groups(self, map_name, pickup_group):
        """
        Adds sprite groups references for class to call.
        :param map_name:
        :param pickup_group:
        :return:
        """
        self.map = map_name
        self.pickup_group = pickup_group

    def center_target_camera(self, target):
        """
        Assigns target's center position to self.offset
        :param target:
        :return:
        """
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        """
        Calls draw with offset on appropriate sprite groups, applies z ordering to appropriate sprites, and calls
        draw method on objects to appear on top of any other sprite like health/xp bars and attacks.
        :param player:
        :return:
        """
        self.center_target_camera(player)

        # Draw map tiles
        self.map.draw_with_offset(self.offset)
        self.pickup_group.draw_with_offset(self.offset)

        # Draw sprites with pseudo z sorting
        for sprite in sorted(self.sprites(), key=lambda sprite_sort: sprite_sort.rect.center):
            offset_pos = sprite.rect.topleft - self.offset

            self.display_surface.blit(sprite.image, offset_pos)

        # Draw attacks
        player.attack_manager.draw_with_offset(self.offset)
        # Player health bar always rendered above other images
        player.draw_health_bar()
        player.upgrades.upgrade_bar.draw()
