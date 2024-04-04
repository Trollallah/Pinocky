import pygame
import os
from scripts.utilities.scale import scale_singleton as scale
from scripts.utilities.enums import TileType


class Tile:
    """Creates tiles that make up the TileMap.
    Would benefit from a tile manager that stores the tile data and creates a tile by passing a reference to the
    appropriate data, so a single image is referenced by a tile instead of many individual tiles containing an image.
    """
    def __init__(self, tile_type):
        self.tile_image = pygame.image.load((os.path.join('assets', 'temp.png'))).convert()

        # Load appropriate image
        match tile_type.value:
            case TileType.DEFAULT.value:
                self.tile_image = pygame.image.load((os.path.join('assets', 'map', 'background_0.png'))).convert()

        if scale.scale:
            self.tile_image = pygame.transform.scale(self.tile_image,
                (scale.r1440(self.tile_image.get_width()),
                scale.r1440(self.tile_image.get_height())))
