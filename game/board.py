"""
SnakeYCL Game Board
==================

Main game board implementation for SnakeYCL.
Manages game state, entities, and the main game loop.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import logging
from typing import Tuple, Optional
import time

import pygame

from .snake import Snake
from .fruit import Fruit
from .collision import CollisionDetector, CollisionType
from utils.config import GameConfig
from utils.records import get_records_manager, create_game_record
from utils.constants import Direction, Colors, POINTS_PER_FRUIT
from utils.logger import log_game_event, time_operation

logger = logging.getLogger(__name__)


class GameBoard:
    """
    Main game board for SnakeYCL.
    
    Manages the complete game state including snake, fruit, scoring,
    collision detection, and the main game loop.
    """
    
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        """
        Initialize the game board.
        
        Args:
            screen: Pygame surface for rendering
            config: Game configuration
        """
        self.screen = screen
        self.config = config
        
        # Game entities
        self.snake = Snake(screen, config.cell_size, config.snake)
        self.fruit = Fruit(screen, config.cell_size, config.fruit)
        
        # Game state
        self.score = 0
        self.fruits_eaten = 0
        self.running = False
        self.paused = False
        self.game_start_time = 0
        self.last_score_update = 0
        
        # Systems
        self.collision_detector = CollisionDetector(*config.board_size)
        self.records_manager = get_records_manager()
        
        # Timing
        self.clock = pygame.time.Clock()
        self.frame_count = 0
        
        # UI elements
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)
        
        logger.info("Game board initialized")
    
    def reset_game(self) -> None:
        """Reset game to initial state for a new game."""
        self.score = 0
        self.fruits_eaten = 0
        self.running = True
        self.paused = False
        self.game_start_time = time.time()
        self.last_score_update = 0
        self.frame_count = 0
        
        # Reset entities
        self.snake.reset()
        self.fruit.spawn(self.snake.get_occupied_positions())
        
        log_game_event("game_start", f"New game started")
        logger.info("Game reset for new session")
    
    def handle_events(self) -> None:
        """Handle pygame events and user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                log_game_event("game_quit", "User quit game")
                
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
                
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event.key)
    
    def _handle_keydown(self, key: int) -> None:
        """
        Handle key press events.
        
        Args:
            key: Pygame key constant
        """
        # Movement keys
        direction_map = {
            pygame.K_UP: Direction.UP,
            pygame.K_w: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_s: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_a: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_d: Direction.RIGHT,
        }
        
        if key in direction_map:
            direction = direction_map[key]
            if self.snake.change_direction(direction):
                logger.debug(f"Direction changed to: {direction}")
        
        # Control keys
        elif key == pygame.K_ESCAPE:
            if self.paused:
                self.resume_game()
            else:
                self.pause_game()
                
        elif key == pygame.K_p:
            if self.paused:
                self.resume_game()
            else:
                self.pause_game()
        
        elif key == pygame.K_r and not self.running:
            # Restart game (only when game over)
            self.reset_game()
    
    def _handle_keyup(self, key: int) -> None:
        """
        Handle key release events.
        
        Args:
            key: Pygame key constant
        """
        # Future: Handle key release events if needed
        pass
    
    def pause_game(self) -> None:
        """Pause the game."""
        if self.running and not self.paused:
            self.paused = True
            log_game_event("game_pause", "Game paused")
            logger.info("Game paused")
    
    def resume_game(self) -> None:
        """Resume the game."""
        if self.running and self.paused:
            self.paused = False
            log_game_event("game_resume", "Game resumed")
            logger.info("Game resumed")
    
    def update(self) -> Optional[int]:
        """
        Update game state.
        
        Returns:
            Optional[int]: Final score if game ended, None if continuing
        """
        if not self.running or self.paused:
            return None
        
        with time_operation("game_update"):
            current_time = pygame.time.get_ticks()
            
            # Update snake
            if self.snake.move(current_time):
                # Check collisions after movement
                collision_result = self._check_collisions()
                
                if collision_result:
                    return self._end_game()
                
                # Check fruit collision
                if self.snake.check_food_collision(self.fruit.get_position()):
                    self._handle_fruit_eaten()
            
            # Update fruit animation
            self.fruit.update(current_time)
            
            self.frame_count += 1
        
        return None
    
    def _check_collisions(self) -> bool:
        """
        Check for game-ending collisions.
        
        Returns:
            bool: True if game-ending collision detected
        """
        snake_collisions = self.collision_detector.check_snake_collisions(
            self.snake.get_occupied_positions()
        )
        
        for collision in snake_collisions:
            if collision.collision_type in [CollisionType.WALL, CollisionType.SELF]:
                collision_type = collision.collision_type.value
                position = collision.position
                
                log_game_event(
                    "collision", 
                    f"{collision_type} collision at {position}"
                )
                logger.info(f"Game ending collision: {collision}")
                return True
        
        return False
    
    def _handle_fruit_eaten(self) -> None:
        """Handle fruit being eaten by snake."""
        # Get fruit value before marking as eaten
        fruit_value = self.fruit.mark_eaten()
        
        # Update snake
        self.snake.grow()
        
        # Update score
        old_score = self.score
        self.score += fruit_value
        self.fruits_eaten += 1
        
        # Spawn new fruit
        self.fruit.spawn(self.snake.get_occupied_positions())
        
        # Log event
        log_game_event(
            "fruit_eaten", 
            f"Score: {old_score} -> {self.score} (+{fruit_value})"
        )
        
        logger.info(f"Fruit eaten! Score: {self.score}, Length: {self.snake.get_length()}")
    
    def _end_game(self) -> int:
        """
        End the current game and return final score.
        
        Returns:
            int: Final score
        """
        self.running = False
        game_duration = time.time() - self.game_start_time
        
        # Create game record
        record = create_game_record(
            score=self.score,
            player_name="YACL",  # Future: Get from user input
            duration=game_duration,
            difficulty=self.config.difficulty if hasattr(self.config, 'difficulty') else "normal",
            snake_length=self.snake.get_length(),
            fruits_eaten=self.fruits_eaten
        )
        
        # Check if it's a high score
        is_high_score = self.records_manager.add_record(record)
        
        if is_high_score:
            log_game_event("high_score", f"New high score: {self.score}")
            logger.info(f"NEW HIGH SCORE: {self.score}")
        
        log_game_event(
            "game_over", 
            f"Final score: {self.score}, Duration: {game_duration:.1f}s"
        )
        
        logger.info(f"Game ended - Score: {self.score}, Duration: {game_duration:.1f}s")
        return self.score
    
    def draw(self) -> None:
        """
        Render the complete game board with retro design.
        """
        with time_operation("game_draw"):
            # Clear screen
            self.screen.fill(pygame.Color(0, 50, 0))  # Dark green background

            # Draw grid (always visible in retro design)
            self._draw_grid()

            # Draw game entities
            self.fruit.draw()
            self.snake.draw()

            # Draw UI elements
            self._draw_score()
            self._draw_length()

            if self.paused:
                self._draw_pause_overlay()

            # Update display
            pygame.display.flip()
    
    def _draw_grid(self) -> None:
        """
        Draw retro-style grid lines on the board.
        """
        grid_color = pygame.Color(0, 100, 0)  # Dark green for grid lines

        # Vertical lines
        for x in range(0, self.screen.get_width(), self.config.cell_size):
            pygame.draw.line(
                self.screen, 
                grid_color, 
                (x, 0), 
                (x, self.screen.get_height())
            )

        # Horizontal lines
        for y in range(0, self.screen.get_height(), self.config.cell_size):
            pygame.draw.line(
                self.screen, 
                grid_color, 
                (0, y), 
                (self.screen.get_width(), y)
            )

    def _draw_score(self) -> None:
        """
        Draw current score in retro style.
        """
        score_text = self.font_medium.render(
            f"SCORE: {self.score}", 
            True, 
            pygame.Color(0, 255, 0)  # Bright green for text
        )

        # Draw background
        text_rect = score_text.get_rect()
        text_rect.topleft = (10, 10)

        bg_rect = text_rect.inflate(10, 5)
        pygame.draw.rect(self.screen, pygame.Color(0, 50, 0), bg_rect)  # Dark green background
        pygame.draw.rect(self.screen, pygame.Color(0, 255, 0), bg_rect, 2)  # Bright green border

        self.screen.blit(score_text, text_rect)

    def _draw_length(self) -> None:
        """
        Draw current snake length in retro style.
        """
        length_text = self.font_small.render(
            f"LENGTH: {self.snake.get_length()}", 
            True, 
            pygame.Color(0, 255, 0)  # Bright green for text
        )

        # Position below score
        text_rect = length_text.get_rect()
        text_rect.topleft = (10, 50)

        bg_rect = text_rect.inflate(8, 3)
        pygame.draw.rect(self.screen, pygame.Color(0, 50, 0), bg_rect)  # Dark green background
        pygame.draw.rect(self.screen, pygame.Color(0, 255, 0), bg_rect, 1)  # Bright green border

        self.screen.blit(length_text, text_rect)
    
    def _draw_pause_overlay(self) -> None:
        """Draw pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, Colors.WHITE)
        text_rect = pause_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(pause_text, text_rect)
        
        # Instructions
        instruction_text = self.font_small.render(
            "Press ESC or P to resume", 
            True, 
            Colors.WHITE
        )
        instruction_rect = instruction_text.get_rect(
            center=(self.screen.get_rect().centerx, text_rect.bottom + 30)
        )
        self.screen.blit(instruction_text, instruction_rect)
    
    def run(self) -> int:
        """
        Run the main game loop.
        
        Returns:
            int: Final score when game ends
        """
        self.reset_game()
        
        logger.info("Starting main game loop")
        
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            final_score = self.update()
            if final_score is not None:
                logger.info(f"Game loop ended with score: {final_score}")
                return final_score
            
            # Render
            self.draw()
            
            # Control frame rate
            self.clock.tick(self.config.fps)
        
        # Game ended without score (quit)
        logger.info("Game loop ended (quit)")
        return self.score
    
    def get_statistics(self) -> dict:
        """
        Get current game statistics.
        
        Returns:
            dict: Game statistics
        """
        current_time = time.time()
        game_duration = current_time - self.game_start_time if self.game_start_time > 0 else 0
        
        return {
            'score': self.score,
            'fruits_eaten': self.fruits_eaten,
            'snake_length': self.snake.get_length(),
            'game_duration': game_duration,
            'frame_count': self.frame_count,
            'fps': self.clock.get_fps(),
            'running': self.running,
            'paused': self.paused
        }