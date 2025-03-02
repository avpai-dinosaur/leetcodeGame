import pygame
import utils
import requests
from camera import Camera
from player import Player
from enemy import Enemy
from roomba import Roomba
from map import Map
from button import Button
import objects as o
import constants as c

class Level():
    """Represents a level in the game."""

    def __init__(self, map):
        self.map = map
        self.load_entities()

    def load_entities(self):
        self.player = Player("data/images/Oldhero.png", self.map.playerSpawn, {})
        self.roomba = Roomba("data/images/roomba.png", self.map.roombaPath)
        self.objects = self.map.object_factory()
        self.walls = self.map.walls_factory()
        self.doors = self.map.doors_factory()

    def load_camera(self, camera):
        camera.add(self.player)
        camera.add(self.roomba)
        camera.add(self.objects)
        camera.add(self.doors)
        # camera.background_objects.add(self.map.background_objects)

        camera.target = self.player.rect
        camera.background = self.map.image
    
    def reset(self, camera):
        self.load_entities()
        self.load_camera(camera)

    def end_level(self):
        pygame.event.post(pygame.event.Event(c.LEVEL_ENDED))
    
    def player_died(self):
        # TODO: the player should probably post this event
        pygame.event.post(pygame.event.Event(c.PLAYER_DIED))

    def update(self):
        self.player.update(self.walls, self.doors)
        self.roomba.update(self.player)
        self.doors.update(self.player)
        self.objects.update(self.player)
        # self.map.background_objects.update(self.player)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.end_level()
            # TODO: This is just for testing purposes
            if event.key == pygame.K_v:
                self.player_died()


class Game():
    """Manages high-level gameplay logic like switching between levels and camera functions."""
   
    def __init__(self, manager, playerStats):
        self.manager = manager
        self.camera = Camera()
        self.levels = [
            Level(Map("data/images/atticusMap.png", "data/map/atticusMap.tmj")),
            Level(Map("data/images/atticusMap.png", "data/map/atticusMap.tmj"))
        ]
        self.level = 0
        self.levels[self.level].load_camera(self.camera)

    def update(self):
        self.levels[self.level].update()
        self.camera.update()
    
    def next_level(self):
        if self.level == len(self.levels) - 1:
            self.manager.set_state("menu")
        else:
            self.level += 1
            self.levels[self.level].load_camera(self.camera)

    def handle_event(self, event):
        self.levels[self.level].handle_event(event)
        self.camera.handle_event(event)

        if event.type == c.LEVEL_ENDED:
            self.camera.reset()
            self.next_level()
        elif event.type == c.PLAYER_DIED:
            self.camera.reset()
            self.levels[self.level].reset(self.camera)
            self.manager.set_state("died")

    def draw(self, surface):
        self.camera.draw(surface)
