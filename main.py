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
    image = pygame.image.load('Oldhero.png').convert_alpha()
    color = (0,0,0)
    sheet = spritesheet.SpriteSheet(image)
    animationrun = []
    animationjump = []
    animationpunch = []
    animationkick = []
    animationidle = []
    masteraction = {"idle": 2, "run" : 6 , "jump" : 4, "punch" : 3, "kick" : 4}
    last_update = pygame.time.get_ticks()
    animation_cooldown = 200 #in milli secs
    frame = 0

    #IDLE
    #MAKE IDLE SLOWER TIME
    for x in range(masteraction["idle"]):
        animationidle.append(sheet.get_image(0, 0, 16 ,16, 3, color))
        animationidle.append(sheet.get_image(1, 0, 16,16, 3, color))


    for x in range(masteraction["run"]):
        animationrun.append(sheet.get_image(0, 1, 16,16, 3, color))
        animationrun.append(sheet.get_image(1, 1, 16,16, 3, color))
        animationrun.append(sheet.get_image(2, 1, 16,16, 3, color))
        animationrun.append(sheet.get_image(3, 1, 16,16, 3, color))
        animationrun.append(sheet.get_image(4, 1, 16,16, 3, color))
        animationrun.append(sheet.get_image(5, 1, 16,16, 3, color))
    
    for x in range(masteraction["jump"]):
        animationjump.append(sheet.get_image(1, 0, 16,16, 3, color))
        animationjump.append(sheet.get_image(2, 0, 16,16, 3, color))
        animationjump.append(sheet.get_image(3, 0, 16,16, 3, color))
        animationjump.append(sheet.get_image(4, 0, 16,16, 3, color))
    
    for x in range(masteraction["punch"]):
        animationpunch.append(sheet.get_image(0, 4, 16,16, 3, color))
        animationpunch.append(sheet.get_image(1, 4, 16,16, 3, color))
        animationpunch.append(sheet.get_image(2, 4, 16,16, 3, color))

    for x in range(masteraction["kick"]):
        animationkick.append(sheet.get_image(0, 2, 16,16, 3, color))
        animationkick.append(sheet.get_image(1, 2, 16,16, 3, color))
        animationkick.append(sheet.get_image(2, 2, 16,16, 3, color))
        animationkick.append(sheet.get_image(3, 2, 16,16, 3, color))

    
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

        action = "idle"
        #current time
        current_time = pygame.time.get_ticks()
        if(current_time - last_update >= animation_cooldown):
            #if #animation cooldown has passed between last update and current time, switch frame
            frame += 1
            last_update = current_time
            #reset frame back to 0 so it doesn't index out of bounds
            if(frame >= masteraction[action]):
                frame = 0
        screen.blit(animationidle[frame], (0,0))



        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()