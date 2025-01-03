import pygame
from world import World
import constants as c

def main(playerDict):
    pygame.display.set_caption("Leetcode game")
    clock = pygame.time.Clock()
    world = World(screen, playerDict)
    running = True
    
    # Game loop
    while running:
        # Poll for events.
        # Note that user input devices are not accessed here,
        # instead they are accessed directly through their modules.
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close the window
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # fill the screen with a color to wipe away anything from last frame
        world.update()
        screen.fill("black")
        world.draw(screen)

        if world.endGame():
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    main(c.TEST_PLAYER_DICT)