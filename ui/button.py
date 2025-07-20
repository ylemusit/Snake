"""button.py - Botones personalizados."""

import pygame
from typing import Callable, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        action: Optional[Callable] = None,
        normal_color: Tuple[int, int, int] = (100, 100, 100),
        hover_color: Tuple[int, int, int] = (150, 150, 150),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        font_size: int = 32,
        border_radius: int = 0
    ):
        self.rect = rect
        self.text = text
        self.action = action
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.border_radius = border_radius
        self.is_hovered = False
        self.font = pygame.font.Font(None, font_size)
        logger.debug(f"Botón creado: {text}")

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                logger.info(f"Botón clickeado: {self.text}")
                self.action()
                return True
        return False

    def draw(self, surface: pygame.Surface):
        color = self.hover_color if self.is_hovered else self.normal_color
        pygame.draw.rect(
            surface, color, self.rect, 
            border_radius=self.border_radius
        )
        pygame.draw.rect(
            surface, (0, 0, 0), self.rect, 
            2, self.border_radius
        )
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)