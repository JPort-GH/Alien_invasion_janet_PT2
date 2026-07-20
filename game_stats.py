"""
Author: Janet Portillo
Course: CSCI-1511 – Python Programming
Professor: Walters
Assignment: Alien Invasion – Part 2 
Date: July 2026
"""

class GameStats:
    """Track game statistics for Alien Invasion."""

    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        """Initialize stats that change during the game."""
        self.ships_left = self.settings.ship_limit
