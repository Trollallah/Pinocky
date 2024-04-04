import pygame

from scripts.utilities.scale import scale_singleton as scale


class Enemy(pygame.sprite.Sprite):
    """Every enemy is an instance of this class with customized properties passed as parameters on init method"""
    def __init__(self, pickup_group, position, ID, name_enum, speed, dam, health, image, mask, pickup_type):
        pygame.sprite.Sprite.__init__(self)

        self.pickup_group = pickup_group
        self.pickup_type = pickup_type

        # Add ID
        self.ID = ID
        # Name
        self.name = name_enum
        # Add speed
        self.speed = speed
        # Damage
        self.damage_amount = dam
        # Health
        self.health = health
        # Image
        self.image = image
        # Mask for custom collisions
        self.mask = mask

        # Scale
        if scale.scale:
            self.speed = scale.speed_scale(self.speed)

        # Rect after scaling to get correct size
        self.rect = self.image.get_rect(center=position)

        # Attack timer
        self.timer_attack = pygame.time.get_ticks()
        self.timer_attack_wait = 1000  # Milliseconds before next attack
        self.timer_stunned = self.timer_attack
        self.timer_stunned_wait = 500
        self.is_stunned = False

    def take_damage(self, damage):
        """
        Enemy applies damage to it's health and sets stun status.
        :param damage:
        :return:
        """
        current_time = pygame.time.get_ticks()

        # Stun unlocked in EnemyGroup.update()
        if not self.is_stunned:
            self.timer_stunned = current_time
            self.is_stunned = True

        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def stun_time(self):
        """
        Returns stun duration.
        :return: int
        """
        # Used in EnemyGroup.update()
        return self.timer_stunned + self.timer_stunned_wait

    def apply_damage(self, target):
        """
        Checks if eligible to damage target and applies damage accordingly.
        :param target:
        :return:
        """
        current_time = pygame.time.get_ticks()
        if self.timer_attack + self.timer_attack_wait <= current_time:
            self.timer_attack = current_time
            target.take_damage(self.damage_amount)

    def destroy(self):
        """
        Spawns pickup, removes self from groups, and deletes instance from memory.
        :return:
        """
        # Spawn xp pickup
        self.pickup_group.spawn_pickup(self.rect.center, self.pickup_type)
        # The enemy instance  will be removed from all groups then deleted
        self.kill()
        del self
