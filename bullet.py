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
    """A bullet fired vertically from the ship."""

    def __init__(self, ai_game):
        """Create a bullet at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midbottom = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet vertically upward."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
