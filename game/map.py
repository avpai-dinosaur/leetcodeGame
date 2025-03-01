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

class Map():
    """Parses exported map data from Tiled."""

    def __init__(self, imageFile, dataFile):
        """Constructor.
        
            imageFile: background of the map in .png format
            dataFile: map data exported from Tiled in .json format
        """
        self.image, _ = utils.load_png(imageFile)
        self.graph = Graph()
        self.walls = {}
        self.laserDoors = {}
        self.computers = {}
        self.generatedComputers = {}
        self.objects = {}
        self.playerSpawn = None
        self.roombaPath = []

        self.load_json(dataFile)
        self.parse_objects()


    def load_json(self, filename):
        """Load JSON data for the map."""
        f = open(filename)
        self.raw_json = json.load(f)
        layers = self.raw_json["layers"]
        for layer in layers:
            if layer["name"] == "walls":
                self.walls = layer
            elif layer["name"] == "objects":
                self.objects = layer
            elif layer["name"] == "playerSpawn":
                self.playerSpawn = (
                    layer["objects"][0]["x"],
                    layer["objects"][0]["y"]
                )
            elif layer["name"] == "roombaPath":
                roomba_path_data = layer["objects"][0]

        for point in roomba_path_data["polyline"]:
            self.roombaPath.append(
                pygame.Vector2(point.get("x") + roomba_path_data["x"], point.get("y") + roomba_path_data["y"])
            )
    
    def parse_object(object, internalDict):
        """Parse an object into the internal dictionary."""

        id = object["id"]
        internalDict[id] = {
            "width": object["width"],
            "height": object["height"],
            "x": object["x"],
            "y": object["y"]
        }
        if "properties" in object.keys():
            for property in object["properties"]:
                internalDict[id][property["name"]] = property["value"]
    
    def parse_objects(self):
        """Parse the objects layer of the JSON data."""

        for object in self.objects["objects"]:
            if object["type"] == "Computer":
                Map.parse_object(object, self.computers)
            elif object["type"] == "LaserDoor":
                Map.parse_object(object, self.laserDoors)
    
    def walls_factory(self):
        """Generates the walls for this map as a list of rects."""
        startX = self.walls["x"]
        startY = self.walls["y"]
        wallRects = []
        for wall in self.walls["objects"]:
            wallRects.append(
                pygame.Rect(
                    (startX + wall["x"], startY + wall["y"]),
                    (wall["width"], wall["height"])
                )
            )
        return wallRects

    def computer_factory(self, computer, id, startX, startY):
        """Generates a computer from an entry in the internal computer dict."""
        generatedComputer = None
        if "hasProblem" in computer.keys() and computer["hasProblem"]:
            generatedComputer = o.ProblemComputer(
                pygame.Rect(
                    startX + computer["x"],
                    startY + computer["y"],
                    computer["width"],
                    computer["height"]
                ),
                computer["note"],
                computer["problemUrl"]
            ) 
        else:
            generatedComputer = o.Computer(
                pygame.Rect(
                    startX + computer["x"],
                    startY + computer["y"],
                    computer["width"],
                    computer["height"]
                ),
                computer["note"] if "note" in computer.keys() else "TODO"
            )
        self.generatedComputers[id] = generatedComputer
        return generatedComputer

    def laser_door_factory(self, laserDoor, startX, startY):
        """Generates a laser door from an entry in the internal laser door dict."""
        door = o.LaserDoor(
            pygame.Rect(
                startX + laserDoor["x"],
                startY + laserDoor["y"],
                laserDoor["width"],
                laserDoor["height"]
            )
        )
        if "brokenComputer" in laserDoor.keys():
            computerId = laserDoor["brokenComputer"]
            door.problems.add(self.generatedComputers[computerId])
        return door
              
    def object_factory(self):
        """Get the objects for this map as a sprite group."""
        startX = self.objects["x"]
        startY = self.objects["y"]
        objectGroup = pygame.sprite.Group()
        for object in self.objects["objects"]:
            if object["type"] == "Computer":
                computer = self.computers[object["id"]]
                objectGroup.add(self.computer_factory(computer, object["id"], startX, startY))
            elif object["type"] == "DanceFloor":
                objectGroup.add(
                    o.DanceFloor((startX + object["x"], startY + object["y"]))
                )
        
        # Second pass for objects which need dependency injection
        for object in self.objects["objects"]:
            if object["type"] == "LaserDoor":
                laserDoor = self.laserDoors[object["id"]]
                objectGroup.add(self.laser_door_factory(laserDoor, startX, startY))
        
        return objectGroup

    def draw(self, surface, offset):
        """Draw map background to surface."""
        surface.blit(self.image, offset)







#         msg_text = [
# "User: Bill\n\
# Mateo:\n\
#     Just patched a bug in the guidance system. If this thing had launched, we'd be aiming for the Sun right now.\n\
# You:\n\
#     Hahahaha...I'm scared.",
# "User: Mateo\n\
# Alice:\n\
#     I don't think Aakash looks so good?\n\
# You:\n\
#     *side-eye* maybe I'll check on him after the office party...",
# "User: Jinyan\n\
# Status Update:\n\
#     They let me design the rocket's warnings dashboard.\n\
#     Druck asked for it to look 'more like Fakebook.'\n\
#     Now it has infinite scroll. God help us.",
# "User: Alice\n\
# Fakebook post:\n\
#     Feeling beyond blessed to be part of this once-in-a-lifetime mission to Mars with Druck Dripersburg\n\
#     Never imagined I'd be delivering agile, scalable, integrated solutions in zero gravity!\n",
# "User: Chuck\n\
# Fakebook post:\n\
#     Bro, imagine Mars but with AI-powered DAO governance.\n\
#     No governments, just vibes.\n\
#     We are literally disrupting planets right now. WAGMI."
#         ]