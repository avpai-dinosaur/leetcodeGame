import pygame
import utils
import json

class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename):
        super().__init__()
        self.image, self.rect = utils.load_png(filename)
        self.walls = [] # List of Rects
        self.load_json("data/map/map.tmj")
    
    def draw(self, surface):
        surface.blit(self.image, (0, 0))
    
    def load_json(self, filename):
        f = open(filename)
        map_data = json.load(f)
        wall_data = map_data["layers"][2]["objects"]
        for wall in wall_data:
            wall_rect = pygame.Rect((wall["x"], wall["y"]), (wall["width"], wall["height"]))
            self.walls.append(wall_rect)
        