# Add Command History

**ID:** V1-S2-005
**Epic:** UX Improvements
**Priority:** P2
**Size:** S (1.5 hours)
**Sprint:** V1 Sprint 2 - Day 2

## User Story
As a frequent user,
I want to access my previous queries using up/down arrows,
So that I can quickly repeat or modify past searches.

## Acceptance Criteria
- [ ] Command history persists across sessions
- [ ] Up/down arrows navigate history
- [ ] Ctrl+R for reverse search
- [ ] History stored in `~/.local/share/cybuddy/history`
- [ ] Max 1000 entries (configurable)
- [ ] Deduplicate consecutive identical commands
- [ ] Clear history with `cybuddy history --clear`
- [ ] View history with `cybuddy history`

## Technical Notes

### Implementation
```python
from pathlib import Path
import json

class CommandHistory:
    def __init__(self, max_size: int = 1000):
        self.history_file = Path.home() / '.local/share' / 'cybuddy' / 'history.json'
        self.max_size = max_size
        self.history = self.load()

    def load(self) -> list:
        """Load history from file"""
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file) as f:
                data = json.load(f)
                return data.get('commands', [])
        except:
            return []

    def save(self):
        """Save history to file"""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.history_file, 'w') as f:
            json.dump({
                'commands': self.history[-self.max_size:],
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)

    def add(self, command: str):
        """Add command to history"""
        # Don't add if same as last command
        if self.history and self.history[-1] == command:
            return

        self.history.append(command)
        self.save()

    def clear(self):
        """Clear history"""
        self.history = []
        if self.history_file.exists():
            self.history_file.unlink()
```

### TUI Integration
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

# In TUI mode
session = PromptSession(
    history=FileHistory(str(history_file))
)

user_input = session.prompt('cybuddy> ')
```

### CLI Integration
```python
import readline

# Setup readline for CLI
histfile = os.path.expanduser("~/.local/share/cybuddy/history.txt")
try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

import atexit
atexit.register(readline.write_history_file, histfile)
```

### File Changes
- `src/secbuddy/history.py` - History management
- `src/secbuddy/tui/input.py` - TUI history
- `src/secbuddy/cli.py` - CLI history
- `src/secbuddy/commands/history.py` - History command

### Commands
```bash
# View history
cybuddy history

# Clear history
cybuddy history --clear

# Search history
cybuddy history --search "nmap"
```

## Definition of Done
- [ ] History works in TUI mode
- [ ] History works in CLI mode
- [ ] Up/down arrows work
- [ ] Ctrl+R search works (TUI)
- [ ] History persists across sessions
- [ ] `cybuddy history` command works
- [ ] Git commit: "feat: add command history"

## Testing Checklist
- [ ] Add commands to history
- [ ] Navigate with up/down arrows
- [ ] History persists after restart
- [ ] Deduplication works
- [ ] Max size limit works
- [ ] Clear history works
- [ ] View history works

## Time Estimate Breakdown
- Implement history class: 30 mins
- TUI integration: 30 mins
- CLI integration: 20 mins
- Testing: 10 mins

**Total: 1.5 hours**
