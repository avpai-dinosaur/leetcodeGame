import pygame
import utils
import constants as c
import objects as o
import random
import math
from spritesheet import SpriteSheet

class Enemy(pygame.sprite.Sprite):
    """Represents an enemy."""

    def __init__(self, image, pos):
        """Constructor.

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
        self.path = [] # list of Vector2 objects specifying path for enemy to follow
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos
        self.direction = 1
        self.search = True

        # Enemy characteristics
        self.health = o.EnemyHealthBar(self.rect.left, self.rect.top, 60, 10, 100)
        self.melee_lose_cooldown = 200
        self.last_melee_hit = pygame.time.get_ticks()
        self.speed = c.ENEMY_SPEED

    def get_path(self, route):
        path = []
        for node in route:
            row = node // c.MAP_WIDTH
            col = node - row * c.MAP_WIDTH
            coord = pygame.Vector2(col * c.TILE_SIZE + c.TILE_SIZE / 2, row * c.TILE_SIZE + c.TILE_SIZE / 2)
            path.append(coord)
        return path

    def update_path(self, player, map):
        tile_y = int(self.pos.y // c.TILE_SIZE)
        tile_x = int(self.pos.x // c.TILE_SIZE)
        my_node = tile_y * c.MAP_WIDTH + tile_x
     
        target_node = int(player.pos.y // c.TILE_SIZE) * c.MAP_WIDTH + int(player.pos.x // c.TILE_SIZE)
        dist, prev = map.graph.dijkstra(my_node, target_node)

        route = []
        node = target_node
        while node:
            route.append(node)
            node = prev[node]
        self.path = self.get_path(route)
        self.search = False

    def update(self, player, bullets, map):
        """Update function to run each game tick.
        
        Enemy should move towards player using djikstra's.

            walls: list of pygame.Rects representing walls in the map.
        """
        
        if self.search:
            self.update_path(player, map)
        if self.move(self.path[-2] if len(self.path) > 1 else self.path[0], []):
            self.search = True
        
        # receive hits from player
        if pygame.Rect.colliderect(player.rect, self.rect) and player.action == "punch":
            if pygame.time.get_ticks() - self.last_melee_hit > self.melee_lose_cooldown:
                self.last_melee_hit = pygame.time.get_ticks()
                self.health.lose(2)
        
        # receive hits from bullets
        hit_bullet = pygame.sprite.spritecollideany(self, bullets)
        if hit_bullet:
            hit_bullet.kill()
            self.health.lose(hit_bullet.damage)

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

    def move(self, target, walls):
        """Move enemy to the target point.

        Returns true if target was reached.
        
            target: Vector2.
        """
        old_pos = self.pos.copy()
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
        for wall in walls:
            if pygame.Rect.colliderect(wall, self.rect):
                self.rect.center = old_pos
                self.pos = old_pos
                return
            
        self.health.update(self.rect.left - 10, self.rect.top - 15)
        return reached

    def draw(self, surface, offset):
        # for p in self.path:
        #     pygame.draw.circle(surface, (255, 0, 0), p + offset, 10)
        surface.blit(self.image, self.rect.topleft + offset)
        self.health.draw(surface, offset)
