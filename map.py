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
        self.enemy_paths = [] # List of polylines
        self.rooms = pygame.sprite.Group()
        self.laser_doors = pygame.sprite.Group()
        self.antidote_doors = pygame.sprite.Group()
        self.load_json(f"data/map/outer_world.tmj")
    
    def draw(self, surface):
        surface.blit(self.image, (0, 0))
        for room in self.rooms:
            room.draw(surface)
        for door in self.laser_doors:
            door.draw(surface)
        for door in self.antidote_doors:
            door.draw(surface)
    
    def load_json(self, filename):
        """Load all JSON data for the map."""

        f = open(filename)
        map_data = json.load(f)
        wall_data = map_data["layers"][3]["objects"]
        room_data = map_data["layers"][4]["objects"]

        # enemy_path_data = map_data["layers"][5]["objects"]
        # laser_door_data = map_data["layers"][1]["objects"]
        # antidote_door_data = map_data["layers"][2]["objects"]
        # for path in enemy_path_data:
        #     self.enemy_paths.append(
        #         [pygame.Vector2(datum.get("x") + path["x"], datum.get("y") + path["y"]) for datum in path["polyline"]]
        #     )
        # for door in laser_door_data:
        #     door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
        #     self.laser_doors.add(o.LaserDoor(door_rect))
        # for door in antidote_door_data:
        #     door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
        #     self.antidote_doors.add(o.AntidoteDoor(door_rect, 10))
        
        for wall in wall_data:
            wall_rect = pygame.Rect(
                (wall["x"], wall["y"]),
                (wall["width"], wall["height"])
            )
            self.walls.append(wall_rect)
        
        for room in room_data:
            self.rooms.add(
                o.Room("data/images/small_room.png",
                pygame.Vector2(room["x"], room["y"]))
            )
        