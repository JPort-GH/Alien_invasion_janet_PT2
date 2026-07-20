# Name: Janet Portillo
# GitHub: JPort-GH
# Date: 07.12.2026

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

        # Laser settings
        self.laser_speed = 6
