"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026

Description:
This file is part of the Alien Invasion PT2 project, implementing the
Unit 7 features including alien fleet creation, movement, collision
detection, and game state management.
"""

import pygame
from pathlib import Path
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class representing a single alien."""

    def __init__(self, ai_game, boss=False):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.is_boss = boss

        asset_path = Path(__file__).resolve().parent / "Assets" / "images" / "enemy_4.png"
        self.image = pygame.image.load(asset_path)
        if self.is_boss:
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
            self.hit_points = 6
            self.points = self.settings.boss_points
        else:
            self.hit_points = 1
            self.points = self.settings.alien_points

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        """Move alien left or right."""
        speed = self.settings.alien_speed * (2 if self.is_boss else 1)
        self.x += speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien hits screen edge."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
