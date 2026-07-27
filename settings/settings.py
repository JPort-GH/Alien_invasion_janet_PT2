"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026
"""

from pathlib import Path

class Settings:
    """A class to store all settings for the Track 1 side-scrolling game."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (8, 18, 42)
        self.text_color = (245, 245, 245)
        self.accent_color = (255, 95, 95)
        self.panel_color = (20, 32, 58)
        self.button_color = (15, 132, 90)
        self.button_text_color = (255, 255, 255)
        self.button_border_color = (255, 255, 255)
        self.status_message_color = (255, 220, 120)
        self.hud_padding = 20
        self.ship_icon_spacing = 16

        # Ship settings (vertical movement)
        self.ship_speed = 3.0
        self.ship_limit = 3

        # Bullet settings (horizontal)
        self.bullet_speed = 6.0
        self.bullet_width = 6
        self.bullet_height = 3
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3
        self.starting_ammo = 12
        self.max_ammo = 12
        self.reload_delay = 3.0
        self.alien_points = 50

        # Alien fleet settings
        self.base_alien_speed = 0.5
        self.base_fleet_drop_speed = 5
        self.alien_speed = self.base_alien_speed
        self.fleet_drop_speed = self.base_fleet_drop_speed
        self.fleet_direction = 1
        self.boss_points = 300

        # Asset paths using pathlib
        self.asset_dir = Path(__file__).resolve().parents[1] / "Assets" / "images"
        self.ship_image = self.asset_dir / "ship.png"
        self.bullet_image = self.asset_dir / "laserBlast.png"

    def initialize_dynamic_settings(self):
        """Reset settings that change during play."""
        self.ship_speed = 3.0
        self.bullet_speed = 6.0
        self.alien_speed = self.base_alien_speed
        self.fleet_drop_speed = self.base_fleet_drop_speed
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase the speed of the game elements."""
        self.ship_speed *= 1.1
        self.bullet_speed *= 1.1
        self.alien_speed *= 1.1
        self.fleet_drop_speed *= 1.1
