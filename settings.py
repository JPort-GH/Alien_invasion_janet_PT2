"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Purpose: Store the game settings used by the milestone 2 version.
"""

from pathlib import Path


class Settings:
    """Store all adjustable settings for the game."""

    def __init__(self):
        """Initialize the static settings for the game."""
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.text_color = (250, 250, 250)
        self.status_message_color = (180, 220, 255)
        self.accent_color = (255, 102, 102)
        self.panel_color = (24, 24, 32)
        self.button_color = (40, 40, 60)
        self.button_text_color = (250, 250, 250)
        self.button_border_color = (255, 102, 102)
        self.hud_padding = 16
        self.ship_icon_spacing = 8

        self.asset_dir = Path(__file__).resolve().parent / "Assets" / "images"
        self.ship_image = self.asset_dir / "ship.png"

        self.ship_speed = 1.5
        self.ship_limit = 3

        self.bullet_speed = 2.5
        self.bullet_width = 8
        self.bullet_height = 4
        self.bullet_color = (255, 255, 255)

        self.starting_ammo = 10
        self.max_ammo = 10

        self.alien_points = 50
        self.boss_points = 200

        self.base_alien_speed = 0.5
        self.base_fleet_drop_speed = 5
        self.alien_speed = self.base_alien_speed
        self.fleet_drop_speed = self.base_fleet_drop_speed
        self.fleet_direction = -1
        self.alien_image = self.asset_dir / "enemy_4.png"

    def initialize_dynamic_settings(self):
        """Reset the settings that change each playthrough."""
        self.alien_speed = self.base_alien_speed
        self.fleet_drop_speed = self.base_fleet_drop_speed
        self.fleet_direction = -1
