"""Simple CLI with Rich formatting - no complex async TUI."""
from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .cli import (
    explain_command,
    help_troubleshoot,
    history_append,
    micro_report,
    quick_tip,
    quiz_flashcards,
    step_planner,
)


def run_simple_guide(session: str | None = None) -> int:
    """Run the simple guide with Rich formatting."""
    console = Console()

    # Show welcome
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Cybuddy - Simple Security Learning Helper[/bold cyan]",
        border_style="cyan"
    ))
    console.print()

    console.print("[cyan]Available commands:[/cyan]")
    commands = {
        "explain": "Learn commands (e.g., explain 'nmap -sV')",
        "tip": "Study guide (e.g., tip 'SQL injection')",
        "help": "Troubleshoot (e.g., help 'connection refused')",
        "report": "Practice write-ups (e.g., report 'Found SQLi')",
        "quiz": "Active recall (e.g., quiz 'SQL Injection')",
        "plan": "Next steps (e.g., plan 'found port 80 open')",
        "exit": "Exit Cybuddy",
    }

    for cmd, desc in commands.items():
        console.print(f"  [yellow]{cmd:8s}[/yellow] → {desc}")

    console.print()
    console.print("[dim]Examples:[/dim]")
    console.print("  [dim]explain 'nmap -sV target.local'[/dim]")
    console.print("  [dim]tip 'SQL injection basics'[/dim]")
    console.print("  [dim]help 'connection refused'[/dim]")
    console.print()

    # Main loop
    while True:
        try:
            text = console.input("[bold cyan]❯[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            break

        if not text:
            continue

        if text.lower() in {"exit", "quit"}:
            console.print("[green]Good luck! Document your steps and be safe.[/green]")
            break

        # Parse command
        parts = text.split(maxsplit=1)
        if not parts:
            continue

        cmd = parts[0].lower()
        arg = parts[1].strip('"\'') if len(parts) > 1 else ""

        # Process command
        console.print()

        if cmd == "explain":
            if not arg:
                console.print("[red]⚠[/red] Usage: explain '<command>'")
            else:
                result = explain_command(arg)
                _print_response(console, "Explanation", result)

        elif cmd == "tip":
            if not arg:
                console.print("[red]⚠[/red] Usage: tip '<topic>'")
            else:
                result = quick_tip(arg)
                _print_response(console, "Tip", result)

        elif cmd == "help":
            if not arg:
                console.print("[red]⚠[/red] Usage: help '<error message>'")
            else:
                result = help_troubleshoot(arg)
                _print_response(console, "Troubleshooting", result)

        elif cmd == "report":
            if not arg:
                console.print("[red]⚠[/red] Usage: report '<finding>'")
            else:
                result = micro_report(arg)
                _print_response(console, "Report Template", result)

        elif cmd == "quiz":
            if not arg:
                console.print("[red]⚠[/red] Usage: quiz '<topic>'")
            else:
                result = quiz_flashcards(arg)
                _print_response(console, "Quiz", result)

        elif cmd == "plan":
            if not arg:
                console.print("[red]⚠[/red] Usage: plan '<context>'")
            else:
                result = step_planner(arg)
                _print_response(console, "Next Steps", result)

        else:
            console.print(f"[red]⚠[/red] Unknown command: {cmd}")
            console.print("[dim]Available: " + ", ".join(commands.keys()) + "[/dim]")

        console.print()

        # Log to history
        history_append({"type": "interactive_cli", "data": {"cmd": cmd, "arg": arg}}, session=session)

    return 0


def _print_response(console: Console, title: str, content: str) -> None:
    """Print a formatted response."""
    console.print(Panel(
        Text(content),
        title=f"[bold yellow]{title}[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    ))


__all__ = ["run_simple_guide"]