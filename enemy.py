import pygame
import utils
import constants as c
import objects as o
import random
import math
from spritesheet import SpriteSheet
from enum import Enum

class Enemy(pygame.sprite.Sprite):
    """Represents an enemy."""

    class MoveState(Enum):
        """State of the enemy's movement."""
        PATH = 0
        CHASE = 1
        RECOVER = 2

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
        self.face_right = True

        # Path following
        self.path = path
        self.pos = self.path[0].copy() # This NEEDS to be a copy to avoid modifying path!
        self.rect.center = self.pos
        self.target_point = 1
        self.target = self.path[self.target_point]
        self.direction = 1

        self.move_state = Enemy.MoveState.PATH
        self.radius = 50

        # Enemy characteristics
        self.health = o.EnemyHealthBar(self.rect.left, self.rect.top, 60, 10, 100)
        self.speed = c.ENEMY_SPEED
    
    def update(self, player, walls):
        """Update function to run each game tick.
        
        Enemy should move randomly and reverse direction if it bounces off a wall.

            walls: list of pygame.Rects representing walls in the map.
        """
        if self.move_state == Enemy.MoveState.PATH:
            self.pathmove(walls)
        elif self.move_state == Enemy.MoveState.CHASE:
            self.chasemove(player, walls)
        else:
            self.recovermove(walls)

        if pygame.sprite.collide_circle(player, self):
            self.move_state = Enemy.MoveState.CHASE
            self.speed = c.ENEMY_CHASE_SPEED
        else:
            if self.move_state == Enemy.MoveState.CHASE:
                self.move_state = Enemy.MoveState.RECOVER
                self.speed = c.ENEMY_SPEED
        
        # receive hits from player
        if pygame.Rect.colliderect(player.rect, self.rect) and player.action == "punch":
            self.health.lose(10)
            if self.health.hp <= 0:
                self.kill()
        
        self.update_animation()

    def update_animation(self):
        """Update animation of enemy."""
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
                self.face_right,
                False
            )

    def pathmove(self, walls):
        """Move the enemy towards next path point.
        
        Enemy should reverse direction upon reaching either end of path.
        """
        if self.move(self.target, walls):
            if self.target_point == len(self.path) - 1 or self.target_point == 0:
                self.direction *= -1
                self.face_right = not self.face_right
            self.target_point += self.direction
            self.target = self.path[self.target_point]
    
    def chasemove(self, player, walls):
        """Chase the player."""
        self.move(player.pos, walls)
    
    def recovermove(self, walls):
        """Recover back to patrol."""
        if self.move(self.target, walls):
            self.move_state = Enemy.MoveState.PATH

    def move(self, target, walls):
        """Move enemy to the target point.

        Returns true if target was reached.
        
            target: Vector2.
        """
        old_pos = self.pos
        reached = False
        movement = target - self.pos
        distance = movement.length()

        if movement[0] < 0:
            self.face_right = False
        elif movement[0] == 0:
            pass
        else:
            self.face_right = True

        if distance >= self.speed:
            self.pos += movement.normalize() * self.speed
        else:
            if distance != 0:
                self.pos += movement.normalize() * distance
            reached = True
        
        self.rect.center = self.pos
        if self.rect.collidelist(walls):
            self.rect.center = old_pos
            self.pos = old_pos
            
        self.health.update(self.rect.left - 10, self.rect.top - 15)
        return reached

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.health.draw(surface)
