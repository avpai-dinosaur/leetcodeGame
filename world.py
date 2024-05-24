import pygame
import utils
from player import Player
from map import Map
import constants as c

class World():
    """Top level class to keep track of all game objects."""

    def __init__(self, screen):
        self.player = Player("data/images/dude.png", c.INIT_PLAYER_POS)
        self.map = Map("data/images/map.png", c.INIT_PLAYER_POS)
        self.camera_pos = pygame.Vector2(
            screen.get_width() / 2,
            screen.get_height() / 2
        )
    
    def update(self):
        self.player.update()
        self.camera_pos = self.player.pos
    
    def draw(self, surface):
        self.map.draw(surface, self.camera_pos)
        self.player.draw(surface)