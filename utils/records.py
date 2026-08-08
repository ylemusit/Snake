"""
SnakeYCL Records Management
==========================

High score and records management system for the SnakeYCL game.
Handles loading, saving, and managing player scores and statistics.

Author: Yeison Arbey Carrillo Lemus (YACL)
Version: 1.0.0
Date: 2025-10-11
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from .constants import (
    RECORDS_FILE_PATH,
    HIGH_SCORE_LIMIT,
    AUTHOR,
    AUTHOR_ID
)

logger = logging.getLogger(__name__)


@dataclass
class GameRecord:
    """
    Represents a single game record/score entry.
    """
    
    score: int
    player_name: str
    date: str
    duration: float  # Game duration in seconds
    difficulty: str = "normal"
    snake_length: int = 3
    fruits_eaten: int = 0
    
    def __post_init__(self) -> None:
        """Validate record data after initialization."""
        if self.score < 0:
            raise ValueError("Score cannot be negative")
        if self.duration < 0:
            raise ValueError("Duration cannot be negative")
        if self.snake_length < 1:
            raise ValueError("Snake length must be at least 1")
        if self.fruits_eaten < 0:
            raise ValueError("Fruits eaten cannot be negative")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameRecord':
        """
        Create a GameRecord from dictionary data.
        
        Args:
            data: Dictionary containing record data
            
        Returns:
            GameRecord: Created record instance
        """
        return cls(
            score=data.get('score', 0),
            player_name=data.get('player_name', 'Anonymous'),
            date=data.get('date', datetime.now().isoformat()),
            duration=data.get('duration', 0.0),
            difficulty=data.get('difficulty', 'normal'),
            snake_length=data.get('snake_length', 3),
            fruits_eaten=data.get('fruits_eaten', 0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert record to dictionary format.
        
        Returns:
            Dict[str, Any]: Record as dictionary
        """
        return asdict(self)
    
    @property
    def formatted_date(self) -> str:
        """
        Get formatted date string for display.
        
        Returns:
            str: Formatted date string
        """
        try:
            dt = datetime.fromisoformat(self.date)
            return dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, AttributeError):
            return self.date
    
    @property
    def formatted_duration(self) -> str:
        """
        Get formatted duration string for display.
        
        Returns:
            str: Formatted duration string (e.g., "2:34")
        """
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes}:{seconds:02d}"


class RecordsManager:
    """
    Manages high scores and game records for SnakeYCL.
    """
    
    def __init__(self, records_file: Optional[Union[str, Path]] = None):
        """
        Initialize the records manager.
        
        Args:
            records_file: Path to records file (optional)
        """
        self.records_file = Path(records_file) if records_file else Path(RECORDS_FILE_PATH)
        self.records: List[GameRecord] = []
        self.load_records()
        
        logger.info("Records manager initialized")
    
    def load_records(self) -> bool:
        """
        Load records from file.
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if not self.records_file.exists():
            logger.info("Records file not found, starting with empty records")
            self.records = []
            return True
        
        try:
            with open(self.records_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Validate file format
            if not isinstance(data, dict) or 'records' not in data:
                logger.warning("Invalid records file format")
                self.records = []
                return False
            
            # Load records
            records_data = data.get('records', [])
            self.records = []
            
            for record_data in records_data:
                try:
                    record = GameRecord.from_dict(record_data)
                    self.records.append(record)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Skipping invalid record: {e}")
            
            # Sort records by score (descending)
            self.records.sort(key=lambda r: r.score, reverse=True)
            
            logger.info(f"Loaded {len(self.records)} records from file")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing records file: {e}")
            self.records = []
            return False
        
        except Exception as e:
            logger.error(f"Error loading records: {e}")
            self.records = []
            return False
    
    def save_records(self) -> bool:
        """
        Save records to file.
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Ensure directory exists
            self.records_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare data structure
            data = {
                'metadata': {
                    'game': 'SnakeYCL',
                    'version': '1.0.0',
                    'author': f"{AUTHOR} ({AUTHOR_ID})",
                    'last_updated': datetime.now().isoformat()
                },
                'records': [record.to_dict() for record in self.records]
            }
            
            # Write to file
            with open(self.records_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.records)} records to file")
            return True
            
        except Exception as e:
            logger.error(f"Error saving records: {e}")
            return False
    
    def add_record(self, record: GameRecord) -> bool:
        """
        Add a new record to the collection.
        
        Args:
            record: GameRecord to add
            
        Returns:
            bool: True if added (is a high score), False otherwise
        """
        try:
            # Add record to list
            self.records.append(record)
            
            # Sort by score (descending)
            self.records.sort(key=lambda r: r.score, reverse=True)
            
            # Keep only top scores
            if len(self.records) > HIGH_SCORE_LIMIT:
                self.records = self.records[:HIGH_SCORE_LIMIT]
            
            # Check if the added record is still in the list (is a high score)
            is_high_score = record in self.records
            
            if is_high_score:
                logger.info(f"New high score added: {record.score} by {record.player_name}")
                self.save_records()
            
            return is_high_score
            
        except Exception as e:
            logger.error(f"Error adding record: {e}")
            return False
    
    def get_high_scores(self, limit: Optional[int] = None) -> List[GameRecord]:
        """
        Get high scores list.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List[GameRecord]: List of high score records
        """
        if limit is None:
            return self.records.copy()
        return self.records[:limit]
    
    def get_best_score(self) -> Optional[GameRecord]:
        """
        Get the best (highest) score record.
        
        Returns:
            Optional[GameRecord]: Best score record or None if no records
        """
        return self.records[0] if self.records else None
    
    def is_high_score(self, score: int) -> bool:
        """
        Check if a score qualifies as a high score.
        
        Args:
            score: Score to check
            
        Returns:
            bool: True if it's a high score, False otherwise
        """
        if len(self.records) < HIGH_SCORE_LIMIT:
            return True
        
        return score > self.records[-1].score
    
    def get_player_records(self, player_name: str) -> List[GameRecord]:
        """
        Get all records for a specific player.
        
        Args:
            player_name: Name of the player
            
        Returns:
            List[GameRecord]: List of player's records
        """
        return [record for record in self.records if record.player_name == player_name]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall game statistics.
        
        Returns:
            Dict[str, Any]: Statistics dictionary
        """
        if not self.records:
            return {
                'total_games': 0,
                'highest_score': 0,
                'average_score': 0.0,
                'total_playtime': 0.0,
                'most_active_player': None
            }
        
        scores = [record.score for record in self.records]
        durations = [record.duration for record in self.records]
        
        # Count games per player
        player_counts = {}
        for record in self.records:
            player_counts[record.player_name] = player_counts.get(record.player_name, 0) + 1
        
        most_active_player = max(player_counts.items(), key=lambda x: x[1]) if player_counts else None
        
        return {
            'total_games': len(self.records),
            'highest_score': max(scores),
            'average_score': sum(scores) / len(scores),
            'total_playtime': sum(durations),
            'most_active_player': most_active_player[0] if most_active_player else None,
            'unique_players': len(player_counts)
        }
    
    def clear_records(self) -> bool:
        """
        Clear all records.
        
        Returns:
            bool: True if cleared successfully, False otherwise
        """
        try:
            self.records.clear()
            self.save_records()
            logger.info("All records cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing records: {e}")
            return False
    
    def export_records(self, export_path: Union[str, Path]) -> bool:
        """
        Export records to a different file.
        
        Args:
            export_path: Path where to export records
            
        Returns:
            bool: True if exported successfully, False otherwise
        """
        try:
            export_path = Path(export_path)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'exported_from': 'SnakeYCL',
                'export_date': datetime.now().isoformat(),
                'records': [record.to_dict() for record in self.records],
                'statistics': self.get_statistics()
            }
            
            with open(export_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Records exported to: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting records: {e}")
            return False


# Global records manager instance
_records_manager: Optional[RecordsManager] = None


def get_records_manager() -> RecordsManager:
    """
    Get the global records manager instance.
    
    Returns:
        RecordsManager: Global records manager
    """
    global _records_manager
    if _records_manager is None:
        _records_manager = RecordsManager()
    return _records_manager


def create_game_record(
    score: int,
    player_name: str,
    duration: float,
    difficulty: str = "normal",
    snake_length: int = 3,
    fruits_eaten: int = 0
) -> GameRecord:
    """
    Create a new game record with current timestamp.
    
    Args:
        score: Final game score
        player_name: Name of the player
        duration: Game duration in seconds
        difficulty: Game difficulty level
        snake_length: Final snake length
        fruits_eaten: Number of fruits eaten
        
    Returns:
        GameRecord: Created game record
    """
    return GameRecord(
        score=score,
        player_name=player_name,
        date=datetime.now().isoformat(),
        duration=duration,
        difficulty=difficulty,
        snake_length=snake_length,
        fruits_eaten=fruits_eaten
    )