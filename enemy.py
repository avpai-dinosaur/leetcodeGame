import pygame
import utils
import constants as c
import objects as o
import random
import math
from spritesheet import SpriteSheet

class Enemy(pygame.sprite.Sprite):
    """Represents an enemy."""

    def __init__(self, image, path):
        """Constructor.

            path: List of Vector2 objects specifying path along 
                  which the enemy will walk.
            image: enemy sprite PNG file.
        """
        super().__init__()

        # Animation Variables
        self.spritesheet = SpriteSheet(image, c.ENEMY_SHEET_METADATA)
        self.action = "walk"
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.cooldown = 100
        
        # Image variables
        self.image = self.spritesheet.get_image(self.action, self.current_frame)
        self.rect = self.image.get_rect()
        self.face_left = True

        # Path following
        self.path = path
        self.pos = self.path[0].copy() # This NEEDS to be a copy to avoid modifying path!
        self.rect.center = self.pos
        self.target_point = 1
        self.target = self.path[self.target_point]
        self.direction = 1

        # Enemy characteristics
        self.health = o.HealthBar(self.rect.left, self.rect.top, 60, 10, 100)
        self.speed = 0.5
    
    def update(self, player):
        """Update function to run each game tick.
        
        Enemy should move randomly and reverse direction if it bounces off a wall.

            walls: list of pygame.Rects representing walls in the map.
        """
        self.move()

        if pygame.Rect.colliderect(player.rect, self.rect) and player.action == "punch":
            self.health.lose(10)
            if self.health.hp <= 0:
                self.kill()


        # Update the animation
        current_time = pygame.time.get_ticks()
        if(current_time - self.last_update >= self.cooldown):
            #if animation cooldown has passed between last update and current time, switch frame
            self.current_frame += 1
            self.last_update = current_time
            
            #reset frame back to 0 so it doesn't index out of bounds
            if(self.current_frame >= self.spritesheet.num_frames(self.action)):
                self.current_frame = 0
            
            self.image = pygame.transform.flip(
                self.spritesheet.get_image(self.action, self.current_frame), 
                self.face_left,
                False
            )

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
                self.face_left = not self.face_left
            self.target_point += self.direction
            self.target = self.path[self.target_point]
        
        self.rect.center = self.pos
        self.health.update(self.rect.left - 10, self.rect.top - 15)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.health.draw(surface)
