import pygame
import utils

class Player(pygame.sprite.Sprite):
    """Represents the player."""

    def __init__(self, filename, pos):
        super().__init__()
        self.speed = 0.01
        self.pos = pygame.Vector2(pos)
        self.image, self.rect = utils.load_png(filename)
    
    def update(self, walls, doors):
        """Updates the player's position."""
        new_pos = pygame.Vector2(self.pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            new_pos.y = self.pos.y - 300 * self.speed
        if keys[pygame.K_s]:
            new_pos.y = self.pos.y + 300 * self.speed
        if keys[pygame.K_a]:
            new_pos.x = self.pos.x - 300 * self.speed
        if keys[pygame.K_d]:
            new_pos.x = self.pos.x + 300 * self.speed
        
        self.rect.center = new_pos
        for wall in walls:
            if pygame.Rect.colliderect(wall, self.rect):
                # dont update the position
                self.rect.center = self.pos
                return
        
        for door in doors:
            if door.toggle and pygame.sprite.collide_rect(door, self):
                # dont update the positionmm
                self.rect.center = self.pos
                # present the button to press
                if keys[pygame.K_m]:
                    door.toggle = False
                return
        self.pos = new_pos
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
