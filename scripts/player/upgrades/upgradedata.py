from scripts.utilities.enums import PlayerUpgrades
from scripts.utilities.enums import SBUpgrades
from scripts.utilities.enums import PlayerAttack
from scripts.utilities.enums import UpgradeType
from scripts.player.upgrades.upgradesuper import UpgradeSuper


class UpgradeData:
    """Stores the data for upgrades and the ability to aplay the upgrade."""

    def __init__(self, upgrades_class, player, attack_manager):

        self.upgrades_class = upgrades_class
        self.player = player
        self.attack_manager = attack_manager

        # Player Speed upgrade
        self.p_walk_speed = self.player.walk_speed
        self.p_walk_speed_tier = 0
        self.p_walk_speed_max_tier = 2
        self.p_walk_speed_modifier = 1.5
        self.p_speed_upgrade = UpgradeSuper(self.p_walk_speed, self.p_walk_speed_tier, self.p_walk_speed_max_tier,
                                            self.p_walk_speed_modifier, UpgradeType.MULTIPLICATION)

        # Player Health upgrade
        self.p_max_health = self.player.max_health
        self.p_max_health_tier = 0
        self.p_max_health_max_tier = 3
        self.p_max_health_modifier = 1.5
        self.p_health_upgrade = UpgradeSuper(self.p_max_health, self.p_max_health_tier, self.p_max_health_max_tier,
                                             self.p_max_health_modifier, UpgradeType.MULTIPLICATION)

        # Player Xp absorb upgrade
        self.p_absorb_radius = self.upgrades_class.absorb_radius
        self.p_absorb_radius_tier = 0
        self.p_absorb_radius_max_tier = 2
        self.p_absorb_radius_modifier = 1.5
        self.p_absorb_upgrade = UpgradeSuper(self.p_absorb_radius, self.p_absorb_radius_tier,
                                             self.p_absorb_radius_max_tier, self.p_absorb_radius_modifier,
                                             UpgradeType.MULTIPLICATION)

        for attack in self.attack_manager.attacks:
            match attack.enum.value:
                case PlayerAttack.STRAIGHT_BALL.value:
                    # StraightBall upgrades

                    # SB Damage upgrade
                    self.sb_damage_amount = attack.damage_amount
                    self.sb_damage_tier = 0
                    self.sb_damage_max_tier = 4
                    self.sb_damage_modifier = 2
                    self.sb_damage_upgrade = UpgradeSuper(self.sb_damage_amount, self.sb_damage_tier,
                                                          self.sb_damage_max_tier, self.sb_damage_modifier,
                                                          UpgradeType.MULTIPLICATION)

                    # SB Duration upgrade
                    self.sb_duration = attack.active_duration
                    self.sb_duration_tier = 0
                    self.sb_duration_max_tier = 2
                    self.sb_duration_modifier = 1.5
                    self.sb_duration_upgrade = UpgradeSuper(self.sb_duration, self.sb_duration_tier,
                                                            self.sb_duration_max_tier, self.sb_duration_modifier,
                                                            UpgradeType.MULTIPLICATION)

                    self.sb_speed = attack.speed
                    self.sb_speed_tier = 0
                    self.sb_speed_max_tier = 3
                    self.sb_speed_modifier = 1.5
                    self.sb_speed_upgrade = UpgradeSuper(self.sb_speed, self.sb_speed_tier, self.sb_speed_max_tier,
                                                         self.sb_speed_modifier, UpgradeType.MULTIPLICATION)

                    self.sb_second_ball = attack.second_ball
                    self.sb_second_ball_tier = 0
                    self.sb_second_ball_max_tier = 1
                    self.sb_second_ball_modifier = True
                    self.sb_second_ball_upgrade = UpgradeSuper(self.sb_second_ball, self.sb_second_ball_tier,
                                                               self.sb_second_ball_max_tier,
                                                               self.sb_second_ball_modifier, UpgradeType.BOOL)

        self.upgrade_dict = {
            PlayerUpgrades.SPEED: self.p_speed_upgrade,
            PlayerUpgrades.HEALTH: self.p_health_upgrade,
            PlayerUpgrades.ABSORB: self.p_absorb_upgrade,
            SBUpgrades.DAMAGE: self.sb_damage_upgrade,
            SBUpgrades.DURATION: self.sb_duration_upgrade,
            SBUpgrades.SPEED: self.sb_speed_upgrade,
            SBUpgrades.SECOND_BALL: self.sb_second_ball_upgrade
        }

        # Used to determine available upgrades
        # Elements removed when an upgrade's max tier is hit
        self.available_upgrades = [
            PlayerUpgrades.SPEED,
            PlayerUpgrades.HEALTH,
            PlayerUpgrades.ABSORB,
            SBUpgrades.DAMAGE,
            SBUpgrades.DURATION,
            SBUpgrades.SPEED,
            SBUpgrades.SECOND_BALL
        ]

    def upgrade(self, upgrade_type):
        """
        Determine whether an upgrade should be removed from available upgrades and applies the upgrade data.
        :param upgrade_type:
        :return:
        """
        upgrade = self.upgrade_dict[upgrade_type]
        upgrade.apply_upgrade()
        if upgrade.is_maxed:
            self.remove_available_upgrade(upgrade_type)
        self.upgrade_relevant_data(upgrade_type)

    def remove_available_upgrade(self, upgrade_type):
        """
        Removes the upgrades that have been maxed out from available upgrades.
        :param upgrade_type:
        :return:
        """
        self.available_upgrades.remove(upgrade_type)

    def add_available_upgrade(self, upgrade_type):
        """
        Adds an upgrade to available upgrades.
        :param upgrade_type:
        :return:
        """
        self.available_upgrades.append(upgrade_type)

    def upgrade_relevant_data(self, upgrade_to_apply):
        """
        Updates the relevant data on target for the upgrade chosen.
        :param upgrade_to_apply:
        :return:
        """
        enum_type = type(upgrade_to_apply)
        if enum_type == PlayerUpgrades:
            match upgrade_to_apply.value:
                case PlayerUpgrades.SPEED.value:
                    self.player.walk_speed = self.upgrade_dict[upgrade_to_apply].value
                case PlayerUpgrades.HEALTH.value:
                    self.player.max_health = self.upgrade_dict[upgrade_to_apply].value
                    self.player.apply_health(self.player.max_health)
                case PlayerUpgrades.ABSORB.value:
                    self.upgrades_class.absorb_radius = self.upgrade_dict[upgrade_to_apply].value
        else:
            for attack in self.attack_manager.attacks:
                match attack.enum.value:
                    case PlayerAttack.STRAIGHT_BALL.value:
                        if enum_type == SBUpgrades:
                            match upgrade_to_apply.value:
                                case SBUpgrades.DAMAGE.value:
                                    attack.damage_amount = self.upgrade_dict[upgrade_to_apply].value
                                case SBUpgrades.DURATION.value:
                                    attack.active_duration = self.upgrade_dict[upgrade_to_apply].value
                                case SBUpgrades.SPEED.value:
                                    attack.speed = self.upgrade_dict[upgrade_to_apply].value
                                case SBUpgrades.SECOND_BALL.value:
                                    if not attack.second_ball:
                                        attack.create_second_ball()
                                    attack.second_ball = self.upgrade_dict[upgrade_to_apply].value
