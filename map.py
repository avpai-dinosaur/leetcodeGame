import pygame
import utils
import json

class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename, player_pos):
        super().__init__()
        self.image, self.rect = utils.load_png(filename)
        self.walls = [] # List of Rects
        self.load_json("data/map/map.tmj")
    
    def draw(self, surface, camera_pos):
        # screen_width, screen_height = surface.get_size()
        # left = camera_pos.x - screen_width / 2
        # top = camera_pos.y - screen_height / 2
        # map_area = pygame.Rect((left, top), (screen_width, screen_height))
        # surface.blit(self.image, (0, 0), area=map_area)
        surface.blit(self.image, (0, 0))
        # for wall in self.walls:
        #     pygame.draw.rect(surface, (0, 0, 0), wall)
    
    def load_json(self, filename):
        f = open(filename)
        map_data = json.load(f)
        wall_data = map_data["layers"][2]["objects"]
        for wall in wall_data:
            wall_rect = pygame.Rect((wall["x"], wall["y"]), (wall["width"], wall["height"]))
            self.walls.append(wall_rect)
        