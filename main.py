import pygame
import sys
from world import World
from button import Button

def menu():
    screen = pygame.display.set_mode((1280, 800))
    pygame.display.set_caption("Menu")
    font=pygame.font.SysFont("cambria", 40)
    play_img = pygame.image.load("data/images/Play.png")
    background = pygame.image.load("data/images/menu_background.png")
    while True: 
        screen.blit(background,(0,0))
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = font.render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center = (640, 100))

        play_button = Button(play_img, pos=(640, 400), 
                            text_input="PLAY", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
  

        screen.blit(menu_text, menu_rect)
        buttons = [play_button]
        for button in buttons:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    main()
              

def main():
    
    clock = pygame.time.Clock()
    world = World()
    running = True
    #menu stuff
    
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
    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    menu()