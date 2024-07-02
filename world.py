import pygame
import utils
from player import Player
from enemy import Enemy
from map import Map
import constants as c

class World():
    """Top level class to keep track of all game objects."""
   
    def __init__(self):
        self.player = Player("Oldhero.png", c.INIT_PLAYER_POS)
        self.enemies = pygame.sprite.Group()
        self.map = Map("data/images/map.png")
        for path in self.map.enemy_paths:
            self.enemies.add(Enemy("robot.png", path))
    
    def update(self):
        self.player.update(self.map.walls, self.map.laser_doors)
        self.enemies.update(self.player, self.map.walls)
        self.map.laser_doors.update(self.player)
        self.map.antidote_doors.update(self.player)
    
    def draw(self, surface):
        self.map.draw(surface)
        self.player.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)
        

