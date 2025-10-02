from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class CommandHistory:
    """Persistent command history with deduplication and size limits."""
    
    def __init__(self, max_size: int = 1000):
        self.history_file = Path.home() / '.local' / 'share' / 'cybuddy' / 'history.json'
        self.max_size = max_size
        self.history = self.load()
    
    def load(self) -> List[str]:
        """Load history from file."""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                return data.get('commands', [])
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save(self) -> None:
        """Save history to file."""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.history_file, 'w') as f:
            json.dump({
                'commands': self.history[-self.max_size:],
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
    
    def add(self, command: str) -> None:
        """Add command to history with deduplication."""
        # Don't add if same as last command
        if self.history and self.history[-1] == command:
            return
        
        self.history.append(command)
        self.save()
    
    def clear(self) -> None:
        """Clear history."""
        self.history = []
        if self.history_file.exists():
            self.history_file.unlink()
    
    def get_history(self) -> List[str]:
        """Get all history entries."""
        return self.history.copy()
    
    def search(self, query: str) -> List[str]:
        """Search history for commands containing query."""
        return [cmd for cmd in self.history if query.lower() in cmd.lower()]


# Global history instance
_history_instance: Optional[CommandHistory] = None


def get_history() -> CommandHistory:
    """Get the global history instance."""
    global _history_instance
    if _history_instance is None:
        _history_instance = CommandHistory()
    return _history_instance


def add_command(command: str) -> None:
    """Add a command to history."""
    get_history().add(command)


def clear_history() -> None:
    """Clear command history."""
    get_history().clear()


def get_history_entries() -> List[str]:
    """Get all history entries."""
    return get_history().get_history()


def search_history(query: str) -> List[str]:
    """Search history for commands containing query."""
    return get_history().search(query)
