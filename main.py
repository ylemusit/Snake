#!/usr/bin/env python3
"""Punto de entrada principal del juego Sneak."""

import pygame
import logging
from pathlib import Path
from ui.menu import MainMenu
from utils.logger import setup_logging
from utils.config import load_game_config

def main():
    """Función principal que inicia el juego."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Iniciando juego Sneak")
    
    try:
        config = load_game_config(Path("data/settings.yaml"))
        pygame.init()
        pygame.mixer.init()
        
        screen = pygame.display.set_mode(
            (config.screen_width, config.screen_height)
        )
        pygame.display.set_caption("Sneak")
        
        clock = pygame.time.Clock()
        main_menu = MainMenu(screen, config, clock)
        main_menu.run()
        
    except Exception as e:
        logger.critical(f"Error crítico: {e}", exc_info=True)
    finally:
        pygame.quit()
        logger.info("Juego terminado correctamente")

if __name__ == "__main__":
    main()