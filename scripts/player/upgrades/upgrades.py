import pygame
import random
from scripts.player.upgrades.upgradebar import UpgradeBar
from scripts.player.upgrades.upgradedata import UpgradeData

class Upgrades:
    """Upgrade logic. Facilitates the bridge between player xp and upgrade options."""
    def __init__(self, player, attack_manager, in_game_upgrade):

        self.display_surface = pygame.display.get_surface()

        self.player = player
        self.attack_manager = attack_manager
        self.in_game_upgrade = in_game_upgrade

        self.player_level = 0
        self.xp = 0
        self.xp_til_next_level = 10
        self.upgrade_bar = UpgradeBar(self.player)
        self.absorb_radius = self.display_surface.get_height() // 4  # -= 1 for 2 upgrades

        # All upgrades defined in UpgradeData()
        self.upgrader = UpgradeData(self, self.player, self.attack_manager)

    def xp_absorb(self, pickup_group_sprites):
        """
        Circle surrounding player that triggers the absorbing xp when pickup containing xp is collided with.
        :param pickup_group_sprites:
        :return:
        """
        player_x, player_y = self.player.rect.center
        for item in pickup_group_sprites:
            xp_x, xp_y = item.rect.center
            if ((xp_x - player_x)**2) + ((xp_y - player_y)**2) <= self.absorb_radius**2:
                item.assign_target(self.player)

    def gain_xp(self, amount):
        """
        Adds xp amount and check if level up is triggered.
        :param amount:
        :return:
        """
        self.xp += amount
        if self.xp >= self.xp_til_next_level:
            temp_xp = self.xp - self.xp_til_next_level
            self.level_up(temp_xp)

    def level_up(self, xp):
        """
        Increases player level and allows upgrades to be chosen.
        :param xp:
        :return:
        """
        self.player_level += 1
        self.xp_til_next_level = int(self.xp_til_next_level * 1.3)
        self.xp = xp
        self.pick_upgrades()
        self.player.apply_health(self.player.max_health // 4)
        self.player.level_up_signal()


    def pick_upgrades(self):
        """
        Randomly selects 2 upgrades for the player to select from or the only upgrade available.
        :return:
        """
        available_upgrades = self.upgrader.available_upgrades[:]
        length = len(available_upgrades)
        min = 0
        upgrade_options = []

        for i in range(length):
            length = len(available_upgrades)
            if length > 1:
                rand = random.randint(min, length - 1)
                upgrade_chosen = available_upgrades[rand]
            else:
                upgrade_chosen = available_upgrades[0]

            upgrade_options.append(upgrade_chosen)
            available_upgrades.remove(upgrade_chosen)

        self.in_game_upgrade.pause_and_upgrade(upgrade_options)

    def apply_selected_upgrade(self, upgrade_to_apply):
        """
        Facilitates applying an upgrade's data to relevant target's data.
        :param upgrade_to_apply:
        :return:
        """
        self.upgrader.upgrade(upgrade_to_apply)
