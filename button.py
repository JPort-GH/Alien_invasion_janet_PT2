"""
Author: Janet Portillo
GitHub: JPort-GH
Program: Alien Invasion - Track 1
Date: 07.22.2026
"""

import pygame.font

class Button:
    """A class to build a Play button."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 220, 58
        self.button_color = ai_game.settings.button_color
        self.text_color = ai_game.settings.button_text_color
        self.border_color = ai_game.settings.button_border_color
        self.font = pygame.font.SysFont(None, 46)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the button with a contrast-friendly border."""
        pygame.draw.rect(self.screen, self.border_color, self.rect, 3)
        pygame.draw.rect(self.screen, self.button_color, self.rect.inflate(-6, -6))
        self.screen.blit(self.msg_image, self.msg_image_rect)
