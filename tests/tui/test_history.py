from __future__ import annotations

from rich.console import Console

from secbuddy.tui.core.history import HistoryBuffer


def test_history_buffer_trims_to_max_items() -> None:
    history = HistoryBuffer(max_items=3)
    history.extend(["one", "two", "three", "four"])
    assert history.snapshot() == ["two", "three", "four"]


def test_history_render_placeholder_and_entries() -> None:
    console = Console(record=True, width=60)
    history = HistoryBuffer()
    console.print(history.render())
    placeholder = console.export_text(clear=True)
    assert "Start typing to record notes..." in placeholder

    history.append("logged")
    console.print(history.render())
    rendered = console.export_text(clear=True)
    assert "logged" in rendered
