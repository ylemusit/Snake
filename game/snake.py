"""
snake.py - Implementación completa de la serpiente con todos los métodos necesarios.
"""

import pygame
import logging
from typing import Tuple, List, Optional
from dataclasses import dataclass
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)

@dataclass
class SnakeConfig:
    initial_length: int = 3
    initial_direction: str = 'RIGHT'
    growth_increment: int = 1
    move_cooldown: int = 150
    head_color: str = 'darkgreen'
    body_color: str = 'green'

class Snake:
    def __init__(self, screen: pygame.Surface, cell_size: int, config_path: Optional[Path] = None):
        self.screen = screen
        self.cell_size = cell_size
        self.config = self._load_config(config_path)
        self.reset()
        logger.info("Serpiente inicializada")

    def _load_config(self, config_path: Optional[Path]) -> SnakeConfig:
        default_config = SnakeConfig()
        if not config_path or not config_path.exists():
            return default_config
            
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
                snake_config = config_data.get('snake', {})
                return SnakeConfig(
                    initial_length=snake_config.get('initial_length', default_config.initial_length),
                    initial_direction=snake_config.get('initial_direction', default_config.initial_direction),
                    growth_increment=snake_config.get('growth_increment', default_config.growth_increment),
                    move_cooldown=snake_config.get('move_cooldown', default_config.move_cooldown),
                    head_color=snake_config.get('head_color', default_config.head_color),
                    body_color=snake_config.get('body_color', default_config.body_color)
                )
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            return default_config

    def reset(self):
        center_x = self.screen.get_width() // 2 // self.cell_size
        center_y = self.screen.get_height() // 2 // self.cell_size
        self.body = [(center_x - i, center_y) for i in range(self.config.initial_length)]
        self.direction = self.config.initial_direction
        self.next_direction = self.direction
        self.last_move_time = 0
        self.growth_pending = 0

    def change_direction(self, new_direction: str) -> bool:
        opposite_directions = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }
        
        if new_direction not in opposite_directions:
            logger.warning(f"Dirección inválida recibida: {new_direction}")
            return False
            
        if opposite_directions[new_direction] != self.direction:
            self.next_direction = new_direction
            logger.debug(f"Dirección cambiada a: {new_direction}")
            return True
        return False

    def move(self, current_time: int) -> bool:
        if current_time - self.last_move_time < self.config.move_cooldown:
            return False
            
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        
        direction_map = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        dx, dy = direction_map[self.direction]
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.body.pop()
        
        self.last_move_time = current_time
        return True

    def grow(self):
        self.growth_pending += self.config.growth_increment

    def check_collision(self, board_size: Tuple[int, int]) -> bool:
        head = self.body[0]
        if (head[0] < 0 or head[0] >= board_size[0] or 
            head[1] < 0 or head[1] >= board_size[1]):
            return True
        return head in self.body[1:]

    def draw(self):
        try:
            head_color = pygame.Color(self.config.head_color)
            body_color = pygame.Color(self.config.body_color)
            
            for i, segment in enumerate(self.body):
                color = head_color if i == 0 else body_color
                rect = pygame.Rect(
                    segment[0] * self.cell_size,
                    segment[1] * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, pygame.Color('black'), rect, 1)
                
        except Exception as e:
            logger.error(f"Error dibujando serpiente: {e}")
            raise