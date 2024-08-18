import pygame
import utils
import json
import queue
import objects as o
import constants as c

class Edge():
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight

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
            Edge(nodeid - c.MAP_WIDTH - 1, 1.4), 
            Edge(nodeid - c.MAP_WIDTH + 1, 1.4), 
            Edge(nodeid - c.MAP_WIDTH, 1), 
            Edge(nodeid + c.MAP_WIDTH, 1), 
            Edge(nodeid + c.MAP_WIDTH + 1, 1.4),
            Edge(nodeid + c.MAP_WIDTH - 1, 1.4),
            Edge(nodeid - 1, 1),
            Edge(nodeid + 1, 1)
        ] # walkable tiles are never on the edge
        for n in neighbors:
            if data[n.id] in c.WALKABLE_TILES:
                self.adj_list[nodeid].append(n)
    
    def dijkstra(self, src, dest):
        """Run dijkstras on graph, stopping when path to dest is found."""
        def next_node(tovisit, dist):
            min_node = tovisit[0]
            min_dist = dist[min_node] 
            for node in tovisit:
                if dist[node] < min_dist:
                    min_dist = dist[node]
                    min_node = node
            return min_node
        
        tovisit = []
        dist = {}
        prev = {}
        for k in self.adj_list.keys():
            if k == src:
                dist[k] = 0
            else:
                dist[k] = float('inf')
            prev[k] = None
            tovisit.append(k)
        
        while len(tovisit) > 0:
            node = next_node(tovisit, dist)
            if node == dest:
                break
            tovisit.remove(node)
            for neighbor in self.adj_list[node]:
                if neighbor.id in tovisit:
                    alt = dist[node] + neighbor.weight
                    if alt < dist[neighbor.id]:
                        dist[neighbor.id] = alt
                        prev[neighbor.id] = node
        return dist, prev

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
            break
        for door in laser_door_data:
            door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
            self.laser_doors.add(o.LaserDoor(door_rect))
        for door in antidote_door_data:
            door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
            self.antidote_doors.add(o.AntidoteDoor(door_rect, 10))
        for wall in wall_data:
            wall_rect = pygame.Rect((wall["x"], wall["y"]), (wall["width"], wall["height"]))
            self.walls.append(wall_rect)
        