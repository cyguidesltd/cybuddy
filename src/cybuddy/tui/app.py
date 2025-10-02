from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, cast, TYPE_CHECKING

from rich.console import RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .core import FrameScheduler, HistoryBuffer, CybuddyEvent, TerminalController
from .core.events import EventType, KeyEvent, PasteEvent
from .overlays import Overlay, PagerOverlay
from ..history import add_command, get_history_entries

if TYPE_CHECKING:
    from cybuddy.handlers import GuideResponse


@dataclass
class OverlayStack:
    """Lightweight stack to manage overlay lifetimes."""

    _stack: list[Overlay] = field(default_factory=list)

    def push(self, overlay: Overlay) -> None:
        overlay.on_show()
        self._stack.append(overlay)

    def pop(self) -> Optional[Overlay]:
        if not self._stack:
            return None
        overlay = self._stack.pop()
        overlay.on_hide()
        return overlay

    def top(self) -> Optional[Overlay]:
        return self._stack[-1] if self._stack else None

    def clear(self) -> None:
        while self._stack:
            self.pop()


class CybuddyApp:
    """Main TUI orchestrator mirroring the Codex architecture."""

    def __init__(self, *, terminal: Optional[TerminalController] = None, session: Optional[str] = None) -> None:
        self.history = HistoryBuffer()
        self._terminal = terminal or TerminalController()
        self._overlay_stack = OverlayStack()
        self._scheduler: Optional[FrameScheduler] = None
        self._current_input: list[str] = []
        self._session = session
        self._command_history = get_history_entries()
        self._history_index = -1
        self._current_line = ""

    async def run(self) -> None:
        async with self._terminal:
            self._scheduler = FrameScheduler(self._terminal.event_queue)
            self._scheduler.schedule_now()
            async for event in self._terminal.event_stream():
                self._handle_event(event)

    def process_event(self, event: CybuddyEvent) -> None:
        """Expose deterministic event processing for tests or headless drivers."""
        self._handle_event(event)

    def render_for_testing(self) -> RenderableType:
        """Return the current layout without writing to the terminal."""
        return self._compose_layout()

    def _handle_event(self, event: CybuddyEvent) -> None:
        if event.event_type is EventType.DRAW:
            self._draw()
            return
        overlay = self._overlay_stack.top()
        if overlay and overlay.handle_event(event):
            self._request_frame()
            return
        if event.event_type is EventType.KEY:
            self._handle_key_event(cast(KeyEvent, event))
        elif event.event_type is EventType.PASTE:
            paste_event = cast(PasteEvent, event)
            self._current_input.append(paste_event.text)
            self._request_frame()

    def _toggle_pager(self) -> None:
        current = self._overlay_stack.top()
        if isinstance(current, PagerOverlay):
            self._hide_overlay()
        else:
            overlay = PagerOverlay(self.history.snapshot())
            self._show_overlay(overlay)

    def _show_overlay(self, overlay: Overlay) -> None:
        if self._overlay_stack.top() is None:
            self._terminal.enter_alt_screen()
        self._overlay_stack.push(overlay)
        self._request_frame()

    def _hide_overlay(self) -> None:
        removed = self._overlay_stack.pop()
        if removed and self._overlay_stack.top() is None:
            self._terminal.leave_alt_screen()
        self._request_frame()

    def _request_frame(self) -> None:
        if self._scheduler is None:
            return
        self._scheduler.schedule_in(0.05)

    def _draw(self) -> None:
        layout = self._compose_layout()
        self._terminal.draw_renderable(layout)

    def _compose_layout(self) -> Layout:
        overlay = self._overlay_stack.top()
        if overlay:
            return self._compose_overlay_layout(overlay)
        layout = Layout(name="root")
        layout.split_column(
            Layout(self._render_history(), name="history", ratio=5),
            Layout(self._render_prompt(), name="prompt", size=3),
            Layout(self._render_shortcuts(None), name="shortcuts", size=3),
        )
        return layout

    def _compose_overlay_layout(self, overlay: Overlay) -> Layout:
        layout = Layout(name="overlay")
        layout.split_column(
            Layout(self._render_overlay_body(overlay), name="overlay-body", ratio=5),
            Layout(self._overlay_footer(overlay), name="overlay-footer", size=3),
        )
        return layout

    def _render_history(self) -> RenderableType:
        return self.history.render()

    def _render_prompt(self) -> RenderableType:
        prompt = Text("> ", style="cyan")
        if self._current_input:
            prompt.append("".join(self._current_input))
        else:
            prompt.append("Type security questions or /commands (try /tip, /checklist, /todo) · F2 for transcript", style="dim")
        return Panel(prompt, title="CyBuddy Guide", border_style="cyan")

    def _render_shortcuts(self, overlay: Optional[Overlay]) -> RenderableType:
        table = Table.grid(expand=True)
        table.add_column(justify="left")
        table.add_column(justify="right")
        table.add_row("F2: transcript overlay", "Ctrl+C: quit (shell)")
        table.add_row("Enter: commit input", "Esc: clear input")
        if overlay is not None:
            table.add_row("Esc: close overlay", "")
        return Panel(table, title="Shortcuts", border_style="cyan")

    def _render_overlay_body(self, overlay: Overlay) -> RenderableType:
        body = overlay.render(
            self._terminal.console,
            self._terminal.console.size.width,
        )
        if isinstance(body, Panel):
            return body
        return Panel(body, title=overlay.name.title(), border_style="cyan")

    def _overlay_footer(self, overlay: Overlay) -> RenderableType:
        status = overlay.status_bar()
        if status is not None:
            return status
        return self._render_shortcuts(overlay)

    def _handle_key_event(self, event: KeyEvent) -> None:
        if event.key == "escape" and not event.ctrl and not event.alt:
            if self._overlay_stack.top() is not None:
                self._hide_overlay()
            else:
                self._current_input.clear()
                self._request_frame()
            return
        if event.key == "q" and not (event.ctrl or event.alt) and self._overlay_stack.top() is not None:
            self._hide_overlay()
            return
        if event.key == "f2":
            self._toggle_pager()
            return
        
        # History navigation
        if event.key == "up" and not (event.ctrl or event.alt):
            self._navigate_history(-1)
            return
        if event.key == "down" and not (event.ctrl or event.alt):
            self._navigate_history(1)
            return
        
        # Ctrl+R for reverse search (basic implementation)
        if event.key == "r" and event.ctrl:
            self._reverse_search()
            return
        
        if event.key in {"c-m", "enter"}:
            if self._current_input:
                text = "".join(self._current_input).strip()
                if text:
                    self._process_user_input(text)
                self._current_input.clear()
                self._history_index = -1
                self._current_line = ""
                self._request_frame()
            return
        if event.key in {"backspace"}:
            if self._current_input:
                last = self._current_input.pop()
                if len(last) > 1:
                    # Respect multi-character entries (e.g. paste) by trimming.
                    self._current_input.append(last[:-1])
                self._request_frame()
            return
        if event.data and not (event.ctrl or event.alt):
            self._current_input.append(event.data)
            self._request_frame()

    def _navigate_history(self, direction: int) -> None:
        """Navigate through command history."""
        if not self._command_history:
            return
        
        if direction < 0:  # Up arrow - go to older commands
            if self._history_index == -1:
                # First time navigating up - save current input
                self._current_line = "".join(self._current_input)
                self._history_index = len(self._command_history) - 1
            elif self._history_index > 0:
                self._history_index -= 1
        else:  # Down arrow - go to newer commands
            if self._history_index == -1:
                return
            elif self._history_index < len(self._command_history) - 1:
                self._history_index += 1
            else:
                # At newest - restore original input
                self._history_index = -1
                self._current_input = list(self._current_line)
                self._request_frame()
                return
        
        # Update input with history entry
        if self._history_index >= 0:
            self._current_input = list(self._command_history[self._history_index])
        self._request_frame()
    
    def _reverse_search(self) -> None:
        """Basic reverse search implementation."""
        # For now, just show a message - full implementation would be more complex
        self.history.append("(Reverse search not fully implemented yet)")
        self._request_frame()

    def _process_user_input(self, text: str) -> None:
        """Process user input through CyBuddy handlers and render response."""
        # Add user input to history
        self.history.append(f"> {text}")
        
        # Add to command history
        add_command(text)

        # Handle exit commands
        if text.lower() in {"exit", "quit"}:
            import asyncio
            loop = asyncio.get_running_loop()
            loop.stop()
            return

        # Route through handlers
        if text.startswith("/"):
            from cybuddy.handlers import handle_slash_command
            response = handle_slash_command(text, session=self._session)
            self._render_simple_response(response.output)
        else:
            from cybuddy.handlers import handle_user_input
            from cybuddy.cli import history_append
            response = handle_user_input(text, session=self._session)
            self._render_structured_response(response)
            # Log to persistent history
            history_append({"type": "guide", "data": {"input": text, "plan": response.plan}}, session=self._session)

    def _render_simple_response(self, output: str) -> None:
        """Render simple text response."""
        for line in output.split("\n"):
            if line.strip():
                self.history.append(line)

    def _render_structured_response(self, response: GuideResponse) -> None:
        """Render structured PLAN/ACTION/CMD/OUT/NEXT response."""
        from cybuddy.handlers import GuideResponse
        from cybuddy.formatters import create_syntax_highlight, is_likely_code

        self.history.append("")
        self.history.append("PLAN:")
        self.history.append(f"  {response.plan}")
        self.history.append("")
        self.history.append("ACTION:")
        self.history.append(f"  {response.action}")

        if response.cmd:
            self.history.append("")
            self.history.append("CMD:")
            # Apply syntax highlighting to commands
            if is_likely_code(response.cmd):
                syntax = create_syntax_highlight(response.cmd, language="bash", line_numbers=False)
                self.history.append(syntax)
            else:
                self.history.append(f"  {response.cmd}")

        self.history.append("")
        self.history.append("OUT:")
        self.history.append(f"  {response.output}")
        self.history.append("")
        self.history.append("NEXT:")
        self.history.append(f"  {response.next_step}")
        self.history.append("")

__all__ = ["CybuddyApp"]
