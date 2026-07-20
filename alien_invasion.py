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
from alien import Alien
from game_stats import GameStats


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self.settings = Settings()

        # Screen setup
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

        # Game stats
        self.stats = GameStats(self.settings)

        # Aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.clock = pygame.time.Clock()

    # -------------------------------------------------------------
    # Main Game Loop
    # -------------------------------------------------------------
    def run_game(self) -> None:
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.lasers.update()
                self._update_lasers()
                self._update_aliens()
                self._check_bullet_alien_collisions()

            self._update_screen()
            self.clock.tick(self.settings.FPS)

    # -------------------------------------------------------------
    # Event Handling
    # -------------------------------------------------------------
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_laser()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # -------------------------------------------------------------
    # Laser Handling
    # -------------------------------------------------------------
    def _fire_laser(self):
        """Create a new laser and add it to the group."""
        if len(self.lasers) < self.settings.bullet_allowed:
            new_laser = Laser(self)
            pygame.mixer.Sound(self.settings.laser_sound).play()
            self.lasers.add(new_laser)

    def _update_lasers(self):
        """Remove lasers that have disappeared."""
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

    # -------------------------------------------------------------
    # Fleet Math Helpers (Part 2)
    # -------------------------------------------------------------
    def _get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_w - (2 * alien_width)
        return available_space_x // (2 * alien_width)

    def _get_number_rows(self, alien_height, ship_height):
        available_space_y = (
            self.settings.screen_h -
            (3 * alien_height) -
            ship_height
        )
        return available_space_y // (2 * alien_height)

    # -------------------------------------------------------------
    # Fleet Creation (Part 2)
    # -------------------------------------------------------------
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        number_aliens_x = self._get_number_aliens_x(alien_width)
        number_rows = self._get_number_rows(alien_height, self.ship.rect.height)

        self.aliens.empty()
        for row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x

        alien.rect.y = alien_height + 2 * alien_height * row_number

        self.aliens.add(alien)

    # -------------------------------------------------------------
    # Fleet Movement & Collisions (Part 2)
    # -------------------------------------------------------------
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.lasers, self.aliens, True, True
        )

        if not self.aliens:
            self.lasers.empty()
            self._create_fleet()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.lasers.empty()

            self.ship.center_ship()
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    # -------------------------------------------------------------
    # Drawing
    # -------------------------------------------------------------
    def _update_screen(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.ship.blitme()

        for laser in self.lasers.sprites():
            laser.draw_laser()

        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
