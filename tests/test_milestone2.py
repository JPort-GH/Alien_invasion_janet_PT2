import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship


class DummyGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.settings = Settings()
        self.ship = Ship(self)


class Milestone2Tests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = DummyGame()

    def test_horizontal_fleet_defaults(self):
        self.assertEqual(self.game.settings.fleet_direction, -1)
        self.assertGreater(self.game.settings.base_alien_speed, 0)
        self.assertEqual(self.game.settings.alien_speed, self.game.settings.base_alien_speed)

    def test_alien_starts_on_right_side(self):
        alien = Alien(self.game)
        self.assertGreater(alien.rect.x, 0)
        self.assertGreater(self.game.screen.get_rect().width, alien.rect.x)
        self.assertLess(alien.rect.x, self.game.screen.get_rect().width)

    def test_ship_starts_on_left_and_moves_vertically(self):
        ship = self.game.ship
        self.assertEqual(ship.rect.left, 0)
        self.assertEqual(ship.rect.centery, self.game.screen.get_rect().centery)

        initial_y = ship.rect.y
        ship.moving_up = True
        ship.update()
        self.assertLess(ship.rect.y, initial_y)

    def test_bullet_fires_horizontally(self):
        bullet = Bullet(self.game)
        initial_x = bullet.rect.x
        bullet.update()
        self.assertGreater(bullet.rect.x, initial_x)


if __name__ == "__main__":
    unittest.main()
