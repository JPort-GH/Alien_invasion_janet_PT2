"""
Author: Janet Portillo
GitHub: JPort-GH
Course: CSCI-1511 – Python Programming
Professor: Walters
Assignment: Alien Invasion – Part 2 (Unit 7)
Date: 07.12.2026

Description:
This file manages the main game loop, event handling, rendering, and
fleet-related helper functions for calculating alien grid dimensions.
"""

import sys
import pygame
from settings import Settings
from ship import Ship
from laser import Laser

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )
        pygame.display.set_caption(self.settings.name)

        # Background
        self.bg_image = pygame.image.load(self.settings.bg_file)

        # Intro sound
        pygame.mixer.Sound(self.settings.intro_sound).play()

        # Ship
        self.ship = Ship(self)

        # Lasers
        self.lasers = pygame.sprite.Group()

        self.running = True
        self.clock = pygame.time.Clock()

    def run_game(self) -> None:
        """Start the main loop for the game."""
        while self.running:
            self._check_events()
            self.ship.update()
            self.lasers.update()

            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE:
                    self._fire_laser()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    # -------------------------------------------------------------
    # Fleet Math Helpers (Unit 7 - Part 2)
    # -------------------------------------------------------------
    def _get_number_aliens_x(self, alien_width):
        """Calculate how many aliens fit in one row."""
        available_space_x = self.settings.screen_w - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        return number_aliens_x

    def _get_number_rows(self, alien_height, ship_height):
        """Calculate how many rows of aliens fit on the screen."""
        available_space_y = (
            self.settings.screen_h -
            (3 * alien_height) -
            ship_height
        )
        number_rows = available_space_y // (2 * alien_height)
        return number_rows

    def _fire_laser(self):
        """Create a new laser and add it to the group."""
        new_laser = Laser(self)
        self.lasers.add(new_laser)

    def _update_screen(self):
        """Draw everything."""
        self.screen.blit(self.bg_image, (0, 0))
        self.ship.blitme()

        for laser in self.lasers.sprites():
            laser.draw_laser()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
