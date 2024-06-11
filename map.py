import pygame
import utils
import json
import objects as o

class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename):
        super().__init__()
        self.image, self.rect = utils.load_png(filename)
        self.walls = [] # List of Rects
        self.laser_doors = pygame.sprite.Group()
        self.antidote_doors = pygame.sprite.Group()
        self.load_json("data/map/map.tmj")
    
    def draw(self, surface):
        surface.blit(self.image, (0, 0))
        for door in self.laser_doors:
            door.draw(surface)
        for door in self.antidote_doors:
            door.draw(surface)
    
    def load_json(self, filename):
        f = open(filename)
        map_data = json.load(f)
        wall_data = map_data["layers"][4]["objects"]
        laser_door_data = map_data["layers"][1]["objects"]
        antidote_door_data = map_data["layers"][2]["objects"]
        for door in laser_door_data:
            door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
            self.laser_doors.add(o.LaserDoor(door_rect))
        for door in antidote_door_data:
            door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
            self.antidote_doors.add(o.AntidoteDoor(door_rect, 10))
        for wall in wall_data:
            wall_rect = pygame.Rect((wall["x"], wall["y"]), (wall["width"], wall["height"]))
            self.walls.append(wall_rect)
        