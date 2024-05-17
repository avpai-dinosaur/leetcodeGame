import pygame
import utils
from map import Map

class World():
    """Top level class to keep track of all game objects."""

    def __init__(self):
        self.map = None