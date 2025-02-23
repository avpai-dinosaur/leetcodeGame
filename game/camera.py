import pygame


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

    def draw(self, player_rect, surface):
        """Draw the sprites belonging to the camera group to surface."""
        # Draw to the camera's internal surface
        self.internal_surface.fill((0, 0, 0))
        self.internal_surface.blit(self.background, -self.offset + self.internal_offset)
        [obj.draw(self.internal_surface, -self.offset + self.internal_offset)
         for obj in self.background_objects]
        for sprite in sorted(self.sprites(), key=lambda s : s.rect.centery):
            sprite.draw(self.internal_surface, -self.offset + self.internal_offset)
        [obj.draw(self.internal_surface, -self.offset + self.internal_offset) 
         for obj in self.foreground_objects]
        
        # Scale image to zoom level
        scaled_surface = pygame.transform.scale(self.internal_surface, self.zoom * self.internal_surface_size_vector)
        scaled_rect = scaled_surface.get_rect(center=(self.half_w, self.half_h))
        surface.blit(scaled_surface, scaled_rect)

        # Dance floor
        dim_surface = pygame.Surface((1280, 800), pygame.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))  # RGBA: Dark transparent overlay
        if self.dim:
            surface.blit(dim_surface, (0, 0))