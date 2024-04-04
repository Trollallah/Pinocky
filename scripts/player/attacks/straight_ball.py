import pygame
import os

from scripts.utilities.scale import scale_singleton as scale


class StraightBall(pygame.sprite.Sprite):
    """Attack for player. StraightBall is a ball that is spawned and damages enemies it collides with."""
    def __init__(self, speed, attack_type, attack_manager):
        pygame.sprite.Sprite.__init__(self)

        self.display_surface = pygame.display.get_surface()
        self.enum = attack_type
        self.attack_manager = attack_manager

        self.already_attacked_IDs = []

        self.is_active = True
        self.is_right = True
        self.damage_amount = 1
        # Speed to scale with player
        self.player_speed = speed
        self.ball_speed = 3
        self.speed = self.player_speed + self.ball_speed
        self.last_time = 0
        self.active_duration = 500

        # Upgrades that sends another ball behind player
        self.second_ball: bool = False
        self.is_second_ball = False

        self.image = self.image = pygame.image.load(
            os.path.join("assets", "player_attacks", "straight_ball.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (
            (int(self.image.get_width() * 0.35)), int(self.image.get_height() * 0.35)))
        if scale.scale:
            self.speed = scale.speed_scale(self.speed)
        self.rect = self.image.get_rect()

    def apply_damage(self, enemy):
        """
        Calls the take damage function of enemy that was collided with.
        :param enemy:
        :return:
        """
        enemy.take_damage(self.damage_amount)

    def spawn(self, is_right, player_rect):
        """
        Activates the attack and resets it to correct initial location.
        :param is_right:
        :param player_rect:
        :return:
        """
        self.is_active = True
        self.is_right = is_right
        self.last_time = pygame.time.get_ticks()
        if not self.is_second_ball:
            if is_right:  # Right
                self.rect.midleft = player_rect.bottomright
            else:  # Left
                self.rect.midright = player_rect.bottomleft
        else:
            if is_right:  # Right
                self.rect.midright = player_rect.topleft
            else:  # Left
                self.rect.midleft = player_rect.topright

    def update(self):
        """
        Called every frame. The attack movement logic.
        :return:
        """
        current_time = pygame.time.get_ticks()
        self.is_active = current_time < self.last_time + self.active_duration
        if self.is_active:
            if not self.is_second_ball:
                if self.is_right:
                    self.rect.x += self.speed
                else:
                    self.rect.x -= self.speed
            else:
                if self.is_right:
                    self.rect.x -= self.speed
                else:
                    self.rect.x += self.speed
        else:
            # Empty attacked list to allow enemies to be attacked next roll
            self.already_attacked_IDs = []

    def create_second_ball(self):
        """
        Upgrade which adds a second ball and modifies attributes so no further second ball can be and attributes for the
        second ball to be recognized as the second ball.
        :return:
        """
        second_ball = StraightBall(self.speed, self.enum, self.attack_manager)
        # set bools for second ball to use proper logic and prevent a 2nd second ball upgrade
        second_ball.second_ball = True
        second_ball.is_second_ball = True
        # Apply any already received upgrades to second ball
        second_ball.damage_amount = self.damage_amount
        second_ball.ball_speed = self.ball_speed
        second_ball.active_duration = self.active_duration
        # Add to attacks for logic, rendering, and upgrades
        self.attack_manager.attacks.append(second_ball)
        # Add to the sprite group for collisions
        self.attack_manager.add(second_ball)
