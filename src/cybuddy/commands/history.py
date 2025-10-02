from __future__ import annotations

import sys
from typing import List

from ..history import get_history_entries, search_history, clear_history


def cmd_history(args: List[str]) -> int:
    """Handle the history command."""
    if not args:
        # Show recent history
        entries = get_history_entries()
        if not entries:
            print("No command history yet.")
            return 0
        
        print("Recent commands:")
        for i, cmd in enumerate(entries[-20:], 1):  # Show last 20
            print(f"{i:3d}. {cmd}")
        return 0
    
    if args[0] == "--clear":
        clear_history()
        print("Command history cleared.")
        return 0
    
    if args[0] == "--search" and len(args) > 1:
        query = " ".join(args[1:])
        results = search_history(query)
        if not results:
            print(f"No commands found matching '{query}'.")
            return 0
        
        print(f"Commands matching '{query}':")
        for i, cmd in enumerate(results, 1):
            print(f"{i:3d}. {cmd}")
        return 0
    
    print("Usage: cybuddy history [--clear|--search <query>]")
    return 1
