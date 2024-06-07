import pygame
import constants as c
from world import World
#hello world
def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    clock = pygame.time.Clock()
    world = World(screen)
    running = True
    
    # Game loop
    while running:
        # Poll for events.
        # Note that user input devices are not accessed here,
        # instead they are accessed directly through their modules.
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close the window
            if event.type == pygame.QUIT:
                running = False
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        world.update()
        world.draw(screen)
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()