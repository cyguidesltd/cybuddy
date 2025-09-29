from __future__ import annotations

import asyncio
import contextlib
import sys
import time
from contextlib import ExitStack
from typing import AsyncIterator, Optional

from prompt_toolkit.input.defaults import create_input
from prompt_toolkit.key_binding import KeyPress
from prompt_toolkit.keys import Keys
from prompt_toolkit.output.defaults import create_output
from rich.console import Console
from rich.console import RenderableType

from .events import DrawEvent, FocusEvent, KeyEvent, PasteEvent, ResizeEvent, SecbuddyEvent


class TerminalController:
    """Low-level terminal glue around prompt_toolkit and Rich rendering."""

    def __init__(self) -> None:
        self._input = create_input(sys.stdin)
        self._output = create_output(stdout=True)
        self.console = Console(force_terminal=True, highlight=False)
        self._event_queue: asyncio.Queue[SecbuddyEvent] = asyncio.Queue()
        self._reader_task: Optional[asyncio.Task[None]] = None
        self._exit_stack = ExitStack()
        self._alt_active = False

    async def __aenter__(self) -> "TerminalController":
        self._enter_terminal_modes()
        self._reader_task = asyncio.create_task(self._read_input(), name="secbuddy-tui-input")
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._reader_task is not None:
            self._reader_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._reader_task
        self._reader_task = None
        self.leave_alt_screen()
        self._exit_stack.close()

    def _enter_terminal_modes(self) -> None:
        self._exit_stack.enter_context(self._input.raw_mode())
        self._exit_stack.enter_context(self._input.bracketed_paste_mode())
        self._exit_stack.enter_context(self._input.attach(self._output))

    async def _read_input(self) -> None:
        try:
            while True:
                key_presses = await self._input.read_keys()
                for key_press in key_presses:
                    event = self._convert_key_press(key_press)
                    if event is not None:
                        await self._event_queue.put(event)
        except asyncio.CancelledError:
            pass

    def _convert_key_press(self, key_press: KeyPress) -> SecbuddyEvent | None:
        if key_press.key == Keys.BracketedPaste:
            text = key_press.data or ""
            return PasteEvent(text=text)
        if key_press.key == Keys.CPRResponse:
            return None
        if key_press.key == Keys.Vt100_MouseEvent:
            return None
        modifiers = key_press.key
        ctrl = "c-" in str(modifiers)
        alt = "a-" in str(modifiers)
        shift = "s-" in str(modifiers)
        key_name = key_press.key.value if hasattr(key_press.key, "value") else str(key_press.key)
        data = key_press.data or None
        return KeyEvent(key=key_name, data=data, ctrl=ctrl, alt=alt, shift=shift)

    async def event_stream(self) -> AsyncIterator[SecbuddyEvent]:
        while True:
            event = await self._event_queue.get()
            yield event

    def schedule_draw(self) -> None:
        event = DrawEvent(requested_at=time.time())
        self._event_queue.put_nowait(event)

    @property
    def event_queue(self) -> "asyncio.Queue[SecbuddyEvent]":
        return self._event_queue

    def send_focus(self, gained: bool) -> None:
        self._event_queue.put_nowait(FocusEvent(gained=gained))

    def send_resize(self, width: int, height: int) -> None:
        self._event_queue.put_nowait(ResizeEvent(width=width, height=height))

    def enter_alt_screen(self) -> None:
        if self._alt_active:
            return
        self._output.write_raw("\x1b[?1049h")
        self._output.flush()
        self._alt_active = True

    def leave_alt_screen(self) -> None:
        if not self._alt_active:
            return
        self._output.write_raw("\x1b[?1049l")
        self._output.flush()
        self._alt_active = False

    def draw_renderable(self, renderable: RenderableType) -> None:
        self._output.write_raw("\x1b[2J\x1b[H")
        self._output.flush()
        self.console.print(renderable, soft_wrap=True)
        self.console.file.flush()

    async def aclose(self) -> None:
        if self._reader_task is not None:
            self._reader_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._reader_task
        self._reader_task = None
        self.leave_alt_screen()
        self._exit_stack.close()

__all__ = ["TerminalController"]
