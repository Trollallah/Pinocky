import pygame
from scripts.utilities.enums import TileType
from scripts.map.tile import Tile


class TileMap:
    """Creates a tile map by generating a grid which has a center of 0,0."""
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        # Making center grid the middle
        self.tile_grid_width = 15  # MUST BE ODD NUM
        self.tile_grid_height = 15  # MUST BE ODD NUM

        # Create 2 arrays of same length
        # One for Tile Type
        # One for tile coordinates
        self.tile_grid_types = []
        self.tile_grid_coords = []
        # Fill grid types array with default value, could easily be swapped out for a custom text file version or class
        for i in range(self.tile_grid_width):
            temp_array = []
            for j in range(self.tile_grid_height):
                temp_array.append(0)
            self.tile_grid_types.append(temp_array[:])

        # Get center tile array location
        self.center_tile_x = self.tile_grid_width // 2
        self.center_tile_y = self.tile_grid_height // 2
        self.tile_size = self.display_surface.get_size()  # Tiles are same as window size as of now

        self.array_offset_neg = -((self.tile_grid_width - 1) // 2)
        self.array_offset_pos = ((self.tile_grid_width - 1) // 2) + 1
        self.position_offset = []
        for i in range(self.array_offset_neg, self.array_offset_pos):
            self.position_offset.append(i)  # For 9 this would result in [-4 to 4]

        for i in range(self.tile_grid_width):
            temp_array = []
            x_offset = self.position_offset[i]
            for j in range(self.tile_grid_height):
                y_offset = self.position_offset[j]
                coord = (x_offset * self.tile_size[0], y_offset * self.tile_size[1])
                temp_array.append(coord)
            self.tile_grid_coords.append(temp_array[:])

        self.tiles_to_draw_with_coords = list()
        for ttd_list, pos_list in zip(self.tile_grid_types, self.tile_grid_coords):
            for ttd, pos in zip(ttd_list, pos_list):
                self.tiles_to_draw_with_coords.append((ttd, pos))
        self.tiles_to_draw_with_coords = tuple(self.tiles_to_draw_with_coords)

        # Load tiles into tile_images. Easily scalable by adding to enums and appending to tile images
        self.tile_images = []
        self.tile_images.append(Tile(TileType.DEFAULT))
        self.tile_images = tuple(self.tile_images)

    def draw_with_offset(self, offset):
        """
        Draws tiles in relation to the player's current position to simulate movement.
        :param offset:
        :return:
        """
        for row in self.tiles_to_draw_with_coords:
            offset_pos = row[1] - offset
            self.display_surface.blit(self.tile_images[row[0]].tile_image, offset_pos)

    def min_max_coords(self):
        """
        The outer bounds of the tile map.
        :return: tuple(int, int, int, int)
        """
        spawn_x_min = self.tiles_to_draw_with_coords[0][1][0]
        spawn_x_max = self.tiles_to_draw_with_coords[-1][1][0]
        spawn_y_min = self.tiles_to_draw_with_coords[0][1][1]
        spawn_y_max = self.tiles_to_draw_with_coords[-1][1][1]
        return spawn_x_min, spawn_x_max, spawn_y_min, spawn_y_max
