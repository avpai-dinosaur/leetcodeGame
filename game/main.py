import pygame

# Pygame needs to be initialized before other modules can be imported
pygame.init()

import constants as c
from world import Game
from menu import MainMenu, OptionsMenu, LoginMenu, YouDiedMenu

class GameManager:
    def __init__(self):
        self.states = {
            "menu": MainMenu(self),
            "options": OptionsMenu(self),
            "login": LoginMenu(self),
            "world": Game(self, {}),
            "died": YouDiedMenu(self)
        }
        self.active_state = self.states["menu"]

    def set_state(self, state_name):
        pygame.display.set_caption(state_name)
        self.active_state = self.states[state_name]

    def handle_event(self, event):
        self.active_state.handle_event(event)

    def update(self):
        self.active_state.update()

    def draw(self, screen):
        self.active_state.draw(screen)

def main(screen):
    pygame.display.set_caption("EscapeCodes")
    clock = pygame.time.Clock()
    manager = GameManager()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            manager.handle_event(event)
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        manager.update()
        manager.draw(screen)

        # flip() the display to put work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

if __name__ == "__main__":
    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    main(screen)
    pygame.quit()
