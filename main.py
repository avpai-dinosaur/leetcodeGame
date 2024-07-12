import pygame
import sys
from world import World
from button import Button

def menu(Start):
    pygame.display.set_caption("Menu")
    Titlefont=pygame.font.SysFont("cambria", 75)
    play_img = pygame.image.load("data/images/Play.png")
    option_img = pygame.image.load("data/images/Play.png")
    quit_img = pygame.image.load("data/images/Play.png")
    background = pygame.image.load("data/images/menu_background.png")
     
    while True: 
        screen.blit(background,(0,0))
        menu_mouse_pos = pygame.mouse.get_pos()
        main_button = Button(play_img, pos=(640, 300), 
                text_input="PLAY", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        if(Start == True):
            menu_text = Titlefont.render("Locked Escaped: E.T.", True, "#bcbcbc")
        else:
            menu_text = Titlefont.render("MAIN MENU", True, "#bcbcbc")
            main_button = Button(play_img, pos=(640, 300), 
                text_input="RESUME", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")

        menu_rect = menu_text.get_rect(center = (640, 150))


        
        option_button = Button(option_img, pos=(640, 420), 
                text_input="OPTIONS", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(quit_img, pos=(640, 540), 
                text_input="QUIT", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
  
        screen.blit(menu_text, menu_rect)
        buttons = [main_button, option_button, quit_button]
        for button in buttons:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_button.checkForInput(menu_mouse_pos):
                    pygame.display.set_caption("Game Time!")
                    if(Start == True):   
                        main()
                    else:
                        return
                if option_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def options():
    pygame.display.set_caption("options")
    Titlefont=pygame.font.SysFont("cambria", 75)
    block_img = pygame.image.load("data/images/Play.png")
    background = pygame.image.load("data/images/menu_background.png")
    while True:
        screen.blit(background,(0,0))
        mouse_pos = pygame.mouse.get_pos()
        option_text = Titlefont.render("MAIN MENU", True, "#bcbcbc")
        option_rect = option_text.get_rect(center = (640, 150))
        back_button = Button(block_img, pos=(640, 600), 
                text_input="BACK", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        
        screen.blit(option_text, option_rect)
        
        buttons = [back_button]
        for button in buttons:
            button.changeColor(mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    return

        pygame.display.update()

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
            keys = pygame.key.get_pressed()
            
            if(keys[pygame.K_ESCAPE]):
                menu(False)
        
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
    menu(True)