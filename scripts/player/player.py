import pygame
import os
from scripts.utilities.healthbar import HealthBar
from scripts.player.upgrades.upgrades import Upgrades
from scripts.player.playerattackmanager import PlayerAttackManager
from scripts.utilities.enums import Pickups
from scripts.utilities.scale import scale_singleton as scale


class Player(pygame.sprite.Sprite):
    """The player class represents the player and is accessed by many classes."""
    def __init__(self, in_game_upgrade):
        pygame.sprite.Sprite.__init__(self)

        self.display_surface = pygame.display.get_surface()

        self.walk_speed = 4
        self.health = 10
        self.max_health = 10
        self.is_dead = False
        self.is_right = True
        self.score = 0

        self.image = pygame.image.load((os.path.join('assets', 'player', 'idle', 'player_idle_front_1.png'))).convert_alpha()
        self.idle_front_image = pygame.image.load((os.path.join('assets', 'player', 'idle', 'player_idle_front_1.png'))).convert_alpha()
        self.idle_back_image = pygame.image.load((os.path.join('assets', 'player', 'idle', 'player_idle_back_1.png'))).convert_alpha()
        self.idle_side_r_image = pygame.image.load((os.path.join('assets', 'player', 'idle', 'player_idle_side_1.png'))).convert_alpha()
        self.idle_side_l_image = pygame.transform.flip(self.idle_side_r_image, True, False)
        self.idle_images = [self.idle_front_image, self.idle_back_image, self.idle_side_r_image, self.idle_side_l_image]
        for i in range(len(self.idle_images)):
            self.idle_images[i] = pygame.transform.scale(self.idle_images[i],
                                    ((int(self.idle_images[i].get_width() * 0.5), int(self.idle_images[i].get_height() * 0.5))))
        if scale.scale:
            self.walk_speed = scale.speed_scale(self.walk_speed)
            for i in range(len(self.idle_images)):
                self.idle_images[i] = pygame.transform.scale(self.idle_images[i], (scale.r1440(self.idle_images[i].get_width()),scale.r1440(self.idle_images[i].get_height())))

        self.idle_images = tuple(self.idle_images)
        self.image = self.idle_images[0]

        # self.rect works because all images are same dimensions
        self.rect = self.image.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))

        # Mask for better collisions
        self.mask = pygame.mask.from_surface(self.image)

        # Create helper classes
        self.health_bar = HealthBar(self)
        self.attack_manager = PlayerAttackManager(self)
        self.upgrades = Upgrades(self, self.attack_manager, in_game_upgrade)

        self.direction = pygame.math.Vector2()

        # Ref to other sprite groups for collisions
        self.player_group = None
        self.enemy_group = None
        self.pickup_group = None

    def draw_health_bar(self):
        """
        Draws the healthbar on the screen under the player.
        :return:
        """
        self.health_bar.draw()

    def add_groups(self, player_group, enemy_group, pickup_group):
        """
        Adds pygame sprite group references to the player for collision logic.
        :param player_group:
        :param enemy_group:
        :param pickup_group:
        :return:
        """
        self.player_group = player_group
        self.enemy_group = enemy_group
        self.pickup_group = pickup_group
        self.attack_manager.add_groups(enemy_group)

    def collision_check(self):
        """
        Check for collisions with enemies and pickups.
        :return:
        """
        collisions = pygame.sprite.spritecollide(self, self.enemy_group, False, pygame.sprite.collide_mask)
        if len(collisions) > 0:
            for enemy in collisions:
                enemy.apply_damage(self)


        collisions = pygame.sprite.spritecollide(self, self.pickup_group, False)
        if len(collisions) > 0:
            for pickup in collisions:
                if pickup.enum in self.pickup_group.xp_list:
                    self.upgrades.gain_xp(pickup.value)
                    self.add_to_score(pickup.enum)
                    pickup.destroy()

    def add_to_score(self, enum):
        """
        Add a score to the score on xp pickups.
        A dictionary with this info would probably be better.
        :param enum:
        :return:
        """
        match enum.value:
            case Pickups.XP_SMALL.value:
                self.score += 1
            case Pickups.XP_BIG.value:
                self.score += 5


    def take_damage(self, damage_amount):
        """
        Apply a damage amount self health and manage is_dead bool.
        :param damage_amount:
        :return:
        """
        self.health = max(0, self.health - damage_amount)
        if self.health <= 0:
            self.is_dead = True

    def apply_health(self, health_amount):
        """
        Apply a health amount to self health.
        :param health_amount:
        :return:
        """
        self.health += health_amount
        if self.health > self.max_health:
            self.health = self.max_health

    def update(self, keys):
        """
        Called every frame. Updates the player's movement, calls attack manager update, and various collision check
        calls.
        :param keys:
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.image = self.idle_images[1]  # Back

        # Movement logic
        # Move the character without diagonals being faster
        # Returns 1 or 0
        # Sets image for direction
        # No diagonal image so side images are used in that case
        up = 0
        down = 0
        left = 0
        right = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            up = 1
            self.image = self.idle_images[1]  # Back
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            down = 1
            self.image = self.idle_images[0]  # Front
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            left = 1
            self.image = self.idle_images[3]  # ide Left
            self.is_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            right = 1
            self.image = self.idle_images[2]  # Side Right
            self.is_right = True

        # Uses the directions values to create a vector to scale for new coord point
        self.direction = pygame.math.Vector2(right - left, down - up)
        if self.direction.length() != 0:
            self.direction.scale_to_length(self.walk_speed)
            self.rect.move_ip(round(self.direction.x), round(self.direction.y))

        # Handle the attack logic
        self.attack_manager.update()

        # Collision checking
        self.upgrades.xp_absorb(self.pickup_group.sprites())
        self.collision_check()
        self.attack_manager.check_collisions()

    def level_up_signal(self):
        """
        Relays level up signal to the enemy group.
        :return:
        """
        self.enemy_group.rebalance()
