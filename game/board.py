"""
board.py - Tablero de juego principal con todos los métodos corregidos.
"""

import pygame
import logging
from typing import Tuple
from .snake import Snake
from .fruit import Fruit
from utils.config import GameConfig

logger = logging.getLogger(__name__)

class GameBoard:
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        self.screen = screen
        self.config = config
        self.snake = Snake(screen, config.cell_size)
        self.fruit = Fruit(screen, config.cell_size)
        self.score = 0
        self.running = False
        self.clock = pygame.time.Clock()
        logger.info("Tablero de juego inicializado")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key):
        key_directions = {
            pygame.K_UP: 'UP',
            pygame.K_DOWN: 'DOWN',
            pygame.K_LEFT: 'LEFT',
            pygame.K_RIGHT: 'RIGHT'
        }
        
        if key in key_directions:
            self.snake.change_direction(key_directions[key])
        elif key == pygame.K_ESCAPE:
            self.running = False

    def update(self):
        current_time = pygame.time.get_ticks()
        self.snake.move(current_time)
        
        if self.snake.body[0] == self.fruit.position:
            self.snake.grow()
            self.fruit.spawn(self.snake.body)
            self.score += 10
            logger.info(f"Nuevo puntaje: {self.score}")
        
        board_size = (
            self.screen.get_width() // self.config.cell_size,
            self.screen.get_height() // self.config.cell_size
        )
        if self.snake.check_collision(board_size):
            self.running = False
            logger.info(f"Juego terminado. Puntaje final: {self.score}")
            return self.score

    def draw(self):
        self.screen.fill(pygame.Color(self.config.bg_color))
        self.snake.draw()
        self.fruit.draw()
        self._draw_score()
        pygame.display.flip()

    def _draw_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Puntaje: {self.score}", True, pygame.Color('white'))
        self.screen.blit(score_text, (10, 10))

    def run(self):
        self.running = True
        self.score = 0
        self.snake.reset()
        self.fruit.spawn(self.snake.body)
        
        logger.info("Iniciando partida")
        
        while self.running:
            self.handle_events()
            final_score = self.update()
            if final_score is not None:
                return final_score
            self.draw()
            self.clock.tick(self.config.fps)