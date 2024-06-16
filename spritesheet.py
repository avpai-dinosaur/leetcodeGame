import pygame

class SpriteSheet():
    def __init__(self, image) -> None:
        self.sheet = image
    
    def get_image(self, frame_w, frame_h, width, height, scale, color):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame_w * width),(frame_h * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image
