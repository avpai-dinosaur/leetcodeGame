import pygame
import sys
import requests
import json
from world import World
from button import Button
import constants as c

def menu(Start):
    pygame.display.set_caption("Menu")
    Titlefont=pygame.font.SysFont("cambria", 75)
    play_img = pygame.image.load("data/images/Play.png")
    #play_img dimentions: 370 x 109 px
    leaderboard_img = pygame.image.load("data/images/Options.png")
    #leaderboard_img dimentions: 585 x 109 px
    leadersize = (200, 50)
    leaderboard_img = pygame.transform.scale(leaderboard_img, leadersize)

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
        
        option_button = Button(play_img, pos=(640, 420), 
                text_input="OPTIONS", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(play_img, pos=(640, 540), 
                text_input="QUIT", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        leaderboard_button = Button(leaderboard_img, pos=(640, 680),
                text_input = "LEADERBOARD", font = pygame.font.SysFont("cambria", 20), base_color="azure4", hovering_color="White")
  
        screen.blit(menu_text, menu_rect)
        buttons = [main_button, option_button, quit_button, leaderboard_button]
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
                        #input
                        main(c.TEST_PLAYER_DICT)
                    else:
                        return
                if option_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if leaderboard_button.checkForInput(menu_mouse_pos):
                    leaderboard()

        pygame.display.flip()

def options():
    pygame.display.set_caption("options")
    Titlefont=pygame.font.SysFont("cambria", 75)
    block_img = pygame.image.load("data/images/Play.png")
    background = pygame.image.load("data/images/menu_background.png")
    while True:
        screen.blit(background,(0,0))
        mouse_pos = pygame.mouse.get_pos()
        option_text = Titlefont.render("OPTIONS", True, "#bcbcbc")
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


        #Quit Button
        mouse_pos = pygame.mouse.get_pos()
        quit_button = Button(block_img, pos=(640, 600), 
                text_input="QUIT", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        buttons = [quit_button]
        for button in buttons:
            button.changeColor(mouse_pos)
            button.update(screen)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.checkForInput(mouse_pos):

                    pygame.quit()
                    sys.exit()
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
                            menu(True)
                            #main(c.TEST_PLAYER_DICT)
                            
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
    
    return playerDict

def leaderboard():
    pygame.display.set_caption("Leaderboard")
    Titlefont=pygame.font.SysFont("cambria", 75)
    block_img = pygame.image.load("data/images/Play.png")
    background = pygame.image.load("data/images/menu_background.png")
    while True:
        screen.blit(background,(0,0))
        mouse_pos = pygame.mouse.get_pos()
        ltext = Titlefont.render("LEADERBOARD", True, "#bcbcbc")
        leader_rect = ltext.get_rect(center = (640, 150))
        back_button = Button(block_img, pos=(640, 600), 
                text_input="BACK", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        
        screen.blit(ltext, leader_rect)
        
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

def endscreen():
    pygame.display.set_caption("End Screen")
    Titlefont=pygame.font.SysFont("cambria", 75)
    block_img = pygame.image.load("data/images/Play.png")
    background = pygame.image.load("data/images/menu_background.png")
    while True:
        screen.blit(background,(0,0))
        mouse_pos = pygame.mouse.get_pos()
        ltext = Titlefont.render("YOU LOSE", True, "#bcbcbc")
        leader_rect = ltext.get_rect(center = (640, 150))
        quit_button = Button(block_img, pos=(640, 660), 
                text_input="QUIT", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        continue_button = Button(block_img, pos=(640, 540), 
                text_input="CONTINUE", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        screen.blit(ltext, leader_rect)
        
        buttons = [quit_button, continue_button]
        for button in buttons:
            button.changeColor(mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if continue_button.checkForInput(mouse_pos):
                    return

        pygame.display.update()



def main(playerDict):
    pygame.display.set_caption("Leetcode game")
    clock = pygame.time.Clock()
    world = World(screen, playerDict)
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
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            
            if(keys[pygame.K_ESCAPE]):
                menu(False)
            
            
            if(world.player.health.number() <= 0):
                running = False
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        world.update()
        world.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60


    print("here")
    endscreen()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    #main(c.TEST_PLAYER_DICT)
    #menu(True)
    input()