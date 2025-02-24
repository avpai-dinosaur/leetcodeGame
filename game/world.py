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

    def __init__(self, game, camera, map):
        self.game = game
        self.camera = camera
        self.map = map
        self.player = Player("data/images/Oldhero.png", self.map.player_spawn, {})
        self.roomba = Roomba("data/images/roomba.png", self.map.roomba_path)
        self.npcs = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()

        self.camera.add(self.player)
        [self.camera.add(laser_door) for laser_door in self.map.laser_doors]
        [self.camera.add(computer) for computer in self.map.computers]
        self.camera.add(self.roomba)
        self.camera.foreground_objects.add(self.map.static_objects)
        self.camera.background_objects.add(self.map.background_objects)

        self.camera.target = self.player.rect
        self.camera.background = self.map.image

    def add_npcs(self):
        pass

    def add_objects(self):
        pass

    def end_level(self):
        self.game.next_level()

    def update(self):
        self.player.update(self.map.walls, self.map.laser_doors)
        self.roomba.update(self.player)
        self.npcs.update(self.player)
        self.map.laser_doors.update(self.player)
        self.map.computers.update(self.player)
        self.map.static_objects.update(self.player, self.camera)
        self.map.background_objects.update(self.player, self.camera)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.end_level()


class Game():
    """Manages high-level gameplay logic like switching between levels and camera functions."""
   
    def __init__(self, manager, playerStats):
        self.manager = manager
        self.camera = Camera()
        self.levels = [
            Level(self, self.camera, Map("data/images/atticusMap.png"))
        ]
        self.level = 0

    def update(self):
        self.levels[self.level].update()
        self.camera.update()
    
    def next_level(self):
        if self.level == len(self.levels) - 1:
            self.manager.set_state("menu")
        else:
            self.level += 1

    def handle_event(self, event):
        self.levels[self.level].handle_event(event)
        self.camera.handle_event(event)

    def draw(self, surface):
        self.camera.draw(surface)
