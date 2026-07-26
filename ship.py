"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026
"""

import pygame
from pathlib import Path

class Ship:
    """A vertically-moving ship positioned on the left side of the screen."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image using pathlib
        self.image = pygame.image.load(self.settings.ship_image)
        self.rect = self.image.get_rect()

        # Ship starts on the left edge, centered vertically
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the ship's vertical position
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
