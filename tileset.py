import pygame
import utils
import constants as c

class TileSet:
    """Class to parse tiles out of the tileset for convenience."""
    PIN_PAD_RED = None
    PIN_PAD_GREEN = None

    def __init__(self):
        """Constructor.
        
        filename: png file for the tileset
        """
        self.image, _ = utils.load_png("data/images/tileset.png")
        TileSet.PIN_PAD_RED = self.parse_tile(4, 6)
        TileSet.PIN_PAD_GREEN = self.parse_tile(4, 7)

    def parse_tile(self, row, col):
        """Grabs an individual frame from the spritesheet.
        
            row, col: the row and column of the image in the spritsheet
        """
        image = pygame.Surface((c.TILE_SIZE, c.TILE_SIZE)).convert_alpha()
        image.blit(
            self.image,
            (0,0),
            ((col * c.TILE_SIZE), (row * c.TILE_SIZE), c.TILE_SIZE, c.TILE_SIZE)
        )
        image.set_colorkey((0,0,0))
        return image