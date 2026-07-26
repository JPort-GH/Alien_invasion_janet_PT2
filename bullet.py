"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026

Description: Horizontal laser fired from left-side ship.
"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A bullet fired horizontally from the ship."""

    def __init__(self, ai_game):
        """Create a bullet at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Bullet starts at ship mid-right
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midleft = ai_game.ship.rect.midright

        # Store bullet's horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet horizontally to the right."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
