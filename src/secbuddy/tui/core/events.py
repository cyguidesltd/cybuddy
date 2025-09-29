from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Protocol, Union


class EventType(str, Enum):
    KEY = "key"
    PASTE = "paste"
    DRAW = "draw"
    FOCUS = "focus"
    RESIZE = "resize"


@dataclass(frozen=True)
class BaseEvent:
    """Common base type carrying the event discriminator."""

    event_type: EventType


@dataclass(frozen=True)
class KeyEvent(BaseEvent):
    """Represents a key press with normalized modifier metadata."""

    key: str
    data: str | None
    ctrl: bool
    alt: bool
    shift: bool

    def __init__(self, key: str, data: str | None, *, ctrl: bool, alt: bool, shift: bool) -> None:
        super().__setattr__("event_type", EventType.KEY)
        super().__setattr__("key", key)
        super().__setattr__("data", data)
        super().__setattr__("ctrl", ctrl)
        super().__setattr__("alt", alt)
        super().__setattr__("shift", shift)


@dataclass(frozen=True)
class PasteEvent(BaseEvent):
    """Represents a bracketed paste payload."""

    text: str

    def __init__(self, text: str) -> None:
        super().__setattr__("event_type", EventType.PASTE)
        super().__setattr__("text", text)


@dataclass(frozen=True)
class DrawEvent(BaseEvent):
    """Signals that the UI should draw a frame."""

    requested_at: float

    def __init__(self, requested_at: float) -> None:
        super().__setattr__("event_type", EventType.DRAW)
        super().__setattr__("requested_at", requested_at)


@dataclass(frozen=True)
class FocusEvent(BaseEvent):
    """Tracks terminal focus transitions where supported by the backend."""

    gained: bool

    def __init__(self, gained: bool) -> None:
        super().__setattr__("event_type", EventType.FOCUS)
        super().__setattr__("gained", gained)


@dataclass(frozen=True)
class ResizeEvent(BaseEvent):
    """Terminal size change notification."""

    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        super().__setattr__("event_type", EventType.RESIZE)
        super().__setattr__("width", width)
        super().__setattr__("height", height)


SecbuddyEvent = Union[KeyEvent, PasteEvent, DrawEvent, FocusEvent, ResizeEvent]


class EventConsumer(Protocol):
    """Lightweight protocol so overlays/app can advertise event handling."""

    def handle_event(self, event: SecbuddyEvent) -> bool:
        """Handle the event; return True if it was consumed."""


__all__ = [
    "BaseEvent",
    "DrawEvent",
    "EventConsumer",
    "EventType",
    "FocusEvent",
    "KeyEvent",
    "PasteEvent",
    "ResizeEvent",
    "SecbuddyEvent",
]
