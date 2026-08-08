# SnakeYCL Technical Documentation

## API Reference

### Core Classes

#### `Snake` Class
```python
class Snake:
    """Snake entity for the SnakeYCL game."""
    
    def __init__(self, screen: pygame.Surface, cell_size: int, config: Optional[SnakeConfig] = None)
    def reset(self) -> None
    def change_direction(self, new_direction: str) -> bool
    def move(self, current_time: int) -> bool
    def grow(self, segments: Optional[int] = None) -> None
    def check_collision(self, board_size: Tuple[int, int]) -> bool
    def draw(self) -> None
    def get_statistics(self) -> dict
```

#### `Fruit` Class
```python
class Fruit:
    """Fruit entity for the SnakeYCL game."""
    
    def __init__(self, screen: pygame.Surface, cell_size: int, config: Optional[FruitConfig] = None)
    def spawn(self, occupied_positions: Optional[List[Tuple[int, int]]] = None) -> None
    def get_position(self) -> Tuple[int, int]
    def get_value(self) -> int
    def draw(self) -> None
    def mark_eaten(self) -> int
```

#### `GameBoard` Class
```python
class GameBoard:
    """Main game board and game loop management."""
    
    def __init__(self, screen: pygame.Surface, config: GameConfig)
    def handle_events(self) -> None
    def update(self) -> Optional[int]
    def draw(self) -> None
    def run(self) -> int
```

### Configuration Classes

#### `GameConfig`
```python
@dataclass
class GameConfig:
    screen_width: int = 800
    screen_height: int = 600
    cell_size: int = 20
    fps: int = 60
    bg_color: str = "lightblue"
    # ... additional fields
```

#### `SnakeConfig`
```python
@dataclass
class SnakeConfig:
    initial_length: int = 3
    initial_direction: str = Direction.RIGHT
    growth_increment: int = 1
    move_cooldown: int = 150
    # ... additional fields
```

## Event System

### Game Events
- `GAME_START`: Game session begins
- `GAME_OVER`: Game session ends
- `FRUIT_EATEN`: Player collects fruit
- `SCORE_UPDATE`: Score changes
- `HIGH_SCORE`: New high score achieved

### Input Events
- Arrow keys: Snake movement
- WASD keys: Alternative movement
- ESC: Pause/Menu
- Space: Restart (on game over)

## File Formats

### Configuration File (YAML)
```yaml
# Game settings
game:
  screen_width: 800
  screen_height: 600
  cell_size: 20
  fps: 60
  
# Snake settings  
snake:
  initial_length: 3
  move_cooldown: 150
  
# Fruit settings
fruit:
  color: "red"
  radius: 8
```

### Records File (JSON)
```json
{
  "metadata": {
    "game": "SnakeYCL",
    "version": "1.0.0",
    "author": "Yeison Arbey Carrillo Lemus (200725)"
  },
  "records": [
    {
      "score": 450,
      "player_name": "YACL",
      "date": "2025-10-11T14:30:00",
      "duration": 125.5,
      "difficulty": "normal"
    }
  ]
}
```

## Error Handling

### Exception Hierarchy
```
Exception
├── GameError
│   ├── ConfigurationError
│   ├── AssetLoadError
│   └── GameStateError
├── RenderError
└── InputError
```

### Error Recovery
- Graceful degradation for missing assets
- Fallback to default configurations
- Safe mode for corrupted data files

## Performance Optimization

### Memory Management
- Object pooling for entities
- Asset caching and preloading
- Garbage collection optimization

### Rendering Optimization
- Dirty rectangle updates
- Sprite batching
- Frame rate limiting

## Logging Configuration

### Log Levels
- `DEBUG`: Detailed debugging information
- `INFO`: General information messages
- `WARNING`: Warning messages
- `ERROR`: Error conditions
- `CRITICAL`: Critical error conditions

### Log Format
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Log Rotation
- Max file size: 10MB
- Backup count: 5 files
- Automatic cleanup

## Build Process

### PyInstaller Configuration
```python
# build.py
import PyInstaller.__main__ as PI

PI.run([
    'main.py',
    '--onefile',
    '--name', 'SnakeYCL',
    '--icon', 'assets/images/icon.ico',
    '--add-data', 'assets;assets',
    '--add-data', 'data;data',
    '--paths', '.'
])
```

### Build Optimization
- Executable compression
- Asset bundling
- Dependency analysis
- Cross-platform compatibility

## Testing Framework

### Unit Tests
```python
import unittest
from game.snake import Snake

class TestSnake(unittest.TestCase):
    def test_snake_movement(self):
        # Test snake movement logic
        pass
        
    def test_collision_detection(self):
        # Test collision detection
        pass
```

### Test Coverage
- Aim for 90%+ code coverage
- Focus on critical paths
- Include edge cases

## Deployment

### Distribution Formats
- Standalone executable (PyInstaller)
- Python package (setuptools)
- Portable ZIP archive

### System Requirements
- Windows 10+ / macOS 10.14+ / Linux (Ubuntu 18.04+)
- Python 3.8+ (for source)
- 100MB disk space
- DirectX 9.0c compatible graphics

## Security Considerations

### Input Validation
- Sanitize configuration files
- Validate user input
- Prevent code injection

### File Security
- Safe file operations
- Path traversal prevention
- Permission checking

## Extensibility

### Plugin System
Future versions may include:
- Custom game modes
- Themes and skins
- AI opponents
- Multiplayer support

### Modding Support
- Asset replacement
- Configuration overrides
- Custom scripts

## Troubleshooting Guide

### Common Issues

#### "pygame.error: No available video device"
**Solution:** Install SDL2 development libraries
```bash
# Ubuntu/Debian
sudo apt-get install libsdl2-dev

# macOS
brew install sdl2
```

#### "ImportError: No module named 'yaml'"
**Solution:** Install PyYAML
```bash
pip install PyYAML
```

#### Performance Issues
**Solutions:**
- Reduce screen resolution
- Lower FPS setting
- Disable visual effects
- Close background applications

### Debug Mode
Enable debug logging:
```python
from utils.logger import setup_logging
setup_logging(log_level="DEBUG")
```

### Profiling
Use built-in performance monitoring:
```python
from utils.logger import time_operation

with time_operation("game_update"):
    game.update()
```