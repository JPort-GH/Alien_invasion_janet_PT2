"""
Author: Janet Portillo
GitHub: JPort-GH
Course: CSCI-1511 – Python Programming
Professor: Walters
Assignment: Alien Invasion – Part 2
Date: 07.12.2026
"""

from pathlib import Path

class Settings:
    """Store all game settings."""

    def __init__(self) -> None:
        self.name = "Alien Invasion"
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60

        # Professor's intro background (blank/no background)
        self.bg_file = Path.cwd() / "Assets" / "images" / "no_background.png"

        # Sounds
        self.intro_sound = Path.cwd() / "Assets" / "sounds" / "intro.wav"
        self.laser_sound = Path.cwd() / "Assets" / "sounds" / "laser.wav"

        # Ship settings
        self.ship_speed = 3
        self.ship_limit = 3  # Part 2: lives

        # Laser/Bullet settings
        self.laser_speed = 6
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_allowed = 3

        # Alien / fleet settings (Part 2)
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 = right, -1 = left

