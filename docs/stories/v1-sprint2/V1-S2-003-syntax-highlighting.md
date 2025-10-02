# Add Syntax Highlighting in TUI

**ID:** V1-S2-003
**Epic:** UX Improvements
**Priority:** P1
**Size:** S (1.5 hours)
**Sprint:** V1 Sprint 2 - Day 2
**Status:** ✅ COMPLETED

## Implementation Summary
- **Commit:** `d5ac80f feat: add syntax highlighting for code blocks`
- **Files Modified:** 4 files (cli.py, tui.py, tui/app.py, formatters.py)
- **Implementation:** Rich library integration with smart language detection
- **Testing:** Verified in both CLI and TUI modes

## User Story
As a user viewing command examples,
I want syntax highlighting for code blocks,
So that commands are easier to read and understand.

## UX Preservation Requirements
- [x] Maintain existing keyboard interactions (F2 for transcript, Esc for clear/close, Enter for submit)
- [x] Preserve smooth TUI functionality and responsiveness
- [x] Keep existing logo and tagline "Your Security Learning Companion"
- [x] Ensure syntax highlighting doesn't break existing overlay system

## Acceptance Criteria
- [x] Syntax highlighting for:
  - Bash/shell commands
  - Python code
  - Common tool commands (nmap, sqlmap, etc.)
- [x] Use Rich library's syntax highlighting
- [x] Color scheme matches terminal theme
- [x] Works in both TUI and CLI modes
- [x] Graceful fallback if colors not supported

## Technical Notes

### Implementation
```python
from rich.syntax import Syntax
from rich.console import Console

def display_command(command: str, language: str = "bash"):
    """Display command with syntax highlighting"""
    console = Console()

    syntax = Syntax(
        command,
        language,
        theme="monokai",
        line_numbers=False,
        word_wrap=True
    )

    console.print(syntax)

# Example usage
display_command("""
# Scan target with nmap
nmap -sV -sC -oA scan 10.10.10.5

# Common ports
nmap -p- 10.10.10.5
""", language="bash")
```

### Language Detection
```python
def detect_language(command: str) -> str:
    """Detect language from command"""
    if command.strip().startswith('#!'):
        shebang = command.split('\n')[0]
        if 'python' in shebang:
            return 'python'
        if 'bash' in shebang or 'sh' in shebang:
            return 'bash'

    # Common tool detection
    tools = command.split()[0] if command else ''
    if tools in ['nmap', 'sqlmap', 'gobuster', 'ffuf']:
        return 'bash'

    return 'bash'  # default
```

### File Changes
- `src/cybuddy/tui/app.py` - Add syntax highlighting to TUI rendering ✅
- `src/cybuddy/cli.py` - Add syntax highlighting to CLI output ✅
- `src/cybuddy/tui.py` - Add syntax highlighting to simple TUI ✅
- `src/cybuddy/formatters.py` - Syntax formatter (new file) ✅

### Themes
Support popular themes:
- monokai (default)
- dracula
- github-dark
- nord

## Definition of Done
- [x] Syntax highlighting works in TUI
- [x] Syntax highlighting works in CLI
- [x] Language auto-detection works
- [x] Colors look good on dark/light terminals
- [x] Test: `cybuddy explain "nmap"` shows highlighted commands
- [x] Git commit: "feat: add syntax highlighting for code blocks"

## Testing Checklist
- [x] Bash commands highlighted correctly
- [x] Python code highlighted
- [x] Multi-line commands work
- [x] Dark terminal theme
- [x] Light terminal theme
- [x] No colors on dumb terminal

## Time Estimate Breakdown
- Implement syntax highlighting: 45 mins
- Language detection: 30 mins
- Testing: 15 mins

**Total: 1.5 hours**
