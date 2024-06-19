import pygame
import utils
import constants as c
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        """Constructor.

            pos: tuple representing enemy's inital position
        """
        super().__init__()
        self.health = 100
        self.speed = 0.01
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(pos[0], pos[0], 16 * 3, 16 * 3)
    
    def update(self, walls):
        """Update function to run each game tick.
        
        Enemy should move randomly and reverse direction if it bounces off a wall.

            walls: list of pygame.Rects representing walls in the map.
        """
        new_pos = self.pos
        x_dir = random.randint(-1, 1)
        y_dir = random.randint(-1, 1)
        new_pos.x = self.pos.x + 300 * self.speed * x_dir
        new_pos.y = self.pos.y + 300 * self.speed * y_dir

        # tentatively update to the new position
        # might have to undo if it turns out new position
        # collides with a barrier
        self.rect.center = new_pos

        # check if the proposed position collides with walls
        for wall in walls:
            if pygame.Rect.colliderect(wall, self.rect):
                # dont update the position
                self.rect.center = self.pos
                return

    
    def draw(self, surface):
        pygame.draw.rect(surface, "green", self.rect)