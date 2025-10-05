from __future__ import annotations

import json
import os
import sys
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

from .history import add_command

STARTER_PROMPT = (
    "You are CyBuddy, a helpful cybersecurity study companion. "
    "You explain steps simply, provide safe defaults, and always suggest next actions. "
    "You avoid running destructive commands and emphasize documenting findings."
)


def print_help() -> int:
    print(
        """
CyBuddy - beginner-friendly cybersecurity helper

Usage:
  cybuddy                    Launch interactive learning interface (TUI)
  cybuddy <command> [args]   Run specific command

7 Core Commands (Interactive TUI):
  explain '<command>'        Learn what commands do (e.g., explain 'nmap -sV')
  tip '<topic>'              Study guide for security topics
  help '<error>'             Troubleshoot errors and issues
  report '<finding>'         Practice writing security reports (2-3 lines)
  quiz '<topic>'             Active recall with flashcards
  plan '<context>'           Get next steps guidance (3 steps)
  history                    Show command history
  exit                       Exit the interface

Additional Commands:
  cybuddy explain "<command>"   One-shot explain (use TUI for interactive)
  cybuddy tip "<topic>"         One-shot tip (use TUI for interactive)
  cybuddy assist "<issue>"      One-shot troubleshoot
  cybuddy report "<finding>"    One-shot report template
  cybuddy quiz "<topic>"        One-shot quiz
  cybuddy plan "<context>"      One-shot plan
  cybuddy history [--clear]     Show or clear recent session history

Examples:
  cybuddy                      # Launch interactive mode
  explain 'nmap -sV target.local'         # Inside TUI
  tip 'SQL injection basics'              # Inside TUI
  help 'sqlmap connection refused'        # Inside TUI
        """.strip()
    )
    return 0




def cmd_guide(stdin: Iterable[str] = sys.stdin, session: str | None = None) -> int:
    # Setup readline for CLI history
    import readline

    from .history import add_command
    
    # Load history into readline
    histfile = os.path.expanduser("~/.local/share/cybuddy/history.txt")
    try:
        readline.read_history_file(histfile)
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass
    
    # Register cleanup
    import atexit
    atexit.register(readline.write_history_file, histfile)
    
    # Print colored shield logo with gradient (green to cyan) and medical cross
    # Matches the SVG design: rgb(0,255,136) → rgb(0,255,255)
    print("\033[1;38;2;0;255;136m        ▄▀▀▀▄\033[0m")
    print("\033[1;38;2;0;255;150m       █  │  █\033[0m")
    print("\033[1;38;2;0;255;170m      █ ──┼── █\033[0m      \033[1;97mCY\033[1;38;2;0;255;255mBUDDY\033[0m")
    print("\033[1;38;2;0;255;190m      █   │   █\033[0m")
    print("\033[1;38;2;0;255;210m       █     █\033[0m       \033[2mYour Security Learning Companion\033[0m")
    print("\033[1;38;2;0;255;230m        █   █\033[0m")
    print("\033[1;38;2;0;255;245m         █ █\033[0m")
    print("\033[1;38;2;0;255;255m          ▀\033[0m\n")
    print("Type 'exit' to quit. Use /tip, /plan, /checklist <topic>, /todo add <..>, /run <tool> \"args\"")
    print("Use ↑↓ arrows for command history, Ctrl+R for reverse search")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            print()
            break

        if not line:
            continue
        if line.lower() in {"exit", "quit"}:
            print("Good luck! Document your steps and be safe.")
            break

        # Add to command history
        add_command(line)

        # Slash commands
        if line.startswith("/"):
            print(_guide_handle_slash(line, session=session))
            continue

        # Render codex-like sections using handlers
        from .handlers import handle_user_input

        response = handle_user_input(line, session=session)
        print("PLAN:")
        print("- " + response.plan)
        print("ACTION:\n- " + response.action)
        if response.cmd:
            print("CMD:")
            print(response.cmd)
        print("OUT:\n" + response.output)
        print("NEXT:\n- " + response.next_step)
        history_append({"type": "guide", "data": {"input": line, "plan": response.plan}}, session=session)
    return 0


def _guide_handle_slash(line: str, session: str | None = None) -> str:
    """Handle slash commands in guide mode (delegates to handlers)."""
    from .handlers import handle_slash_command
    response = handle_slash_command(line, session=session)
    return response.output


def cmd_guide_tui(session: str | None = None, simple: bool = True) -> int:
    """
    Launch the interactive TUI for guide mode.

    Uses prompt_toolkit's proper async API (PromptSession.prompt_async)
    instead of low-level read_keys() for reliable input handling.
    """
    import asyncio

    # Use the TUI with proper prompt_toolkit usage
    from .tui import SimpleTUI
    app = SimpleTUI(session=session)

    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\nGood luck! Document your steps and be safe.")
    return 0


def _guide_command_hint(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["nmap", "scan", "port"]):
        return "nmap -sV -Pn -T2 <target>"
    if any(k in t for k in ["dir", "enum", "hidden", "wordlist"]):
        return "gobuster dir -u http://<host> -w <wordlist>"
    if any(k in t for k in ["vuln", "nikto"]):
        return "nikto -h http://<host>"
    return ""


def suggest_next(user_text: str) -> str:
    t = user_text.lower()
    if any(k in t for k in ["nmap", "scan", "port"]):
        return (
            "Try: nmap -sV -Pn -T2 <target>. Start safe; document findings."
        )
    if any(k in t for k in ["web", "http", "xss", "sql", "burp"]):
        return (
            "Check robots.txt, headers, inputs. Consider Burp with passive scans first."
        )
    if any(k in t for k in ["hash", "cipher", "encode", "crypto"]):
        return (
            "Identify format (hashid), test small samples, avoid brute-force blindly."
        )
    if any(k in t for k in ["forensic", "image", "pcap", "memory"]):
        return (
            "Verify file magic, run strings/hexdump, use appropriate carve/analysis tools."
        )
    return (
        "Break the task down: scope -> safe defaults -> record results -> next step."
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    
    # If no arguments, launch TUI directly
    if not args:
        return cmd_guide_tui()
    
    # Check for help flags
    if args[0] in {"-h", "--help", "help"}:
        return print_help()

    # Check for natural language query (quoted string or multiple words)
    if len(args) == 1 and (' ' in args[0] or args[0].startswith('"') or args[0].startswith("'")):
        from .nl_parser import is_natural_language, parse_natural_query
        query = args[0].strip('"\'')
        if is_natural_language(query):
            cmd, parsed_query = parse_natural_query(query)
            # Execute the parsed command directly
            args = [cmd, parsed_query]
        else:
            cmd = args[0]
    else:
        cmd = args[0]

    # Student helpers
    if cmd == "explain":
        if len(args) < 2:
            from .errors import handle_missing_argument
            return handle_missing_argument("explain", "command", "cybuddy explain 'nmap -sV'")
        text = _extract_text(args[1:])
        add_command(f"explain {text}")
        return _maybe_json_print("explain", text, explain_command(text))
    if cmd in {"assist", "help"}:
        if len(args) < 2:
            from .errors import handle_missing_argument
            return handle_missing_argument(cmd, "issue", "cybuddy assist 'connection refused'")
        text = _extract_text(args[1:])
        add_command(f"{cmd} {text}")
        return _maybe_json_print("assist", text, help_troubleshoot(text))
    if cmd == "tip":
        if len(args) < 2:
            from .errors import handle_missing_argument
            return handle_missing_argument("tip", "topic", "cybuddy tip 'sql injection'")
        text = _extract_text(args[1:])
        add_command(f"tip {text}")
        return _maybe_json_print("tip", text, quick_tip(text))
    if cmd == "report":
        if len(args) < 2:
            from .errors import handle_missing_argument
            return handle_missing_argument("report", "finding", "cybuddy report 'found XSS in login'")
        text = _extract_text(args[1:])
        add_command(f"report {text}")
        return _maybe_json_print("report", text, micro_report(text))
    if cmd == "quiz":
        if len(args) < 2:
            from .errors import handle_missing_argument
            return handle_missing_argument("quiz", "topic", "cybuddy quiz 'nmap'")
        text = _extract_text(args[1:])
        add_command(f"quiz {text}")
        return _maybe_json_print("quiz", text, quiz_flashcards(text))
    if cmd == "plan":
        if len(args) < 2:
            from .errors import handle_missing_argument
            return handle_missing_argument("plan", "context", "cybuddy plan 'found open port 8080'")
        text = _extract_text(args[1:])
        add_command(f"plan {text}")
        return _maybe_json_print("plan", text, step_planner(text))
        

    if cmd == "history":
        from .commands.history import cmd_history
        return cmd_history(args[1:])

    # Unknown command - provide smart suggestions
    from .errors import handle_unknown_command
    return handle_unknown_command(cmd)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


def _maybe_json_print(kind: str, input_text: str, output_text: str) -> int:
    if os.environ.get("CYBUDDY_JSON") == "1":
        obj = {"type": kind, "input": input_text, "output": output_text, "ts": _now_iso()}
        print(json.dumps(obj))
        return 0
    print(output_text)
    return 0

# === Student-focused helpers (uses rich mockup data) ===

def explain_command(command_text: str) -> str:
    from .data import smart_explain
    return smart_explain(command_text)


def quick_tip(topic: str) -> str:
    from .data import smart_tip
    return smart_tip(topic)


def help_troubleshoot(issue: str) -> str:
    from .data import smart_assist
    return smart_assist(issue)


def micro_report(finding: str) -> str:
    from .data import smart_report
    return smart_report(finding)


def quiz_flashcards(topic: str) -> str:
    from .data import smart_quiz
    return smart_quiz(topic)


def step_planner(context: str) -> str:
    from .data import smart_plan
    return smart_plan(context)


# === Lightweight session history and TODO tracker ===

def _app_dir() -> Path:
    # Respect HOME override; do not create directories unless needed later
    home = os.environ.get("HOME") or os.path.expanduser("~")
    return Path(home) / ".cybuddy"


def _history_file(session: str | None = None) -> Path:
    cfg = load_config()
    if session:
        base = _app_dir() / "sessions" / session
        path = base / "history.jsonl"
    else:
        path = Path(os.path.expanduser(cfg.get("history.path", str(_app_dir() / "history.jsonl"))))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return path




def _config_file() -> Path:
    """Legacy config file path for backward compatibility."""
    return _app_dir() / "config.toml"


def load_config() -> dict:
    """Load configuration using the new config system."""
    from .config import load_config as load_new_config
    
    # Load new config system
    new_config = load_new_config()
    
    # Convert to old format for backward compatibility
    cfg = {
        "history.enabled": new_config.get("history", {}).get("enabled", True),
        "history.path": new_config.get("history", {}).get("path", str(_app_dir() / "history.jsonl")),
        "output.truncate_lines": new_config.get("output", {}).get("truncate_lines", 60),
        "history.verbatim": new_config.get("history", {}).get("verbatim", False),
    }
    
    return cfg




def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def history_append(event: dict, session: str | None = None) -> None:
    cfg = load_config()
    if not cfg.get("history.enabled", True):
        return
    try:
        payload = {"ts": _now_iso(), **event}
        with _history_file(session).open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        pass












def _extract_text(args: list[str]) -> str:
    """Extract text from command arguments."""
    return " ".join(args).strip("\"")




# === Dry-run runner (approvals-like) ===



