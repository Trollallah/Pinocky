import pygame


class Pickup(pygame.sprite.Sprite):
    """Pickup class is customized during init to be any potential pickup."""
    def __init__(self, center, enum, value, image):
        pygame.sprite.Sprite.__init__(self)

        self.enum = enum
        self.value = value
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.target = None
        self.speed = None

    def update(self):
        """
        Allows pickups to make their way to target.
        :return:
        """
        if self.speed:
            target_x, target_y = self.target.rect.center
            new_x = (target_x - self.rect.centerx)
            new_y = (target_y - self.rect.centery)

            new_direction = pygame.Vector2(new_x, new_y)

            if new_direction.length() != 0:
                new_direction.scale_to_length(self.speed)
                self.rect.move_ip(round(new_direction.x), round(new_direction.y))

    def assign_target(self, target):
        """
        Assigns a target for the pickup to travel towards.
        :param target:
        :return:
        """
        self.target = target
        self.speed = target.walk_speed * 2

    def destroy(self):
        """
        Removes pickup from PickupGroup sprite list and deletes memory footprint.
        :return:
        """
        self.kill()
        del self
