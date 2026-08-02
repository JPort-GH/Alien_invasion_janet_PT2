"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Purpose: Define the alien sprite for the horizontal fleet.
"""

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Represent a single alien in the horizontal fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and place it near the right edge of the screen."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load(self.settings.alien_image)
        self.rect = self.image.get_rect()
        self.rect.x = self.settings.screen_width - self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if the alien reaches the left edge of the screen."""
        return self.rect.left <= 0

    def update(self):
        """Move the alien horizontally according to the fleet direction."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
