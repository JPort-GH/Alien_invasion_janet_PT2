"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026
"""

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A horizontally-moving ship positioned on the bottom of the screen."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_image)
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_left = False
        self.moving_right = False

    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        """Center the ship on the bottom of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
