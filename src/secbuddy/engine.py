from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class AnswerEngine(Protocol):
    def explain(self, text: str) -> str: ...
    def tip(self, text: str) -> str: ...
    def assist(self, text: str) -> str: ...
    def report(self, text: str) -> str: ...
    def quiz(self, text: str) -> str: ...
    def plan(self, text: str) -> str: ...


@dataclass(frozen=True)
class HeuristicEngine:
    explain_fn: callable
    tip_fn: callable
    assist_fn: callable
    report_fn: callable
    quiz_fn: callable
    plan_fn: callable

    def explain(self, text: str) -> str:
        return self.explain_fn(text)

    def tip(self, text: str) -> str:
        return self.tip_fn(text)

    def assist(self, text: str) -> str:
        return self.assist_fn(text)

    def report(self, text: str) -> str:
        return self.report_fn(text)

    def quiz(self, text: str) -> str:
        return self.quiz_fn(text)

    def plan(self, text: str) -> str:
        return self.plan_fn(text)


@dataclass(frozen=True)
class OpenAIEngine:
    api_key: str
    model: str
    redact_fn: callable

    def _call(self, kind: str, prompt: str) -> str:
        redacted, summary = self.redact_fn(prompt)
        # Stub: we don't call network here. Explain what would be sent.
        return (
            f"[AI disabled in this build] Would call {self.model} for {kind}.\n"
            f"Summary: {summary}"
        )

    def explain(self, text: str) -> str:
        return self._call("explain", _prompt_explain(text))

    def tip(self, text: str) -> str:
        return self._call("tip", _prompt_tip(text))

    def assist(self, text: str) -> str:
        return self._call("assist", _prompt_assist(text))

    def report(self, text: str) -> str:
        return self._call("report", _prompt_report(text))

    def quiz(self, text: str) -> str:
        return self._call("quiz", _prompt_quiz(text))

    def plan(self, text: str) -> str:
        return self._call("plan", _prompt_plan(text))


# Prompt templates
SYSTEM = (
    "You are SecBuddy, a beginner-friendly cybersecurity helper. "
    "Use 2-4 concise bullets, safe defaults, no destructive commands."
)


def _fmt(user: str) -> str:
    return f"SYSTEM: {SYSTEM}\nUSER: {user}"


def _prompt_explain(text: str) -> str:
    return _fmt(f"Explain succinctly: {text}\nInclude: flags, when-to-use, cautions.")


def _prompt_tip(text: str) -> str:
    return _fmt(f"Give 3 quick tips on: {text}")


def _prompt_assist(text: str) -> str:
    return _fmt(
        f"Troubleshoot this error: {text}\nReturn 3 checks/fixes, simplest first."
    )


def _prompt_report(text: str) -> str:
    return _fmt(
        f"Produce a 2–3 line micro-report for: {text}\nFormat: Vulnerability, Impact, Mitigation."
    )


def _prompt_quiz(text: str) -> str:
    return _fmt(
        f"Create 2–3 flashcards for: {text}\nFormat lines as Q: ... then A: ..."
    )


def _prompt_plan(text: str) -> str:
    return _fmt(
        f"Propose the next 3 safe steps for: {text}\nNumbered 1-3, concise."
    )


def redact(text: str) -> tuple[str, str]:
    # naive redaction: IPs, hostnames, tokens
    import re

    summary = []
    red = text
    # IP addresses
    if re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", text):
        red = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "<IP>", red)
        summary.append("IPs redacted")
    # domains
    if re.search(r"\b[a-z0-9.-]+\.[a-z]{2,}\b", text, re.I):
        red = re.sub(r"\b[a-z0-9.-]+\.[a-z]{2,}\b", "<DOMAIN>", red, flags=re.I)
        summary.append("domains redacted")
    # token-like
    if re.search(r"sk-[A-Za-z0-9]{20,}", text):
        red = re.sub(r"sk-[A-Za-z0-9]{20,}", "<TOKEN>", red)
        summary.append("tokens redacted")
    return red, ", ".join(summary) or "no sensitive patterns detected"

