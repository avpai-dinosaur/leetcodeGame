import pygame
import utils
import constants as c
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path):
        """Constructor.

            path: List of Vector2 objects specifying path along 
                  which the enemy will walk.
        """
        super().__init__()
        self.health = 100
        self.speed = 1

        # Path following
        self.path = path
        self.pos = self.path[0].copy() # This NEEDS to be a copy to avoid modifying path!
        self.target_point = 1
        self.target = self.path[self.target_point]
        self.direction = 1

        # Image Stuff
        self.rect = pygame.Rect(self.pos[0], self.pos[0], 16 * 3, 16 * 3)
        self.rect.center = self.pos
        self.image = pygame.Surface((16 * 3, 16 * 3))
    
    def update(self):
        """Update function to run each game tick.
        
        Enemy should move randomly and reverse direction if it bounces off a wall.

            walls: list of pygame.Rects representing walls in the map.
        """
        self.move()
        self.rect.center = self.pos

    def move(self):
        """Move the enemy towards next target point.
        
        Enemy should reverse direction upon reaching either end of path.
        """
        movement = self.target - self.pos
        distance = movement.length()
        
        if distance >= self.speed:
            self.pos += movement.normalize() * self.speed
        else:
            if distance != 0:
                self.pos += movement.normalize() * distance
            if self.target_point == len(self.path) - 1 or self.target_point == 0:
                self.direction *= -1
            self.target_point += self.direction
            self.target = self.path[self.target_point]

    # def rotate(self):
    #     #use distance to calculate angle
    #     distance = self.target - self.pos
    #     self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
    #     self.image = pygame.transform.rotate(self.original_image, self.angle)
    #     self.rect = self.image.get_rect()
    #     self.rect.center = self.pos
    
    def draw(self, surface):
        pygame.draw.rect(surface, "green", self.rect)