"""
fruit.py - Módulo para la fruta del juego Sneak.
Implementa una fruta redonda con efecto de brillo.
"""

import pygame
import random
import logging
from typing import Tuple, List, Optional
from dataclasses import dataclass
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)

@dataclass
class FruitConfig:
    color: str = 'red'
    radius: int = 8

class Fruit:
    def __init__(self, screen: pygame.Surface, cell_size: int, config_path: Optional[Path] = None):
        """Inicializa la fruta del juego.
        
        Args:
            screen: Superficie de Pygame para dibujar
            cell_size: Tamaño de cada celda del tablero
            config_path: Ruta al archivo de configuración (opcional)
        """
        self.screen = screen
        self.cell_size = cell_size
        self.config = self._load_config(config_path)
        self.position = (0, 0)
        self.spawn()
        logger.debug("Fruta inicializada")

    def _load_config(self, config_path: Optional[Path]) -> FruitConfig:
        """Carga la configuración desde archivo o usa valores por defecto."""
        default_config = FruitConfig()
        
        if not config_path or not config_path.exists():
            return default_config
            
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
                fruit_config = config_data.get('fruit', {})
                return FruitConfig(
                    color=fruit_config.get('color', default_config.color),
                    radius=fruit_config.get('radius', default_config.radius)
                )
        except Exception as e:
            logger.error(f"Error cargando configuración de fruta: {e}")
            return default_config

    def spawn(self, snake_body: Optional[List[Tuple[int, int]]] = None):
        """Genera una nueva posición para la fruta, evitando la serpiente."""
        width_in_cells = self.screen.get_width() // self.cell_size
        height_in_cells = self.screen.get_height() // self.cell_size
        
        while True:
            new_position = (
                random.randint(0, width_in_cells - 1),
                random.randint(0, height_in_cells - 1)
            )
            
            if snake_body is None or new_position not in snake_body:
                self.position = new_position
                logger.debug(f"Fruta generada en {new_position}")
                break

    def draw(self):
        """Dibuja la fruta como un círculo con efecto de brillo."""
        try:
            # Calcular posición central de la celda
            center_x = self.position[0] * self.cell_size + self.cell_size // 2
            center_y = self.position[1] * self.cell_size + self.cell_size // 2
            
            # Dibujar fruta principal
            pygame.draw.circle(
                self.screen,
                pygame.Color(self.config.color),
                (center_x, center_y),
                self.config.radius
            )
            
            # Efecto de brillo (punto de luz)
            pygame.draw.circle(
                self.screen,
                pygame.Color(255, 255, 255, 150),
                (center_x - 3, center_y - 3),
                self.config.radius // 3
            )
            
            # Borde sutil
            pygame.draw.circle(
                self.screen,
                pygame.Color('black'),
                (center_x, center_y),
                self.config.radius,
                1
            )
            
        except Exception as e:
            logger.error(f"Error dibujando fruta: {e}")
            raise

if __name__ == "__main__":
    """Pruebas de la clase Fruit."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    fruit = Fruit(screen, 20)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fruit.spawn()
        
        screen.fill((240, 240, 240))
        fruit.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.quit()