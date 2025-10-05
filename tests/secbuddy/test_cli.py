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
    load_config,
)
from cybuddy.commands.history import cmd_history
from cybuddy.engine import HeuristicEngine


def run_cli(args: List[str]) -> int:
    return main(args)


def test_help_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    code = run_cli(["--help"])
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




def test_history_file_created(tmp_path, capsys) -> None:
    import os
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)
    try:
        # Test that history command works
        assert cmd_history([]) == 0
        # Clear history
        assert cmd_history(["--clear"]) == 0
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
