import pygame
import utils
from player import Player
from enemy import Enemy
from map import Map
import constants as c

class World():
    """Top level class to keep track of all game objects."""
   
    def __init__(self, screen):
        self.player = Player("Oldhero.png", c.INIT_PLAYER_POS)
        self.enemy = Enemy((100, 100), "robot.png")
        self.map = Map("data/images/map.png")
    
    def update(self):
        self.player.update(self.map.walls, self.map.laser_doors)
        self.enemy.update(self.map.walls)
        self.map.laser_doors.update(self.player)
        self.map.antidote_doors.update(self.player)
    
    def draw(self, surface):
        self.map.draw(surface)
        self.player.draw(surface)
        self.enemy.draw(surface)
        

