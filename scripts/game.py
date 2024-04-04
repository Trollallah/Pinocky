import pygame

from scripts.map.tilemap import TileMap
from scripts.player.player import Player
from scripts.player.upgrades.ingameupgrade import InGameUpgrade
from scripts.utilities.gametimer import GameTimer
from scripts.utilities.enums import GameState
from scripts.pickups.pickupgroup import PickupGroup
from scripts.enemies.enemygroup import EnemyGroup
from scripts.camera_group import CameraGroup
from scripts.utilities.endscreen import EndScreen


class Game:
    """Class to manage game."""
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        # Game Timer
        self.game_timer = GameTimer()

        # Ingame upgrade
        self.in_game_upgrade = InGameUpgrade()

        # Create player
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player(self.in_game_upgrade)
        self.player_group.add(self.player)

        # Create tilemap
        self.map = TileMap()

        # Create pickup group
        self.pickup_group = PickupGroup()

        # Create enemy group
        self.enemy_group = EnemyGroup(self.player, self.map.min_max_coords(), self.pickup_group, self.game_timer)

        # Add groups to player for collision testing
        self.player.add_groups(self.player_group, self.enemy_group, self.pickup_group)

        # All drawing will be handled within the camera group
        self.camera_group = CameraGroup()
        self.camera_group.add_groups(self.map, self.pickup_group)

        self.mouse_pos = None

    def game_loop(self, is_running):
        """
        Main game loop.
        :param is_running:
        :return:
        """

        if self.game_timer.first_loop:
            self.game_timer.first_loop = False
            self.game_timer.time_start = pygame.time.get_ticks()

        running = is_running
        state = GameState.GAME

        if self.player.is_dead:
            end_screen = EndScreen(self, self.player, self.game_timer)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Keydown events handling
            if event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    state = GameState.MENU

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.in_game_upgrade.isPaused:
                    self.in_game_upgrade.select_card(self.mouse_pos)
                    if self.in_game_upgrade.selected_card is not None:
                        self.player.upgrades.apply_selected_upgrade(self.in_game_upgrade.selected_card)
                        self.in_game_upgrade.reset()
                elif self.player.is_dead:
                    end_screen.select_option(self.mouse_pos)

        if not self.player.is_dead:
            # Game is not paused
            if not self.in_game_upgrade.isPaused:
                # Handle player movement
                keys = pygame.key.get_pressed()
                self.player_group.sprite.update(keys)

                # Enemy Logic
                self.enemy_group.update()

                # Pickup logic
                self.pickup_group.update()

                # Finish pause time
                if self.game_timer.is_time_paused:
                    self.game_timer.is_time_paused = False
                    self.game_timer.calculate_time_paused()

            # Game is paused for upgrade
            else:
                if not self.in_game_upgrade.isCreated:
                    self.in_game_upgrade.create_cards()
                else:
                 self.mouse_pos = pygame.mouse.get_pos()
                # Pause time tracking to prevent time to accrue on game counter while paused
                self.game_timer.pause_time()

            # Add to one group for z sorting
            self.camera_group.add(self.player_group.sprites())
            self.camera_group.add(self.enemy_group.sprites())
            self.camera_group.custom_draw(self.player)

            # Draw time
            if not self.game_timer.is_time_paused and not self.player.is_dead:
                self.game_timer.draw_time()
            else:
             self.game_timer.draw_last_time()

            if self.in_game_upgrade.isPaused and self.in_game_upgrade.isCreated:
                self.in_game_upgrade.draw_cards()

        else:
            end_screen.draw()
            self.mouse_pos = pygame.mouse.get_pos()
            if end_screen.menu:
                state = GameState.MENU
            elif end_screen.exit:
                running = False

        return running, state
