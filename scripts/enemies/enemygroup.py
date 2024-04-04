import pygame
import random

from scripts.enemies.enemybuilder import EnemyBuilder


class EnemyGroup(pygame.sprite.Group):
    """Custom pygame sprite group that handles high level enemy logic."""
    def __init__(self, player, tile_map_min_max_coords, pickup_group, game_timer):
        super().__init__()
        self.game_timer = game_timer
        self.pickup_group = pickup_group
        self.player = player
        self.player_pos = self.player.rect.center
        self.player_x, self.player_y = self.player_pos
        self.spawn_x_min, self.spawn_x_max, self.spawn_y_min, self.spawn_y_max = tile_map_min_max_coords
        self.enemy_builder = EnemyBuilder(pickup_group, self)

        self.display_surface = pygame.display.get_surface()
        self.ds_w = self.display_surface.get_width()
        self.ds_hw = self.ds_w // 2
        self.ds_h = self.display_surface.get_height()
        self.ds_hh = self.ds_h // 2

        self.spawn_time = 10000
        self.spawn_time_adjusted = self.spawn_time
        self.initial_spawn = True

        # Make enemies stronger every 3 levels
        self.buff = 1
        self.buff_amount = 2

        self.safe_distance = self.ds_h * 1.5
        self.max_spawn_distance = self.ds_h * 3

    def rebalance(self):
        """
        Scales difficulty up by increasing spawn rate, increasing enemy damage, and enemy health.
        :return:
        """
        if self.spawn_time > 500:
            self.spawn_time -= 500
        self.enemy_builder.rebalance()
        if self.buff % 4 == 0:
            self.buff += 1
            for enemy in self.sprites():
                enemy.damage_amount += self.buff_amount
                enemy.health += self.buff_amount

    def spawn_initial(self):
        """
        Creates an initial enemy pack at top right of screen upon game start.
        :return:
        """
        x, y = self.display_surface.get_rect().topright
        self.enemy_builder.build_pack(x, y)

    def calculate_spawn_spot(self):
        """
        Uses player position to determine areas just outside the window to spawn enemies.
        :return:
        """
        player_x, player_y = self.player.rect.centerx, self.player.rect.centery
        safe_dist = self.safe_distance
        max_dist = self.max_spawn_distance

        outside_left_far_x = player_x - max_dist
        inside_left_near_x = player_x - safe_dist

        outside_right_far_x = player_x + max_dist
        inside_right_near_x = player_x + safe_dist

        top_bottom_y = player_y - safe_dist
        top_top_y = player_y - max_dist

        bottom_bottom_y = player_y + max_dist
        bottom_top_y = player_y + safe_dist

        rand_box = random.randint(0, 3)
        x, y = None, None
        match rand_box:
            case 0:  # Top
                x = random.randint(outside_left_far_x, outside_right_far_x)
                y = random.randint(top_top_y, top_bottom_y)
            case 1:  # Right
                x = random.randint(inside_right_near_x, outside_right_far_x)
                y = random.randint(top_bottom_y, bottom_top_y)
            case 2:  # Bottom
                x = random.randint(outside_left_far_x, outside_right_far_x)
                y = random.randint(bottom_top_y, bottom_bottom_y)
            case 3:  # Left
                x = random.randint(outside_left_far_x, inside_left_near_x)
                y = random.randint(top_bottom_y, bottom_top_y)

        return x, y

    def spawn_enemies(self):
        """
        Spawn enemies within approved coordinates.
        :return:
        """
        x, y = self.calculate_spawn_spot()
        self.enemy_builder.build_pack(x, y)

    def spawn_timer(self):
        """Uses timers to determine whether or not to spawn enemies."""
        if self.spawn_time_adjusted <= self.game_timer.current_time_ms:
            self.spawn_time_adjusted = self.spawn_time + self.game_timer.current_time_ms
            for _ in range(random.randint(2, 5)):
                self.spawn_enemies()

    def update(self):
        """
        Called every frame. Checks spawnability, updates all enemies' movement, stun status in sprite list.
        :return:
        """
        # Cache player Position
        player_x, player_y = self.player.rect.center

        if self.initial_spawn:
            self.initial_spawn = False
            self.spawn_initial()

        self.spawn_timer()

        current_time = pygame.time.get_ticks()

        # Move enemies towards player
        for sprite in self.sprites():
            if not sprite.is_stunned:
                new_x = (player_x - sprite.rect.centerx)
                new_y = (player_y - sprite.rect.centery)

                new_direction = pygame.Vector2(new_x, new_y)

                if new_direction.length() > 0:
                    new_direction = new_direction.normalize() * sprite.speed
                    sprite.rect.move_ip(new_direction)

            elif sprite.stun_time() <= current_time:
                sprite.is_stunned = False
