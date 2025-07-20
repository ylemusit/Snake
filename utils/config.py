"""config.py - Manejo de configuración del juego."""

from dataclasses import dataclass
import pygame

@dataclass
class GameConfig:
    screen_width: int = 800
    screen_height: int = 600
    cell_size: int = 20
    fps: int = 60
    bg_color: str = 'lightblue'
    grid_color: str = 'gray20'

def load_game_config(config_path):
    """Carga la configuración o usa valores por defecto."""
    return GameConfig()  # Implementación básica