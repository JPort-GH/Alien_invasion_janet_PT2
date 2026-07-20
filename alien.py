"""
Author: Janet Portillo
Course: CSCI-1511 – Python Programming
Professor: Walters
Assignment: Alien Invasion – Part 2 
Date: July 2026

Description:
This file is part of the Alien Invasion PT2 project, implementing the
Unit 7 features including alien fleet creation, movement, collision
detection, and game state management.
"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class representing a single alien."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("Assets/images/alien.png")
        self.rect = self.image.get_rect()

        # Start near top-left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        """Move alien left or right."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien hits screen edge."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
