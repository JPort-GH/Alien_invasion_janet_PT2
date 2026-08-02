"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Purpose: Manage the main game loop, events, and milestone 2 gameplay.
"""

import sys

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage the game assets and behavior."""

    def __init__(self):
        """Initialize the game window, HUD, and sprites."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion - Track 1")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sb.show_status_message("Press Play to begin")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "Play")
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_ammo()
            self.sb.show_status_message("Good luck, destroy the fleet!")

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if self.stats.ammo_left <= 0:
            self.stats.game_active = False
            self.sb.show_status_message(
                "Game over — you ran out of ammo. Click Play to restart."
            )
            pygame.mouse.set_visible(True)
            return

        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        self.stats.ammo_left -= 1
        self.sb.prep_ammo()
        self.sb.show_status_message("Bullet fired!")

    def _update_bullets(self):
        """Update bullet positions and remove bullets that leave the screen."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.stats.score += len(collisions)
            self.sb.prep_score()
            self.sb.prep_ammo()
            self.sb.check_high_score()
            self.sb.show_status_message("Alien destroyed!")

        if not self.aliens:
            self.bullets.empty()
            self.stats.level += 1
            self.settings.alien_speed = self.settings.base_alien_speed * self.stats.level
            self.settings.fleet_drop_speed = self.settings.base_fleet_drop_speed * self.stats.level
            self.sb.prep_level()
            self.sb.show_status_message(
                f"Level {self.stats.level}! Incredible work!",
                message_color=self.settings.accent_color,
                flash=True,
            )
            self._create_fleet()

    def _update_aliens(self):
        """Update alien positions and handle collisions and loss conditions."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_left()

    def _check_fleet_edges(self):
        """Respond if any aliens reach an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the fleet and reverse its direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond when the ship is hit by an alien."""
        if self.stats.ships_left <= 0:
            self.stats.game_active = False
            self.sb.show_status_message(
                "Game over — you died. Click Play to restart."
            )
            pygame.mouse.set_visible(True)
            return

        self.stats.ships_left -= 1
        self.sb.prep_ships()

        self.aliens.empty()
        self.bullets.empty()
        self.ship.center_ship()

        if self.stats.ships_left <= 0:
            self.stats.game_active = False
            self.sb.show_status_message(
                "Game over — you died. Click Play to restart."
            )
            pygame.mouse.set_visible(True)
            return

        if self.stats.ships_left == 1:
            self.sb.show_status_message("One life remaining, stay sharp!")
        else:
            self.sb.show_status_message(
                f"Ship lost, {self.stats.ships_left} lives remaining."
            )

        self._create_fleet()

    def _check_aliens_left(self):
        """Check if the fleet has reached the left edge behind the ship."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create a vertical column of aliens on the right side of the screen."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_y = self.settings.screen_height - (2 * alien_height)
        number_rows = int(available_space_y // (2 * alien_height))

        for row in range(number_rows):
            self._create_alien(row)

    def _create_alien(self, row):
        """Create an alien and place it in the given row on the right side."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        alien.rect.x = self.settings.screen_width - alien_width
        alien.rect.y = alien_height + 2 * alien_height * row
        alien.x = float(alien.rect.x)

        self.aliens.add(alien)

    def _update_screen(self):
        """Update the images on the screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
