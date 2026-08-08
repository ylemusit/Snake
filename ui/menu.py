"""
SnakeYCL Main Menu
=================

Professional main menu system for the SnakeYCL game.
Provides navigation, game options, and credits display.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import logging
from typing import List, Optional
import sys

import pygame

from .button import Button
from game.board import GameBoard
from utils.config import GameConfig
from utils.records import get_records_manager
from utils.constants import (
    GAME_TITLE, 
    GAME_VERSION, 
    AUTHOR, 
    AUTHOR_ID,
    Colors
)
from utils.logger import log_game_event

logger = logging.getLogger(__name__)


class MainMenu:
    """
    Main menu system for SnakeYCL.
    
    Provides navigation between game modes, settings, high scores,
    and other game features.
    """
    
    def __init__(
        self, 
        screen: pygame.Surface, 
        config: GameConfig, 
        clock: pygame.time.Clock
    ):
        """
        Initialize the main menu.
        
        Args:
            screen: Pygame surface for rendering
            config: Game configuration
            clock: Pygame clock for timing
        """
        self.screen = screen
        self.config = config
        self.clock = clock
        self.running = True
        self.current_view = "main"  # main, high_scores, about
        
        # Menu state
        self.selected_button = 0
        self.fade_alpha = 255
        
        # UI elements
        self.buttons = self._create_main_buttons()
        self.high_score_buttons = self._create_high_score_buttons()
        self.about_buttons = self._create_about_buttons()
        
        # Fonts
        self.font_title = pygame.font.Font(None, 82)
        self.font_subtitle = pygame.font.Font(None, 36)
        self.font_text = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 24)
        
        # Background and visual elements
        self.background = self._create_background()
        self.title_surface = self._create_title()
        
        # Records manager
        self.records_manager = get_records_manager()
        
        # Animation state
        self.animation_offset = 0  # For animated background
        
        # Font
        self.font = None  # Ensure font is initialized
        self._load_custom_font()
        
        logger.info("Main menu initialized")
    
    def _create_main_buttons(self) -> List[Button]:
        """
        Create main menu buttons.
        
        Returns:
            List[Button]: List of main menu buttons
        """
        button_width = 300
        button_height = 60
        button_spacing = 20
        center_x = self.screen.get_width() // 2 - button_width // 2
        start_y = 320
        
        buttons = []
        
        # Play button
        buttons.append(Button(
            rect=pygame.Rect(center_x, start_y, button_width, button_height),
            text="PLAY GAME",
            action=self.start_game,
            normal_color=Colors.BUTTON_NORMAL,
            hover_color=Colors.BUTTON_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            font_size=36,
            border_radius=15
        ))
        
        # High scores button
        buttons.append(Button(
            rect=pygame.Rect(
                center_x, 
                start_y + (button_height + button_spacing) * 1, 
                button_width, 
                button_height
            ),
            text="HIGH SCORES",
            action=self.show_high_scores,
            normal_color=Colors.BUTTON_NORMAL,
            hover_color=Colors.BUTTON_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            font_size=32,
            border_radius=15
        ))
        
        # About button
        buttons.append(Button(
            rect=pygame.Rect(
                center_x, 
                start_y + (button_height + button_spacing) * 2, 
                button_width, 
                button_height
            ),
            text="ABOUT",
            action=self.show_about,
            normal_color=Colors.BUTTON_NORMAL,
            hover_color=Colors.BUTTON_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            font_size=32,
            border_radius=15
        ))
        
        # Exit button
        buttons.append(Button(
            rect=pygame.Rect(
                center_x, 
                start_y + (button_height + button_spacing) * 3, 
                button_width, 
                button_height
            ),
            text="EXIT",
            action=self.quit_game,
            normal_color=Colors.BUTTON_DANGER,
            hover_color=Colors.BUTTON_DANGER_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            font_size=32,
            border_radius=15
        ))
        
        return buttons
    
    def _create_high_score_buttons(self) -> List[Button]:
        """
        Create high score view buttons.
        
        Returns:
            List[Button]: List of high score buttons
        """
        button_width = 200
        button_height = 50
        
        return [
            Button(
                rect=pygame.Rect(50, self.screen.get_height() - 70, button_width, button_height),
                text="BACK TO MENU",
                action=self.show_main_menu,
                normal_color=Colors.BUTTON_NORMAL,
                hover_color=Colors.BUTTON_HOVER,
                text_color=Colors.TEXT_PRIMARY,
                font_size=24,
                border_radius=10
            )
        ]
    
    def _create_about_buttons(self) -> List[Button]:
        """
        Create about view buttons.
        
        Returns:
            List[Button]: List of about buttons
        """
        button_width = 200
        button_height = 50
        
        return [
            Button(
                rect=pygame.Rect(50, self.screen.get_height() - 70, button_width, button_height),
                text="BACK TO MENU",
                action=self.show_main_menu,
                normal_color=Colors.BUTTON_NORMAL,
                hover_color=Colors.BUTTON_HOVER,
                text_color=Colors.TEXT_PRIMARY,
                font_size=24,
                border_radius=10
            )
        ]
    
    def _create_background(self) -> pygame.Surface:
        """
        Create animated background surface with a modern gradient.
        
        Returns:
            pygame.Surface: Background surface
        """
        background = pygame.Surface(self.screen.get_size())
        
        # Dynamic gradient background
        for y in range(self.screen.get_height()):
            ratio = y / self.screen.get_height()
            color = (
                int(50 + (100 - 50) * ratio),  # Dark blue to light blue
                int(50 + (150 - 50) * ratio),
                int(100 + (200 - 100) * ratio)
            )
            pygame.draw.line(background, color, (0, y), (self.screen.get_width(), y))
        
        return background
    
    def _create_title(self) -> pygame.Surface:
        """
        Create title surface with effects.
        
        Returns:
            pygame.Surface: Title surface
        """
        title_text = self.font_title.render(GAME_TITLE, True, Colors.TEXT_SECONDARY)
        
        # Create shadow effect
        shadow_text = self.font_title.render(GAME_TITLE, True, (100, 100, 100))
        
        # Combine title and shadow
        title_rect = title_text.get_rect()
        title_surface = pygame.Surface((title_rect.width + 5, title_rect.height + 5), pygame.SRCALPHA)
        
        # Blit shadow first (offset)
        title_surface.blit(shadow_text, (3, 3))
        # Blit main title
        title_surface.blit(title_text, (0, 0))
        
        return title_surface
    
    def start_game(self) -> None:
        """Start a new game."""
        log_game_event("menu_action", "Start game selected")
        logger.info("Starting new game from menu")
        
        try:
            game_board = GameBoard(self.screen, self.config)
            final_score = game_board.run()
            
            log_game_event("game_completed", f"Game completed with score: {final_score}")
            logger.info(f"Game completed with final score: {final_score}")
            
            # Return to menu after game
            self.current_view = "main"
            
        except Exception as e:
            logger.error(f"Error starting game: {e}")
            # Stay in menu on error
    
    def show_high_scores(self) -> None:
        """Show high scores view."""
        log_game_event("menu_action", "High scores selected")
        self.current_view = "high_scores"
        logger.debug("Switched to high scores view")
    
    def show_about(self) -> None:
        """Show about view."""
        log_game_event("menu_action", "About selected")
        self.current_view = "about"
        logger.debug("Switched to about view")
    
    def show_main_menu(self) -> None:
        """Return to main menu."""
        log_game_event("menu_action", "Back to main menu")
        self.current_view = "main"
        logger.debug("Returned to main menu")
    
    def quit_game(self) -> None:
        """Quit the application."""
        log_game_event("menu_action", "Exit game selected")
        logger.info("Exiting game from menu")
        self.running = False
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def handle_events(self) -> None:
        """Handle pygame events, including mouse interactions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keyboard_input(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse clicks
                current_buttons = self._get_current_buttons()
                for button in current_buttons:
                    if button.handle_event(event):
                        break  # Stop processing if button was clicked

            elif event.type == pygame.MOUSEMOTION:
                # Highlight buttons on hover
                current_buttons = self._get_current_buttons()
                for button in current_buttons:
                    button.is_hovered = button.rect.collidepoint(event.pos)

    def _handle_keyboard_input(self, key: int) -> None:
        """
        Handle keyboard input for menu navigation.
        
        Args:
            key: Pygame key constant
        """
        if key == pygame.K_ESCAPE:
            if self.current_view != "main":
                self.show_main_menu()
            else:
                self.quit_game()
        
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            # Activate selected button
            current_buttons = self._get_current_buttons()
            if current_buttons and 0 <= self.selected_button < len(current_buttons):
                button = current_buttons[self.selected_button]
                if button.action:
                    button.action()
        
        elif key == pygame.K_UP:
            self._navigate_up()
        
        elif key == pygame.K_DOWN:
            self._navigate_down()
    
    def _navigate_up(self) -> None:
        """Navigate up in button selection."""
        current_buttons = self._get_current_buttons()
        if current_buttons:
            self.selected_button = (self.selected_button - 1) % len(current_buttons)
    
    def _navigate_down(self) -> None:
        """Navigate down in button selection."""
        current_buttons = self._get_current_buttons()
        if current_buttons:
            self.selected_button = (self.selected_button + 1) % len(current_buttons)
    
    def _get_current_buttons(self) -> List[Button]:
        """
        Get buttons for current view.
        
        Returns:
            List[Button]: Current view buttons
        """
        if self.current_view == "main":
            return self.buttons
        elif self.current_view == "high_scores":
            return self.high_score_buttons
        elif self.current_view == "about":
            return self.about_buttons
        else:
            return []
    
    def update(self) -> None:
        """Update menu animations and state."""
        # Future: Add menu animations, particle effects, etc.
        pass
    
    def _draw_background(self):
        """
        Draw an animated background for the main menu.
        """
        # Example: Simple gradient animation
        for y in range(0, self.screen.get_height(), 10):
            color = (0, (y + self.animation_offset) % 255, 50)
            pygame.draw.rect(self.screen, color, pygame.Rect(0, y, self.screen.get_width(), 10))
        self.animation_offset = (self.animation_offset + 1) % 255

    def _draw_buttons(self):
        """
        Draw buttons with hover effects.
        """
        for button in self.buttons:
            if button.is_hovered:  # `is_hovered` is a boolean attribute
                button.draw(self.screen)  # Call draw without additional parameters
            else:
                button.draw(self.screen)  # Call draw without additional parameters

    def _load_custom_font(self):
        """
        Load a custom font for the menu.
        """
        try:
            self.font = pygame.font.Font("assets/fonts/consolas.ttf", 24)
        except FileNotFoundError:
            self.font = pygame.font.SysFont("Consolas", 24)  # Fallback to system font

    def __init__(self, screen):
        """
        Initialize the menu with improved visuals.
        """
        self.screen = screen
        self.buttons = []  # Initialize buttons
        self.animation_offset = 0  # For animated background
        self.font = pygame.font.SysFont("Consolas", 24)  # Default font
        try:
            self.font = pygame.font.Font("assets/fonts/consolas.ttf", 24)  # Custom font
        except FileNotFoundError:
            pass  # Fallback to default font
        # Ensure font is not None
        if not self.font:
            self.font = pygame.font.SysFont("Consolas", 24)

    def draw(self):
        """
        Render the main menu with improved visuals.
        """
        self._draw_background()
        self._draw_buttons()
        # Ensure font is valid before rendering title
        if not self.font:
            self.font = pygame.font.SysFont("Consolas", 24)  # Fallback to default font
        title_surface = self.font.render("SnakeYCL", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - title_surface.get_width() // 2, 50))
        pygame.display.flip()
    
    def _draw_main_menu(self) -> None:
        """Draw main menu view with modern design."""
        # Draw title
        title_rect = self.title_surface.get_rect(
            center=(self.screen.get_width() // 2, 100)
        )
        self.screen.blit(self.title_surface, title_rect)

        # Draw subtitle
        subtitle_text = self.font_subtitle.render(
            f"by {AUTHOR} - {AUTHOR_ID}", 
            True, 
            Colors.TEXT_SECONDARY
        )
        subtitle_rect = subtitle_text.get_rect(
            center=(self.screen.get_width() // 2, 150)
        )
        self.screen.blit(subtitle_text, subtitle_rect)

        # Draw version
        version_text = self.font_small.render(
            f"Version {GAME_VERSION}", 
            True, 
            Colors.TEXT_SECONDARY
        )
        version_rect = version_text.get_rect(
            center=(self.screen.get_width() // 2, 180)
        )
        self.screen.blit(version_text, version_rect)

        # Draw buttons
        for i, button in enumerate(self.buttons):
            button.draw(self.screen)

        # Draw best score in a modern bar at the top
        pygame.draw.rect(self.screen, Colors.BUTTON_NORMAL, (0, 0, self.screen.get_width(), 40))
        best_record = self.records_manager.get_best_score()
        if best_record:
            best_score_text = self.font_text.render(
                f"Best Score: {best_record.score}", 
                True, 
                Colors.TEXT_PRIMARY
            )
            self.screen.blit(best_score_text, (10, 10))
    
    def _draw_high_scores(self) -> None:
        """Draw high scores view."""
        # Title
        title_text = self.font_title.render("HIGH SCORES", True, Colors.TEXT_SECONDARY)
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Get high scores
        high_scores = self.records_manager.get_high_scores(10)
        
        if not high_scores:
            no_scores_text = self.font_text.render(
                "No high scores yet!", 
                True, 
                Colors.TEXT_SECONDARY
            )
            no_scores_rect = no_scores_text.get_rect(
                center=(self.screen.get_width() // 2, 200)
            )
            self.screen.blit(no_scores_text, no_scores_rect)
        else:
            # Draw scores
            start_y = 150
            for i, record in enumerate(high_scores):
                rank_text = f"{i+1:2d}."
                score_text = f"{record.score:5d}"
                name_text = f"{record.player_name[:10]:10s}"
                date_text = record.formatted_date
                
                full_text = f"{rank_text} {score_text}  {name_text}  {date_text}"
                
                color = Colors.TEXT_SECONDARY
                if i == 0:  # Highlight first place
                    color = (255, 215, 0)  # Gold
                elif i == 1:  # Second place
                    color = (192, 192, 192)  # Silver
                elif i == 2:  # Third place
                    color = (205, 127, 50)  # Bronze
                
                score_surface = self.font_text.render(full_text, True, color)
                self.screen.blit(score_surface, (50, start_y + i * 30))
        
        # Draw back button
        for button in self.high_score_buttons:
            button.draw(self.screen)
    
    def _draw_about(self) -> None:
        """Draw about view."""
        # Title
        title_text = self.font_title.render("ABOUT", True, Colors.TEXT_SECONDARY)
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # About information
        about_lines = [
            f"{GAME_TITLE} v{GAME_VERSION}",
            "",
            f"Author: {AUTHOR}",
            f"Student ID: {AUTHOR_ID}",
            "",
            "A modern implementation of the classic Snake game",
            "built with Python and Pygame.",
            "",
            "Features:",
            "• Professional code architecture",
            "• High score system",
            "• Multiple fruit types",
            "• Smooth animations",
            "• Comprehensive logging",
            "",
            "Controls:",
            "• Arrow keys or WASD to move",
            "• ESC to pause/menu",
            "• P to pause",
            "",
            "© 2025 - Built with ❤️ by YACL"
        ]
        
        start_y = 130
        line_height = 25
        
        for i, line in enumerate(about_lines):
            if line.startswith("•"):
                # Bullet points
                text_surface = self.font_small.render(line, True, Colors.TEXT_SECONDARY)
                self.screen.blit(text_surface, (80, start_y + i * line_height))
            elif line in [f"{GAME_TITLE} v{GAME_VERSION}", "Features:", "Controls:"]:
                # Section headers
                text_surface = self.font_text.render(line, True, (70, 130, 200))
                self.screen.blit(text_surface, (50, start_y + i * line_height))
            else:
                # Regular text
                text_surface = self.font_small.render(line, True, Colors.TEXT_SECONDARY)
                self.screen.blit(text_surface, (50, start_y + i * line_height))
        
        # Draw back button
        for button in self.about_buttons:
            button.draw(self.screen)
    
    def run(self) -> None:
        """
        Run the main menu loop.
        
        This is the main entry point for the menu system.
        """
        log_game_event("menu_start", "Main menu started")
        logger.info("Starting main menu loop")
        
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update menu state
            self.update()
            
            # Render menu
            self.draw()
            
            # Control frame rate
            self.clock.tick(self.config.fps)
        
        log_game_event("menu_end", "Main menu ended")
        logger.info("Main menu loop ended")