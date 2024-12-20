"""Classes for different objects within the game."""

import pygame
import utils
import random
import constants as c


class StaminaBar():
    """Represents a stamina bar."""
    def __init__(self, x, y, w, h, max_stamina):
        self.x = x 
        self.y = y
        self.w = w 
        self.h = h
        self.stamina = max_stamina
        self.max_stamina = max_stamina
    
    def update(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, offset):
        for bar in range(self.stamina):
            pygame.draw.rect(surface, "blue",
                             pygame.Rect(self.x + self.w * bar + 1, self.y, self.w - 2, self.h)
                                .move(offset.x, offset.y))
        for bar in range(self.stamina, self.max_stamina):
            pygame.draw.rect(surface, "grey",
                             pygame.Rect(self.x + self.w * bar + 1, self.y, self.w - 2, self.h)
                                .move(offset.x, offset.y))


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
        if player.stats['totalSolved'] < self.cost:
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


class Gun(pygame.sprite.Sprite):
    """Class to represent a player's gun."""

    def __init__(self, player, filename):
        """Constructor.

            player: player who owns the gun
            filename: png image of gun
        """
        super().__init__()
        self.pos = player.pos
        self.all_guns, _ = utils.load_png(filename)
        width = 90
        height = 48
        scale = 0.6
        self.x_offset = 20
        self.y_offset = 15
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.blit(
            self.all_guns,
            (0,0),
            (width * 0, height * 1, width, height)
        )
        self.image = pygame.transform.scale(self.image, (width * scale, height * scale))
        self.image.set_colorkey((0, 0, 0))

    def update(self, player):
        self.pos = player.pos
        self.rect.center = (self.pos.x + self.x_offset, self.pos.y + self.y_offset)

    def draw(self, surface, offset):
        surface.blit(self.image, self.rect.topleft + offset)


class Bullet(pygame.sprite.Sprite):
    """Class to represent a bullet."""

    def __init__(self, pos, speed, direction, range):
        """Constructor.
            
            pos: Vec2() showing position of the bullet. 
            speed: the speed of the bullet
            direction: normalized Vec2() showing direction of bullet.
            range: how far the bullet can travel
        """
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = pygame.Surface((5, 5))
        pygame.draw.rect(self.image, (0, 0, 0), pygame.Rect(pos.x, pos.y, 5, 5))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.direction = pygame.Vector2(direction)
        self.damage = 20
        self.distance_traveled = 0
        self.range = range
    
    def update(self, walls):
        self.distance_traveled += self.speed
        self.pos = self.pos + self.direction * self.speed
        self.rect.topleft = self.pos
        if self.distance_traveled >= self.range:
            self.kill()
        for wall in walls:
            if pygame.Rect.colliderect(wall, self.rect):
                self.kill()
    
    def draw(self, surface, offset):
        surface.blit(self.image, self.rect.topleft + offset)
    