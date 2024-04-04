import pygame

from scripts.menus.dials import Dials
from scripts.utilities.window import Window
from scripts.menus.menu import Menu
from scripts.game import Game
from scripts.utilities.enums import GameState

# Initializes the pygame package
pygame.init()

# Necessary classes
window = Window()

# GAME CONSTANTS
FPS = 60


def main():
    """Contains all aspects of the game and runs main game loop."""
    is_running = True
    clock = pygame.time.Clock()
    state = GameState.MENU
    menu = Menu()
    game = None
    dials = None

    while is_running:
        clock.tick(FPS)  # Draws 60 frames per second

        # Menus or game logic
        match state.value:
            case GameState.MENU.value:
                is_running, state = menu.game_loop(is_running)
                window.window_surface.blit(menu.menu_to_show(), (0, 0))
                if state != GameState.MENU:
                    # Get rid of non-used classes
                    del menu
                    if state == GameState.GAME:
                        game = Game()
                    else:
                        dials = Dials()

            case GameState.GAME.value:
                is_running, state = game.game_loop(is_running)
                # Restart game by initializing in menu match statement
                if state != GameState.GAME:
                    del game
                    if state == GameState.MENU:
                        menu = Menu()

            case GameState.DIALS.value:
                is_running, state = dials.game_loop(is_running)
                if state != GameState.DIALS:
                    del dials
                    if state == GameState.MENU:
                        menu = Menu()

        pygame.display.update()  # Draw new blits

    # End the game after main loop
    pygame.quit()  # End the session


if __name__ == "__main__":
    main()
