#!/usr/bin/env python3
"""
SnakeYCL - Snake Game Implementation
====================================

Main entry point for the SnakeYCL game application.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
License: MIT
"""

import sys
import logging
from pathlib import Path
from typing import NoReturn

import pygame

from ui.menu import MainMenu
from utils.logger import setup_logging
from utils.config import load_game_config
from utils.constants import (
    GAME_TITLE,
    GAME_VERSION,
    DEFAULT_CONFIG_PATH,
    EXIT_SUCCESS,
    EXIT_FAILURE
)


def initialize_pygame() -> None:
    """
    Initialize Pygame subsystems.
    
    Raises:
        pygame.error: If Pygame initialization fails
    """
    try:
        pygame.init()
        pygame.mixer.init()
        logging.info("Pygame initialized successfully")
    except pygame.error as e:
        logging.critical(f"Failed to initialize Pygame: {e}")
        raise


def create_display(width: int, height: int, title: str) -> pygame.Surface:
    """
    Create and configure the main game display.
    
    Args:
        width: Screen width in pixels
        height: Screen height in pixels
        title: Window title
        
    Returns:
        pygame.Surface: The main screen surface
        
    Raises:
        pygame.error: If display creation fails
    """
    try:
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        logging.info(f"Display created: {width}x{height}")
        return screen
    except pygame.error as e:
        logging.critical(f"Failed to create display: {e}")
        raise


def main() -> NoReturn:
    """
    Main function that initializes and runs the SnakeYCL game.
    
    This function serves as the primary entry point for the application.
    It handles initialization, error management, and cleanup.
    
    Exits:
        EXIT_SUCCESS (0): Normal termination
        EXIT_FAILURE (1): Error occurred during execution
    """
    # Setup logging system
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("="*50)
    logger.info(f"Starting {GAME_TITLE} v{GAME_VERSION}")
    logger.info("Author: Yeison Arbey Carrillo Lemus (YACL)")
    logger.info("="*50)
    
    try:
        # Load game configuration
        config_path = Path(DEFAULT_CONFIG_PATH)
        config = load_game_config(config_path)
        logger.info(f"Configuration loaded from: {config_path}")
        
        # Initialize Pygame
        initialize_pygame()
        
        # Create main display
        screen = create_display(
            config.screen_width,
            config.screen_height,
            f"{GAME_TITLE} v{GAME_VERSION}"
        )
        
        # Initialize game clock
        clock = pygame.time.Clock()
        
        # Create and run main menu
        main_menu = MainMenu(screen, config, clock)
        logger.info("Starting main menu")
        main_menu.run()
        
        logger.info("Game session completed successfully")
        sys.exit(EXIT_SUCCESS)
        
    except FileNotFoundError as e:
        logger.critical(f"Required file not found: {e}")
        sys.exit(EXIT_FAILURE)
        
    except pygame.error as e:
        logger.critical(f"Pygame error: {e}")
        sys.exit(EXIT_FAILURE)
        
    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
        sys.exit(EXIT_SUCCESS)
        
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(EXIT_FAILURE)
        
    finally:
        # Cleanup
        try:
            pygame.quit()
            logger.info("Pygame cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


if __name__ == "__main__":
    main()