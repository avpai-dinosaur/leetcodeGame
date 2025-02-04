import pygame
import utils
import requests
from player import Player
from enemy import Enemy
from roomba import Roomba
from map import Map
from button import Button
import objects as o
import constants as c

class Camera(pygame.sprite.Group):
    """Represents the world's camera"""

    def __init__(self, surface, background, foreground_objects, init_pos):
        super().__init__()
        self.background = background
        self.offset = pygame.math.Vector2()
        self.half_w = surface.get_size()[0] // 2
        self.half_h = surface.get_size()[1] // 2

        # Camera positioning
        self.center_camera_on_target(init_pos)

        # Zoom
        self.zoom = 1
        self.internal_surface_size = (surface.get_size()[0], surface.get_size()[1])
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_h
        self.x_bound_distance = self.half_w
        self.y_bound_distance = self.half_h

        # Lighting
        self.light_radius = 300
        self.dim = False

        # Bullets
        self.foreground_objects = foreground_objects
        self.background_objects = pygame.sprite.Group()
    
    def center_camera_on_target(self, target):
        """Centers the camera on the target rect.
        
            target: pygame.Rect
        """
        self.offset.x = target.centerx - self.half_w
        self.offset.y = target.centery - self.half_h

    def zoom_keyboard_control(self):
        """Control the zoom level with keyboard."""
        keys = pygame.key.get_just_pressed()
        pressed_key = False
        if keys[pygame.K_q]:
            pressed_key = True
            self.zoom = 2.5 
        if keys[pygame.K_e]:
            pressed_key = True
            self.zoom = 1
        if pressed_key:
            self.x_bound_distance = self.half_w / self.zoom
            self.y_bound_distance = self.half_h / self.zoom

    def update(self, player_rect):
        """Update the camera."""
        self.zoom_keyboard_control()
        self.center_camera_on_target(player_rect)

    def draw_filter(self, player_rect, sprite_rect):
        """Filter out sprites outside of game window."""
        if player_rect.left - sprite_rect.right > self.x_bound_distance:
            return False
        if sprite_rect.left - player_rect.right > self.x_bound_distance:
            return False
        if player_rect.top - sprite_rect.bottom > self.y_bound_distance:
            return False
        if sprite_rect.top - player_rect.bottom > self.y_bound_distance:
            return False
        return True

    def draw(self, player_rect, surface):
        """Draw the sprites belonging to the camera group to surface."""

        dim_surface = pygame.Surface((1280, 800), pygame.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))  # RGBA: Dark transparent overlay

        self.internal_surface.fill((0, 0, 0))
        self.internal_surface.blit(self.background, -self.offset + self.internal_offset)
        [obj.draw(self.internal_surface, -self.offset + self.internal_offset)
         for obj in self.background_objects]
        for sprite in sorted(self.sprites(), key=lambda s : s.rect.centery):
            sprite.draw(self.internal_surface, -self.offset + self.internal_offset)
        [obj.draw(self.internal_surface, -self.offset + self.internal_offset) 
         for obj in self.foreground_objects]
        
        scaled_surface = pygame.transform.scale(self.internal_surface, self.zoom * self.internal_surface_size_vector)
        scaled_rect = scaled_surface.get_rect(center=(self.half_w, self.half_h))

        surface.blit(scaled_surface, scaled_rect)
        if self.dim:
            surface.blit(dim_surface, (0, 0))


class World():
    """Top level class to keep track of all game objects."""
   
    def __init__(self, screen, playerStats):
        self.screen = screen
        self.map = Map("data/images/brickMap.png")
        self.player = Player("data/images/Oldhero.png", self.map.player_spawn, playerStats)
        self.roomba = Roomba("data/images/roomba.png", self.map.roomba_path)
        self.tech_note = o.TechNote("data/images/techNote.png", self.map.tech_note_spawn)
        self.enemies = pygame.sprite.Group()
        self.level = 1
        # [self.enemies.add(Enemy("data/images/robot.png", self.map.enemy_spawn[i])) for i in range(self.level)]
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        
        self.camera = Camera(screen, self.map.image, self.bullets, self.player.rect)
        self.camera.add(self.player)
        [self.camera.add(laser_door) for laser_door in self.map.laser_doors]
        self.camera.add(self.roomba)
        self.camera.add(self.enemies)
        self.camera.add(self.tech_note)
        self.camera.foreground_objects.add(self.map.static_objects)
        self.camera.background_objects.add(self.map.background_objects)
    
    def spawn_enemies(self):
        [self.enemies.add(Enemy("data/images/robot.png", self.map.enemy_spawn[i])) for i in range(self.level * 5)]
        self.camera.add(self.enemies)

    def update(self):
        self.player.update(self.map.walls, self.map.laser_doors)
        self.enemies.update(self.player, self.bullets, self.map)
        self.roomba.update(self.player)
        self.bullets.update(self.map.walls)
        self.map.laser_doors.update(self.player)
        self.tech_note.update(self.player)
        self.camera.update(self.player.rect)
        self.map.static_objects.update(self.player, self.camera)
        self.map.background_objects.update(self.player, self.camera)

        mouse = pygame.mouse.get_pressed()
        if mouse[0] and pygame.time.get_ticks() - self.last_shot > 200:
            self.last_shot = pygame.time.get_ticks()
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            center_pos = pygame.Vector2(self.camera.half_w, self.camera.half_h)
            direction = (mouse_pos - center_pos).normalize()
            self.bullets.add(o.Bullet(self.player.pos, 10, direction, 200))

        if len(self.enemies.sprites()) == 0:
            self.level += 1
            # self.spawn_enemies()
            return False
        return True
    
    def endGame(self):
        return self.player.health.hp <= 0

    def draw(self, surface):
        self.camera.draw(self.player.rect, surface)
