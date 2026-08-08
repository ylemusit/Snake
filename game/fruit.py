"""
SnakeYCL Fruit Entity
====================

Fruit implementation for the SnakeYCL game.
Handles fruit spawning, positioning, visual effects, and collision detection.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import random
import logging
import math
from typing import Tuple, List, Optional, Union
from pathlib import Path

import pygame

from utils.config import FruitConfig
from utils.constants import Colors, FRUIT_IMAGE_PATH

logger = logging.getLogger(__name__)


class Fruit:
    """
    Fruit entity for the SnakeYCL game.
    
    Manages fruit spawning, positioning, visual effects, and animations.
    Provides various fruit types and visual enhancements.
    """
    
    def __init__(
        self,
        screen: pygame.Surface,
        cell_size: int,
        config: Optional[FruitConfig] = None
    ):
        """
        Initialize the fruit entity.
        
        Args:
            screen: Pygame surface for rendering
            cell_size: Size of each grid cell in pixels
            config: Fruit configuration (optional, uses default if None)
        """
        self.screen = screen
        self.cell_size = cell_size
        self.config = config or FruitConfig()
        
        # Fruit state
        self.position = (0, 0)
        self.fruit_type = "normal"
        self.spawn_time = 0
        self.animation_offset = 0
        
        # Visual assets
        self.fruit_image: Optional[pygame.Surface] = None
        self.glow_surface: Optional[pygame.Surface] = None
        
        # Statistics
        self.total_spawned = 0
        self.total_eaten = 0
        
        self._load_assets()
        self.spawn()
        
        logger.info("Fruit initialized")
    
    def _load_assets(self) -> None:
        """Load fruit visual assets."""
        try:
            # Try to load fruit image
            fruit_image_path = Path(FRUIT_IMAGE_PATH)
            if fruit_image_path.exists():
                self.fruit_image = pygame.image.load(fruit_image_path)
                self.fruit_image = pygame.transform.scale(
                    self.fruit_image, 
                    (self.cell_size, self.cell_size)
                )
                logger.debug("Fruit image loaded")
            
            # Create glow effect surface
            self._create_glow_surface()
            
        except Exception as e:
            logger.warning(f"Could not load fruit assets: {e}")
            self.fruit_image = None
            self.glow_surface = None
    
    def _create_glow_surface(self) -> None:
        """Create a glow effect surface for the fruit."""
        try:
            glow_size = self.cell_size + 10
            self.glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            
            # Create radial gradient for glow effect
            center = glow_size // 2
            max_radius = center
            
            for radius in range(max_radius, 0, -1):
                alpha = int(30 * (1 - radius / max_radius))
                color = (*Colors.FRUIT[:3], alpha)
                
                pygame.draw.circle(
                    self.glow_surface, 
                    color, 
                    (center, center), 
                    radius
                )
            
            logger.debug("Glow surface created")
            
        except Exception as e:
            logger.warning(f"Could not create glow surface: {e}")
            self.glow_surface = None
    
    def spawn(self, occupied_positions: Optional[List[Tuple[int, int]]] = None) -> None:
        """
        Generate a new position for the fruit, avoiding occupied positions.
        
        Args:
            occupied_positions: List of positions to avoid (e.g., snake body)
        """
        if occupied_positions is None:
            occupied_positions = []
        
        # Calculate board dimensions
        width_in_cells = self.screen.get_width() // self.cell_size
        height_in_cells = self.screen.get_height() // self.cell_size
        
        # Ensure we have valid board dimensions
        if width_in_cells <= 0 or height_in_cells <= 0:
            logger.error("Invalid board dimensions for fruit spawning")
            return
        
        # Find valid position
        max_attempts = width_in_cells * height_in_cells
        attempts = 0
        
        while attempts < max_attempts:
            new_position = (
                random.randint(0, width_in_cells - 1),
                random.randint(0, height_in_cells - 1)
            )
            
            if new_position not in occupied_positions:
                self.position = new_position
                self.spawn_time = pygame.time.get_ticks()
                self.total_spawned += 1
                
                # Randomly determine fruit type (future expansion)
                self.fruit_type = self._determine_fruit_type()
                
                logger.debug(f"Fruit spawned at {new_position} (type: {self.fruit_type})")
                return
            
            attempts += 1
        
        # Fallback: place at (0, 0) if no valid position found
        logger.warning("Could not find valid spawn position, using fallback")
        self.position = (0, 0)
        self.spawn_time = pygame.time.get_ticks()
        self.total_spawned += 1
    
    def _determine_fruit_type(self) -> str:
        """
        Determine the type of fruit to spawn.
        
        Returns:
            str: Fruit type identifier
        """
        # Simple random fruit type selection
        # This can be expanded for different fruit types with different properties
        fruit_types = ["normal", "bonus", "speed", "large"]
        weights = [70, 15, 10, 5]  # Percentage chances
        
        roll = random.randint(1, 100)
        cumulative = 0
        
        for i, weight in enumerate(weights):
            cumulative += weight
            if roll <= cumulative:
                return fruit_types[i]
        
        return "normal"
    
    def get_position(self) -> Tuple[int, int]:
        """
        Get current fruit position.
        
        Returns:
            Tuple[int, int]: Fruit position (x, y) in grid coordinates
        """
        return self.position
    
    def get_pixel_position(self) -> Tuple[int, int]:
        """
        Get fruit position in pixel coordinates.
        
        Returns:
            Tuple[int, int]: Fruit position (x, y) in pixel coordinates
        """
        return (
            self.position[0] * self.cell_size,
            self.position[1] * self.cell_size
        )
    
    def get_center_position(self) -> Tuple[int, int]:
        """
        Get fruit center position in pixel coordinates.
        
        Returns:
            Tuple[int, int]: Fruit center position (x, y) in pixels
        """
        pixel_x, pixel_y = self.get_pixel_position()
        return (
            pixel_x + self.cell_size // 2,
            pixel_y + self.cell_size // 2
        )
    
    def get_fruit_type(self) -> str:
        """
        Get the current fruit type.
        
        Returns:
            str: Current fruit type
        """
        return self.fruit_type
    
    def get_value(self) -> int:
        """
        Get the point value of this fruit.
        
        Returns:
            int: Point value based on fruit type
        """
        fruit_values = {
            "normal": 10,
            "bonus": 25,
            "speed": 15,
            "large": 20
        }
        
        return fruit_values.get(self.fruit_type, 10)
    
    def update(self, current_time: int) -> None:
        """
        Update fruit animation and effects.
        
        Args:
            current_time: Current game time in milliseconds
        """
        # Update animation offset for pulsing effect
        time_since_spawn = current_time - self.spawn_time
        self.animation_offset = math.sin(time_since_spawn * 0.005) * 2
    
    def draw(self) -> None:
        """
        Render the fruit on the screen.
        
        Draws the fruit with visual effects including glow, pulsing,
        and type-specific appearance modifications.
        """
        if not self.position:
            return
        
        try:
            current_time = pygame.time.get_ticks()
            self.update(current_time)
            
            # Get drawing positions
            center_x, center_y = self.get_center_position()
            pixel_x, pixel_y = self.get_pixel_position()
            
            # Draw glow effect (if available)
            if self.glow_surface:
                glow_rect = self.glow_surface.get_rect(center=(center_x, center_y))
                self.screen.blit(self.glow_surface, glow_rect)
            
            # Draw main fruit
            if self.fruit_image:
                # Use image if available
                fruit_rect = self.fruit_image.get_rect()
                animated_y = int(center_y + self.animation_offset)
                fruit_rect.center = (center_x, animated_y)
                self.screen.blit(self.fruit_image, fruit_rect)
            else:
                # Draw geometric fruit
                self._draw_geometric_fruit(center_x, center_y)
            
            # Draw type-specific effects
            self._draw_type_effects(center_x, center_y)
            
        except Exception as e:
            logger.error(f"Error drawing fruit: {e}")
            # Fallback to simple drawing
            self._draw_simple()
    
    def _draw_geometric_fruit(self, center_x: int, center_y: int) -> None:
        """
        Draw geometric fruit when no image is available.
        
        Args:
            center_x: Center X coordinate in pixels
            center_y: Center Y coordinate in pixels
        """
        # Get fruit color based on type
        fruit_color = self._get_fruit_color()
        
        # Adjust center for animation
        animated_center_y = center_y + self.animation_offset
        
        # Draw main fruit circle
        pygame.draw.circle(
            self.screen,
            fruit_color,
            (center_x, int(animated_center_y)),
            self.config.radius
        )
        
        # Draw highlight/shine effect
        highlight_offset = 3
        highlight_radius = max(1, self.config.radius // 3)
        pygame.draw.circle(
            self.screen,
            Colors.WHITE,
            (center_x - highlight_offset, int(animated_center_y) - highlight_offset),
            highlight_radius
        )
        
        # Draw border
        pygame.draw.circle(
            self.screen,
            Colors.BLACK,
            (center_x, int(animated_center_y)),
            self.config.radius,
            1
        )
    
    def _get_fruit_color(self) -> Tuple[int, int, int]:
        """
        Get color based on fruit type.
        
        Returns:
            Tuple[int, int, int]: RGB color tuple
        """
        type_colors = {
            "normal": Colors.FRUIT,
            "bonus": (255, 215, 0),     # Gold
            "speed": (0, 255, 255),     # Cyan
            "large": (255, 165, 0),     # Orange
        }
        
        return type_colors.get(self.fruit_type, Colors.FRUIT)
    
    def _draw_type_effects(self, center_x: int, center_y: int) -> None:
        """
        Draw type-specific visual effects.
        
        Args:
            center_x: Center X coordinate in pixels
            center_y: Center Y coordinate in pixels
        """
        animated_center_y = int(center_y + self.animation_offset)
        
        if self.fruit_type == "bonus":
            # Draw sparkle effect for bonus fruit
            sparkle_positions = [
                (center_x - 10, animated_center_y - 10),
                (center_x + 10, animated_center_y - 10),
                (center_x - 10, animated_center_y + 10),
                (center_x + 10, animated_center_y + 10)
            ]
            
            for pos in sparkle_positions:
                pygame.draw.circle(self.screen, Colors.WHITE, pos, 2)
        
        elif self.fruit_type == "speed":
            # Draw speed lines for speed fruit
            line_length = 8
            for i in range(3):
                start_x = center_x + self.config.radius + 2 + (i * 3)
                start_y = animated_center_y
                end_x = start_x + line_length
                end_y = animated_center_y
                
                pygame.draw.line(
                    self.screen, 
                    Colors.WHITE, 
                    (start_x, start_y), 
                    (end_x, end_y), 
                    2
                )
        
        elif self.fruit_type == "large":
            # Draw size indicator for large fruit
            outer_radius = self.config.radius + 3
            pygame.draw.circle(
                self.screen,
                Colors.WHITE,
                (center_x, animated_center_y),
                outer_radius,
                2
            )
    
    def _draw_simple(self) -> None:
        """
        Simple fallback drawing method.
        
        Used when the main drawing method fails.
        """
        try:
            center_x, center_y = self.get_center_position()
            
            pygame.draw.circle(
                self.screen,
                Colors.FRUIT,
                (center_x, center_y),
                self.config.radius
            )
            
            pygame.draw.circle(
                self.screen,
                Colors.BLACK,
                (center_x, center_y),
                self.config.radius,
                1
            )
            
        except Exception as e:
            logger.error(f"Error in simple fruit drawing: {e}")
    
    def mark_eaten(self) -> int:
        """
        Mark fruit as eaten and return its value.
        
        Returns:
            int: Point value of the eaten fruit
        """
        self.total_eaten += 1
        value = self.get_value()
        
        logger.debug(f"Fruit eaten (type: {self.fruit_type}, value: {value})")
        return value
    
    def get_statistics(self) -> dict:
        """
        Get fruit statistics.
        
        Returns:
            dict: Statistics including spawn count, eaten count, etc.
        """
        return {
            'total_spawned': self.total_spawned,
            'total_eaten': self.total_eaten,
            'current_type': self.fruit_type,
            'current_value': self.get_value(),
            'position': self.position
        }


# Helper functions for testing and utilities

def create_random_fruit_position(
    width: int, 
    height: int, 
    cell_size: int,
    excluded_positions: Optional[List[Tuple[int, int]]] = None
) -> Tuple[int, int]:
    """
    Create a random fruit position within given bounds.
    
    Args:
        width: Screen width in pixels
        height: Screen height in pixels
        cell_size: Size of each cell in pixels
        excluded_positions: Positions to avoid
        
    Returns:
        Tuple[int, int]: Random position (x, y) in grid coordinates
    """
    if excluded_positions is None:
        excluded_positions = []
    
    width_in_cells = width // cell_size
    height_in_cells = height // cell_size
    
    max_attempts = width_in_cells * height_in_cells
    
    for _ in range(max_attempts):
        position = (
            random.randint(0, width_in_cells - 1),
            random.randint(0, height_in_cells - 1)
        )
        
        if position not in excluded_positions:
            return position
    
    # Fallback
    return (0, 0)