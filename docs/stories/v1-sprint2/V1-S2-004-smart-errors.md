# Implement Smart Error Messages

**ID:** V1-S2-004
**Epic:** UX Improvements
**Priority:** P1
**Size:** S (1.5 hours)
**Sprint:** V1 Sprint 2 - Day 2
**Status:** ✅ COMPLETED

## User Story
As a user who makes mistakes,
I want helpful error messages that guide me to the solution,
So that I can fix issues quickly without reading documentation.

## Acceptance Criteria
- [ ] Error messages include:
  - What went wrong (clear description)
  - Why it happened
  - How to fix it (actionable steps)
  - Similar commands (suggestions)
- [ ] Detect common mistakes:
  - Typos in tool names
  - Invalid command syntax
  - Missing arguments
- [ ] Suggest corrections using fuzzy matching
- [ ] Link to relevant documentation
- [ ] Show examples of correct usage

## Technical Notes

### Smart Error System
```python
from difflib import get_close_matches

class SmartError:
    def __init__(self, message: str, suggestions: list = None):
        self.message = message
        self.suggestions = suggestions or []

    def display(self):
        """Display error with helpful information"""
        console.print(f"[red]✗ Error:[/red] {self.message}")

        if self.suggestions:
            console.print("\n[yellow]💡 Did you mean:[/yellow]")
            for suggestion in self.suggestions:
                console.print(f"  • {suggestion}")

def handle_unknown_tool(tool_name: str):
    """Handle unknown tool with suggestions"""
    all_tools = get_all_tool_names()
    matches = get_close_matches(tool_name, all_tools, n=3, cutoff=0.6)

    error = SmartError(
        f"Tool '{tool_name}' not found in database",
        suggestions=[
            f"cybuddy explain \"{match}\"" for match in matches
        ]
    )
    error.display()

    # Show similar categories
    console.print("\n[cyan]💭 Browse categories:[/cyan]")
    console.print("  cybuddy list tools")
    console.print("  cybuddy search \"web scanning\"")
```

### Common Error Scenarios

#### 1. Unknown Tool
```
✗ Error: Tool 'nmpa' not found

💡 Did you mean:
  • cybuddy explain "nmap"
  • cybuddy explain "masscan"

💭 Browse all tools:
  cybuddy list tools
```

#### 2. Invalid Command
```
✗ Error: Invalid command 'explian'

💡 Did you mean:
  • cybuddy explain "nmap"
  • cybuddy list

📚 See all commands:
  cybuddy --help
```

#### 3. Missing Argument
```
✗ Error: Command 'explain' requires a tool name

💡 Usage:
  cybuddy explain "nmap"
  cybuddy explain "sql injection"

📚 See examples:
  cybuddy examples
```

### File Changes
- `src/secbuddy/errors.py` - Smart error classes
- `src/secbuddy/suggestions.py` - Fuzzy matching
- `src/secbuddy/main.py` - Error handling

## Definition of Done
- [x] All error messages are helpful
- [x] Fuzzy matching suggests alternatives
- [x] Error messages include examples
- [x] Test common mistake scenarios
- [x] Git commit: "feat: smart error messages with suggestions"

## Testing Checklist
- [ ] Unknown tool name
- [ ] Typo in command
- [ ] Missing required argument
- [ ] Invalid argument format
- [ ] Empty query
- [ ] Special characters in input

## Time Estimate Breakdown
- Implement error classes: 30 mins
- Fuzzy matching: 30 mins
- Error templates: 20 mins
- Testing: 10 mins

**Total: 1.5 hours**
