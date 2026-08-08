"""
SnakeYCL Snake Entity
====================

Complete snake implementation for the SnakeYCL game.
Handles snake movement, growth, collision detection, and rendering.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import logging
from typing import Tuple, List, Optional, Union
from pathlib import Path

import pygame

from utils.config import SnakeConfig
from utils.constants import Direction, Colors

logger = logging.getLogger(__name__)


class Snake:
    """
    Snake entity for the SnakeYCL game.
    
    Manages snake position, movement, growth, collision detection,
    and visual rendering with smooth animations.
    """
    
    def __init__(
        self,
        screen: pygame.Surface,
        cell_size: int,
        config: Optional[SnakeConfig] = None
    ):
        """
        Initialize the snake entity.
        
        Args:
            screen: Pygame surface for rendering
            cell_size: Size of each grid cell in pixels
            config: Snake configuration (optional, uses default if None)
        """
        self.screen = screen
        self.cell_size = cell_size
        self.config = config or SnakeConfig()
        
        # Snake state
        self.body: List[Tuple[int, int]] = []
        self.direction = self.config.initial_direction
        self.next_direction = self.direction
        self.last_move_time = 0
        self.growth_pending = 0
        
        # Animation and visual state
        self.head_image: Optional[pygame.Surface] = None
        self.body_segments: List[pygame.Rect] = []
        
        # Statistics
        self.total_moves = 0
        self.fruits_eaten = 0
        
        self.reset()
        self._load_assets()
        
        logger.info(f"Snake initialized with {self.config.initial_length} segments")
    
    def _load_assets(self) -> None:
        """Load snake visual assets."""
        try:
            # Try to load head image
            head_image_path = Path("assets/images/head.png")
            if head_image_path.exists():
                self.head_image = pygame.image.load(head_image_path)
                self.head_image = pygame.transform.scale(
                    self.head_image, 
                    (self.cell_size, self.cell_size)
                )
                logger.debug("Snake head image loaded")
        except Exception as e:
            logger.warning(f"Could not load snake head image: {e}")
            self.head_image = None
    
    def reset(self) -> None:
        """
        Reset snake to initial state.
        
        Resets position, direction, and growth state for a new game.
        """
        # Calculate center position
        center_x = self.screen.get_width() // 2 // self.cell_size
        center_y = self.screen.get_height() // 2 // self.cell_size
        
        # Create initial body segments
        self.body = [
            (center_x - i, center_y) 
            for i in range(self.config.initial_length)
        ]
        
        # Reset state
        self.direction = self.config.initial_direction
        self.next_direction = self.direction
        self.last_move_time = 0
        self.growth_pending = 0
        
        # Reset statistics
        self.total_moves = 0
        self.fruits_eaten = 0
        
        logger.debug(f"Snake reset to center position: {self.body[0]}")
    
    def change_direction(self, new_direction: str) -> bool:
        """
        Change snake movement direction.
        
        Args:
            new_direction: New direction (UP, DOWN, LEFT, RIGHT)
            
        Returns:
            bool: True if direction was changed, False if invalid/opposite
        """
        # Validate direction
        if new_direction not in Direction.VECTORS:
            logger.warning(f"Invalid direction: {new_direction}")
            return False
        
        # Prevent reversing into itself
        opposite_direction = Direction.OPPOSITE.get(new_direction)
        if opposite_direction == self.direction:
            logger.debug(f"Blocked opposite direction: {new_direction}")
            return False
        
        self.next_direction = new_direction
        logger.debug(f"Direction queued: {new_direction}")
        return True
    
    def move(self, current_time: int) -> bool:
        """
        Move the snake one step forward.
        
        Args:
            current_time: Current game time in milliseconds
            
        Returns:
            bool: True if snake moved, False if move was on cooldown
        """
        # Check move cooldown
        if current_time - self.last_move_time < self.config.move_cooldown:
            return False
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.body[0]
        dx, dy = Direction.VECTORS[self.direction]
        new_head = (head_x + dx, head_y + dy)
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Handle growth or remove tail
        if self.growth_pending > 0:
            self.growth_pending -= 1
            logger.debug(f"Snake grew, remaining growth: {self.growth_pending}")
        else:
            # Remove tail segment
            self.body.pop()
        
        # Update timing and statistics
        self.last_move_time = current_time
        self.total_moves += 1
        
        return True
    
    def grow(self, segments: Optional[int] = None) -> None:
        """
        Make the snake grow by adding segments.
        
        Args:
            segments: Number of segments to add (uses config default if None)
        """
        growth = segments if segments is not None else self.config.growth_increment
        self.growth_pending += growth
        self.fruits_eaten += 1
        
        logger.debug(f"Snake will grow by {growth} segments")
    
    def check_collision(self, board_size: Tuple[int, int]) -> bool:
        """
        Check for collisions with walls or self.
        
        Args:
            board_size: Board dimensions (width, height) in cells
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        head = self.body[0]
        board_width, board_height = board_size
        
        # Wall collision
        if (head[0] < 0 or head[0] >= board_width or 
            head[1] < 0 or head[1] >= board_height):
            logger.info(f"Wall collision at {head}")
            return True
        
        # Self collision (check if head overlaps with body)
        if head in self.body[1:]:
            logger.info(f"Self collision at {head}")
            return True
        
        return False
    
    def check_food_collision(self, food_position: Tuple[int, int]) -> bool:
        """
        Check if snake head collides with food.
        
        Args:
            food_position: Position of food in grid coordinates
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        return self.body[0] == food_position
    
    def get_head_position(self) -> Tuple[int, int]:
        """
        Get the current head position.
        
        Returns:
            Tuple[int, int]: Head position (x, y) in grid coordinates
        """
        return self.body[0]
    
    def get_length(self) -> int:
        """
        Get current snake length.
        
        Returns:
            int: Current length including pending growth
        """
        return len(self.body) + self.growth_pending
    
    def get_occupied_positions(self) -> List[Tuple[int, int]]:
        """
        Get all positions occupied by the snake.
        
        Returns:
            List[Tuple[int, int]]: List of occupied grid positions
        """
        return self.body.copy()
    
    def draw(self) -> None:
        """
        Render the snake on the screen with a retro design.
        """
        if not self.body:
            return

        try:
            # Parse colors
            head_color = pygame.Color(0, 255, 0)  # Bright green for head
            body_color = pygame.Color(0, 200, 0)  # Darker green for body
            border_color = pygame.Color(0, 100, 0)  # Dark green for borders

            # Draw body segments (including head)
            for i, segment in enumerate(self.body):
                color = head_color if i == 0 else body_color

                rect = pygame.Rect(
                    segment[0] * self.cell_size,
                    segment[1] * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, border_color, rect, 1)

        except Exception as e:
            logger.error(f"Error drawing snake: {e}")
            # Fallback to simple drawing
            self._draw_simple()
    
    def _rotate_head_image(
        self, 
        image: pygame.Surface, 
        direction: str
    ) -> pygame.Surface:
        """
        Rotate head image based on movement direction.
        
        Args:
            image: Original head image
            direction: Current movement direction
            
        Returns:
            pygame.Surface: Rotated image
        """
        rotation_angles = {
            Direction.UP: 0,
            Direction.RIGHT: 270,
            Direction.DOWN: 180,
            Direction.LEFT: 90
        }
        
        angle = rotation_angles.get(direction, 0)
        return pygame.transform.rotate(image, angle)
    
    def _draw_direction_indicator(
        self, 
        head_rect: pygame.Rect, 
        direction: str
    ) -> None:
        """
        Draw a small triangle indicating movement direction.
        
        Args:
            head_rect: Rectangle containing the head
            direction: Current movement direction
        """
        center_x = head_rect.centerx
        center_y = head_rect.centery
        size = self.cell_size // 4
        
        if direction == Direction.UP:
            points = [
                (center_x, center_y - size),
                (center_x - size//2, center_y + size//2),
                (center_x + size//2, center_y + size//2)
            ]
        elif direction == Direction.DOWN:
            points = [
                (center_x, center_y + size),
                (center_x - size//2, center_y - size//2),
                (center_x + size//2, center_y - size//2)
            ]
        elif direction == Direction.LEFT:
            points = [
                (center_x - size, center_y),
                (center_x + size//2, center_y - size//2),
                (center_x + size//2, center_y + size//2)
            ]
        elif direction == Direction.RIGHT:
            points = [
                (center_x + size, center_y),
                (center_x - size//2, center_y - size//2),
                (center_x - size//2, center_y + size//2)
            ]
        else:
            return
        
        pygame.draw.polygon(self.screen, Colors.WHITE, points)
    
    def _draw_simple(self) -> None:
        """
        Simple fallback drawing method.
        
        Used when the main drawing method fails or for basic rendering.
        """
        try:
            for i, segment in enumerate(self.body):
                color = Colors.SNAKE_HEAD if i == 0 else Colors.SNAKE_BODY
                
                rect = pygame.Rect(
                    segment[0] * self.cell_size,
                    segment[1] * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, Colors.BLACK, rect, 1)
                
        except Exception as e:
            logger.error(f"Error in simple snake drawing: {e}")
    
    def get_statistics(self) -> dict:
        """
        Get snake statistics for the current game.
        
        Returns:
            dict: Statistics including length, moves, efficiency, etc.
        """
        current_length = len(self.body)
        efficiency = (self.fruits_eaten / max(1, self.total_moves)) * 100
        
        return {
            'current_length': current_length,
            'total_moves': self.total_moves,
            'fruits_eaten': self.fruits_eaten,
            'efficiency': efficiency,
            'growth_pending': self.growth_pending,
            'direction': self.direction
        }