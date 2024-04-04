import pygame

from scripts.player.upgrades.upgrade_card import UpgradeCard

class InGameUpgrade:
    """Allows player to select an upgrade after leveling up."""
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.isPaused = False
        self.isCreated = False
        self.upgrade_options = None
        self.amount_of_upgrades = 0


        self.left_card = UpgradeCard(True)
        self.right_card = UpgradeCard(False)
        self.cards = [self.left_card, self.right_card]

        self.selected_card = None

    def pause_and_upgrade(self, upgrade_options):
        """
        Pauses game and loads available upgrades.
        :param upgrade_options:
        :return:
        """
        self.isPaused = True
        self.upgrade_options = upgrade_options[:]
        self.amount_of_upgrades = len(self.upgrade_options)
        if self.amount_of_upgrades == 0:
            self.isPaused = False
            return

    def create_cards(self):
        """
        Creates upgrade cards to be selected.
        :return:
        """
        self.left_card.customize_card(self.upgrade_options[0])
        if self.amount_of_upgrades > 1:
            self.right_card.customize_card(self.upgrade_options[1])
        self.isCreated = True

    def draw_cards(self):
        """
        Renders upgrade cards.
        :return:
        """
        if self.amount_of_upgrades > 1:
            for card in self.cards:
                card.draw()
        else:
            self.left_card.draw()

    def select_card(self, mouse_pos):
        """
        Uses mouses position to select upgrade card.
        :param mouse_pos:
        :return:
        """
        # Returns the selection to be assigned to the picked upgrade in player class
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                self.selected_card = card.enum

    def reset(self):
        """
        Resets class attributes so class can be used again.
        :return:
        """
        self.isPaused = False
        self.isCreated = False
        self.upgrade_options = None
        self.selected_card = None
