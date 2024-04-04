import pygame

from scripts.utilities.enums import PlayerAttack
from scripts.player.attacks.straight_ball import StraightBall


class PlayerAttackManager(pygame.sprite.Group):
    """Class to manage the attacks for the Player class."""
    def __init__(self, player):
        super().__init__()

        self.player = player
        self.enemy_group = None

        self.display_surface = pygame.display.get_surface()

        self.last_time = 0
        self.attack_delay = 2500

        # List of attacks
        self.attacks = [
            StraightBall(self.player.walk_speed, PlayerAttack.STRAIGHT_BALL, self)
        ]

        # Add the attacks to the sprite group
        for attack in self.attacks:
            self.add(attack)

    def spawn_attacks(self):
        """
        Iterates through the attacks in the attacks list and spawns them.
        :return:
        """
        for attack in self.attacks:
            attack.spawn(self.player.is_right, self.player.rect)

    def update(self):
        """
        Called every frame and either spawns attacks or calls their update methods.
        :return:
        """
        current_time = pygame.time.get_ticks()
        if self.last_time + self.attack_delay <= current_time:
            self.last_time = current_time
            self.spawn_attacks()

        for attack in self.attacks:
            if attack.is_active:
                attack.update()

    def draw_with_offset(self, offset):
        """
        Draws the attacks relative to the player's current position.
        :param offset:
        :return:
        """
        for attack in self.attacks:
            if attack.is_active:
                offset_pos = (attack.rect.x - offset[0], attack.rect.y - offset[1])
                self.display_surface.blit(attack.image, offset_pos)

    def add_groups(self, enemy_group):
        """
        Allows for the EnemyGroup to be added as a reference after initialization of this class.
        :param enemy_group:
        :return:
        """
        self.enemy_group = enemy_group

    def check_collisions(self):
        """
        Iterates through attacks in the attacks list and checks if they have collided with enemies and applies
        damage.
        :return:
        """
        collisions = pygame.sprite.groupcollide(self, self.enemy_group, False, False)
        for attack in collisions:
            if attack.is_active:
                for enemy in collisions[attack]:
                    if enemy.ID not in attack.already_attacked_IDs:
                        attack.already_attacked_IDs.append(enemy.ID)
                        attack.apply_damage(enemy)
