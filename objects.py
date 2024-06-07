"""Classes for different objects within the game."""


import pygame


class LaserDoor(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.toggle = True
        

