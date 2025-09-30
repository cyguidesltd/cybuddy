from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import json
import os


@dataclass(frozen=True)
class ChecklistItem:
    name: str
    steps: List[str]


CHECKLISTS: dict[str, ChecklistItem] = {
    "recon": ChecklistItem(
        name="Recon",
        steps=[
            "Gather target scope and constraints",
            "Passive recon (whois, crt.sh, Google dorking)",
            "Scan with safe defaults (nmap -sV -Pn)",
            "Enumerate services (http, ssh, smb, etc.)",
            "Document findings with timestamps",
        ],
    ),
    "web": ChecklistItem(
        name="Web",
        steps=[
            "Check robots.txt and sitemap.xml",
            "Look for common endpoints (/admin, /api)",
            "Test inputs for auth/broken access control",
            "Check for injection and XSS",
            "Review cookies, headers, CSP",
        ],
    ),
    "crypto": ChecklistItem(
        name="Crypto",
        steps=[
            "Identify cipher/hash/encoding",
            "Check for common mistakes (ECB, reuse, weak keys)",
            "Try known tools (hashid, cyberchef)",
            "Validate assumptions with small test vectors",
        ],
    ),
    "forensics": ChecklistItem(
        name="Forensics",
        steps=[
            "Verify file magic and metadata",
            "Strings and hexdump for quick clues",
            "Carve/inspect with appropriate tools",
            "Keep a chain-of-custody log",
        ],
    ),
}


STARTER_PROMPT = (
    "You are CyBuddy, a helpful cybersecurity study companion. "
    "You explain steps simply, provide safe defaults, and always suggest next actions. "
    "You avoid running destructive commands and emphasize documenting findings."
)


def print_help() -> int:
    print(
        """
CyBuddy - beginner-friendly cybersecurity helper

7 Core Commands (Interactive TUI):
  cybuddy guide [--tui]         Launch interactive learning interface (recommended)
    → explain '<command>'        Learn what commands do (e.g., explain 'nmap -sV')
    → tip '<topic>'              Study guide for security topics
    → help '<error>'             Troubleshoot errors and issues
    → report '<finding>'         Practice writing security reports (2-3 lines)
    → quiz '<topic>'             Active recall with flashcards
    → plan '<context>'           Get next steps guidance (3 steps)
    → exit                       Exit the interface

Additional Commands:
  cybuddy checklist [topic]     Show a checklist (recon|web|crypto|forensics)
  cybuddy prompt                Print a starter LLM system prompt
  cybuddy explain "<command>"   One-shot explain (use TUI for interactive)
  cybuddy tip "<topic>"         One-shot tip (use TUI for interactive)
  cybuddy assist "<issue>"      One-shot troubleshoot
  cybuddy report "<finding>"    One-shot report template
  cybuddy quiz "<topic>"        One-shot quiz
  cybuddy plan "<context>"      One-shot plan
  cybuddy todo [subcmd]         Plan tracker: list/add/done/clear
  cybuddy history [--clear]     Show or clear recent session history
  cybuddy config                Show resolved configuration
  cybuddy run <tool> "<args>"   Dry-run wrapper with safety notes (use --exec to run)

Examples:
  cybuddy guide --tui                    # Launch interactive mode
  explain 'nmap -sV target.local'         # Inside TUI
  tip 'SQL injection basics'              # Inside TUI
  help 'sqlmap connection refused'        # Inside TUI
        """.strip()
    )
    return 0


def cmd_prompt() -> int:
    print(STARTER_PROMPT)
    return 0


def cmd_checklist(topic: Optional[str]) -> int:
    if not topic:
        print("Available topics:")
        for key in sorted(CHECKLISTS):
            print(f"- {key}")
        return 0

    key = topic.lower()
    item = CHECKLISTS.get(key)
    if not item:
        print(f"Unknown topic: {topic}")
        print("Try one of: " + ", ".join(sorted(CHECKLISTS)))
        return 1

    print(f"{item.name} Checklist:")
    for i, step in enumerate(item.steps, start=1):
        print(f"{i}. {step}")
    return 0


def cmd_guide(stdin: Iterable[str] = sys.stdin, session: Optional[str] = None) -> int:
    # Print colored shield logo with gradient (green to cyan) and medical cross
    # Matches the SVG design: rgb(0,255,136) → rgb(0,255,255)
    print("\033[1;38;2;0;255;136m        ▄▀▀▀▄\033[0m")
    print("\033[1;38;2;0;255;150m       █  │  █\033[0m")
    print("\033[1;38;2;0;255;170m      █ ──┼── █\033[0m      \033[1;97mCY\033[1;38;2;0;255;255mBUDDY\033[0m")
    print("\033[1;38;2;0;255;190m      █   │   █\033[0m")
    print("\033[1;38;2;0;255;210m       █     █\033[0m       \033[2mYour Security Learning Companion\033[0m")
    print("\033[1;38;2;0;255;230m        █   █\033[0m")
    print("\033[1;38;2;0;255;245m         █ █\033[0m")
    print("\033[1;38;2;0;255;255m          ▀\033[0m\n")
    print("Type 'exit' to quit. Use /tip, /plan, /checklist <topic>, /todo add <..>, /run <tool> \"args\"")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            print()
            break

        if not line:
            continue
        if line.lower() in {"exit", "quit"}:
            print("Good luck! Document your steps and be safe.")
            break

        # Slash commands
        if line.startswith("/"):
            print(_guide_handle_slash(line, session=session))
            continue

        # Render codex-like sections using handlers
        from .handlers import handle_user_input
        response = handle_user_input(line, session=session)
        print("PLAN:")
        print("- " + response.plan)
        print("ACTION:\n- " + response.action)
        if response.cmd:
            print("CMD:\n" + response.cmd)
        print("OUT:\n" + response.output)
        print("NEXT:\n- " + response.next_step)
        history_append({"type": "guide", "data": {"input": line, "plan": response.plan}}, session=session)
    return 0


def _guide_handle_slash(line: str, session: Optional[str] = None) -> str:
    """Handle slash commands in guide mode (delegates to handlers)."""
    from .handlers import handle_slash_command
    response = handle_slash_command(line, session=session)
    return response.output


def cmd_guide_tui(session: Optional[str] = None, simple: bool = True) -> int:
    """
    Launch the interactive TUI for guide mode.

    Uses prompt_toolkit's proper async API (PromptSession.prompt_async)
    instead of low-level read_keys() for reliable input handling.
    """
    import asyncio

    # Use the fixed SimpleTUI with proper prompt_toolkit usage
    from .simple_tui_fixed import SimpleTUI
    app = SimpleTUI(session=session)

    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\nGood luck! Document your steps and be safe.")
    return 0


def _guide_command_hint(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["nmap", "scan", "port"]):
        return "nmap -sV -Pn -T2 <target>"
    if any(k in t for k in ["dir", "enum", "hidden", "wordlist"]):
        return "gobuster dir -u http://<host> -w <wordlist>"
    if any(k in t for k in ["vuln", "nikto"]):
        return "nikto -h http://<host>"
    return ""


def suggest_next(user_text: str) -> str:
    t = user_text.lower()
    if any(k in t for k in ["nmap", "scan", "port"]):
        return (
            "Try: nmap -sV -Pn -T2 <target>. Start safe; document findings."
        )
    if any(k in t for k in ["web", "http", "xss", "sql", "burp"]):
        return (
            "Check robots.txt, headers, inputs. Consider Burp with passive scans first."
        )
    if any(k in t for k in ["hash", "cipher", "encode", "crypto"]):
        return (
            "Identify format (hashid), test small samples, avoid brute-force blindly."
        )
    if any(k in t for k in ["forensic", "image", "pcap", "memory"]):
        return (
            "Verify file magic, run strings/hexdump, use appropriate carve/analysis tools."
        )
    return (
        "Break the task down: scope -> safe defaults -> record results -> next step."
    )


def main(argv: Optional[List[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help", "help"}:
        return print_help()

    engine = _select_engine()
    cmd = args[0]
    if cmd == "prompt":
        return cmd_prompt()
    if cmd == "checklist":
        topic = args[1] if len(args) > 1 else None
        return cmd_checklist(topic)
    if cmd == "guide":
        session = None
        use_tui = False
        remaining_args = args[1:]

        # Parse --session and --tui flags
        while remaining_args:
            if remaining_args[0] == "--session" and len(remaining_args) > 1:
                session = remaining_args[1]
                remaining_args = remaining_args[2:]
            elif remaining_args[0] == "--tui":
                use_tui = True
                remaining_args = remaining_args[1:]
            else:
                remaining_args = remaining_args[1:]

        if use_tui:
            return cmd_guide_tui(session=session)
        return cmd_guide(session=session)

    # Student helpers
    if cmd == "explain" and len(args) > 1:
        text, send = _extract_text_and_send(args[1:])
        return _maybe_json_print("explain", text, _maybe_ai(engine, "explain", text, send))
    if cmd in {"assist", "help"} and len(args) > 1:
        text, send = _extract_text_and_send(args[1:])
        return _maybe_json_print("assist", text, _maybe_ai(engine, "assist", text, send))
    if cmd == "tip" and len(args) > 1:
        text, send = _extract_text_and_send(args[1:])
        return _maybe_json_print("tip", text, _maybe_ai(engine, "tip", text, send))
    if cmd == "report" and len(args) > 1:
        text, send = _extract_text_and_send(args[1:])
        return _maybe_json_print("report", text, _maybe_ai(engine, "report", text, send))
    if cmd == "quiz" and len(args) > 1:
        text, send = _extract_text_and_send(args[1:])
        return _maybe_json_print("quiz", text, _maybe_ai(engine, "quiz", text, send))
    if cmd == "plan" and len(args) > 1:
        text, send = _extract_text_and_send(args[1:])
        return _maybe_json_print("plan", text, _maybe_ai(engine, "plan", text, send))
        

    if cmd == "todo":
        return cmd_todo(args[1:])
    if cmd == "history":
        return cmd_history(args[1:])
    if cmd == "config":
        return cmd_config()
    if cmd == "run":
        return cmd_run(args[1:])

    print(f"Unknown command: {cmd}")
    return print_help()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


def _maybe_json_print(kind: str, input_text: str, output_text: str) -> int:
    if os.environ.get("CYBUDDY_JSON") == "1":
        obj = {"type": kind, "input": input_text, "output": output_text, "ts": _now_iso()}
        print(json.dumps(obj))
        return 0
    print(output_text)
    return 0

# === Student-focused helpers (uses rich mockup data) ===

def explain_command(command_text: str) -> str:
    from .mockup_data import smart_explain
    return smart_explain(command_text)


def quick_tip(topic: str) -> str:
    from .mockup_data import smart_tip
    return smart_tip(topic)


def help_troubleshoot(issue: str) -> str:
    from .mockup_data import smart_assist
    return smart_assist(issue)


def micro_report(finding: str) -> str:
    from .mockup_data import smart_report
    return smart_report(finding)


def quiz_flashcards(topic: str) -> str:
    from .mockup_data import smart_quiz
    return smart_quiz(topic)


def step_planner(context: str) -> str:
    from .mockup_data import smart_plan
    return smart_plan(context)


# === Lightweight session history and TODO tracker ===

def _app_dir() -> Path:
    # Respect HOME override; do not create directories unless needed later
    home = os.environ.get("HOME") or os.path.expanduser("~")
    return Path(home) / ".cybuddy"


def _history_file(session: Optional[str] = None) -> Path:
    cfg = load_config()
    if session:
        base = _app_dir() / "sessions" / session
        path = base / "history.jsonl"
    else:
        path = Path(os.path.expanduser(cfg.get("history.path", str(_app_dir() / "history.jsonl"))))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return path


def _todo_file(session: Optional[str] = None) -> Path:
    cfg = load_config()
    if session:
        base = _app_dir() / "sessions" / session
        path = base / "todo.json"
    else:
        path = Path(os.path.expanduser(cfg.get("todo.path", str(_app_dir() / "todo.json"))))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return path


def _config_file() -> Path:
    return _app_dir() / "config.toml"


def load_config() -> dict:
    # Defaults
    cfg: dict = {
        "history.enabled": True,
        "history.path": str(_app_dir() / "history.jsonl"),
        "todo.path": str(_app_dir() / "todo.json"),
        "output.truncate_lines": 60,
        "approvals.require_exec": True,
        "approvals.ai_consent": False,
        "ai.enabled": False,
        "ai.provider": "openai",
        "ai.redact": True,
        "ai.max_tokens": 300,
        "history.verbatim": False,
    }
    path = _config_file()
    if not path.exists():
        return cfg
    try:
        # Minimal TOML parser: handle key = value lines without sections
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = [p.strip() for p in line.split("=", 1)]
            v = v.strip()
            if v.lower() in {"true", "false"}:
                cfg[k] = v.lower() == "true"
            elif v.startswith('"') and v.endswith('"'):
                cfg[k] = v.strip('"')
            else:
                try:
                    cfg[k] = int(v)
                except ValueError:
                    cfg[k] = v
    except Exception:
        pass
    return cfg


def cmd_config() -> int:
    cfg = load_config()
    print("Config file:", _config_file())
    for k in sorted(cfg):
        print(f"{k} = {cfg[k]}")
    return 0


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def history_append(event: dict, session: Optional[str] = None) -> None:
    cfg = load_config()
    if not cfg.get("history.enabled", True):
        return
    try:
        payload = {"ts": _now_iso(), **event}
        if event.get("type", "").startswith("ai:") and not load_config().get("history.verbatim", False):
            data = event.get("data")
            if isinstance(data, dict):
                data = {k: v for k, v in data.items() if k in {"kind", "redaction", "len"}}
            payload["data"] = data
        with _history_file(session).open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        pass


def cmd_history(args: List[str]) -> int:
    if args and args[0] == "--clear":
        try:
            _history_file().unlink(missing_ok=True)
            print("History cleared.")
        except Exception as e:
            print(f"Failed to clear history: {e}")
            return 1
        return 0

    path = _history_file()
    if not path.exists():
        print("No history yet.")
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = obj.get("ts", "?")
            kind = obj.get("type", "event")
            data = obj.get("data")
            print(f"[{ts}] {kind}: {data}")
            count += 1
    if count == 0:
        print("No history yet.")
    return 0


def _todo_load(session: Optional[str] = None) -> List[dict]:
    path = _todo_file(session)
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []


def _todo_save(items: List[dict], session: Optional[str] = None) -> None:
    _todo_file(session).write_text(json.dumps(items, indent=2), encoding="utf-8")


def cmd_todo(args: List[str]) -> int:
    session = None
    if args[:2] == ["--session"] and len(args) > 2:
        session = args[2]
        args = args[3:]
    items = _todo_load(session)
    if not args:
        if not items:
            print("No TODO items. Add one with: secbuddy todo add \"Do recon\"")
            return 0
        for i, it in enumerate(items, 1):
            status = it.get("status", "pending")
            print(f"{i}. [{status}] {it.get('text','')}")
        return 0

    sub = args[0]
    if sub == "add" and len(args) > 1:
        text = " ".join(args[1:]).strip("\"")
        items.append({"text": text, "status": "pending", "added": _now_iso()})
        _todo_save(items, session)
        history_append({"type": "todo:add", "data": text}, session=session)
        print(f"Added: {text}")
        return 0
    if sub == "done" and len(args) > 1:
        try:
            idx = int(args[1]) - 1
            if idx < 0 or idx >= len(items):
                raise ValueError
        except ValueError:
            print("Provide a valid item number.")
            return 1
        items[idx]["status"] = "completed"
        items[idx]["completed"] = _now_iso()
        _todo_save(items, session)
        history_append({"type": "todo:done", "data": items[idx]["text"]}, session=session)
        print(f"Done: {items[idx]['text']}")
        return 0
    if sub == "clear":
        _todo_save([], session)
        history_append({"type": "todo:clear", "data": None}, session=session)
        print("Cleared all TODO items.")
        return 0

    print("Unknown todo command. Use: list | add <text> | done <num> | clear")
    return 1


def _select_engine() -> AnswerEngine:
    cfg = load_config()
    if not cfg.get("ai.enabled", False):
        return HeuristicEngine(
            explain_fn=explain_command,
            tip_fn=quick_tip,
            assist_fn=help_troubleshoot,
            report_fn=micro_report,
            quiz_fn=quiz_flashcards,
            plan_fn=step_planner,
        )
    provider = str(cfg.get("ai.provider", "openai"))
    if provider == "openai":
        api_key = str(cfg.get("openai.api_key", ""))
        model = str(cfg.get("openai.model", "gpt-4o-mini"))
        if not api_key:
            return HeuristicEngine(
                explain_fn=explain_command,
                tip_fn=quick_tip,
                assist_fn=help_troubleshoot,
                report_fn=micro_report,
                quiz_fn=quiz_flashcards,
                plan_fn=step_planner,
            )
        return OpenAIEngine(api_key=api_key, model=model, redact_fn=redact)
    if provider == "claude":
        return ClaudeEngine(api_key=str(cfg.get("claude.api_key", "")), model=str(cfg.get("claude.model", "claude-3")), redact_fn=redact)
    if provider == "gemini":
        return GeminiEngine(api_key=str(cfg.get("gemini.api_key", "")), model=str(cfg.get("gemini.model", "gemini-1.5")), redact_fn=redact)
    # Future: claude, gemini, custom
    return HeuristicEngine(
        explain_fn=explain_command,
        tip_fn=quick_tip,
        assist_fn=help_troubleshoot,
        report_fn=micro_report,
        quiz_fn=quiz_flashcards,
        plan_fn=step_planner,
    )


def _extract_text_and_send(args: List[str]) -> Tuple[str, bool]:
    send = False
    cleaned: List[str] = []
    for a in args:
        if a == "--send":
            send = True
        else:
            cleaned.append(a)
    return " ".join(cleaned).strip("\""), send


def _maybe_ai(engine: AnswerEngine, kind: str, text: str, send: bool) -> str:
    cfg = load_config()
    if not cfg.get("ai.enabled", False):
        return getattr(_HeuristicProxy(), kind)(text)
    if not cfg.get("approvals.ai_consent", False) and not send:
        return f"[AI disabled without consent] Use --send or set approvals.ai_consent=true.\n" + getattr(_HeuristicProxy(), kind)(text)
    redacted_text, summary = redact(text) if cfg.get("ai.redact", True) else (text, "no redaction")
    history_append({"type": "ai:request", "data": {"kind": kind, "redaction": summary}})
    result = getattr(engine, kind)(text)
    history_append({"type": "ai:response", "data": {"kind": kind, "len": len(result)}})
    return result


def _HeuristicProxy() -> AnswerEngine:
    return HeuristicEngine(
        explain_fn=explain_command,
        tip_fn=quick_tip,
        assist_fn=help_troubleshoot,
        report_fn=micro_report,
        quiz_fn=quiz_flashcards,
        plan_fn=step_planner,
    )


# === Dry-run runner (approvals-like) ===

def cmd_run(args: List[str]) -> int:
    if not args:
        print("Usage: secbuddy run <tool> \"<args>\" [--exec]")
        return 1
    tool = args[0]
    exec_flag = "--exec" in args
    joined = " ".join(a for a in args[1:] if a != "--exec").strip()
    command = f"{tool} {joined}".strip()

    safety, notes = _safety_review(tool, joined)
    print("SAFETY:")
    for n in safety:
        print(f"- {n}")
    for tip in notes:
        print(f"- TIP: {tip}")
    print("CMD:")
    print(command or tool)

    if not exec_flag and load_config().get("approvals.require_exec", True):
        print("NOT RUN (dry-run). Pass --exec to execute.")
        history_append({"type": "run:dry", "data": command})
        return 0

    # Actually run the command
    try:
        import subprocess

        proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        out = proc.stdout.strip()
        err = proc.stderr.strip()
        code = proc.returncode
        print("OUT:")
        print(_truncate_lines(out))
        if err:
            print("ERR:")
            print(_truncate_lines(err))
        history_append({"type": "run:exec", "data": {"cmd": command, "code": code}})
        return code
    except Exception as e:
        print(f"Failed to execute: {e}")
        return 1


def _truncate_lines(s: str) -> str:
    if not s:
        return ""
    max_lines = int(load_config().get("output.truncate_lines", 60) or 60)
    lines = s.splitlines()
    if len(lines) <= max_lines:
        return s
    return "\n".join(lines[:max_lines] + ["(truncated)"])


def _safety_review(tool: str, argstr: str) -> Tuple[List[str], List[str]]:
    notes: List[str] = []
    tips: List[str] = []
    t = (tool + " " + argstr).lower()
    if tool == "nmap":
        if " -t5" in t or " -t4" in t:
            notes.append("Timing is aggressive; prefer T2 in shared labs")
        if " --script" in t:
            notes.append("NSE scripts can be intrusive; review scripts")
        if " -a " in t:
            notes.append("-A bundles aggressive scans; use selectively")
        if " -p-" in t:
            notes.append("Full port scan can be noisy and slow")
        if " -suv" in t or " -su" in t:
            notes.append("UDP scans are slow/noisy; consider targeting")
        tips.append("Common safe start: nmap -sV -Pn -T2 <target>")
    elif tool == "gobuster":
        if " -w " not in t:
            notes.append("Provide a wordlist with -w <file>")
        if " dir " in t or " -u " in t:
            tips.append("Start with small wordlists to reduce noise")
        notes.append("Respect robots.txt and scope; avoid production targets")
    elif tool == "nikto":
        notes.append("Nikto can be noisy; prefer off-hours in labs")
        tips.append("Target specific host: nikto -h <url>")
    else:
        notes.append("Unknown tool; review flags before execution")
    return notes, tips
from .engine import (
    AnswerEngine,
    HeuristicEngine,
    OpenAIEngine,
    redact,
)
