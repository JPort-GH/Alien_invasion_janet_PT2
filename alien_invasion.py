# Name: Janet Portillo
# GitHub: JPort-GH
# Date: 07.12.2026

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
