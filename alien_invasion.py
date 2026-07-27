"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026

Description:
This file manages the main game loop, event handling, rendering, and
fleet-related helper functions for calculating alien grid positions.
"""

import sys
from time import sleep, time

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
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
        self.boss_pending = False
        self.boss_spawn_time = None
        self.boss_active = False

        self._create_fleet()

        self.play_button = Button(self, "Play")

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
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            self.stats.ammo_left = self.settings.starting_ammo
            self.stats.reloading = False
            self.stats.reload_time = 0.0
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_ammo()
            self.sb.show_status_message("Good luck, destroy the fleet!")

            self.aliens.empty()
            self.bullets.empty()
            self.boss_pending = False
            self.boss_spawn_time = None
            self.boss_active = False

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if self.stats.reloading:
            self.sb.show_status_message("Reloading, wait 3 seconds.")
            return

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
        """Update bullet positions and remove old bullets."""
        if self.stats.reloading and time() >= self.stats.reload_time:
            self.stats.reloading = False
            self.stats.ammo_left = self.settings.max_ammo
            self.sb.prep_ammo()
            self.sb.show_status_message("Reload complete, ammo full.")

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)

        for alien_list in collisions.values():
            for alien in alien_list:
                if not isinstance(alien, Alien):
                    continue

                alien.hit_points -= 1
                if alien.hit_points <= 0:
                    if alien.is_boss:
                        self.boss_active = False
                    self.aliens.remove(alien)
                    self.stats.score += alien.points
                    if self.stats.ammo_left < self.settings.max_ammo:
                        self.stats.ammo_left += 1
                        self.sb.prep_ammo()
                        self.sb.show_status_message("Ammo Pick-Up!")
                    elif alien.is_boss:
                        self.sb.show_status_message("Boss destroyed!")
                else:
                    if alien.is_boss:
                        self.sb.show_status_message(
                            f"Boss hit, {alien.hit_points} left"
                        )
        if collisions:
            self.sb.prep_score()
            self.sb.prep_ammo()
            self.sb.check_high_score()

        if not self.aliens and not self.boss_pending and not self.boss_active:
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
            self.boss_pending = True
            self._create_fleet()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond if any aliens reach an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the fleet and change direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
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
        self.boss_pending = False
        self.boss_spawn_time = None
        self.boss_active = False
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
        pygame.display.flip()
        sleep(0.5)

    def _check_aliens_bottom(self):
        """Check if any aliens reach the bottom."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        sample_alien = Alien(self)
        normal_width, normal_height = sample_alien.rect.size

        base_rows = [6, 4, 2, 1]
        row_counts = base_rows.copy()
        for level_number in range(2, self.stats.level + 1):
            row_counts = [6 + 2 * (level_number - 1)] + row_counts
        row_spacing = 14
        y = self.settings.hud_padding + 140

        for row_index, count in enumerate(row_counts):
            if row_index == 0:
                if self.boss_pending:
                    boss = Alien(self, boss=True)
                    boss.rect.x = (self.settings.screen_width - boss.rect.width) / 2
                    boss.rect.y = int(y)
                    boss.x = float(boss.rect.x)
                    self.aliens.add(boss)
                    self.boss_pending = False
                    self.boss_active = True
                    y += boss.rect.height + row_spacing
                    continue

                boss = Alien(self, boss=True)
                boss.rect.x = (self.settings.screen_width - boss.rect.width) / 2
                boss.rect.y = int(y)
                boss.x = float(boss.rect.x)
                self.aliens.add(boss)
                y += boss.rect.height + row_spacing
                continue

            if count == 1:
                x = (self.settings.screen_width - normal_width) / 2
                self._create_alien_at(x, y)
                y += normal_height + row_spacing
                continue

            if count <= 1:
                x = (self.settings.screen_width - normal_width) / 2
                self._create_alien_at(x, y)
                y += normal_height + row_spacing
                continue

            spacing = max(6, (self.settings.screen_width - self.settings.hud_padding * 2 - count * normal_width) / (count - 1))
            total_width = count * normal_width + (count - 1) * spacing
            start_x = (self.settings.screen_width - total_width) / 2
            for alien_number in range(count):
                x = start_x + alien_number * (normal_width + spacing)
                self._create_alien_at(x, y)
            y += normal_height + row_spacing

    def _create_alien_at(self, x, y, boss=False):
        """Create an alien at the given position."""
        alien = Alien(self, boss=boss)
        alien.rect.x = int(x)
        alien.rect.y = int(y)
        alien.x = float(alien.rect.x)
        self.aliens.add(alien)

    def _update_screen(self):
        """Update images on the screen."""
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
