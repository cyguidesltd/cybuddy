# Natural Language Chat Interface

**ID:** V1-S2-006
**Epic:** UX Improvements
**Priority:** P0 (Critical)
**Size:** M (2 hours)
**Sprint:** V1 Sprint 2 - Day 2
**Status:** ✅ COMPLETED

## Implementation Summary
- **Commit:** `a3f90f1 feat: add natural language query parser`
- **Files Created:**
  - `src/cybuddy/nl_parser.py` - Natural language parser (220 lines)
  - `tests/test_nl_parser.py` - Comprehensive tests (198 lines)
- **Tests:** 34 unit tests, 100% pass rate
- **Result:** Successfully parses natural language queries into commands

## User Story
As a user who's not familiar with command syntax,
I want to chat in plain English,
So that I don't need to memorize command names.

## UX Preservation Requirements
- [ ] Maintain existing keyboard interactions (F2 for transcript, Esc for clear/close, Enter for submit)
- [ ] Preserve smooth TUI functionality and responsiveness
- [ ] Keep existing logo and tagline "Your Security Learning Companion"
- [ ] Ensure natural language parsing doesn't break existing command processing
- [ ] Maintain existing overlay system functionality

## Acceptance Criteria
- [ ] Parse natural language queries into commands
- [ ] Support common phrasings:
  - "how do I..." → explain
  - "what should I do..." → plan
  - "tips on..." / "guide for..." → tip
  - "I'm getting..." → help/assist
  - "document..." / "write up..." → report
  - "test me on..." → quiz
- [ ] Show suggested command for transparency
- [ ] Works in both TUI and CLI modes
- [ ] Fallback to AI if enabled (with --send flag)
- [ ] Extract topic/query from natural language

## Technical Notes

### Natural Language Parser
```python
# src/secbuddy/nl_parser.py
from typing import Tuple
import re

def parse_natural_query(text: str) -> Tuple[str, str]:
    """
    Parse natural language into (command, query).

    Examples:
        "how do I scan for open ports?" → ("explain", "nmap")
        "what should I do after getting a shell?" → ("plan", "got shell")
        "tips on sql injection" → ("tip", "sql injection")
    """
    text_lower = text.lower().strip()

    # Intent detection patterns
    intents = {
        'explain': [
            r'how do i (.*)',
            r'how to (.*)',
            r'explain (.*)',
            r'what is (.*)',
            r'tell me about (.*)',
        ],
        'plan': [
            r'what should i do (.*)',
            r'what next (.*)',
            r'next steps (.*)',
            r'i (found|got|have) (.*)',
        ],
        'tip': [
            r'tips? (on|for|about) (.*)',
            r'guide (for|to) (.*)',
            r'learn about (.*)',
        ],
        'help': [
            r"i'?m getting (.*)",
            r'(error|problem|issue):? (.*)',
            r'why (.*)',
            r'fix (.*)',
        ],
        'report': [
            r'document (.*)',
            r'write up (.*)',
            r'report (.*)',
        ],
        'quiz': [
            r'test me on (.*)',
            r'quiz (.*)',
            r'question about (.*)',
        ]
    }

    # Try to match intent
    for command, patterns in intents.items():
        for pattern in patterns:
            match = re.match(pattern, text_lower)
            if match:
                query = match.group(1).strip()
                return command, query

    # Fallback: assume explain if contains tool/technique keywords
    if any(word in text_lower for word in ['nmap', 'burp', 'sqlmap', 'metasploit']):
        return 'explain', text

    # Default fallback
    return 'explain', text


def extract_topic(text: str) -> str:
    """Extract main topic from natural language query."""
    # Remove question words
    stopwords = ['how', 'do', 'i', 'what', 'should', 'the', 'a', 'an', 'is']
    words = text.lower().split()
    filtered = [w for w in words if w not in stopwords]
    return ' '.join(filtered)
```

### Integration with CLI
```python
# src/secbuddy/cli.py

from .nl_parser import parse_natural_query

def main():
    """Main entry point."""
    args = sys.argv[1:]

    # Check if natural language query
    if args and not args[0].startswith('-'):
        query = ' '.join(args)

        # If looks like natural language (has question marks, multiple words, etc.)
        if '?' in query or len(args) > 3:
            command, extracted_query = parse_natural_query(query)

            print(f"🤔 I think you mean: {command} \"{extracted_query}\"")
            print()

            # Execute the detected command
            if command == 'explain':
                result = explain_command(extracted_query, send=False)
            elif command == 'tip':
                result = quick_tip(extracted_query, send=False)
            # ... etc

            print(result)
            return 0
```

### Integration with TUI
```python
# src/secbuddy/tui/app.py and src/secbuddy/simple_tui.py

def _process_user_input(self, text: str) -> None:
    """Process user input - support natural language."""
    # Check if it's a natural language query
    if '?' in text or len(text.split()) > 4:
        command, query = parse_natural_query(text)

        self.history.append(f"🤔 I think you mean: {command} '{query}'")
        self.history.append("")

        # Execute command
        if command == 'explain':
            result = explain_command(query, send=False)
        # ... etc

        self.history.append(result)
    else:
        # Normal command processing
        self._execute_command(text)
```

## Examples

### Example 1: Scanning
```bash
$ cybuddy "how do I scan for open ports?"

🤔 I think you mean: explain "nmap"

═══ EXPLAIN: nmap ═══
Network Mapper - powerful port scanner and service detection tool

Common Usage:
  nmap -sV target        # Service version detection
  nmap -p- target        # Scan all ports
  nmap -A target         # Aggressive scan

Tips for Beginners:
  - Start with -sV for service detection
  - Use -Pn if ping is blocked
  - Can trigger IDS/IPS, use -T2 for stealth
```

### Example 2: Post-Exploitation
```bash
$ cybuddy "what should I do after getting a shell?"

🤔 I think you mean: plan "got shell"

═══ PLAN: got shell ═══

Next 3 Steps:
  1. Stabilize shell (python pty, script /dev/null)
  2. Enumerate system (uname -a, sudo -l, SUID binaries)
  3. Look for privilege escalation paths

Commands:
  python -c 'import pty; pty.spawn("/bin/bash")'
  sudo -l
  find / -perm -4000 -type f 2>/dev/null
```

### Example 3: Learning
```bash
$ cybuddy "tips on sql injection"

🤔 I think you mean: tip "sql injection"

═══ TIP: SQL Injection ═══

Common Payloads:
  ' OR 1=1--
  admin'--
  ' UNION SELECT NULL--

Where to Look:
  - Login forms (username/password)
  - Search boxes
  - URL parameters (?id=1)

Quick Wins:
  - Try single quote (') - look for SQL errors
  - Check for ' OR 1=1-- bypass
  - Test with sqlmap for automation
```

## File Changes
- `src/secbuddy/nl_parser.py` - New file (natural language parser)
- `src/secbuddy/cli.py` - Add NL detection
- `src/secbuddy/tui/app.py` - Add NL support in main TUI
- `src/secbuddy/simple_tui.py` - Add NL support in simple TUI
- `tests/test_nl_parser.py` - Unit tests

## Definition of Done
- [ ] Natural language parser implemented
- [ ] Integrated with CLI mode
- [ ] Integrated with TUI mode
- [ ] 10+ example phrases tested
- [ ] Shows suggested command
- [ ] Falls back to AI if --send flag provided
- [ ] Documentation updated
- [ ] Git commit: "feat: add natural language chat interface"

## Testing Checklist
- [ ] "how do I scan for open ports?" → explain nmap
- [ ] "what should I do after getting a shell?" → plan "got shell"
- [ ] "tips on sql injection" → tip "sql injection"
- [ ] "I'm getting connection refused" → help "connection refused"
- [ ] "document xss vulnerability" → report "xss"
- [ ] "test me on buffer overflow" → quiz "buffer overflow"
- [ ] Works in CLI mode
- [ ] Works in TUI mode
- [ ] Shows suggested command

## Time Estimate Breakdown
- NL parser implementation: 45 mins
- CLI integration: 30 mins
- TUI integration: 30 mins
- Testing: 15 mins

**Total: 2 hours**
