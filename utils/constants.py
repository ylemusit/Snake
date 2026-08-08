"""
SnakeYCL Constants
==================

Application-wide constants for the SnakeYCL game.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

# Application Information
GAME_TITLE = "SnakeYCL"
GAME_VERSION = "1.0.0"
AUTHOR = "Yeison Arbey Carrillo Lemus"
AUTHOR_ID = "200725"
LICENSE = "MIT"

# File Paths
DEFAULT_CONFIG_PATH = "data/settings.yaml"
LOG_FILE_PATH = "data/logs/game.log"
RECORDS_FILE_PATH = "data/records.txt"

# Asset Paths
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
AUDIO_DIR = f"{ASSETS_DIR}/audio"
FONTS_DIR = f"{ASSETS_DIR}/fonts"

# Specific Asset Files
ICON_PATH = f"{IMAGES_DIR}/icon.ico"
HEAD_IMAGE_PATH = f"{IMAGES_DIR}/head.png"
FRUIT_IMAGE_PATH = f"{IMAGES_DIR}/fruit.png"
BITE_SOUND_PATH = f"{AUDIO_DIR}/bite.wav"
FONT_PATH = f"{FONTS_DIR}/consolas.ttf"

# Exit Codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Game Constants
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
DEFAULT_CELL_SIZE = 20
DEFAULT_FPS = 60

# Snake Constants
DEFAULT_SNAKE_LENGTH = 3
DEFAULT_MOVE_COOLDOWN = 150
DEFAULT_GROWTH_INCREMENT = 1

# Fruit Constants
DEFAULT_FRUIT_RADIUS = 8

# Colors (RGB tuples)
class Colors:
    """Color constants for the game."""
    
    # Primary Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    # Game Specific Colors
    BACKGROUND = (173, 216, 230)  # Light blue
    GRID = (51, 51, 51)           # Dark gray
    SNAKE_HEAD = (0, 100, 0)      # Dark green
    SNAKE_BODY = (0, 128, 0)      # Green
    FRUIT = (220, 20, 60)         # Crimson
    
    # UI Colors
    BUTTON_NORMAL = (70, 130, 200)    # Steel blue
    BUTTON_HOVER = (100, 160, 230)    # Light steel blue
    BUTTON_DANGER = (200, 70, 70)     # Red
    BUTTON_DANGER_HOVER = (230, 100, 100)  # Light red
    TEXT_PRIMARY = (255, 255, 255)    # White
    TEXT_SECONDARY = (0, 0, 0)        # Black

# Directions
class Direction:
    """Direction constants for snake movement."""
    
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    
    # Direction mappings
    OPPOSITE = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT
    }
    
    VECTORS = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0)
    }

# Pygame Key Mappings
DIRECTION_KEYS = {
    'K_UP': Direction.UP,
    'K_w': Direction.UP,
    'K_DOWN': Direction.DOWN,
    'K_s': Direction.DOWN,
    'K_LEFT': Direction.LEFT,
    'K_a': Direction.LEFT,
    'K_RIGHT': Direction.RIGHT,
    'K_d': Direction.RIGHT,
}

# Game States
class GameState:
    """Game state constants."""
    
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"
    HIGH_SCORES = "HIGH_SCORES"
    SETTINGS = "SETTINGS"

# Logging Configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Score System
POINTS_PER_FRUIT = 10
BONUS_MULTIPLIER = 1.5
HIGH_SCORE_LIMIT = 10

# Performance Settings
MAX_FPS = 120
MIN_FPS = 10
DEFAULT_VOLUME = 0.7

# Validation Constants
MIN_SCREEN_WIDTH = 400
MAX_SCREEN_WIDTH = 1920
MIN_SCREEN_HEIGHT = 300
MAX_SCREEN_HEIGHT = 1080
MIN_CELL_SIZE = 10
MAX_CELL_SIZE = 50