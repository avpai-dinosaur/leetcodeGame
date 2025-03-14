import pygame
import webbrowser
import requests
import json
import constants as c

class LeetcodeManager:
    """Class to handle opening leetcode and detect when problems are solved."""

    def __init__(self):
        """Constructor."""
        self.username = None
        self.stats = None
        self.totalSolved = 0
        self.lastRequest = pygame.time.get_ticks()
        self.checkStats = False

    def handle_event(self, event: pygame.Event) -> None:
        """Handle events off the event queue."""
        if event.type == c.OPEN_PROBLEM:
            webbrowser.open(event.url)
            self.checkStats = True
        elif event.type == c.USER_LOGIN:
            self.username = event.username
            self.stats = event.stats
            self.totalSolved = self.stats["totalSolved"]

    def update(self) -> None:
        # TODO: needs to be on a separate thread
        if self.checkStats and pygame.time.get_ticks() - self.lastRequest > 1000:
            self.lastRequest = pygame.time.get_ticks()
            url = "https://leetcode-stats-api.herokuapp.com/" + self.username
            playerStats = json.loads(
                requests.get(
                    url
                ).text
            )
            if playerStats["status"] == "success":
                totalSolved = playerStats["totalSolved"]
                if self.totalSolved < totalSolved:
                    self.totalSolved = totalSolved
                    self.checkStats = False