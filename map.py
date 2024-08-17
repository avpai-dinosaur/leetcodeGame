import pygame
import utils
import json
import objects as o
import constants as c

class Graph():
    """Represents a graph. Used to model where sprites can move on map."""
    
    def __init__(self):
        self.adj_list = {}

    def populate(self, data):
        for i in range(len(data)):
            if data[i] in c.WALKABLE_TILES:
                self.add_node(i, data)

    def add_node(self, nodeid, data):
        self.adj_list[nodeid] = []
        neighbors = [
            nodeid - c.MAP_WIDTH, nodeid + c.MAP_WIDTH,
            nodeid - 1, nodeid + 1
        ] # walkable tiles are never on the edge
        for n in neighbors:
            if data[n] in c.WALKABLE_TILES:
                self.adj_list[nodeid].append(n)

class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename):
        super().__init__()
        self.image, self.rect = utils.load_png(filename)
        self.walls = [] # List of Rects
        self.enemy_paths = [] # List of polylines
        self.laser_doors = pygame.sprite.Group()
        self.antidote_doors = pygame.sprite.Group()
        self.graph = Graph()
        self.load_json("data/map/map.tmj")
    
    def draw(self, surface, offset):
        surface.blit(self.image, offset)
    
    def load_json(self, filename):
        """Load all JSON data for the map."""

        f = open(filename)
        map_data = json.load(f)
        room_data = map_data["layers"][0]["data"]
        wall_data = map_data["layers"][4]["objects"]
        enemy_path_data = map_data["layers"][5]["objects"]
        laser_door_data = map_data["layers"][1]["objects"]
        antidote_door_data = map_data["layers"][2]["objects"]
        self.graph.populate(room_data)
        for path in enemy_path_data:
            self.enemy_paths.append(
                [pygame.Vector2(datum.get("x") + path["x"], datum.get("y") + path["y"]) for datum in path["polyline"]]
            )
        for door in laser_door_data:
            door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
            self.laser_doors.add(o.LaserDoor(door_rect))
        for door in antidote_door_data:
            door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
            self.antidote_doors.add(o.AntidoteDoor(door_rect, 10))
        for wall in wall_data:
            wall_rect = pygame.Rect((wall["x"], wall["y"]), (wall["width"], wall["height"]))
            self.walls.append(wall_rect)
        