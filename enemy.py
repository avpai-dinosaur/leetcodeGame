import pygame
import utils
import constants as c
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, imglink):
        """Constructor.

            pos: tuple representing enemy's inital position
        """
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
        self.face_left = False
        self.rect = pygame.Rect(pos[0], pos[0], 16 * 3, 16 * 3)
        self.image = self.image_dict[self.action][self.current_frame]
        
        #TEMPORARY VARIABLE
        self.temp = 0
    

        super().__init__()
        self.health = 100
        self.speed = 0.005
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(pos[0], pos[0], 16 * 3, 16 * 3)
    
    def update(self, walls):
        """Update function to run each game tick.
        
        Enemy should move randomly and reverse direction if it bounces off a wall.

            walls: list of pygame.Rects representing walls in the map.
        """
        new_pos = self.pos
        x_dir = 1
        y_dir = 1
        self.temp += 1
        if(self.temp == 2):
            x_dir = random.randint(-1, 1)
            y_dir = random.randint(-1, 1)
            self.temp = 0
        
        new_pos.x = self.pos.x + 300 * self.speed * x_dir
        new_pos.y = self.pos.y + 300 * self.speed * y_dir

        # tentatively update to the new position
        # might have to undo if it turns out new position
        # collides with a barrier
        self.rect.center = new_pos

        # check if the proposed position collides with walls
        for wall in walls:
            if pygame.Rect.colliderect(wall, self.rect):
                # dont update the position
                self.rect.center = self.pos
                return
        
        #Sprite update stuff
        current_time = pygame.time.get_ticks()
        if(current_time - self.last_update >= self.cooldown):
            #if animation cooldown has passed between last update and current time, switch frame
            self.current_frame += 1
            self.last_update = current_time
            #reset frame back to 0 so it doesn't index out of bounds
            if(self.current_frame >= self.masteraction[self.action]):
                self.current_frame = 0
            self.image = self.image_dict[self.action][self.current_frame]


    
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


    