from __future__ import annotations

import sys
from typing import List

import pytest

from cybuddy.cli import (
    main,
    suggest_next,
    explain_command,
    quick_tip,
    help_troubleshoot,
    micro_report,
    quiz_flashcards,
    step_planner,
    cmd_todo,
    cmd_run,
    load_config,
    cmd_config,
)
from cybuddy.commands.history import cmd_history
from cybuddy.engine import HeuristicEngine, redact


def run_cli(args: List[str]) -> int:
    return main(args)


def test_help_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    code = run_cli(["--help"])
    captured = capsys.readouterr()
    assert code == 0
    assert "CyBuddy" in captured.out


def test_prompt_prints(capsys: pytest.CaptureFixture[str]) -> None:
    code = run_cli(["prompt"])
    captured = capsys.readouterr()
    assert code == 0
    assert "CyBuddy" in captured.out


def test_explain_nmap() -> None:
    out = explain_command('nmap -sV target.local')
    assert "service detection" in out


def test_tip_sql() -> None:
    out = quick_tip('SQL injection basics')
    assert "UNION" in out


def test_help_sqlmap() -> None:
    out = help_troubleshoot('sqlmap: connection refused')
    assert "may be down" in out


def test_report_template() -> None:
    out = micro_report('Found SQLi on login form')
    assert out.count('\n') >= 2


def test_quiz_sql() -> None:
    out = quiz_flashcards('SQL Injection')
    assert "Q:" in out and "A:" in out


def test_plan_web() -> None:
    out = step_planner('I scanned with nmap and saw port 80 open')
    assert out.startswith('1.')


def test_todo_lifecycle(tmp_path) -> None:
    # Point HOME to tmp to isolate files
    import os
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)
    try:
        assert cmd_todo([]) == 0  # list empty
        assert cmd_todo(["add", "Test item"]) == 0
        assert cmd_todo([]) == 0
        assert cmd_todo(["done", "1"]) == 0
        assert cmd_todo(["clear"]) == 0
    finally:
        if old_home is not None:
            os.environ["HOME"] = old_home


def test_history_file_created(tmp_path, capsys) -> None:
    import os
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)
    try:
        # Add a todo to generate history
        cmd_todo(["add", "History check"])
        # Check that the todo was added (not in command history but in todo system)
        out = capsys.readouterr().out
        assert "Added: History check" in out
        # Test that history command works
        assert cmd_history([]) == 0
        # Clear history
        assert cmd_history(["--clear"]) == 0
    finally:
        if old_home is not None:
            os.environ["HOME"] = old_home


def test_config_defaults(tmp_path, capsys) -> None:
    import os
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)
    try:
        assert cmd_config() == 0
        cfg = load_config()
        assert cfg.get("approvals.require_exec") is True
    finally:
        if old_home is not None:
            os.environ["HOME"] = old_home


def test_run_dry(tmp_path, capsys) -> None:
    import os
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)
    try:
        code = cmd_run(["nmap", "-sV -Pn target.local"])  # dry-run by default
        assert code == 0
        out = capsys.readouterr().out
        assert "NOT RUN" in out
        assert "SAFETY:" in out
    finally:
        if old_home is not None:
            os.environ["HOME"] = old_home


def test_guide_sections(tmp_path, monkeypatch, capsys) -> None:
    import os
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)
    try:
        inputs = iter(["scan target.local", "exit"])  # two lines then exit
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        from cybuddy.cli import cmd_guide

        assert cmd_guide(session="sess1") == 0
        out = capsys.readouterr().out
        assert "PLAN:" in out and "ACTION:" in out and "NEXT:" in out
    finally:
        if old_home is not None:
            os.environ["HOME"] = old_home


def test_engine_heuristic() -> None:
    eng = HeuristicEngine(
        explain_fn=explain_command,
        tip_fn=quick_tip,
        assist_fn=help_troubleshoot,
        report_fn=micro_report,
        quiz_fn=quiz_flashcards,
        plan_fn=step_planner,
    )
    assert "service" in eng.explain("nmap -sV")


def test_redact() -> None:
    red, summary = redact("Contact 10.0.0.1 or api.example.com with sk-ABCDEF0123456789ABCDEF")
    assert "<IP>" in red and "<DOMAIN>" in red and "<TOKEN>" in red
    assert summary


def test_ai_consent_flow(tmp_path, monkeypatch, capsys) -> None:
    import os
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)
    try:
        # Enable AI without consent; should fall back and include notice
        cfg_path = tmp_path / ".cybuddy" / "config.toml"
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text("ai.enabled = true\napprovals.ai_consent = false\n", encoding="utf-8")
        from cybuddy.cli import main
        code = main(["explain", "nmap -sV"])
        out = capsys.readouterr().out
        assert code == 0
        assert "AI disabled without consent" in out
        # With --send, should proceed (still stubbed but no consent warning)
        code = main(["explain", "nmap -sV", "--send"])
        out2 = capsys.readouterr().out
        assert code == 0
        assert "AI disabled without consent" not in out2
    finally:
        if old_home is not None:
            os.environ["HOME"] = old_home


@pytest.mark.parametrize(
    "text, expect",
    [
        ("do an nmap scan", "nmap"),
        ("web app xss", "Burp"),
        ("hash crack", "Identify format"),
        ("pcap forensic", "file magic"),
        ("generic", "Break the task down"),
    ],
)
def test_suggest_next(text: str, expect: str) -> None:
    s = suggest_next(text)
    assert expect.lower()[:4] in s.lower()
