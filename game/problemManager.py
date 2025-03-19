import pygame
import webbrowser
import requests
import json
import threading
import time
import constants as c

class LeetcodeManager:
    """Class to handle opening leetcode and detect when problems are solved."""

    lock = threading.Lock()

    def __init__(self):
        """Constructor."""
        self.username = None
        self.stats = None
        self.totalSolved = 0

        # TODO: For testing purposes only
        self.numRequests = 0

    def handle_event(self, event: pygame.Event) -> None:
        """Handle events off the event queue."""
        if event.type == c.OPEN_PROBLEM:
            webbrowser.open(event.url)
            url = "https://leetcode-stats-api.herokuapp.com/" + self.username
            apiRequestThread = threading.Thread(target=self.check_stats, args=(url,))
            apiRequestThread.start()
        elif event.type == c.USER_LOGIN:
            self.username = event.username
            self.stats = event.stats
            self.totalSolved = self.stats["totalSolved"]

    def check_stats(self, url) -> None:
        """Get the player's leetcode stats.
        
            url: The API endpoint to request.
        """
        LeetcodeManager.lock.acquire_lock()
        while self.numRequests < 5:
            print("getting player's stats")
            LeetcodeManager.lock.release_lock()
            playerStats = json.loads(
                requests.get(
                    url
                ).text
            )
            LeetcodeManager.lock.acquire_lock()
            if playerStats["status"] == "success":
                self.numRequests += 1
        LeetcodeManager.lock.release_lock()

    def update(self) -> None:
        LeetcodeManager.lock.acquire_lock()
        if self.numRequests == 5:
            print("Got a lot of requests!")
            self.numRequests = 0
            pygame.event.post(pygame.Event(c.PROBLEM_SOLVED))
        LeetcodeManager.lock.release_lock()
