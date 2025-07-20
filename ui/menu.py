"""menu.py - Menú principal con créditos Yeison Arbey Carrillo Lemus."""

import pygame
import logging
from typing import List
from .button import Button
from utils.config import GameConfig

logger = logging.getLogger(__name__)

class MainMenu:
    def __init__(self, screen: pygame.Surface, config: GameConfig, clock: pygame.time.Clock):
        self.screen = screen
        self.config = config
        self.clock = clock
        self.buttons = self._create_buttons()
        self.background = self._create_background()
        logger.info("Menú principal inicializado")

    def _create_buttons(self) -> List[Button]:
        button_width = 250
        button_height = 60
        center_x = self.screen.get_width() // 2 - button_width // 2
        
        return [
            Button(
                rect=pygame.Rect(center_x, 300, button_width, button_height),
                text="JUGAR",
                action=self.start_game,
                normal_color=(70, 130, 200),
                hover_color=(100, 160, 230),
                text_color=(255, 255, 255),
                font_size=32,
                border_radius=10
            ),
            Button(
                rect=pygame.Rect(center_x, 380, button_width, button_height),
                text="SALIR",
                action=self.quit_game,
                normal_color=(200, 70, 70),
                hover_color=(230, 100, 100),
                text_color=(255, 255, 255),
                font_size=32,
                border_radius=10
            )
        ]

    def _create_background(self) -> pygame.Surface:
        background = pygame.Surface(self.screen.get_size())
        background.fill(pygame.Color("lightblue"))
        
        # Título
        title_font = pygame.font.Font(None, 82)
        title_text = title_font.render("SNEAK", True, pygame.Color("dodgerblue"))
        title_pos = (self.screen.get_width() // 2 - title_text.get_width() // 2, 100)
        background.blit(title_text, title_pos)
        
        # Créditos YACL
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("by Yeison Arbey Carrillo Lemus - 200725", True, pygame.Color("Black"))
        subtitle_pos = (self.screen.get_width() // 2 - subtitle_text.get_width() // 2, 200)
        background.blit(subtitle_text, subtitle_pos)
        
        return background

    def start_game(self):
        from game.board import GameBoard
        logger.info("Iniciando nueva partida")
        game = GameBoard(self.screen, self.config)
        return game.run()

    def quit_game(self):
        logger.info("Saliendo del juego")
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def run(self):
        logger.info("Mostrando menú principal")
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in self.buttons:
                    button.handle_event(event)
            
            self.screen.blit(self.background, (0, 0))
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(self.config.fps)