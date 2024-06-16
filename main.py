import pygame
import constants as c
from world import World
import spritesheet
#hello world
#switch from health
def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    clock = pygame.time.Clock()
    world = World(screen)
    running = True

    #TEMPORARY

    color = (0,0,0)
    sheet = spritesheet.SpriteSheet('Oldhero.png', color)
    animationjump = []
    animationpunch = []
    animationkick = []

    last_update = pygame.time.get_ticks()
    animation_cooldown = 200 #in milli secs
    frame = 0
 
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

        action = "run"
        #current time
        current_time = pygame.time.get_ticks()
        if(current_time - last_update >= animation_cooldown):
            #if #animation cooldown has passed between last update and current time, switch frame
            frame += 1
            last_update = current_time
            #reset frame back to 0 so it doesn't index out of bounds
            if(frame >= sheet.masteraction[action]):
                frame = 0
        screen.blit(sheet.animationrun[frame], (100,100))



        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()