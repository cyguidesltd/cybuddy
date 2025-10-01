"""Simple TUI with 7 core commands focused on learning and practice."""
from __future__ import annotations

import asyncio
from typing import Optional

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .tui.core import TerminalController, FrameScheduler, HistoryBuffer
from .tui.core.events import EventType, KeyEvent, PasteEvent, CybuddyEvent
from .handlers import handle_slash_command
from .cli import (
    explain_command,
    quick_tip,
    help_troubleshoot,
    micro_report,
    quiz_flashcards,
    step_planner,
    history_append,
)


class SimpleTUI:
    """Minimal TUI with just 7 core commands for security learning."""

    COMMANDS = {
        "explain": "Learn commands (e.g., explain 'nmap -sV')",
        "tip": "Study guide (e.g., tip 'SQL injection')",
        "help": "Troubleshoot (e.g., help 'connection refused')",
        "report": "Practice write-ups (e.g., report 'Found SQLi')",
        "quiz": "Active recall (e.g., quiz 'SQL Injection')",
        "plan": "Next steps (e.g., plan 'found port 80 open')",
        "exit": "Exit CyBuddy",
    }

    def __init__(self, *, terminal: Optional[TerminalController] = None, session: Optional[str] = None) -> None:
        self.history = HistoryBuffer(max_items=100)
        self._terminal = terminal or TerminalController()
        self._scheduler: Optional[FrameScheduler] = None
        self._current_input: list[str] = []
        self._session = session
        self._show_help = True

    async def run(self) -> None:
        """Run the async event loop."""
        async with self._terminal:
            self._scheduler = FrameScheduler(self._terminal.event_queue)
            self._scheduler.schedule_now()

            # Show welcome message
            self._show_welcome()

            async for event in self._terminal.event_stream():
                self._handle_event(event)

    def _show_welcome(self) -> None:
        """Show welcome message on startup."""
        self.history.append("╔════════════════════════════════════════════════════════════╗")
        self.history.append("║        CyBuddy - Simple Security Learning Helper         ║")
        self.history.append("╚════════════════════════════════════════════════════════════╝")
        self.history.append("")
        self.history.append("Available commands:")
        for cmd, desc in self.COMMANDS.items():
            self.history.append(f"  {cmd:8s} → {desc}")
        self.history.append("")
        self.history.append("Examples:")
        self.history.append("  explain 'nmap -sV target.local'")
        self.history.append("  tip 'SQL injection basics'")
        self.history.append("  help 'connection refused'")
        self.history.append("")
        self.history.append("Type a command to begin...")
        self.history.append("")

    def _handle_event(self, event: CybuddyEvent) -> None:
        """Handle incoming events."""
        if event.event_type is EventType.DRAW:
            self._draw()
            return

        if event.event_type is EventType.KEY:
            self._handle_key_event(event)  # type: ignore
        elif event.event_type is EventType.PASTE:
            paste_event: PasteEvent = event  # type: ignore
            self._current_input.append(paste_event.text)
            self._request_frame()

    def _handle_key_event(self, event: KeyEvent) -> None:
        """Handle keyboard input."""
        if event.key == "escape" and not event.ctrl and not event.alt:
            self._current_input.clear()
            self._request_frame()
            return

        if event.key in {"c-m", "enter"}:
            if self._current_input:
                text = "".join(self._current_input).strip()
                if text:
                    self._process_command(text)
                self._current_input.clear()
                self._request_frame()
            return

        if event.key in {"backspace"}:
            if self._current_input:
                last = self._current_input.pop()
                if len(last) > 1:
                    self._current_input.append(last[:-1])
                self._request_frame()
            return

        if event.data and not (event.ctrl or event.alt):
            self._current_input.append(event.data)
            self._request_frame()

    def _process_command(self, text: str) -> None:
        """Process user command."""
        # Show user input
        self.history.append(f"❯ {text}")
        self.history.append("")

        # Handle exit
        if text.lower() in {"exit", "quit"}:
            self.history.append("Good luck! Document your steps and be safe.")
            self.history.append("")
            loop = asyncio.get_running_loop()
            loop.stop()
            return

        # Parse command and argument
        parts = text.split(maxsplit=1)
        if not parts:
            self._show_error("Please enter a command. Type 'help' for usage.")
            return

        cmd = parts[0].lower()
        arg = parts[1].strip('"\'') if len(parts) > 1 else ""

        # Route to appropriate handler
        if cmd == "explain":
            if not arg:
                self._show_error("Usage: explain '<command>'")
                return
            result = explain_command(arg)
            self._render_response("Explanation", result)

        elif cmd == "tip":
            if not arg:
                self._show_error("Usage: tip '<topic>'")
                return
            result = quick_tip(arg)
            self._render_response("Tip", result)

        elif cmd == "help":
            if not arg:
                self._show_error("Usage: help '<error message>'")
                return
            result = help_troubleshoot(arg)
            self._render_response("Troubleshooting", result)

        elif cmd == "report":
            if not arg:
                self._show_error("Usage: report '<finding>'")
                return
            result = micro_report(arg)
            self._render_response("Report Template", result)

        elif cmd == "quiz":
            if not arg:
                self._show_error("Usage: quiz '<topic>'")
                return
            result = quiz_flashcards(arg)
            self._render_response("Quiz", result)

        elif cmd == "plan":
            if not arg:
                self._show_error("Usage: plan '<context>'")
                return
            result = step_planner(arg)
            self._render_response("Next Steps", result)

        else:
            self._show_error(f"Unknown command: {cmd}")
            self.history.append("Available commands: " + ", ".join(c for c in self.COMMANDS.keys() if c != "exit"))
            self.history.append("")

        # Log to persistent history
        history_append({"type": "simple_tui", "data": {"cmd": cmd, "arg": arg}}, session=self._session)

    def _render_response(self, title: str, content: str) -> None:
        """Render a command response."""
        self.history.append(f"─── {title} " + "─" * (50 - len(title)))
        for line in content.split("\n"):
            self.history.append(f"  {line}" if line.strip() else "")
        self.history.append("─" * 60)
        self.history.append("")

    def _show_error(self, message: str) -> None:
        """Show an error message."""
        self.history.append(f"⚠ {message}")
        self.history.append("")

    def _request_frame(self) -> None:
        """Request a UI redraw."""
        if self._scheduler is None:
            return
        self._scheduler.schedule_in(0.05)

    def _draw(self) -> None:
        """Draw the UI."""
        layout = self._compose_layout()
        self._terminal.draw_renderable(layout)

    def _compose_layout(self) -> Layout:
        """Compose the UI layout."""
        layout = Layout(name="root")
        layout.split_column(
            Layout(self._render_history(), name="history", ratio=5),
            Layout(self._render_prompt(), name="prompt", size=3),
            Layout(self._render_shortcuts(), name="shortcuts", size=3),
        )
        return layout

    def _render_history(self) -> Panel:
        """Render the history panel."""
        if not self.history._entries:
            text = Text("Type a command to begin...", style="dim")
        else:
            text = Text()
            entries = self.history._entries[-50:]  # Show last 50 lines
            for index, line in enumerate(entries):
                # Color the prompt lines
                if line.startswith("❯ "):
                    text.append(line, style="bold cyan")
                elif line.startswith("─── "):
                    text.append(line, style="bold yellow")
                elif line.startswith("⚠ "):
                    text.append(line, style="bold red")
                else:
                    text.append(line)

                if index < len(entries) - 1:
                    text.append("\n")

        return Panel(text, title="CyBuddy Session", border_style="cyan")

    def _render_prompt(self) -> Panel:
        """Render the input prompt."""
        prompt = Text("❯ ", style="bold cyan")
        if self._current_input:
            prompt.append("".join(self._current_input))
        else:
            prompt.append("Type command (explain, tip, help, report, quiz, plan)", style="dim")
        return Panel(prompt, title="Command", border_style="cyan")

    def _render_shortcuts(self) -> Panel:
        """Render keyboard shortcuts."""
        table = Table.grid(expand=True)
        table.add_column(justify="left")
        table.add_column(justify="right")
        table.add_row("Enter: submit   Esc: clear   Ctrl+C: exit", "7 simple commands for learning")
        return Panel(table, border_style="cyan")


__all__ = ["SimpleTUI"]