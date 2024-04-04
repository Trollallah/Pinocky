import pygame
import os

from scripts.utilities.scale import scale_singleton as scale
from scripts.utilities.enums import PlayerUpgrades, SBUpgrades


class UpgradeCard(pygame.sprite.Sprite):
    """Stores data for upgrade cards."""
    def __init__(self, is_left):
        pygame.sprite.Sprite.__init__(self)

        self.is_left = is_left
        self.enum = None

        self.display_surface = pygame.display.get_surface()
        self.ds_w = self.display_surface.get_width()
        self.ds_hw = self.ds_w // 2
        self.ds_h = self.display_surface.get_height()
        self.ds_hh = self.ds_h // 2

        self.image = pygame.image.load(os.path.join("assets", "upgrades", "upgrade_template.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*1.5, self.image.get_height()*1.5))

        self.p_image = pygame.image.load(os.path.join("assets", "player", "idle", "player_idle_front_1.png")).convert_alpha()
        self.p_image = pygame.transform.scale(self.p_image, ((
            (int(self.p_image.get_width() * 0.75)), int(self.p_image.get_height() * 0.75))))
        self.sb_image = pygame.image.load(os.path.join("assets", "player_attacks", "straight_ball.png")).convert_alpha()

        self.sb_image = pygame.transform.scale(self.sb_image, (
            (int(self.sb_image.get_width() * 0.6)), int(self.sb_image.get_height() * 0.6)))

        self.icon_dict = {
            PlayerUpgrades: self.p_image,
            SBUpgrades: self.sb_image
        }

        self.text_size = 36

        if scale.scale:
            self.image = pygame.transform.scale(self.image, (
                scale.r1440(self.image.get_width()), scale.r1440(self.image.get_height())))
            for k, v in self.icon_dict.items():
                self.icon_dict[k] = pygame.transform.scale(v, (scale.r1440(v.get_width()), scale.r1440(v.get_height())))
            self.text_size *= 2

        self.rect = self.image.get_rect()
        self.rect.center = (self.ds_hw, self.ds_hh)

        if self.is_left:
            self.rect.centerx -= self.ds_w // 6
        else:
            self.rect.centerx += self.ds_w // 6

        self.icon = None
        self.icon_rect = None
        self.image_subsurface = None

        self.is_ready_to_draw = False

        self.card_text = ""

        self.font = pygame.font.SysFont('arial', self.text_size, bold=False, italic=False)
        self.text_surf = self.font.render("Test", False, 'black')
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.rect.center
        self.text_rect.centery += self.ds_hh // 3

    def customize_card(self, upgrade_enum):
        """
        Takes in upgrade type and customizes card accordingly.
        :param upgrade_enum:
        :return:
        """
        self.enum = upgrade_enum
        enum_type = type(upgrade_enum)

        self.icon = self.icon_dict[enum_type]
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.center = self.rect.center

        if enum_type == PlayerUpgrades:
            self.icon_rect.centery -= self.ds_hh // 7
            match upgrade_enum.value:
                case PlayerUpgrades.SPEED.value:
                    self.card_text = "SPEED"
                case PlayerUpgrades.HEALTH.value:
                    self.card_text = "MAX HEALTH"
                case PlayerUpgrades.ABSORB.value:
                    self.card_text = "ABSORB"
        elif enum_type == SBUpgrades:
            self.icon_rect.centery -= self.ds_hh // 7
            match upgrade_enum.value:
                case SBUpgrades.DAMAGE.value:
                    self.card_text = "DAMAGE"
                case SBUpgrades.DURATION.value:
                    self.card_text = "TIME"
                case SBUpgrades.SPEED.value:
                    self.card_text = "SPEED"
                case SBUpgrades.SECOND_BALL.value:
                    self.card_text = "SECOND BALL"

        self.text_surf = self.font.render(self.card_text, True, 'black')
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.rect.center
        self.text_rect.centery += self.ds_hh // 2.9

        self.is_ready_to_draw = True

    def draw(self):
        """
        Draw the card on the screen.
        :return:
        """
        if self.is_ready_to_draw:
            self.display_surface.blit(self.image, self.rect)
            self.display_surface.blit(self.icon, self.icon_rect)
            self.display_surface.blit(self.text_surf, self.text_rect)
