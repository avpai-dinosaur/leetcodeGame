import pygame
import utils


    #healthbar stuff
class HealthBar():
    def __init__(self,x,y,w,h,max_hp):
        self.x = x 
        self.y = y
        self.w = w 
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    def draw(self, surface):
        self.hp -= 0.01
        ratio = self.hp/self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))
        

class Player(pygame.sprite.Sprite):
    """Represents the player."""

    def __init__(self, filename, pos):
        super().__init__()
        self.health = HealthBar(pos[0], pos[1], 60, 10, 100)
        self.speed = 0.01
        self.pos = pygame.Vector2(pos)
        self.image, self.rect = utils.load_png(filename)
    
    def update(self, walls):
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
        self.pos = new_pos

        self.health.x = self.pos[0] - 30
        self.health.y = self.pos[1] - 50


        #create functions that depreciate health
        
        #create functions that add health
    
    def draw(self, surface):
        self.health.draw(surface)
        surface.blit(self.image, self.rect)
        #pygame.draw.rect(surface, (0, 255, 0), self.rect)





