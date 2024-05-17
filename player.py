import pygame
import utils

class Player(pygame.sprite.Sprite):
    """Represents the player."""

    def __init__(self, screen, filename):
        super().__init__()
        self.speed = 0.01
        self.pos = pygame.Vector2(
            screen.get_width() / 2, 
            screen.get_height() / 2
        )
        self.image, self.rect = utils.load_png(filename)
    
    def update(self):
        """Updates the player's position."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= 300 * self.speed
        if keys[pygame.K_s]:
            self.pos.y += 300 * self.speed
        if keys[pygame.K_a]:
            self.pos.x -= 300 * self.speed
        if keys[pygame.K_d]:
            self.pos.x += 300 * self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.pos)
