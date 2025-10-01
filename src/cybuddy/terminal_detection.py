"""Terminal capability detection for auto-selecting TUI/CLI mode."""

from __future__ import annotations

import os
import sys
from shutil import get_terminal_size
from typing import Literal


def can_use_tui() -> bool:
    """
    Detect if TUI mode can be used based on terminal capabilities.
    
    Returns:
        True if TUI mode is supported, False otherwise.
    """
    # Check if running in interactive terminal
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return False

    # Check terminal size (minimum 80x24 for TUI)
    try:
        size = get_terminal_size()
        if size.columns < 80 or size.lines < 24:
            return False
    except (OSError, ValueError):
        return False

    # Check TERM environment variable
    term = os.environ.get('TERM', '')
    if term in ['dumb', 'unknown', '']:
        return False

    # Check if in SSH without proper terminal
    if os.environ.get('SSH_TTY') and term == 'dumb':
        return False

    # Check for Windows CMD (limited TUI support)
    if os.name == 'nt' and os.environ.get('TERM') is None:
        # Windows CMD without TERM set - limited TUI support
        return False

    return True


def select_mode() -> Literal['tui', 'cli']:
    """
    Select appropriate mode based on terminal capabilities and user preferences.
    
    Returns:
        'tui' if TUI mode is supported and preferred, 'cli' otherwise.
    """
    # Check for manual override flags
    if '--cli' in sys.argv:
        return 'cli'
    if '--tui' in sys.argv:
        return 'tui'

    # Auto-detect based on terminal capabilities
    return 'tui' if can_use_tui() else 'cli'


def get_fallback_message() -> str:
    """
    Get a helpful message explaining why CLI mode was selected.
    
    Returns:
        Explanation message for CLI fallback.
    """
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return "Using CLI mode (not running in interactive terminal)"
    
    # Check terminal size
    try:
        size = get_terminal_size()
        if size.columns < 80 or size.lines < 24:
            return f"Using CLI mode (terminal too small: {size.columns}x{size.lines}, need 80x24+)"
    except (OSError, ValueError):
        return "Using CLI mode (cannot determine terminal size)"
    
    # Check TERM environment variable
    term = os.environ.get('TERM', '')
    if term in ['dumb', 'unknown', '']:
        return f"Using CLI mode (terminal type '{term}' doesn't support TUI)"
    
    # Check SSH without proper terminal
    if os.environ.get('SSH_TTY') and term == 'dumb':
        return "Using CLI mode (SSH session without proper terminal)"
    
    # Check Windows CMD
    if os.name == 'nt' and os.environ.get('TERM') is None:
        return "Using CLI mode (Windows CMD without TERM support)"
    
    return "Using CLI mode (terminal doesn't support TUI)"
