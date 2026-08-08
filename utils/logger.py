"""
SnakeYCL Logging System
======================

Centralized logging configuration and utilities for the SnakeYCL game.
Provides structured logging with file and console output.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Union

from .constants import (
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    LOG_FILE_PATH,
    GAME_TITLE
)


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds color to console log messages.
    """
    
    # Color codes for different log levels
    COLORS = {
        logging.DEBUG: '\033[36m',     # Cyan
        logging.INFO: '\033[32m',      # Green
        logging.WARNING: '\033[33m',   # Yellow
        logging.ERROR: '\033[31m',     # Red
        logging.CRITICAL: '\033[35m',  # Magenta
    }
    RESET = '\033[0m'  # Reset color
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with color for console output.
        
        Args:
            record: Log record to format
            
        Returns:
            str: Formatted log message with color
        """
        # Get color for log level
        color = self.COLORS.get(record.levelno, '')
        
        # Format the message
        formatted = super().format(record)
        
        # Add color only if output is a terminal
        if color and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            return f"{color}{formatted}{self.RESET}"
        
        return formatted


def setup_logging(
    log_level: Union[int, str] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    enable_console: bool = True,
    enable_file: bool = True
) -> None:
    """
    Configure the logging system for the SnakeYCL game.
    
    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (defaults to LOG_FILE_PATH)
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        enable_console: Whether to enable console logging
        enable_file: Whether to enable file logging
    """
    # Convert string log level to integer if necessary
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    handlers = []
    
    # File handler with rotation
    if enable_file:
        log_file_path = Path(log_file) if log_file else Path(LOG_FILE_PATH)
        
        # Ensure log directory exists
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(
                logging.Formatter(
                    fmt=LOG_FORMAT,
                    datefmt=LOG_DATE_FORMAT
                )
            )
            handlers.append(file_handler)
            
        except Exception as e:
            print(f"Warning: Could not create file handler: {e}", file=sys.stderr)
    else:
        log_file_path = None
    
    # Console handler with colors
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(
            ColoredFormatter(
                fmt=LOG_FORMAT,
                datefmt=LOG_DATE_FORMAT
            )
        )
        handlers.append(console_handler)
    
    # Add handlers to root logger
    for handler in handlers:
        root_logger.addHandler(handler)
    
    # Log initialization message
    logger = logging.getLogger(__name__)
    logger.info(f"{GAME_TITLE} logging system initialized")
    logger.debug(f"Log level set to: {logging.getLevelName(log_level)}")
    
    if enable_file and log_file_path:
        logger.debug(f"File logging enabled: {log_file_path}")
    if enable_console:
        logger.debug("Console logging enabled")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the logger (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


def log_system_info() -> None:
    """
    Log system information for debugging purposes.
    """
    import platform
    import pygame
    
    logger = get_logger(__name__)
    
    logger.info("="*50)
    logger.info("SYSTEM INFORMATION")
    logger.info("="*50)
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Python Version: {platform.python_version()}")
    logger.info(f"Pygame Version: {pygame.version.ver}")
    logger.info(f"SDL Version: {pygame.version.SDL}")
    logger.info("="*50)


def log_performance_metrics(
    frame_rate: float,
    memory_usage: Optional[float] = None,
    cpu_usage: Optional[float] = None
) -> None:
    """
    Log performance metrics for monitoring.
    
    Args:
        frame_rate: Current frame rate (FPS)
        memory_usage: Memory usage in MB (optional)
        cpu_usage: CPU usage percentage (optional)
    """
    logger = get_logger("performance")
    
    metrics = [f"FPS: {frame_rate:.1f}"]
    
    if memory_usage is not None:
        metrics.append(f"Memory: {memory_usage:.1f}MB")
    
    if cpu_usage is not None:
        metrics.append(f"CPU: {cpu_usage:.1f}%")
    
    logger.debug(" | ".join(metrics))


def log_game_event(event_type: str, details: Optional[str] = None) -> None:
    """
    Log game events for analytics and debugging.
    
    Args:
        event_type: Type of event (e.g., "game_start", "game_over", "score")
        details: Additional event details
    """
    logger = get_logger("game_events")
    
    if details:
        logger.info(f"EVENT: {event_type} - {details}")
    else:
        logger.info(f"EVENT: {event_type}")


class PerformanceTimer:
    """
    Context manager for timing code execution.
    """
    
    def __init__(self, operation_name: str, logger_name: str = "performance"):
        self.operation_name = operation_name
        self.logger = get_logger(logger_name)
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        if self.start_time is not None:
            duration = time.perf_counter() - self.start_time
            self.logger.debug(f"{self.operation_name} took {duration:.4f}s")


# Convenience function for timing operations
def time_operation(operation_name: str, logger_name: str = "performance"):
    """
    Decorator/context manager for timing operations.
    
    Args:
        operation_name: Name of the operation being timed
        logger_name: Name of the logger to use
        
    Returns:
        PerformanceTimer: Timer context manager
    """
    return PerformanceTimer(operation_name, logger_name)