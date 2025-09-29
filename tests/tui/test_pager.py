from __future__ import annotations

from rich.console import Console

from secbuddy.tui.core.events import KeyEvent, PasteEvent
from secbuddy.tui.overlays.pager import PagerOverlay


def make_key(key: str, data: str | None = None) -> KeyEvent:
    return KeyEvent(key=key, data=data, ctrl=False, alt=False, shift=False)


def test_pager_scrolls_and_renders() -> None:
    lines = [f"line {idx}" for idx in range(1, 21)]
    overlay = PagerOverlay(lines, page_size=5)

    console = Console(record=True, width=40)
    console.print(overlay.render(console, 40))
    rendered = console.export_text(clear=True)
    assert "line 16" in rendered

    overlay.handle_event(make_key("pageup"))
    console.print(overlay.render(console, 40))
    rendered = console.export_text(clear=True)
    assert "line 11" in rendered

    overlay.handle_event(make_key("down"))
    console.print(overlay.render(console, 40))
    rendered = console.export_text(clear=True)
    assert "line 12" in rendered


def test_pager_search_via_paste() -> None:
    lines = ["alpha", "beta", "gamma"]
    overlay = PagerOverlay(lines, page_size=2)
    paste = PasteEvent(text="gamma")
    assert overlay.handle_event(paste)

    console = Console(record=True, width=40)
    console.print(overlay.render(console, 40))
    rendered = console.export_text(clear=True)
    assert "gamma" in rendered

    console.print(overlay.status_bar())
    status = console.export_text(clear=True)
    assert "Matches 1/1" in status
