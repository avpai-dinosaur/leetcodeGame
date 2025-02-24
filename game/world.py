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

    def __init__(self):
        self.map = Map("level file image")
        self.player = Player() # spawn the player again for a new level


class World():
    """Top level class to keep track of all game objects."""
   
    def __init__(self, manager, playerStats):
        self.manager = manager
        self.map = Map("data/images/atticusMap.png")
        self.player = Player("data/images/Oldhero.png", self.map.player_spawn, playerStats)
        self.roomba = Roomba("data/images/roomba.png", self.map.roomba_path)
        self.level = 1
        
        self.camera = Camera(self.map.image, self.player.rect)
        self.camera.add(self.player)
        [self.camera.add(laser_door) for laser_door in self.map.laser_doors]
        [self.camera.add(computer) for computer in self.map.computers]
        self.camera.add(self.roomba)
        self.camera.foreground_objects.add(self.map.static_objects)
        self.camera.background_objects.add(self.map.background_objects)

    def update(self):
        self.player.update(self.map.walls, self.map.laser_doors)
        self.roomba.update(self.player)
        self.map.laser_doors.update(self.player)
        self.map.computers.update(self.player)
        self.camera.update()

        self.map.static_objects.update(self.player, self.camera)
        self.map.background_objects.update(self.player, self.camera)
    
    def handle_event(self, event):
        self.camera.handle_event(event)

    def draw(self, surface):
        self.camera.draw(surface)
