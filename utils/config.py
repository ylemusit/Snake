"""
SnakeYCL Configuration Management
================================

Comprehensive configuration management system for the SnakeYCL game.
Handles loading, validation, and management of game settings.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import logging
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional, Union

from .constants import (
    DEFAULT_SCREEN_WIDTH,
    DEFAULT_SCREEN_HEIGHT,
    DEFAULT_CELL_SIZE,
    DEFAULT_FPS,
    DEFAULT_SNAKE_LENGTH,
    DEFAULT_MOVE_COOLDOWN,
    DEFAULT_GROWTH_INCREMENT,
    DEFAULT_FRUIT_RADIUS,
    Colors,
    Direction,
    MIN_SCREEN_WIDTH,
    MAX_SCREEN_WIDTH,
    MIN_SCREEN_HEIGHT,
    MAX_SCREEN_HEIGHT,
    MIN_CELL_SIZE,
    MAX_CELL_SIZE,
    MIN_FPS,
    MAX_FPS
)

logger = logging.getLogger(__name__)


@dataclass
class SnakeConfig:
    """Configuration settings for the snake entity."""
    
    initial_length: int = DEFAULT_SNAKE_LENGTH
    initial_direction: str = Direction.RIGHT
    growth_increment: int = DEFAULT_GROWTH_INCREMENT
    move_cooldown: int = DEFAULT_MOVE_COOLDOWN
    head_color: str = "darkgreen"
    body_color: str = "green"
    
    def __post_init__(self) -> None:
        """Validate snake configuration after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate snake configuration parameters."""
        if self.initial_length < 1:
            raise ValueError("Snake initial length must be at least 1")
        if self.initial_direction not in Direction.VECTORS:
            raise ValueError(f"Invalid initial direction: {self.initial_direction}")
        if self.move_cooldown < 50:
            raise ValueError("Move cooldown must be at least 50ms")


@dataclass
class FruitConfig:
    """Configuration settings for the fruit entity."""
    
    color: str = "red"
    radius: int = DEFAULT_FRUIT_RADIUS
    
    def __post_init__(self) -> None:
        """Validate fruit configuration after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate fruit configuration parameters."""
        if self.radius < 1:
            raise ValueError("Fruit radius must be at least 1")


@dataclass
class GameConfig:
    """
    Main game configuration class.
    
    Contains all configuration settings for the SnakeYCL game,
    including display, gameplay, and entity-specific settings.
    """
    
    # Display settings
    screen_width: int = DEFAULT_SCREEN_WIDTH
    screen_height: int = DEFAULT_SCREEN_HEIGHT
    cell_size: int = DEFAULT_CELL_SIZE
    fps: int = DEFAULT_FPS
    
    # Visual settings
    bg_color: str = "lightblue"
    grid_color: str = "gray20"
    fullscreen: bool = False
    vsync: bool = True
    
    # Audio settings
    sound_enabled: bool = True
    music_enabled: bool = True
    volume: float = 0.7
    
    # Gameplay settings
    difficulty: str = "normal"
    pause_on_focus_lost: bool = True
    
    # Entity configurations
    snake: SnakeConfig = field(default_factory=SnakeConfig)
    fruit: FruitConfig = field(default_factory=FruitConfig)
    
    def __post_init__(self) -> None:
        """Validate game configuration after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """
        Validate all configuration parameters.
        
        Raises:
            ValueError: If any configuration parameter is invalid
        """
        # Screen dimensions validation
        if not (MIN_SCREEN_WIDTH <= self.screen_width <= MAX_SCREEN_WIDTH):
            raise ValueError(
                f"Screen width must be between {MIN_SCREEN_WIDTH} and {MAX_SCREEN_WIDTH}"
            )
        
        if not (MIN_SCREEN_HEIGHT <= self.screen_height <= MAX_SCREEN_HEIGHT):
            raise ValueError(
                f"Screen height must be between {MIN_SCREEN_HEIGHT} and {MAX_SCREEN_HEIGHT}"
            )
        
        # Cell size validation
        if not (MIN_CELL_SIZE <= self.cell_size <= MAX_CELL_SIZE):
            raise ValueError(
                f"Cell size must be between {MIN_CELL_SIZE} and {MAX_CELL_SIZE}"
            )
        
        # FPS validation
        if not (MIN_FPS <= self.fps <= MAX_FPS):
            raise ValueError(
                f"FPS must be between {MIN_FPS} and {MAX_FPS}"
            )
        
        # Volume validation
        if not (0.0 <= self.volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")
        
        # Ensure screen dimensions are divisible by cell size
        if self.screen_width % self.cell_size != 0:
            logger.warning(
                f"Screen width ({self.screen_width}) not divisible by cell size ({self.cell_size})"
            )
        
        if self.screen_height % self.cell_size != 0:
            logger.warning(
                f"Screen height ({self.screen_height}) not divisible by cell size ({self.cell_size})"
            )
    
    @property
    def board_size(self) -> tuple[int, int]:
        """
        Get the board size in cells.
        
        Returns:
            tuple[int, int]: (width_in_cells, height_in_cells)
        """
        return (
            self.screen_width // self.cell_size,
            self.screen_height // self.cell_size
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary format.
        
        Returns:
            Dict[str, Any]: Configuration as dictionary
        """
        return {
            "game": {
                "screen_width": self.screen_width,
                "screen_height": self.screen_height,
                "cell_size": self.cell_size,
                "fps": self.fps,
                "bg_color": self.bg_color,
                "grid_color": self.grid_color,
                "fullscreen": self.fullscreen,
                "vsync": self.vsync,
                "sound_enabled": self.sound_enabled,
                "music_enabled": self.music_enabled,
                "volume": self.volume,
                "difficulty": self.difficulty,
                "pause_on_focus_lost": self.pause_on_focus_lost
            },
            "snake": {
                "initial_length": self.snake.initial_length,
                "initial_direction": self.snake.initial_direction,
                "growth_increment": self.snake.growth_increment,
                "move_cooldown": self.snake.move_cooldown,
                "head_color": self.snake.head_color,
                "body_color": self.snake.body_color
            },
            "fruit": {
                "color": self.fruit.color,
                "radius": self.fruit.radius
            }
        }


def load_game_config(config_path: Union[str, Path]) -> GameConfig:
    """
    Load game configuration from YAML file or return default configuration.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        GameConfig: Loaded or default game configuration
        
    Raises:
        yaml.YAMLError: If YAML parsing fails
        ValueError: If configuration validation fails
    """
    config_path = Path(config_path)
    
    # Return default configuration if file doesn't exist
    if not config_path.exists():
        logger.warning(f"Configuration file not found: {config_path}")
        logger.info("Using default configuration")
        return GameConfig()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file) or {}
        
        logger.info(f"Configuration loaded from: {config_path}")
        return _parse_config_data(config_data)
        
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        logger.info("Using default configuration")
        return GameConfig()
    
    except FileNotFoundError:
        logger.warning(f"Configuration file not found: {config_path}")
        logger.info("Using default configuration")
        return GameConfig()
    
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        logger.info("Using default configuration")
        return GameConfig()


def _parse_config_data(config_data: Dict[str, Any]) -> GameConfig:
    """
    Parse configuration data from dictionary.
    
    Args:
        config_data: Configuration data as dictionary
        
    Returns:
        GameConfig: Parsed game configuration
    """
    # Extract game settings
    game_settings = config_data.get('game', {})
    snake_settings = config_data.get('snake', {})
    fruit_settings = config_data.get('fruit', {})
    
    # Create entity configurations
    snake_config = SnakeConfig(
        initial_length=snake_settings.get('initial_length', DEFAULT_SNAKE_LENGTH),
        initial_direction=snake_settings.get('initial_direction', Direction.RIGHT),
        growth_increment=snake_settings.get('growth_increment', DEFAULT_GROWTH_INCREMENT),
        move_cooldown=snake_settings.get('move_cooldown', DEFAULT_MOVE_COOLDOWN),
        head_color=snake_settings.get('head_color', 'darkgreen'),
        body_color=snake_settings.get('body_color', 'green')
    )
    
    fruit_config = FruitConfig(
        color=fruit_settings.get('color', 'red'),
        radius=fruit_settings.get('radius', DEFAULT_FRUIT_RADIUS)
    )
    
    # Create main game configuration
    return GameConfig(
        screen_width=game_settings.get('screen_width', DEFAULT_SCREEN_WIDTH),
        screen_height=game_settings.get('screen_height', DEFAULT_SCREEN_HEIGHT),
        cell_size=game_settings.get('cell_size', DEFAULT_CELL_SIZE),
        fps=game_settings.get('fps', DEFAULT_FPS),
        bg_color=game_settings.get('bg_color', 'lightblue'),
        grid_color=game_settings.get('grid_color', 'gray20'),
        fullscreen=game_settings.get('fullscreen', False),
        vsync=game_settings.get('vsync', True),
        sound_enabled=game_settings.get('sound_enabled', True),
        music_enabled=game_settings.get('music_enabled', True),
        volume=game_settings.get('volume', 0.7),
        difficulty=game_settings.get('difficulty', 'normal'),
        pause_on_focus_lost=game_settings.get('pause_on_focus_lost', True),
        snake=snake_config,
        fruit=fruit_config
    )


def save_game_config(config: GameConfig, config_path: Union[str, Path]) -> bool:
    """
    Save game configuration to YAML file.
    
    Args:
        config: Game configuration to save
        config_path: Path where to save the configuration
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    config_path = Path(config_path)
    
    try:
        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(config.to_dict(), file, default_flow_style=False, indent=2)
        
        logger.info(f"Configuration saved to: {config_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return False


def get_default_config() -> GameConfig:
    """
    Get the default game configuration.
    
    Returns:
        GameConfig: Default game configuration
    """
    return GameConfig()