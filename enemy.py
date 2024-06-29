import pygame
import utils
import constants as c
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, imglink, path):
        """Constructor.

            path: List of Vector2 objects specifying path along 
                  which the enemy will walk.
            imglink: path to enemy sprite image.
        """
        super().__init__()

        #This is all the enemy sprite stuff
        self.sheet, _ = utils.load_png(imglink)
        self.color = (0,0,0)
        self.masteraction = {"idle": 5, "idle2" : 6 , "dead" : 5, "jump" : 4, "walk" : 7, "sidejump": 4} # maps action to the number of frames
        self.animationidle = self.idleinit()
        self.animationwalk = self.walkinit()
        self.animationjump = self.jumpinit()
        self.animationsidejump = self.sidejumpinit()
        self.animationdead = self.deadinit()
        self.animationidle2 = self.idle2init()

        self.cooldown = 100

        self.image_dict = {
            "walk": self.animationwalk,
            "idle": self.animationidle,
            "jump": self.animationjump,
            "sidejump": self.animationsidejump,
            "dead": self.animationdead,
            "idle2": self.animationidle2
        }
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
        self.action = "walk"
        self.face_left = True
        self.image = self.image_dict[self.action][self.current_frame]
        
        #TEMPORARY VARIABLE
        self.temp = 0
    

        self.health = 100
        self.speed = 1

        # Path following
        self.path = path
        self.pos = self.path[0].copy() # This NEEDS to be a copy to avoid modifying path!
        self.target_point = 1
        self.target = self.path[self.target_point]
        self.direction = 1

        # Image Stuff
        self.rect = pygame.Rect(self.pos[0], self.pos[0], 16 * 3, 16 * 3)
        self.rect.center = self.pos
    
    def update(self):
        """Update function to run each game tick.
        
        Enemy should move randomly and reverse direction if it bounces off a wall.

            walls: list of pygame.Rects representing walls in the map.
        """
        self.move()
        self.rect.center = self.pos

    def move(self):
        """Move the enemy towards next target point.
        
        Enemy should reverse direction upon reaching either end of path.
        """
        movement = self.target - self.pos
        distance = movement.length()
        
        if distance >= self.speed:
            self.pos += movement.normalize() * self.speed
        else:
            if distance != 0:
                self.pos += movement.normalize() * distance
            if self.target_point == len(self.path) - 1 or self.target_point == 0:
                self.direction *= -1
                self.face_left = not self.face_left
            self.target_point += self.direction
            self.target = self.path[self.target_point]

        #Sprite update stuff
        current_time = pygame.time.get_ticks()
        if(current_time - self.last_update >= self.cooldown):
            #if animation cooldown has passed between last update and current time, switch frame
            self.current_frame += 1
            self.last_update = current_time
            #reset frame back to 0 so it doesn't index out of bounds
            if(self.current_frame >= self.masteraction[self.action]):
                self.current_frame = 0
            self.image = pygame.transform.flip(
                self.image_dict[self.action][self.current_frame], 
                self.face_left,
                False
            )

    # def rotate(self):
    #     #use distance to calculate angle
    #     distance = self.target - self.pos
    #     self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
    #     self.image = pygame.transform.rotate(self.original_image, self.angle)
    #     self.rect = self.image.get_rect()
    #     self.rect.center = self.pos
    
    def draw(self, surface):
        #pygame.draw.rect(surface, "green", self.rect)
        surface.blit(
            pygame.transform.flip(self.image, self.face_left, False),
            self.rect
        )

    def get_image(self, frame_w, frame_h, width, height, scale, color):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame_w * width),(frame_h * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image
    
    def idleinit(self):
        temp = []
        for _ in range(self.masteraction["idle"]):
            temp.append(self.get_image(0, 1, 64, 64, 0.75, self.color))
            temp.append(self.get_image(1, 1, 64, 64, 0.75, self.color))
            temp.append(self.get_image(2, 1, 64, 64, 0.75, self.color))
            temp.append(self.get_image(3, 1, 64, 64, 0.75, self.color))
            temp.append(self.get_image(4, 1, 64, 64, 0.75, self.color))
        return temp

    def walkinit(self):
        temp = []
        for _ in range(self.masteraction["walk"]):
            temp.append(self.get_image(0, 5, 64, 64, 0.75, self.color))
            temp.append(self.get_image(1, 5, 64, 64, 0.75, self.color))
            temp.append(self.get_image(2, 5, 64, 64, 0.75, self.color))
            temp.append(self.get_image(3, 5, 64, 64, 0.75, self.color))
            temp.append(self.get_image(4, 5, 64, 64, 0.75, self.color))
            temp.append(self.get_image(5, 5, 64, 64, 0.75, self.color))
            temp.append(self.get_image(6, 5, 64, 64, 0.75, self.color))
        return temp

    def jumpinit(self):
        temp = []
        for _ in range(self.masteraction["jump"]):
            temp.append(self.get_image(0, 3, 64, 64, 0.75, self.color))
            temp.append(self.get_image(1, 3, 64, 64, 0.75, self.color))
            temp.append(self.get_image(2, 3, 64, 64, 0.75, self.color))
            temp.append(self.get_image(3, 3, 64, 64, 0.75, self.color))
        return temp
    
    def sidejumpinit(self):
        temp = []
        for _ in range(self.masteraction["sidejump"]):
            temp.append(self.get_image(0, 4, 64, 64, 0.75, self.color))
            temp.append(self.get_image(1, 4, 64, 64, 0.75, self.color))
            temp.append(self.get_image(2, 4, 64, 64, 0.75, self.color))
            temp.append(self.get_image(3, 4, 64, 64, 0.75, self.color))
        return temp

    def deadinit(self):
        temp = []
        for _ in range(self.masteraction["dead"]):
            temp.append(self.get_image(0, 0, 64, 64, 0.75, self.color))
            temp.append(self.get_image(1, 0, 64, 64, 0.75, self.color))
            temp.append(self.get_image(2, 0, 64, 64, 0.75, self.color))
            temp.append(self.get_image(3, 0, 64, 64, 0.75, self.color))
            temp.append(self.get_image(4, 0, 64, 64, 0.75, self.color))
        return temp

    def idle2init(self):
        temp = []
        for _ in range(self.masteraction["idle2"]):
            temp.append(self.get_image(0, 2, 64, 64, 0.75, self.color))
            temp.append(self.get_image(1, 2, 64, 64, 0.75, self.color))
            temp.append(self.get_image(2, 2, 64, 64, 0.75, self.color))
            temp.append(self.get_image(3, 2, 64, 64, 0.75, self.color))
            temp.append(self.get_image(4, 2, 64, 64, 0.75, self.color))
            temp.append(self.get_image(5, 2, 64, 64, 0.75, self.color))
        return temp


    