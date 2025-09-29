This file applies repo-wide.

- Python 3.11+, strict typing (`mypy --strict`).
- Format with `ruff format` and import sort with `ruff`.
- Source in `src/`, tests in `tests/` mirroring paths.
- Keep modules small with clear names; avoid one-letter identifiers.
- Don’t add unrelated changes; keep patches focused.

## SecBuddy TUI Notes

- Python-based TUI lives under `src/secbuddy/tui/`, mirroring Codex CLI UX.
- Core stack: `prompt_toolkit` for input/raw mode, `rich` for rendering.
- Event flow uses `TerminalController` + `FrameScheduler`; draw requests coalesce via async queue.
- Overlays implement `Overlay` protocol; transcript pager toggled with `F2`, close using `Esc`.
- Tests capture rendered frames via `rich` recording console; keep snapshots human-readable.
