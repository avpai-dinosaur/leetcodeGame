import pygame
import utils
from tileset import TileSet
from player import Player
from enemy import Enemy
from map import Map
import constants as c

class Camera(pygame.sprite.Group):
    """Represents the world's camera"""

    def __init__(self):
        super().__init__()

    def draw(self, surface):
        for sprite in sorted(self.sprites(), key=lambda s : s.rect.centery):
            sprite.draw(surface)

class World():
    """Top level class to keep track of all game objects."""

    def __init__(self):
        TileSet() # have to wait to initialize here b/c dependencies on pygame.display
        self.camera = Camera()
        self.player = Player("Oldhero.png", c.INIT_PLAYER_POS)
        self.enemies = pygame.sprite.Group()
        self.map = Map("data/images/outer_world.png", self.camera)
        for path in self.map.enemy_paths:
            self.enemies.add(Enemy("robot.png", path))
        
        self.camera.add(self.player)
    
    def update(self):
        self.player.update(self.map.walls, self.map.laser_doors)
        self.map.rooms.update(self.player)
        # self.enemies.update(self.player, self.map.walls)
        # self.map.laser_doors.update(self.player)
        # self.map.antidote_doors.update(self.player)
    
    def draw(self, surface):
        self.map.draw(surface)
        self.camera.draw(surface)
        #self.player.draw(surface)
        # for enemy in self.enemies:
        #     enemy.draw(surface)
