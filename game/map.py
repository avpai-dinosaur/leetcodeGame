import pygame
import utils
import json
import queue
import objects as o
import constants as c
import random

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
        tovisit = []
        pq = queue.PriorityQueue()
        dist = {}
        prev = {}
        for k in self.adj_list.keys():
            if k == src:
                dist[k] = 0
            else:
                dist[k] = float('inf')
            prev[k] = None
            tovisit.append(k)
        pq.put((dist[src], src))
        
        while not pq.empty():
            _, node = pq.get()
            if node not in tovisit:
                continue
            if node == dest:
                break
            tovisit.remove(node)
            for neighbor in self.adj_list[node]:
                if neighbor.id in tovisit:
                    alt = dist[node] + neighbor.weight
                    if alt < dist[neighbor.id]:
                        dist[neighbor.id] = alt
                        prev[neighbor.id] = node
                        pq.put((dist[neighbor.id], neighbor.id))
        return dist, prev

class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename):
        super().__init__()
        self.image, self.rect = utils.load_png(filename)
        self.walls = [] # List of Rects
        self.enemy_spawn = None
        self.player_spawn = None
        self.laser_doors = pygame.sprite.Group()
        self.antidote_doors = pygame.sprite.Group()
        self.graph = Graph()
        self.load_json("data/map/brickMap.tmj")
    
    def draw(self, surface, offset):
        surface.blit(self.image, offset)
    
    def load_json(self, filename):
        """Load all JSON data for the map."""

        f = open(filename)
        map_data = json.load(f)
        layers = map_data["layers"]
        rooms = layers[0]["data"]
        walls = layers[2]["objects"]
        laser_doors = layers[3]["objects"]
        player_spawn = layers[4]["objects"][0]
        self.player_spawn = (player_spawn["x"], player_spawn["y"])
        for wall in walls:
            wall_rect = pygame.Rect((wall["x"], wall["y"]), (wall["width"], wall["height"]))
            self.walls.append(wall_rect)
        for door in laser_doors:
            door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
            self.laser_doors.add(o.LaserDoor(door_rect))
        