import pygame
from button import Button

class LevelMenu:
    """Represents a menu that shows up between levels."""
    
    def __init__(self, screen):
        self.width = screen.get_size()[0] * 0.75
        self.height = screen.get_size()[1] * 0.75
        center_x = screen.get_size()[0] * 0.5
        center_y = screen.get_size()[1] * 0.5
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (center_x, center_y)
        self.nextLevelButton = Button(None, pos=(center_x, center_y), 
                text_input="Next Level", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
    
    def takeover(self, screen, clock):
        running = True
        while running:
            for event in pygame.event.get():
                # pygame.QUIT event means the user clicked X to close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                keys = pygame.key.get_pressed()

                if(keys[pygame.K_ESCAPE]):
                    menu(False)

            self.draw(screen)
            if not self.update(screen):
                running = False

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.nextLevelButton.changeColor(mouse_pos)
        self.nextLevelButton.update(screen)
        if pygame.mouse.get_pressed()[0] and self.nextLevelButton.checkForInput(mouse_pos):
            return False
        return True

    def draw(self, surface):
        pygame.draw.rect(surface, (112, 125, 130), self.rect)
    
class EndMenu:
    """Represents the end game menu."""
    
    def __init__(self, screen):
        self.width = screen.get_size()[0] * 0.75
        self.height = screen.get_size()[1] * 0.75
        center_x = screen.get_size()[0] * 0.5
        center_y = screen.get_size()[1] * 0.5
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (center_x, center_y)
        self.exitButton = Button(None, pos=(center_x , center_y), 
                text_input="Back to Menu", font=pygame.font.SysFont("cambria", 40), base_color="#d7fcd4", hovering_color="White")
        # self.scoreButton = Button(None, pos=(center_x, center_y - 10),
        #     text_input=response["score"], font=pygame.font.SysFont("cambria", 40),
        #     base_color=("#24b345" if response["highScore"] else "#b32424"), hovering_color="White")
    
    def takeover(self, screen, clock):
        running = True
        while running:
            for event in pygame.event.get():
                # pygame.QUIT event means the user clicked X to close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
            keys = pygame.key.get_pressed()
            if(keys[pygame.K_ESCAPE]):
                running = False

            self.draw(screen)
            if not self.update(screen):
                running = False

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.exitButton.changeColor(mouse_pos)
        self.exitButton.update(screen)
        if pygame.mouse.get_pressed()[0] and self.exitButton.checkForInput(mouse_pos):
            return False
        return True

    def draw(self, surface):
        pygame.draw.rect(surface, (112, 125, 130), self.rect)