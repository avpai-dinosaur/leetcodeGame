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
        self.tech_note_spawn = None
        self.laser_doors = pygame.sprite.Group()
        self.static_objects = pygame.sprite.Group()
        self.background_objects = pygame.sprite.Group()
        self.roomba_path = []
        self.computers = pygame.sprite.Group()
        self.graph = Graph()
        self.load_json("data/map/atticusMap.tmj")
    
    def draw(self, surface, offset):
        surface.blit(self.image, offset)
    
    def load_json(self, filename):
        """Load all JSON data for the map."""

        f = open(filename)
        map_data = json.load(f)
        layers = map_data["layers"]
        walls = layers[3]["objects"]
        laser_doors = layers[4]["objects"]
        player_spawn = layers[5]["objects"][0]
        roomba_path_data = layers[6]["objects"][0]
        dance_floor_spawn = layers[7]["objects"][0]
        computers = layers[8]["objects"]
        problems = layers[9]["objects"]

        self.player_spawn = (player_spawn["x"], player_spawn["y"])
        # self.tech_note_spawn = (tech_note_spawn["x"], tech_note_spawn["y"])
        self.background_objects.add(o.DanceFloor((dance_floor_spawn["x"], dance_floor_spawn["y"])))
       
        for wall in walls:
            wall_rect = pygame.Rect((wall["x"], wall["y"]), (wall["width"], wall["height"]))
            self.walls.append(wall_rect)
        for i, door in enumerate(laser_doors):
            door_rect = pygame.Rect((door["x"], door["y"]), (door["width"], door["height"]))
            self.laser_doors.add(o.LaserDoor(door_rect))
        for point in roomba_path_data["polyline"]:
            self.roomba_path.append(
                pygame.Vector2(point.get("x") + roomba_path_data["x"], point.get("y") + roomba_path_data["y"])
            )
        
        msg_text = [
"User: Bill\n\
Mateo:\n\
    Just patched a bug in the guidance system. If this thing had launched, we'd be aiming for the Sun right now.\n\
You:\n\
    Hahahaha...I'm scared.",
"User: Mateo\n\
Alice:\n\
    I don't think Aakash looks so good?\n\
You:\n\
    *side-eye* maybe I'll check on him after the office party...",
"User: Jinyan\n\
Status Update:\n\
    They let me design the rocket's warnings dashboard.\n\
    Druck asked for it to look 'more like Fakebook.'\n\
    Now it has infinite scroll. God help us.",
"User: Alice\n\
Fakebook post:\n\
    Feeling beyond blessed to be part of this once-in-a-lifetime mission to Mars with Druck Dripersburg\n\
    Never imagined I'd be delivering agile, scalable, integrated solutions in zero gravity!\n",
"User: Chuck\n\
Fakebook post:\n\
    Bro, imagine Mars but with AI-powered DAO governance.\n\
    No governments, just vibes.\n\
    We are literally disrupting planets right now. WAGMI."
        ]
        
        for i, computer in enumerate(computers):
            computer_rect = pygame.Rect((computer["x"], computer["y"]), (computer["width"], computer["height"]))
            self.computers.add(o.Computer(computer_rect, msg_text[i]))
        
        for problem in problems:
            problem_rect = pygame.Rect((problem["x"], problem["y"]), (problem["width"], problem["height"]))
            text = "User: Aakash\n\
Dev Note (3/9/2100):\n\
Our stupid spaceship door is breaking again.\n\
Druck says I need to solve (1. TwoSum) to get it working.\n\
I tried going through all pairs of numbers, but that took too long...\n\
Ugh, guess I'll be staying late. Again."
            problem_computer = o.ProblemComputer(
                problem_rect,
                text,
                "https://leetcode.com/problems/two-sum/description/")
            self.computers.add(problem_computer)
            self.laser_doors.sprites()[0].problems.add(problem_computer)
        
