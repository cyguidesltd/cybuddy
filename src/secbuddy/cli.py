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
    "You are SecBuddy, a helpful cybersecurity study companion. "
    "You explain steps simply, provide safe defaults, and always suggest next actions. "
    "You avoid running destructive commands and emphasize documenting findings."
)


def print_help() -> int:
    print(
        """
SecBuddy - beginner-friendly cybersecurity helper

Usage:
  secbuddy guide [--session NAME]  Interactive helper with PLAN/ACTION/CMD/OUT/NEXT; supports slash-commands
  secbuddy checklist [topic]     Show a checklist (recon|web|crypto|forensics)
  secbuddy prompt                Print a starter LLM system prompt
  secbuddy help                  Show this help
  secbuddy explain "<command>"   Explain a shell/tool command
  secbuddy tip "<topic>"         Quick study tip/trick
  secbuddy assist "<issue>"      Troubleshoot an error (alias: help!)
  secbuddy report "<finding>"    2–3 line practice write-up
  secbuddy quiz "<topic>"        Flashcard-style Q&A (2–3 items)
  secbuddy plan "<context>"      Next steps guidance (3 steps)
  secbuddy todo [subcmd]         Plan tracker: list/add/done/clear
  secbuddy history [--clear]     Show or clear recent session history
  secbuddy config                Show resolved configuration
  secbuddy run <tool> "<args>"  Dry-run wrapper with safety notes (use --exec to run)
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
    print("Welcome to SecBuddy Guide. Type 'exit' to quit. Use /tip, /plan, /checklist <topic>, /todo add <..>, /run <tool> \"args\"")
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

        # Render codex-like sections
        plan_text = suggest_next(line)
        print("PLAN:")
        print("- " + plan_text)
        action = "Provide brief next step and safe command (if any)"
        print("ACTION:\n- " + action)
        cmd_hint = _guide_command_hint(line)
        if cmd_hint:
            print("CMD:\n" + cmd_hint)
        print("OUT:\n(analysis in brief; update your todo/history as needed)")
        print("NEXT:\n- " + suggest_next(line))
        history_append({"type": "guide", "data": {"input": line, "plan": plan_text}}, session=session)
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
        if len(args) > 1 and args[1] == "--session" and len(args) > 2:
            session = args[2]
        return cmd_guide(session=session)

    # Student helpers
    if cmd == "explain" and len(args) > 1:
        text = " ".join(args[1:]).strip("\"")
        return _maybe_json_print("explain", text, engine.explain(text))
    if cmd in {"assist", "help"} and len(args) > 1:
        text = " ".join(args[1:]).strip("\"")
        return _maybe_json_print("assist", text, engine.assist(text))
    if cmd == "tip" and len(args) > 1:
        text = " ".join(args[1:]).strip("\"")
        return _maybe_json_print("tip", text, engine.tip(text))
    if cmd == "report" and len(args) > 1:
        text = " ".join(args[1:]).strip("\"")
        return _maybe_json_print("report", text, engine.report(text))
    if cmd == "quiz" and len(args) > 1:
        text = " ".join(args[1:]).strip("\"")
        return _maybe_json_print("quiz", text, engine.quiz(text))
    if cmd == "plan" and len(args) > 1:
        text = " ".join(args[1:]).strip("\"")
        return _maybe_json_print("plan", text, engine.plan(text))
        

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

# === Student-focused helpers (simple heuristics, no external calls) ===

def explain_command(command_text: str) -> str:
    t = command_text.strip()
    if t.startswith("nmap"):
        parts = []
        if "-sV" in t:
            parts.append("-sV: version detection")
        if "-Pn" in t:
            parts.append("-Pn: treat hosts as up (no ping)")
        if "-T" in t:
            parts.append("-T<0-5>: timing (lower is safer)")
        if not parts:
            parts.append("Basic port/service scan")
        parts.append("Use when enumerating services")
        parts.append("Watch out: can be noisy on IDS")
        return "\n".join(parts)
    if t.startswith("sqlmap"):
        return (
            "sqlmap: automated SQLi testing\n"
            "Use with explicit scope and consent\n"
            "Flags: -u URL, --data, --risk/--level"
        )
    return "High-level explanation not found; try a simpler example."


def quick_tip(topic: str) -> str:
    k = topic.lower()
    if "sql" in k:
        return (
            "Look for ' OR '1'='1 in forms\n"
            "Check error messages\n"
            "Use UNION to extract tables"
        )
    if any(s in k for s in ["xss", "cross-site"]):
        return (
            "Test reflected params with <script>alert(1)</script> (safely)\n"
            "Prefer attribute/style/event variations\n"
            "Check CSP and output encoding"
        )
    return "Start from basics, confirm assumptions, and test small examples."


def help_troubleshoot(issue: str) -> str:
    k = issue.lower()
    if "sqlmap" in k and ("refused" in k or "connection" in k):
        return (
            "Target may be down\n"
            "Check host/IP & port\n"
            "Ensure lab is running (Docker / VM)"
        )
    if "nmap" in k and "permission" in k:
        return (
            "Try non-privileged scans or sudo if appropriate\n"
            "Avoid aggressive flags in shared labs\n"
            "Document command and environment"
        )
    return "Reproduce the error, capture the exact message, and simplify the command."


def micro_report(finding: str) -> str:
    # Produce a compact template regardless of input
    return (
        "Vulnerability: "
        + (finding or "(describe succinctly)")
        + "\nImpact: (what can an attacker do)\nMitigation: (least-privilege, patch, validation)"
    )


def quiz_flashcards(topic: str) -> str:
    k = topic.lower()
    if "sql" in k:
        return (
            "Q: What is a common SQLi payload?\n"
            "A: ' OR '1'='1 --\n"
            "Q: Mitigation?\n"
            "A: Use parameterized queries"
        )
    if "xss" in k:
        return (
            "Q: What is reflected XSS?\n"
            "A: Injection reflected in immediate response\n"
            "Q: Mitigation?\n"
            "A: Output encoding + CSP"
        )
    return (
        "Q: Define the core concept\n"
        "A: One-sentence explanation\n"
        "Q: Name a mitigation\n"
        "A: One concrete step"
    )


def step_planner(context: str) -> str:
    k = context.lower()
    if "nmap" in k and ("80" in k or "http" in k or "web" in k):
        return (
            "1. Enumerate the web service (nikto, directory brute force)\n"
            "2. Check banners for version info\n"
            "3. Test for common web vulns (XSS, SQLi)"
        )
    return (
        "1. Clarify scope and objective\n"
        "2. Choose safe default tools/flags\n"
        "3. Record findings and plan next probe"
    )


# === Lightweight session history and TODO tracker ===

def _app_dir() -> Path:
    # Respect HOME override; do not create directories unless needed later
    home = os.environ.get("HOME") or os.path.expanduser("~")
    return Path(home) / ".secbuddy"


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
        with _history_file(session).open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": _now_iso(), **event}) + "\n")
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
    # Future: claude, gemini, custom
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
