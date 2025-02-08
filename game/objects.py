"""Classes for different objects within the game."""

import pygame
import utils
import random
import webbrowser
import constants as c
import music_manager

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
        self.font = pygame.font.Font(size=50)
        self.text = self.font.render(self.open_button[0], True, (250, 250, 250))
        self.textRect = self.text.get_rect()
        self.textRect.left = self.rect.left - self.textRect.width - 20
        self.textRect.top = self.rect.top
        self.bg_rect = self.textRect.inflate(10, 10)
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
            pygame.draw.rect(surface, (240, 0, 0), self.bg_rect.move(offset.x, offset.y), border_radius=5)
            surface.blit(self.text, self.textRect.topleft + offset)
        self.draw_door(surface, offset)

class LaserDoor(Door):
    """Class to represent a laser door."""
    def __init__(self, rect, text_input=None, url=None):
        """Constructor.

            rect: pygame.Rect representing the door's area and position.
            text_input: The question that the door expects the player to solve 
                before it will open.
            url: The url to the leetcode question.
                
            If no text input is provided, functions as 
            a regular door. If text is provided it shows up in a speech bubble
            in plain text and clicking the speech bubble opens a browser at w/ url.
        """
        super().__init__(rect)
        
        # Question prompting
        self.text_input = text_input
        self.speech_bubble = SpeechBubble(
            text_input, self.font, (255, 255, 255), (0, 0, 0), url=url)
        
        # Lasers
        self.lasers = []
        self.inner_lasers = []
        laser_width = 4
        inner_laser_width = 2
        num_lasers = 10
        air_gap = (rect.width - laser_width) // (num_lasers - 1) - laser_width
        inner_laser_x_offset = (laser_width - inner_laser_width) / 2
        
        # Add the laser at the left edge and all lasers in middle
        for i in range(num_lasers - 1):
            left_pos = self.rect.left + i * (laser_width + air_gap)
            self.lasers.append(
                pygame.Rect(
                    left_pos,
                    self.rect.top,
                    laser_width,
                    self.rect.height
                )
            )
            self.inner_lasers.append(
                pygame.rect.Rect(
                    left_pos + inner_laser_x_offset,
                    self.rect.top,
                    inner_laser_width,
                    self.rect.height
                )
            )
        
        # Add the laser that is flush with right edge of door
        end_laser_left_pos = self.rect.right - laser_width
        self.lasers.append(
            pygame.Rect(
                end_laser_left_pos,
                self.rect.top,
                laser_width,
                self.rect.height
            )
        )
        self.inner_lasers.append(
            pygame.Rect(
                end_laser_left_pos + inner_laser_x_offset,
                self.rect.top,
                inner_laser_width,
                self.rect.height
            )
        )
    
    def update(self, player):
        super().update(player)
        if not self.scaled_rect.colliderect(player.rect):
            self.speech_bubble.toggle = False
        self.speech_bubble.update()
    
    def door_action(self, player=None):
        if self.text_input != None:
            self.speech_bubble.toggle = True
        else:
            super().door_action(player)

    def draw_door(self, surface, offset):
        if self.toggle:
            for i in range(len(self.lasers)):
                pygame.draw.rect(surface, (200, 0, 0), self.lasers[i].move(offset.x, offset.y))
                pygame.draw.rect(surface, (255, 0, 0), self.inner_lasers[i].move(offset.x, offset.y))

    def draw(self, surface, offset):
        super().draw(surface, offset)
        if self.text_input != None:
            self.speech_bubble.draw(surface, self.rect.midtop + offset)

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


class SpeechBubble():
    """Class to represent the speech bubble of NPC."""

    def __init__(self, text_input, font, text_color, background_color, url=None):
        """Constructor."""
        self.text_input = text_input
        self.url = url
        self.font = font
        self.text_color = text_color
        self.background_color = background_color

        self.text_image = self.font.render(self.text_input, True, text_color, c.TILE_SIZE * 2)
        self.text_width, self.text_height = self.text_image.get_size()

        self.padding = 10
        self.bg_width, self.bg_height = (self.text_width + self.padding * 2, self.text_height + self.padding * 2)
        self.bg_rect = pygame.Rect(0, 0, self.bg_width, self.bg_height)

        self.toggle = False

    def update_text(self, text_input, text_color=(255, 255, 255)):
        self.text_input = text_input
        self.text_color = text_color
        self.text_image = self.font.render(self.text_input, True, text_color, c.TILE_SIZE * 2)

    def update(self):
        """Checks if the speech bubble is clicked."""
        if self.toggle:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if self.bg_rect.collidepoint(mouse_pos) and mouse_pressed[0]:  # Left mouse button
                if self.url:
                    webbrowser.open(self.url)

    def draw(self, surface, pos):
        if self.toggle:
            self.bg_rect.topleft = (pos[0] - self.bg_width // 2, pos[1] - self.bg_height - 10)
            pygame.draw.rect(surface, self.background_color, self.bg_rect, border_radius=10)

            text_position = (self.bg_rect.topleft[0] + self.padding, self.bg_rect.topleft[1] + self.padding)
            surface.blit(self.text_image, text_position)


class TechNote(pygame.sprite.Sprite):
    """Class to represent a technical note."""

    def __init__(self, filename, pos):
        super().__init__()
        og_image, _ = utils.load_png(filename)
        self.image = pygame.transform.scale(og_image, (72 * 2, 72 * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.pos = pygame.Vector2(pos)
        self.scaled_rect = self.rect.inflate(50, 50)

        self.open_note = ("M", pygame.K_m)
        self.font = pygame.font.Font(size=30)
        self.button_text = self.font.render(self.open_note[0], True, (250, 250, 250), (0, 0, 0))
        self.button_textRect = self.button_text.get_rect()
        self.button_textRect.center = (self.rect.centerx - 100, self.rect.centery - 100)
        self.present_button = False

        text = "A really brute force way would be to search for all possible pairs of numbers but that would be too slow."
        self.note_text = self.font.render(text, True, (250, 250, 25), (0, 0, 0), 72 * 2)
        self.note_textRect = self.note_text.get_rect()
        self.note_textRect.center = (self.rect.centerx - 100, self.rect.centery - 100)
        self.toggle_note = False
    

    def update(self, player):
        """Updates the note based on player position.

        If the player is within the note's range, show the key needed to
        read the note.
            
            player: Player object.
        """
        if self.scaled_rect.colliderect(player.rect):
            keys = pygame.key.get_pressed()
            self.present_button = True
            if (keys[self.open_note[1]]):
                self.toggle_note = True
        else:
            self.present_button = False
            self.toggle_note = False
    
    def draw(self, surface, offset):
        """Draw the note to the surface."""
        #surface.blit(self.image, self.rect.topleft + offset)
        if self.present_button:
            surface.blit(self.button_text, self.button_textRect.topleft + offset)
        if self.toggle_note:
            surface.blit(self.note_text, self.note_textRect.topleft + offset)

class StaticItem(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, filename=None):
        super().__init__()
        self.pos = pos
        #self.image, self.rect = utils.load_png(filename)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], width * c.TILE_SIZE, height * c.TILE_SIZE)
        self.rect.topleft = self.pos
    
    def draw(self, surface, offset):
        pygame.draw.rect(surface, (219, 134, 111), self.rect.move(offset))
        # surface.blit(self.image, self.rect.topleft + offset)

class DanceFloor(StaticItem):

    DISCO_COLORS = [(255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255)]

    def __init__(self, pos, width=5, height=5):
        super().__init__(pos, width, height)
        self.rect.width = 448
        self.rect.height = 320
        self.light_pos = []
        self.colors = []
        self.on_dance_floor = False
        self.disco_timer = pygame.time.get_ticks()

    def update(self, player, camera):
        if self.rect.colliderect(player.rect):
            self.on_dance_floor = True
            camera.dim = True
            # music_manager.play_music()
        else:
            self.on_dance_floor = False
            camera.dim = False
            # music_manager.stop_music()

        if self.on_dance_floor:
            if pygame.time.get_ticks() - self.disco_timer > 1000:  # Change every second
                self.disco_timer = pygame.time.get_ticks()
                self.light_pos = []
                self.colors = []
                for i in range(10):  # Number of lights
                    x = random.randint(self.rect.left, self.rect.right)
                    y = random.randint(self.rect.top, self.rect.bottom)
                    self.light_pos.append((x, y))
                    self.colors.append(random.choice(DanceFloor.DISCO_COLORS))
        
    def draw(self, surface, offset):
        super().draw(surface, offset)
        if self.on_dance_floor:
            for i, pos in enumerate(self.light_pos):
                pygame.draw.circle(surface, self.colors[i], pos + offset, 15)
