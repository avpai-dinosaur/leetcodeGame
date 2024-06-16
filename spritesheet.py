import pygame


class SpriteSheet():

    def __init__(self, characterlink, color) -> None:
        self.image = pygame.image.load(characterlink).convert_alpha()
        self.sheet = self.image
        self.color = color
        self.masteraction = {"idle": 2, "run" : 6 , "jump" : 4, "punch" : 3, "kick" : 4}
        self.animationrun = self.animationruninit()
        self.animationidle = self.animationidleinit()
        self.animationjump = self.animationjumpinit()
        self.animationkick = self.animationkickinit()
        self.animationpunch = self.animationpunchinit()

    
    def get_image(self, frame_w, frame_h, width, height, scale, color):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame_w * width),(frame_h * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image
    

    def animationruninit(self):
        temp = []
        for _ in range(self.masteraction["run"]):
            temp.append(self.get_image(0, 1, 16, 16, 3, self.color))
            temp.append(self.get_image(1, 1, 16, 16, 3, self.color))
            temp.append(self.get_image(2, 1, 16, 16, 3, self.color))
            temp.append(self.get_image(3, 1, 16, 16, 3, self.color))
            temp.append(self.get_image(4, 1, 16, 16, 3, self.color))
            temp.append(self.get_image(5, 1, 16, 16, 3, self.color))
        return temp
    
    def animationidleinit(self):
        temp = []
        for _ in range(self.masteraction["idle"]):
            temp.append(self.get_image(0, 0, 16 ,16, 3, self.color))
            temp.append(self.get_image(1, 0, 16,16, 3, self.color))
        return temp
    
    def animationjumpinit(self):
        temp = []
        for _ in range(self.masteraction["idle"]):
            temp.append(self.get_image(1, 0, 16,16, 3, self.color))
            temp.append(self.get_image(2, 0, 16,16, 3, self.color))
            temp.append(self.get_image(3, 0, 16,16, 3, self.color))
            temp.append(self.get_image(4, 0, 16,16, 3, self.color))
        return temp

    def animationjumpinit(self):
        temp = []
        for _ in range(self.masteraction["jump"]):
            temp.append(self.get_image(1, 0, 16,16, 3, self.color))
            temp.append(self.get_image(2, 0, 16,16, 3, self.color))
            temp.append(self.get_image(3, 0, 16,16, 3, self.color))
            temp.append(self.get_image(4, 0, 16,16, 3, self.color))
        return temp
    
    def animationpunchinit(self):
        temp = []
        for _ in range(self.masteraction["punch"]):
            temp.append(self.get_image(0, 4, 16,16, 3, self.color))
            temp.append(self.get_image(1, 4, 16,16, 3, self.color))
            temp.append(self.get_image(2, 4, 16,16, 3, self.color))
        return temp

    def animationkickinit(self):
        temp = []
        for _ in range(self.masteraction["kick"]):
            temp.append(self.get_image(0, 2, 16,16, 3, self.color))
            temp.append(self.get_image(1, 2, 16,16, 3, self.color))
            temp.append(self.get_image(2, 2, 16,16, 3, self.color))
            temp.append(self.get_image(3, 2, 16,16, 3, self.color))
        return temp

    



