import pygame
import utils
from tileset import TileSet
from player import Player
from enemy import Enemy
from map import Map
import constants as c

class Camera(pygame.sprite.Group):
    """Represents the world's camera"""

    def __init__(self, surface, background, init_pos):
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
            if self.zoom < 2.5:
                self.zoom += 0.5 
        if keys[pygame.K_e]:
            pressed_key = True
            if self.zoom > 1:
                self.zoom -= 0.5
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
            print("not drawing something to the left")
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
        self.internal_surface.fill((0, 0, 0))
        self.internal_surface.blit(self.background, -self.offset + self.internal_offset)
        for sprite in sorted(self.sprites(), key=lambda s : s.rect.centery):
            if self.draw_filter(player_rect, sprite.rect):
                sprite.draw(self.internal_surface, -self.offset + self.internal_offset)
        
        scaled_surface = pygame.transform.scale(self.internal_surface, self.zoom * self.internal_surface_size_vector)
        scaled_rect = scaled_surface.get_rect(center=(self.half_w, self.half_h))

        surface.blit(scaled_surface, scaled_rect)

class World():
    """Top level class to keep track of all game objects."""

    def __init__(self, screen):
        TileSet() # have to wait to initialize here b/c dependencies on pygame.display
        self.player = Player("hero.png", c.INIT_PLAYER_POS)
        self.enemies = pygame.sprite.Group()
        self.map = Map("data/images/outer_world.png")
        for path in self.map.enemy_paths:
            self.enemies.add(Enemy("robot.png", path))
        
        self.camera = Camera(screen, self.map.image, self.player.rect)
        self.camera.add(self.player)
        [self.camera.add(room) for room in self.map.rooms]
    
    def update(self):
        self.player.update(self.map.walls, self.map.laser_doors)
        self.map.rooms.update(self.player)
        self.camera.update(self.player.rect)
        # self.enemies.update(self.player, self.map.walls)
        # self.map.laser_doors.update(self.player)
        # self.map.antidote_doors.update(self.player)
    
    def draw(self, surface):
        self.camera.draw(self.player.rect, surface)
        #self.player.draw(surface)
        # for enemy in self.enemies:
        #     enemy.draw(surface)
