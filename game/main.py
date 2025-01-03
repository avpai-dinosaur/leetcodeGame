import pygame
import sys
import requests
import json
from world import World
from button import Button
from menu import LevelMenu, EndMenu
import constants as c

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

                    if(Start == True):   
                        input()
                    else:
                        return
                if option_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

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

def input():
    #FIND RANDOM BOX SHOWING UP

    #setup
    pygame.display.set_caption("Leet User Name")
    background = pygame.image.load("data/images/menu_background.png")
    font = pygame.font.SysFont("cambria", 50)
    headingfont = pygame.font.SysFont("cambria", 40)
    errorfont = pygame.font.SysFont("cambria", 20)
    #accurate center
    input_width = 200
    input_height = 50
    input_box = pygame.Rect(540, 420, input_width, input_height)
    color_inactive = pygame.Color('azure3')
    color_active = pygame.Color('darkgoldenrod4')
    color = color_inactive
    Titlefont=pygame.font.SysFont("cambria", 75)
    menu_text = Titlefont.render("Locked Escaped: E.T.", True, "#bcbcbc")
    menu_rect = menu_text.get_rect(center = (640, 150))
    in_text = headingfont.render("Enter Your LeetCode Username", True, 'lightsalmon4')
    in_rect = in_text.get_rect(center = (640, 300))
    warning_text = errorfont.render("Make sure it is correct!", True, 'lightsalmon4')
    warning_rect = warning_text.get_rect(center = (640, 350))
    

    active = False
    check = True
    text = ''
    block_img = pygame.image.load("data/images/Play.png")

   
    while True:
        screen.fill((30, 30, 30))

        #input text rendering/adjustment
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        

        # Blit the text and background.
        screen.blit(background,(0,0))
        #screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(menu_text, menu_rect)
        screen.blit(txt_surface, input_box)
        screen.blit(in_text, in_rect)
        screen.blit(warning_text, warning_rect)
        if(width > 200):
            fake = font.render("ahhh its so long", True, "#bcbcbc")
            fake_rect = fake.get_rect(center = (width, 440))
            screen.blit(fake, fake_rect)


        #Back Button
        mouse_pos = pygame.mouse.get_pos()
        back_button = Button(block_img, pos=(640, 600), 
                text_input="BACK", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
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
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        playerStats = verify(text)
                        if(playerStats):
                            main(playerStats)
                            return
                            
                        text = ''

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            
        #verification blit
        if(not check):
            fake = errorfont.render("Username not found, please try again", True, 'firebrick2')
            fake_rect = fake.get_rect(center = (640, 500))
            screen.blit(fake, fake_rect)

        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        #clock.tick(30)


def verify(text):

    url = "https://leetcode-stats-api.herokuapp.com/" + text
    #print(url)

    playerDict = json.loads(
        requests.get(
            url
        ).text
    )
    if(playerDict["status"] != "success"):
        return None
    playerDict["username"] = text
    return playerDict

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