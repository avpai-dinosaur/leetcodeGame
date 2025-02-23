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


class World():
    """Top level class to keep track of all game objects."""
   
    def __init__(self, manager, screen, playerStats):
        self.manager = manager
        self.screen = screen
        self.map = Map("data/images/atticusMap.png")
        self.player = Player("data/images/Oldhero.png", self.map.player_spawn, playerStats)
        self.roomba = Roomba("data/images/roomba.png", self.map.roomba_path)
        self.enemies = pygame.sprite.Group()
        self.level = 1
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        
        self.camera = Camera(screen, self.map.image, self.bullets, self.player.rect)
        self.camera.add(self.player)
        [self.camera.add(laser_door) for laser_door in self.map.laser_doors]
        [self.camera.add(computer) for computer in self.map.computers]
        self.camera.add(self.roomba)
        self.camera.add(self.enemies)
        self.camera.foreground_objects.add(self.map.static_objects)
        self.camera.background_objects.add(self.map.background_objects)
    
    def spawn_enemies(self):
        [self.enemies.add(Enemy("data/images/robot.png", self.map.enemy_spawn[i])) for i in range(self.level * 5)]
        self.camera.add(self.enemies)

    def update(self):
        self.player.update(self.map.walls, self.map.laser_doors)
        self.enemies.update(self.player, self.bullets, self.map)
        self.roomba.update(self.player)
        self.bullets.update(self.map.walls)
        self.map.laser_doors.update(self.player)
        self.map.computers.update(self.player)
        self.camera.update(self.player.rect)

        self.map.static_objects.update(self.player, self.camera)
        self.map.background_objects.update(self.player, self.camera)

        mouse = pygame.mouse.get_pressed()
        if mouse[0] and pygame.time.get_ticks() - self.last_shot > 200:
            self.last_shot = pygame.time.get_ticks()
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            center_pos = pygame.Vector2(self.camera.half_w, self.camera.half_h)
            direction = (mouse_pos - center_pos).normalize()
            self.bullets.add(o.Bullet(self.player.pos, 10, direction, 200))
    
    def handle_event(self, event):
        pass

    def draw(self, surface):
        self.camera.draw(self.player.rect, surface)
