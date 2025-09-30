"""Tests for the simplified TUI with 7 core commands."""
from __future__ import annotations

import asyncio

from rich.console import Console

from secbuddy.simple_tui import SimpleTUI
from secbuddy.tui.core.events import KeyEvent


def key_event(key: str, data: str | None = None) -> KeyEvent:
    return KeyEvent(key=key, data=data, ctrl=False, alt=False, shift=False)


class StubTerminal:
    def __init__(self) -> None:
        self.console = Console(record=True, width=80)
        self._drawn: list = []
        self._queue: asyncio.Queue[object] = asyncio.Queue()

    def draw_renderable(self, renderable) -> None:
        self._drawn.append(renderable)

    @property
    def event_queue(self) -> asyncio.Queue[object]:
        return self._queue


def test_simple_tui_has_7_commands() -> None:
    """Test that SimpleTUI defines exactly 7 commands."""
    app = SimpleTUI(terminal=StubTerminal())  # type: ignore
    assert len(app.COMMANDS) == 7
    assert "explain" in app.COMMANDS
    assert "tip" in app.COMMANDS
    assert "help" in app.COMMANDS
    assert "report" in app.COMMANDS
    assert "quiz" in app.COMMANDS
    assert "plan" in app.COMMANDS
    assert "exit" in app.COMMANDS


def test_simple_tui_shows_welcome() -> None:
    """Test that welcome message is shown."""
    terminal = StubTerminal()
    app = SimpleTUI(terminal=terminal)  # type: ignore
    app._show_welcome()

    snapshot = app.history.snapshot()
    assert any("SecBuddy" in line for line in snapshot)
    assert any("explain" in line for line in snapshot)
    assert any("tip" in line for line in snapshot)


def test_simple_tui_processes_explain_command() -> None:
    """Test explain command processing."""
    terminal = StubTerminal()
    app = SimpleTUI(terminal=terminal)  # type: ignore

    # Simulate typing: explain "nmap"
    for char in 'explain "nmap"':
        app._handle_key_event(key_event(char, char))
    app._handle_key_event(key_event("enter"))

    snapshot = app.history.snapshot()
    # Should have user input and response
    assert any('❯ explain "nmap"' in line for line in snapshot)
    assert any("Explanation" in line for line in snapshot)


def test_simple_tui_processes_tip_command() -> None:
    """Test tip command processing."""
    terminal = StubTerminal()
    app = SimpleTUI(terminal=terminal)  # type: ignore

    app._process_command("tip 'SQL injection'")

    snapshot = app.history.snapshot()
    assert any("Tip" in line for line in snapshot)
    assert any("❯" in line for line in snapshot)


def test_simple_tui_handles_unknown_command() -> None:
    """Test unknown command handling."""
    terminal = StubTerminal()
    app = SimpleTUI(terminal=terminal)  # type: ignore

    app._process_command("foobar something")

    snapshot = app.history.snapshot()
    assert any("Unknown command" in line for line in snapshot)


def test_simple_tui_renders_layout() -> None:
    """Test that layout renders correctly."""
    terminal = StubTerminal()
    app = SimpleTUI(terminal=terminal)  # type: ignore

    layout = app._compose_layout()
    console = Console(record=True, width=80)
    console.print(layout)
    rendered = console.export_text(clear=True)

    assert "SecBuddy Session" in rendered
    assert "Command" in rendered