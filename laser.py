"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026
"""
import pygame
from pygame.sprite import Sprite

class Laser(Sprite):
    """A class to manage lasers fired from the ship."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255, 0, 0)

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Move the laser up the screen."""
        self.y -= self.settings.laser_speed
        self.rect.y = self.y

    def draw_laser(self):
        """Draw the laser to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
