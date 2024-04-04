import os

import pygame
import random
from scripts.enemies.enemy import Enemy
from scripts.utilities.scale import scale_singleton as scale
from scripts.utilities.enums import EnemyName
from scripts.utilities.enums import Pickups


class EnemyBuilder:
    """Handles the creation of enemies."""
    def __init__(self, pickup_group, enemy_group):
        self.ID_Count = 0

        self.display_surface = pygame.display.get_surface()

        self.pickup_group = pickup_group
        self.enemy_group = enemy_group

        # Load images and convert once instead of every instantiation
        self.weak_pin_image = pygame.image.load(os.path.join("assets", "enemies", "pin_weak.png")).convert_alpha()
        self.weak_pin_image = pygame.transform.scale(self.weak_pin_image, (
            (int(self.weak_pin_image.get_width() * 0.25)), int(self.weak_pin_image.get_height() * 0.25)))
        self.strong_pin_image = self.image = pygame.image.load(
            os.path.join("assets", "enemies", "pin_strong.png")).convert_alpha()
        # Scale
        if scale.scale:
            self.weak_pin_image = pygame.transform.scale(self.weak_pin_image, (
                scale.r1440(self.weak_pin_image.get_width()), scale.r1440(self.weak_pin_image.get_height())))
            self.strong_pin_image = pygame.transform.scale(self.strong_pin_image, (
                scale.r1440(self.strong_pin_image.get_width()), scale.r1440(self.strong_pin_image.get_height())))
        self.weak_pin_mask = pygame.mask.from_surface(self.weak_pin_image)
        self.strong_pin_mask = pygame.mask.from_surface(self.strong_pin_image)

        # name, speed, damage_amount, health, path
        self.enemy_attributes = {
            EnemyName.WEAK_PIN: [EnemyName.WEAK_PIN, 2, 1, 2, self.weak_pin_image, self.weak_pin_mask, Pickups.XP_SMALL],
            EnemyName.STRONG_PIN: [EnemyName.STRONG_PIN, 2, 1, 15, self.strong_pin_image, self.strong_pin_mask, Pickups.XP_BIG]
        }

        self.spawn_box_side = self.display_surface.get_width() // 4

        self.pack_size_low = 1
        self.pack_size_high = 5
        self.pack_size_modifier = 2
        self.every_other = 0

        self.chance_weak = 100
        self.chance_modifier = 5
        self.balanced = False


    def next_id(self):
        """
        Assigns a unique id to every enemy.
        :return:
        """
        self.ID_Count += 1
        return self.ID_Count

    def rebalance(self):
        """
        Adjusts enemy packs to have more tough enemies.
        :return:
        """
        if not self.balanced:
            self.chance_weak -= self.chance_modifier
            if self.every_other % 2 == 0 and self.pack_size_high <= 25:
                self.every_other += 1
                self.pack_size_modifier += self.pack_size_modifier
                self.pack_size_high += self.pack_size_modifier
            if self.chance_weak == 60:
                self.balanced = True

    def build(self, pickup_group, position: tuple, enemy_name) -> pygame.sprite.Sprite:
        """
        Instantiates enemy and returns instantiated enemy.
        :param pickup_group:
        :param position:
        :param enemy_name:
        :return: pygame.sprite.Sprite
        """
        # Load appropriate enemy info
        enemy_info = self.enemy_attributes[enemy_name]
        return Enemy(pickup_group, position, self.next_id(), enemy_info[0], enemy_info[1], enemy_info[2], enemy_info[3],
                     enemy_info[4], enemy_info[5], enemy_info[6])

    def build_pack(self, x, y):
        """
        Determines pack size, pack enemy composition, instantiates enemies, adds enemies to EnemyGroup SpriteList.
        :param x:
        :param y:
        :return:
        """
        dist = self.spawn_box_side
        left_x = x - dist
        right_x = x + dist
        top_y = y - dist
        bottom_y = y + dist

        rand_enemy_amount = random.randint(self.pack_size_low, self.pack_size_high)
        for _ in range(rand_enemy_amount):
            rand_x = random.randint(left_x, right_x)
            rand_y = random.randint(top_y, bottom_y)
            rand = random.randint(0, 100)
            if rand <= self.chance_weak:
                self.enemy_group.add(self.build(self.pickup_group, (rand_x, rand_y), EnemyName.WEAK_PIN))
            else:
                self.enemy_group.add(self.build(self.pickup_group, (rand_x, rand_y), EnemyName.STRONG_PIN))
