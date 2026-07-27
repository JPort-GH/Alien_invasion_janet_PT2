"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026
"""
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scoreboard attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = self.settings.text_color
        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 28)
        self.status_message = ""
        self.status_image = None
        self.status_rect = None
        self.status_color = self.settings.status_message_color
        self.status_flash = False
        self.status_flash_until = 0

        self.ammo_image = None
        self.ammo_rect = None

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_ammo()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(f"Score: {score_str}", True,
                                            self.text_color,
                                            self.settings.bg_color)

        # Display the score at the top left of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.settings.hud_padding
        self.score_rect.top = self.settings.hud_padding + 6

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(f"High: {high_score_str}", True,
                                                 self.text_color,
                                                 self.settings.bg_color)

        # Position the high score near the top right.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - self.settings.hud_padding
        self.high_score_rect.top = self.settings.hud_padding + 6

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(f"Level: {level_str}", True,
                                            self.text_color,
                                            self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.score_rect.left
        self.level_rect.top = self.score_rect.bottom + 6

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = self.settings.hud_padding + 4 + ship_number * (ship.rect.width + self.settings.ship_icon_spacing)
            ship.rect.y = self.level_rect.bottom + 8
            self.ships.add(ship)

    def prep_ammo(self):
        """Render the ammo count in the top-right HUD area."""
        ammo_text = f"Ammo: {self.stats.ammo_left}"
        self.ammo_image = self.font.render(ammo_text, True, self.text_color, self.settings.bg_color)
        self.ammo_rect = self.ammo_image.get_rect()
        self.ammo_rect.right = self.screen_rect.right - self.settings.hud_padding
        self.ammo_rect.top = self.high_score_rect.bottom + 6

    def show_status_message(self, message, message_color=None, flash=False, flash_duration_ms=1400):
        """Display a temporary status message for gameplay feedback."""
        self.status_message = message
        self.status_color = message_color or self.settings.status_message_color
        self.status_flash = flash
        self.status_flash_until = pygame.time.get_ticks() + flash_duration_ms if flash else 0
        self._render_status_message()

    def _render_status_message(self):
        """Render the current status message with optional flashing."""
        color = self.status_color
        if self.status_flash and pygame.time.get_ticks() < self.status_flash_until:
            color = self.settings.accent_color if (pygame.time.get_ticks() // 180) % 2 == 0 else self.settings.text_color
        self.status_image = self.small_font.render(self.status_message, True, color, self.settings.bg_color)
        self.status_rect = self.status_image.get_rect()
        self.status_rect.centerx = self.screen_rect.centerx
        self.status_rect.top = self.level_rect.bottom + 16

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        hud_panel = pygame.Rect(10, 10, self.screen_rect.width - 20, 140)
        pygame.draw.rect(self.screen, self.settings.panel_color, hud_panel)
        pygame.draw.rect(self.screen, self.settings.accent_color, hud_panel, 2)

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ammo_image, self.ammo_rect)
        self.ships.draw(self.screen)

        if self.status_message:
            self._render_status_message()
            message_bg = self.status_rect.inflate(24, 12)
            pygame.draw.rect(self.screen, self.settings.panel_color, message_bg)
            pygame.draw.rect(self.screen, self.settings.accent_color, message_bg, 2)
            self.screen.blit(self.status_image, self.status_rect)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
