"""Business logic handlers for SecBuddy commands, shared between CLI and TUI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class GuideResponse:
    """Structured response for guide mode interactions."""
    response_type: str  # "structured" or "simple"
    plan: str
    action: str
    cmd: str
    output: str
    next_step: str
    raw_input: str


@dataclass
class SlashResponse:
    """Response from slash command execution."""
    output: str
    success: bool = True


def handle_user_input(text: str, session: Optional[str] = None) -> GuideResponse:
    """
    Process user input in guide mode and return structured response.

    Args:
        text: User input text
        session: Optional session name for history/todo

    Returns:
        GuideResponse with PLAN/ACTION/CMD/OUT/NEXT fields
    """
    plan_text = suggest_next(text)
    action = "Provide brief next step and safe command (if any)"
    cmd_hint = _guide_command_hint(text)
    output = "(analysis in brief; update your todo/history as needed)"
    next_step = suggest_next(text)

    return GuideResponse(
        response_type="structured",
        plan=plan_text,
        action=action,
        cmd=cmd_hint,
        output=output,
        next_step=next_step,
        raw_input=text,
    )


def handle_slash_command(line: str, session: Optional[str] = None) -> SlashResponse:
    """
    Handle slash commands in guide mode.

    Args:
        line: Slash command line (e.g., "/tip sql injection")
        session: Optional session name

    Returns:
        SlashResponse with output text
    """
    from .cli import (
        CHECKLISTS,
        _todo_load,
        _todo_save,
        _now_iso,
        cmd_run,
        quick_tip,
        step_planner,
    )

    parts = line[1:].split(maxsplit=1)
    if not parts:
        return SlashResponse("Unknown command. Try /tip, /plan, /checklist, /todo, /run", success=False)

    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    # /tip <topic>
    if cmd == "tip":
        if not arg:
            return SlashResponse("Usage: /tip <topic>", success=False)
        result = quick_tip(arg)
        return SlashResponse(f"TIP:\n{result}")

    # /plan <context>
    if cmd == "plan":
        if not arg:
            return SlashResponse("Usage: /plan <context>", success=False)
        result = step_planner(arg)
        return SlashResponse(f"PLAN:\n{result}")

    # /checklist <topic>
    if cmd == "checklist":
        if not arg:
            topics = ", ".join(sorted(CHECKLISTS.keys()))
            return SlashResponse(f"Available checklists: {topics}")

        key = arg.lower()
        item = CHECKLISTS.get(key)
        if not item:
            return SlashResponse(f"Unknown checklist: {arg}", success=False)

        lines = [f"{item.name} Checklist:"]
        for i, step in enumerate(item.steps, start=1):
            lines.append(f"{i}. {step}")
        return SlashResponse("\n".join(lines))

    # /todo add <text>
    if cmd == "todo":
        subparts = arg.split(maxsplit=1)
        if not subparts:
            # List todos
            items = _todo_load(session)
            if not items:
                return SlashResponse("No TODO items. Add with: /todo add \"description\"")
            lines = []
            for i, it in enumerate(items, 1):
                status = it.get("status", "pending")
                lines.append(f"{i}. [{status}] {it.get('text','')}")
            return SlashResponse("\n".join(lines))

        subcmd = subparts[0].lower()
        subarg = subparts[1] if len(subparts) > 1 else ""

        if subcmd == "add":
            if not subarg:
                return SlashResponse("Usage: /todo add <text>", success=False)
            items = _todo_load(session)
            items.append({"text": subarg, "status": "pending", "added": _now_iso()})
            _todo_save(items, session)
            return SlashResponse(f"Added: {subarg}")

        if subcmd == "done":
            if not subarg:
                return SlashResponse("Usage: /todo done <number>", success=False)
            try:
                idx = int(subarg) - 1
                items = _todo_load(session)
                if idx < 0 or idx >= len(items):
                    return SlashResponse("Invalid todo number", success=False)
                items[idx]["status"] = "completed"
                items[idx]["completed"] = _now_iso()
                _todo_save(items, session)
                return SlashResponse(f"Done: {items[idx]['text']}")
            except ValueError:
                return SlashResponse("Invalid todo number", success=False)

        if subcmd == "clear":
            _todo_save([], session)
            return SlashResponse("Cleared all TODO items")

        return SlashResponse(f"Unknown todo command: {subcmd}", success=False)

    # /run <tool> "<args>"
    if cmd == "run":
        if not arg:
            return SlashResponse("Usage: /run <tool> \"<args>\"", success=False)
        # Parse tool and args
        import shlex
        try:
            tokens = shlex.split(arg)
        except ValueError:
            tokens = arg.split()

        if not tokens:
            return SlashResponse("Usage: /run <tool> \"<args>\"", success=False)

        from .cli import _safety_review
        tool = tokens[0]
        rest = tokens[1:]
        joined = " ".join(rest)

        safety, notes = _safety_review(tool, joined)
        lines = ["SAFETY:"]
        for s in safety:
            lines.append(f"- {s}")
        for n in notes:
            lines.append(f"- TIP: {n}")
        lines.append("CMD:")
        lines.append(f"{tool} {joined}".strip())
        lines.append("")
        lines.append("NOT RUN (dry-run). Use 'secbuddy run' CLI for --exec flag.")
        return SlashResponse("\n".join(lines))

    return SlashResponse(f"Unknown command: /{cmd}", success=False)


def _guide_command_hint(text: str) -> str:
    """Generate command hint based on user input context."""
    t = text.lower()
    if any(k in t for k in ["nmap", "scan", "port"]):
        return "nmap -sV -Pn -T2 <target>"
    if any(k in t for k in ["dir", "enum", "hidden", "wordlist"]):
        return "gobuster dir -u http://<host> -w <wordlist>"
    if any(k in t for k in ["vuln", "nikto"]):
        return "nikto -h http://<host>"
    return ""


def suggest_next(user_text: str) -> str:
    """Suggest next steps based on user input."""
    t = user_text.lower()
    if any(k in t for k in ["nmap", "scan", "port"]):
        return "Try: nmap -sV -Pn -T2 <target>. Start safe; document findings."
    if any(k in t for k in ["web", "http", "xss", "sql", "burp"]):
        return "Check robots.txt, headers, inputs. Consider Burp with passive scans first."
    if any(k in t for k in ["hash", "cipher", "encode", "crypto"]):
        return "Identify format (hashid), test small samples, avoid brute-force blindly."
    if any(k in t for k in ["forensic", "image", "pcap", "memory"]):
        return "Verify file magic, run strings/hexdump, use appropriate carve/analysis tools."
    return "Break the task down: scope -> safe defaults -> record results -> next step."


__all__ = [
    "GuideResponse",
    "SlashResponse",
    "handle_user_input",
    "handle_slash_command",
    "suggest_next",
]