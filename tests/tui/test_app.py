from __future__ import annotations

import asyncio

from rich.console import Console
from rich.console import RenderableType

from cybuddy.tui.core.events import KeyEvent
from cybuddy.tui.app import CybuddyApp


def key_event(key: str, data: str | None = None) -> KeyEvent:
    return KeyEvent(key=key, data=data, ctrl=False, alt=False, shift=False)


class StubTerminal:
    def __init__(self) -> None:
        self.console = Console(record=True, width=80)
        self.alt_active = False
        self._drawn: list[RenderableType] = []
        self._queue: asyncio.Queue[object] = asyncio.Queue()

    def draw_renderable(self, renderable: RenderableType) -> None:
        self._drawn.append(renderable)

    def enter_alt_screen(self) -> None:
        self.alt_active = True

    def leave_alt_screen(self) -> None:
        self.alt_active = False

    @property
    def event_queue(self) -> "asyncio.Queue[object]":
        return self._queue


def test_app_collects_input_and_toggles_overlay() -> None:
    terminal = StubTerminal()
    app = CybuddyApp(terminal=terminal)  # type: ignore[arg-type]
    app.process_event(key_event("a", "a"))
    app.process_event(key_event("enter"))
    snapshot = app.history.snapshot()
    # Now the app processes input through handlers, so expect structured response
    assert len(snapshot) > 0
    assert snapshot[0] == "> a"  # User input is prefixed with >
    # Should contain PLAN/ACTION sections
    assert any("PLAN:" in line for line in snapshot)
    assert any("ACTION:" in line for line in snapshot)

    layout = app.render_for_testing()
    console = Console(record=True, width=60)
    console.print(layout)
    rendered = console.export_text(clear=True)
    assert "Session History" in rendered
    assert "CyBuddy Guide" in rendered  # Panel title changed from "Input"

    assert not terminal.alt_active
    app.process_event(key_event("f2"))
    assert terminal.alt_active
    layout = app.render_for_testing()
    console.print(layout)
    rendered = console.export_text(clear=True)
    assert "Transcript" in rendered
    assert "a" in rendered

    app.process_event(key_event("escape"))
    assert not terminal.alt_active
    layout = app.render_for_testing()
    console.print(layout)
    rendered = console.export_text(clear=True)
    assert "Transcript" not in rendered
