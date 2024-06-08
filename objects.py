"""Classes for different objects within the game."""

import pygame
import constants as c


class LaserDoor(pygame.sprite.Sprite):
    """Class to represent a laser door."""
    def __init__(self, rect):
        """Constructor.
            
            rect: pygame.Rect representing the door's area and position
        """
        super().__init__()
        self.rect = rect
        self.scaled_rect = rect.inflate(50, 50)
        self.open_button = ("M", pygame.K_m)
        self.font = pygame.font.Font(size=30)
        self.text = self.font.render(self.open_button[0], True, (250, 250, 250), (0, 0, 0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.rect.centerx + 50, self.rect.centery + 50)
        self.toggle = True
        self.present_button = False
    
    def update(self, player):
        """Updates the door based on player position.

        If the player is within the door's range, show the key needed to
        open the door.
            
            player: pygame.Rect representing the player's area and position.
            keys: list of keys pressed at the time.
        """
        if self.scaled_rect.colliderect(player) and self.toggle:
            keys = pygame.key.get_pressed()
            self.present_button = True
            if (keys[self.open_button[1]]):
                self.toggle = False
        else:
            self.present_button = False
    
    def draw(self, surface):
        if self.toggle:
            pygame.draw.rect(surface, (252, 3, 3), self.rect)
        if self.present_button:
            surface.blit(self.text, self.textRect)
