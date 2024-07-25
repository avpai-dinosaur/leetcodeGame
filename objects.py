"""Classes for different objects within the game."""

import pygame
import utils
import random
import constants as c

class HealthBar():
    """Represents a healthbar."""
    def __init__(self, x, y, w, h, max_hp):
        self.x = x 
        self.y = y
        self.w = w 
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    
    def update(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, offset):
        ratio = self.hp/self.max_hp
        pygame.draw.rect(surface, "red", pygame.Rect(self.x, self.y, self.w, self.h).move(offset.x, offset.y))
        pygame.draw.rect(surface, "green", pygame.Rect(self.x, self.y, self.w * ratio, self.h).move(offset.x, offset.y))
    
    def lose(self, hp):
        self.hp -= hp


class PlayerHealthBar(HealthBar):
    """Represents the player's health bar."""
    def __init__(self, x, y, w, h, max_hp):
        super().__init__(x, y, w, h, max_hp)
    
    def draw(self, surface, offset):
        self.hp -= 0.01
        super().draw(surface, offset)

class EnemyHealthBar(HealthBar):
    """Represents the enemy's health bar."""
    def __init__(self, x, y, w, h, max_hp):
        super().__init__(x, y, w, h, max_hp)
        self.last_shown = None
        self.cooldown = 2000
    
    def lose(self, hp):
        super().lose(hp)
        self.last_shown = pygame.time.get_ticks()
    
    def draw(self, surface, offset):
        if self.last_shown and pygame.time.get_ticks() - self.last_shown < self.cooldown:
            super().draw(surface, offset)

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
    
    def door_action(self, player=None):
        """Runs the action specific to the door.
        
        Default is to turn self.toggle to False.
        """
        self.toggle = False

    def draw_door(self, surface, offset):
        """Logic to draw the door image.
        
        Default is to not draw the door if toggle is False.
        """
        if self.toggle:
            pygame.draw.rect(surface, (252, 3, 3), self.rect.move(offset.x, offset.y))
    
    def update(self, player):
        """Updates the door based on player position.

        If the player is within the door's range, show the key needed to
        open the door.
            
            player: Player object.
        """
        if self.scaled_rect.colliderect(player.rect) and self.toggle:
            keys = pygame.key.get_pressed()
            self.present_button = True
            if (keys[self.open_button[1]]):
                self.door_action(player)
        else:
            self.present_button = False
    
    def draw(self, surface, offset):
        """Draw the door to the surface."""
        if self.present_button:
            surface.blit(self.text, self.textRect.topleft + offset)
        self.draw_door(surface, offset)


class LaserDoor(Door):
    """Class to represent a laser door."""
    

class AntidoteDoor(Door):
    """Class to represent an antidote door."""
   
    def __init__(self, rect, hp):
       super().__init__(rect)
       self.vials = pygame.sprite.Group()
       self.hp = hp
       self.cooldown = 1000
       self.last_dispense = pygame.time.get_ticks()
       self.cost = 1
    
    def door_action(self, player):
        """Door should release an antidote health vial."""
        if player.solved < self.cost:
            return

        curr_time = pygame.time.get_ticks()
        if (curr_time - self.last_dispense >= self.cooldown):
            vial_pos = (
                self.rect.centerx,
                self.rect.centery + random.randint(-20, 20)
            )
            self.vials.add(AntidoteVial(self.hp, vial_pos))
            self.last_dispense = curr_time
            self.cost *=2

    def draw_door(self, surface, offset):
        """Logic to draw the door image.
        
        Default is to not draw the toor if toggle is False.
        """
        pygame.draw.rect(surface, (252, 40, 40), self.rect.move(offset.x, offset.y))

    def update(self, player):
        """Update all vials that this door owns."""
        super().update(player)
        self.text = self.font.render(
            f"{self.open_button[0]}\n{player.stats['totalSolved']}/{self.cost}",
            True, (250, 250, 250), (0, 0, 0)
        )
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.rect.centerx + 50, self.rect.centery + 50)
        self.vials.update(player)

    def draw(self, surface, offset):
       """Draw door and all vials belonging to door."""
       super().draw(surface, offset)
       [vial.draw(surface, offset) for vial in self.vials]


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
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self, player):
        """Allows antidote to be picked up by player.

        If the player collies with antidote, heal player hp and kill antidote sprite.
            
            player: Player object.
        """
        time_delta = pygame.time.get_ticks() - self.spawn_time
        if time_delta > 100 and self.rect.colliderect(player.rect):
            player.health.hp = min(100, player.health.hp + self.hp)
            self.kill()

    def draw(self, surface, offset):
        """Draw a vial to the screen."""
        surface.blit(self.image, self.rect.topleft + offset)