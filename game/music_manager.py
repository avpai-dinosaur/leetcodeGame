import pygame

pygame.mixer.init()
pygame.mixer.music.load("data/music/Robots a Cometh - Dan Lebowitz.mp3")
pygame.mixer.music.set_volume(0.5)

def play_music():
    pygame.mixer.music.play(-1)
    print("playing music")

def stop_music():
    pygame.mixer.music.stop()