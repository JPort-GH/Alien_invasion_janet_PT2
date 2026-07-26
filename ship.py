"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026
"""

import pygame

class Ship:
    """Class to manage the player's ship."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load("Assets/images/ship.png")
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flags
        self.moving_right = False
        self.moving_left = False

        # Store float position for smooth movement
        self.x = float(self.rect.x)

    def update(self):
        """Move ship left/right."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """Draw the ship."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship after a hit."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
