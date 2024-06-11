"""Classes for different objects within the game."""

import pygame
import utils
import random
import constants as c


class Door(pygame.sprite.Sprite):
    """Class to represent doors in the game."""
    
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
    
    def door_action(self):
        """Runs the action specific to the door.
        
        Default is to turn self.toggle to False.
        """
        self.toggle = False

    def draw_door(self, surface):
        """Logic to draw the door image.
        
        Default is to not draw the toor if toggle is False.
        """
        if self.toggle:
            pygame.draw.rect(surface, (252, 3, 3), self.rect)
    
    def update(self, player):
        """Updates the door based on player position.

        If the player is within the door's range, show the key needed to
        open the door.
            
            player: pygame.Rect representing the player's area and position.
        """
        if self.scaled_rect.colliderect(player) and self.toggle:
            keys = pygame.key.get_pressed()
            self.present_button = True
            if (keys[self.open_button[1]]):
                self.door_action()
        else:
            self.present_button = False
    
    def draw(self, surface):
        """Draw the door to the surface."""
        if self.present_button:
            surface.blit(self.text, self.textRect)
        self.draw_door(surface)


class LaserDoor(Door):
    """Class to represent a laser door."""
    

class AntidoteDoor(Door):
    """Class to represent an antidote door."""
   
    def __init__(self, rect, hp):
       super().__init__(rect)
       self.vials = pygame.sprite.Group()
       self.hp = hp
    
    def door_action(self):
        """Door should release an antidote health vial."""
        vial_pos = (self.rect.centerx, self.rect.centery + random.randint(-20, 20))
        self.vials.add(AntidoteVial(self.hp, vial_pos))

    def draw_door(self, surface):
        """Logic to draw the door image.
        
        Default is to not draw the toor if toggle is False.
        """
        pygame.draw.rect(surface, (252, 40, 40), self.rect)

    def update(self, player):
        """Update all vials that this door owns."""
        super().update(player)
        self.vials.update(player)

    def draw(self, surface):
       """Draw door and all vials belonging to door."""
       super().draw(surface)
       self.vials.draw(surface)


class AntidoteVial(pygame.sprite.Sprite):
    """Class to represent an AntidoteVial."""

    def __init__(self, hp, pos):
        """Constructor.
            
            hp: int representing how much health the vial will heal
        """
        super().__init__()
        self.hp = hp
        self.image, self.rect = utils.load_png("data/images/antidote.png")
        self.rect.center = pos
    
    def update(self, player):
        """Allows antidote to be picked up by player.

        If the player collies with antidote, heal player hp and kill antidote sprite.
            
            player: Player object.
        """
        if self.rect.colliderect(player.rect):
            player.health.hp = min(100, player.health.hp + self.hp)
            self.kill()
        else:
            self.present_button = False

    def draw(self, surface):
        """Draw a vial to the screen."""
        surface.blit(self.image, self.rect)