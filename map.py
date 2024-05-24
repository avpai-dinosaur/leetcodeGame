import pygame
import utils

class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename, player_pos):
        super().__init__()
        self.image, self.rect = utils.load_png(filename)
    
    def draw(self, surface, camera_pos):
        screen_width, screen_height = surface.get_size()
        left = camera_pos.x - screen_width / 2
        top = camera_pos.y - screen_height / 2
        map_area = pygame.Rect((left, top), (screen_width, screen_height))
        surface.blit(self.image, (0, 0), area=map_area)