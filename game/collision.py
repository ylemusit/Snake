"""
SnakeYCL Collision Detection System
==================================

Advanced collision detection and handling for the SnakeYCL game.
Provides precise collision detection between game entities.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import logging
from typing import Tuple, List, Optional, Union
from enum import Enum

logger = logging.getLogger(__name__)


class CollisionType(Enum):
    """Types of collisions in the game."""
    
    NONE = "none"
    WALL = "wall"
    SELF = "self"
    FOOD = "food"
    OBSTACLE = "obstacle"


class CollisionResult:
    """
    Result of a collision detection operation.
    
    Contains information about collision type, position, and additional data.
    """
    
    def __init__(
        self,
        collision_type: CollisionType,
        position: Optional[Tuple[int, int]] = None,
        entity_data: Optional[dict] = None
    ):
        """
        Initialize collision result.
        
        Args:
            collision_type: Type of collision detected
            position: Position where collision occurred
            entity_data: Additional data about the colliding entity
        """
        self.collision_type = collision_type
        self.position = position
        self.entity_data = entity_data or {}
    
    @property
    def has_collision(self) -> bool:
        """
        Check if a collision was detected.
        
        Returns:
            bool: True if collision detected, False otherwise
        """
        return self.collision_type != CollisionType.NONE
    
    def __bool__(self) -> bool:
        """Allow boolean evaluation of collision result."""
        return self.has_collision
    
    def __str__(self) -> str:
        """String representation of collision result."""
        if not self.has_collision:
            return "No collision"
        
        result = f"Collision: {self.collision_type.value}"
        if self.position:
            result += f" at {self.position}"
        
        return result


class CollisionDetector:
    """
    Advanced collision detection system for SnakeYCL.
    
    Provides various collision detection methods for different game entities
    and scenarios.
    """
    
    def __init__(self, board_width: int, board_height: int):
        """
        Initialize collision detector.
        
        Args:
            board_width: Game board width in cells
            board_height: Game board height in cells
        """
        self.board_width = board_width
        self.board_height = board_height
        
        logger.debug(f"Collision detector initialized for {board_width}x{board_height} board")
    
    def update_board_size(self, width: int, height: int) -> None:
        """
        Update board dimensions.
        
        Args:
            width: New board width in cells
            height: New board height in cells
        """
        self.board_width = width
        self.board_height = height
        
        logger.debug(f"Board size updated to {width}x{height}")
    
    def check_wall_collision(self, position: Tuple[int, int]) -> CollisionResult:
        """
        Check if position collides with board boundaries.
        
        Args:
            position: Position to check (x, y) in grid coordinates
            
        Returns:
            CollisionResult: Collision result
        """
        x, y = position
        
        if (x < 0 or x >= self.board_width or 
            y < 0 or y >= self.board_height):
            
            logger.debug(f"Wall collision detected at {position}")
            return CollisionResult(
                CollisionType.WALL,
                position,
                {
                    'boundary_exceeded': {
                        'x': x < 0 or x >= self.board_width,
                        'y': y < 0 or y >= self.board_height
                    }
                }
            )
        
        return CollisionResult(CollisionType.NONE)
    
    def check_self_collision(
        self, 
        head_position: Tuple[int, int],
        body_segments: List[Tuple[int, int]]
    ) -> CollisionResult:
        """
        Check if snake head collides with its own body.
        
        Args:
            head_position: Snake head position
            body_segments: List of snake body segment positions (excluding head)
            
        Returns:
            CollisionResult: Collision result
        """
        if head_position in body_segments:
            collision_index = body_segments.index(head_position)
            
            logger.debug(f"Self collision detected at {head_position}")
            return CollisionResult(
                CollisionType.SELF,
                head_position,
                {
                    'collision_segment_index': collision_index,
                    'segments_after_collision': len(body_segments) - collision_index - 1
                }
            )
        
        return CollisionResult(CollisionType.NONE)
    
    def check_food_collision(
        self, 
        head_position: Tuple[int, int],
        food_position: Tuple[int, int]
    ) -> CollisionResult:
        """
        Check if snake head collides with food.
        
        Args:
            head_position: Snake head position
            food_position: Food position
            
        Returns:
            CollisionResult: Collision result
        """
        if head_position == food_position:
            logger.debug(f"Food collision detected at {head_position}")
            return CollisionResult(
                CollisionType.FOOD,
                head_position,
                {'food_position': food_position}
            )
        
        return CollisionResult(CollisionType.NONE)
    
    def check_snake_collisions(
        self,
        snake_body: List[Tuple[int, int]]
    ) -> List[CollisionResult]:
        """
        Check all collisions for a snake.
        
        Args:
            snake_body: Complete snake body (head first)
            
        Returns:
            List[CollisionResult]: List of all detected collisions
        """
        if not snake_body:
            return []
        
        collisions = []
        head_position = snake_body[0]
        body_segments = snake_body[1:]  # Exclude head
        
        # Check wall collision
        wall_collision = self.check_wall_collision(head_position)
        if wall_collision:
            collisions.append(wall_collision)
        
        # Check self collision
        self_collision = self.check_self_collision(head_position, body_segments)
        if self_collision:
            collisions.append(self_collision)
        
        return collisions
    
    def check_point_in_area(
        self,
        point: Tuple[int, int],
        area_top_left: Tuple[int, int],
        area_size: Tuple[int, int]
    ) -> bool:
        """
        Check if a point is within a rectangular area.
        
        Args:
            point: Point to check (x, y)
            area_top_left: Top-left corner of area (x, y)
            area_size: Size of area (width, height)
            
        Returns:
            bool: True if point is in area, False otherwise
        """
        px, py = point
        ax, ay = area_top_left
        aw, ah = area_size
        
        return (ax <= px < ax + aw and 
                ay <= py < ay + ah)
    
    def check_line_collision(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        obstacles: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """
        Check for collisions along a line path.
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            obstacles: List of obstacle positions
            
        Returns:
            List[Tuple[int, int]]: List of collision positions
        """
        collisions = []
        path = self._get_line_path(start, end)
        
        for position in path:
            if position in obstacles:
                collisions.append(position)
        
        return collisions
    
    def _get_line_path(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """
        Get all positions along a line using Bresenham's algorithm.
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Returns:
            List[Tuple[int, int]]: List of positions along the line
        """
        x0, y0 = start
        x1, y1 = end
        
        positions = []
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        
        err = dx - dy
        
        while True:
            positions.append((x0, y0))
            
            if x0 == x1 and y0 == y1:
                break
            
            e2 = 2 * err
            
            if e2 > -dy:
                err -= dy
                x0 += sx
            
            if e2 < dx:
                err += dx
                y0 += sy
        
        return positions
    
    def get_safe_spawn_positions(
        self,
        occupied_positions: List[Tuple[int, int]],
        min_distance: int = 1
    ) -> List[Tuple[int, int]]:
        """
        Get all safe positions for spawning entities.
        
        Args:
            occupied_positions: List of currently occupied positions
            min_distance: Minimum distance from occupied positions
            
        Returns:
            List[Tuple[int, int]]: List of safe spawn positions
        """
        safe_positions = []
        
        for x in range(self.board_width):
            for y in range(self.board_height):
                position = (x, y)
                
                if self._is_position_safe(position, occupied_positions, min_distance):
                    safe_positions.append(position)
        
        return safe_positions
    
    def _is_position_safe(
        self,
        position: Tuple[int, int],
        occupied_positions: List[Tuple[int, int]],
        min_distance: int
    ) -> bool:
        """
        Check if a position is safe (not too close to occupied positions).
        
        Args:
            position: Position to check
            occupied_positions: List of occupied positions
            min_distance: Minimum required distance
            
        Returns:
            bool: True if position is safe, False otherwise
        """
        px, py = position
        
        for ox, oy in occupied_positions:
            distance = abs(px - ox) + abs(py - oy)  # Manhattan distance
            if distance < min_distance:
                return False
        
        return True
    
    def predict_collision(
        self,
        current_position: Tuple[int, int],
        direction: Tuple[int, int],
        steps: int,
        obstacles: List[Tuple[int, int]]
    ) -> Optional[CollisionResult]:
        """
        Predict if a collision will occur within a given number of steps.
        
        Args:
            current_position: Current position
            direction: Movement direction vector (dx, dy)
            steps: Number of steps to predict
            obstacles: List of obstacle positions
            
        Returns:
            Optional[CollisionResult]: Predicted collision result or None
        """
        x, y = current_position
        dx, dy = direction
        
        for step in range(1, steps + 1):
            future_position = (x + dx * step, y + dy * step)
            
            # Check wall collision
            wall_collision = self.check_wall_collision(future_position)
            if wall_collision:
                wall_collision.entity_data['predicted_step'] = step
                return wall_collision
            
            # Check obstacle collision
            if future_position in obstacles:
                return CollisionResult(
                    CollisionType.OBSTACLE,
                    future_position,
                    {'predicted_step': step}
                )
        
        return None
    
    def get_collision_statistics(self) -> dict:
        """
        Get collision detection statistics.
        
        Returns:
            dict: Statistics about collision detection
        """
        return {
            'board_width': self.board_width,
            'board_height': self.board_height,
            'total_cells': self.board_width * self.board_height,
            'detector_initialized': True
        }


# Utility functions for collision detection

def calculate_manhattan_distance(
    pos1: Tuple[int, int], 
    pos2: Tuple[int, int]
) -> int:
    """
    Calculate Manhattan distance between two positions.
    
    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)
        
    Returns:
        int: Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def calculate_euclidean_distance(
    pos1: Tuple[int, int], 
    pos2: Tuple[int, int]
) -> float:
    """
    Calculate Euclidean distance between two positions.
    
    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)
        
    Returns:
        float: Euclidean distance
    """
    import math
    
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    
    return math.sqrt(dx * dx + dy * dy)


def find_nearest_position(
    target: Tuple[int, int],
    positions: List[Tuple[int, int]]
) -> Optional[Tuple[int, int]]:
    """
    Find the nearest position to a target from a list of positions.
    
    Args:
        target: Target position
        positions: List of positions to search
        
    Returns:
        Optional[Tuple[int, int]]: Nearest position or None if list is empty
    """
    if not positions:
        return None
    
    nearest = positions[0]
    min_distance = calculate_manhattan_distance(target, nearest)
    
    for position in positions[1:]:
        distance = calculate_manhattan_distance(target, position)
        if distance < min_distance:
            min_distance = distance
            nearest = position
    
    return nearest
