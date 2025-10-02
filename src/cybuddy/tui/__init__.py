"""Terminal UI package for CyBuddy.

This package mirrors the Codex CLI TUI architecture using Python libraries.
"""

from .app import CybuddyApp
from .simple import SimpleTUI

__all__ = ["CybuddyApp", "SimpleTUI"]
