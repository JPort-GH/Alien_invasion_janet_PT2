"""
Author: Janet Portillo
Course: CSCI-1511 – Python Programming
Professor: Walters
Assignment: Alien Invasion – Part 2 (Unit 7)
Date: July 2026

Description:
This file is part of the Alien Invasion PT2 project, implementing the
Unit 7 features including alien fleet creation, movement, collision
detection, and game state management.
"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class representing a single alien in the fleet."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each alien near the top-left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the screen edge."""
        screen_rect = self.screen.get_rect()
        return (
            self.rect.right >= screen_rect.right or
            self.rect.left <= 0
        )

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.fleet_speed * self.settings.fleet_direction
        self.rect.x = self.x
