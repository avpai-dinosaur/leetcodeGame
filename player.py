import pygame
import utils

class Player(pygame.sprite.Sprite):
    """Represents the player."""

    def __init__(self, filename, pos):
        super().__init__()
        self.speed = 0.01
        self.pos = pygame.Vector2(pos)
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
        surface.blit(self.image,
            pygame.Vector2(
                surface.get_width() / 2,
                surface.get_height() / 2
            )
        )
