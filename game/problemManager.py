import pygame
import webbrowser
import requests
import json
import threading
import time
from queue import Queue
import constants as c

class LeetcodeManager:
    """Class to handle opening leetcode and detect when problems are solved."""

    lock = threading.Lock()

    def __init__(self):
        """Constructor."""
        self.username = None
        self.stats = None
        self.totalSolved = 0

        self.inProgressProblems = set()

    def handle_event(self, event: pygame.Event) -> None:
        """Handle events off the event queue."""
        if event.type == c.OPEN_PROBLEM:
            webbrowser.open(event.url)
            # TODO: Kind of a hacky way to do this
            problemSlug = event.url.split('/')[4]
            self.inProgressProblems.add(problemSlug)
            apiRequestThread = threading.Thread(target=self.check_submissions, args=(problemSlug, event.timestamp))
            apiRequestThread.start()
        elif event.type == c.USER_LOGIN:
            self.username = event.username
            self.stats = event.stats
            self.totalSolved = self.stats["totalSolved"]

    def check_submissions(self, problemSlug: str, lowerTimestamp: int) -> None:
        LeetcodeManager.lock.acquire_lock()
        url = "https://leetcode.com/graphql"
        payload = {
            "query" :
                """
                query recentAcSubmissions($username: String!, $limit: Int!) {
                    recentAcSubmissionList(username: $username, limit: $limit) {
                        id
                        title
                        titleSlug
                        timestamp
                    }
                }
                """,
            "variables" : {
                "username" : self.username,
                "limit" : 5
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        while problemSlug in self.inProgressProblems:
            LeetcodeManager.lock.release_lock()
            # TODO: check recent submissions when player tries to open door to avoid spamming requests
            time.sleep(3) 
            response = requests.get(url, json=payload, headers=headers)
            recentSubmissions = json.loads(response.text)["data"]
            LeetcodeManager.lock.acquire_lock()
            if response.status_code == 200:
                self.was_problem_solved(
                    problemSlug,
                    recentSubmissions["recentAcSubmissionList"],
                    lowerTimestamp
                )
        LeetcodeManager.lock.release_lock()
    
    def was_problem_solved(
        self,
        problemSlug: str,
        submissionList: list,
        lowerTimestamp: int
    ):
        """Given a list of submissions, check if the given problem was solved.
        
            problemSlug: url slug assigned to the problem by leetcode
            submissionList: list of user's recent submissions
            lowerTimestamp: time the submission should have occured after to be considered valid
        """
        for submission in submissionList:
            if submission["titleSlug"] == problemSlug \
                and int(submission["timestamp"]) >= lowerTimestamp:
                self.inProgressProblems.remove(problemSlug)
                pygame.event.post(pygame.Event(c.PROBLEM_SOLVED))
                return
            
    def update(self):
        """Update to run each game loop."""
        pass
