"""
Prompt templates for AI interactions.

Provides structured prompts for different command types.
"""

SYSTEM_PROMPT = """You are CyBuddy, a beginner-friendly cybersecurity learning companion.

Your responses should:
- Be clear and concise (2-4 paragraphs max)
- Explain concepts in simple terms
- Provide practical examples
- Emphasize safe, ethical practices
- Avoid jargon unless you explain it

You are helping security students and CTF players learn."""


def build_explain_prompt(topic: str, mockup_context: str | None = None) -> str:
    """
    Build prompt for 'explain' command.

    Args:
        topic: Security topic/tool to explain
        mockup_context: Optional context from mockup data

    Returns:
        Formatted prompt string
    """
    prompt = f"{SYSTEM_PROMPT}\n\n"
    prompt += f"Explain this security tool/concept for a beginner: {topic}\n\n"
    prompt += "Include:\n"
    prompt += "- What it is and why it's useful\n"
    prompt += "- Common flags/options (if applicable)\n"
    prompt += "- When to use it\n"
    prompt += "- Important cautions or common mistakes\n"

    if mockup_context:
        prompt += f"\nAdditional context from knowledge base:\n{mockup_context}\n"

    return prompt


def build_tip_prompt(topic: str, mockup_context: str | None = None) -> str:
    """
    Build prompt for 'tip' command.

    Args:
        topic: Security topic for tips
        mockup_context: Optional context from mockup data

    Returns:
        Formatted prompt string
    """
    prompt = f"{SYSTEM_PROMPT}\n\n"
    prompt += f"Provide 3-5 practical tips and techniques for: {topic}\n\n"
    prompt += "Format as a bulleted list with:\n"
    prompt += "- Specific actionable techniques\n"
    prompt += "- Where to look/what to test\n"
    prompt += "- Common payloads or commands\n"
    prompt += "- Quick wins for beginners\n"

    if mockup_context:
        prompt += f"\nContext from knowledge base:\n{mockup_context}\n"

    return prompt


def build_plan_prompt(situation: str, mockup_context: str | None = None) -> str:
    """
    Build prompt for 'plan' command.

    Args:
        situation: Current situation/context
        mockup_context: Optional context from mockup data

    Returns:
        Formatted prompt string
    """
    prompt = f"{SYSTEM_PROMPT}\n\n"
    prompt += f"Create a 3-step action plan for this situation: {situation}\n\n"
    prompt += "Format as a numbered list (1-3) with:\n"
    prompt += "- Specific, safe next steps\n"
    prompt += "- Commands to run (with safe defaults)\n"
    prompt += "- What to document\n"
    prompt += "- What to watch out for\n"

    if mockup_context:
        prompt += f"\nRelevant knowledge:\n{mockup_context}\n"

    return prompt


def build_assist_prompt(problem: str, mockup_context: str | None = None) -> str:
    """
    Build prompt for 'assist' command (troubleshooting).

    Args:
        problem: Error or issue description
        mockup_context: Optional context from mockup data

    Returns:
        Formatted prompt string
    """
    prompt = f"{SYSTEM_PROMPT}\n\n"
    prompt += f"Help troubleshoot this issue: {problem}\n\n"
    prompt += "Provide:\n"
    prompt += "- 2-3 most likely causes\n"
    prompt += "- How to verify each cause\n"
    prompt += "- Specific fixes (commands/config changes)\n"
    prompt += "- Order by simplest fix first\n"

    if mockup_context:
        prompt += f"\nContext:\n{mockup_context}\n"

    return prompt


def build_report_prompt(finding: str, mockup_context: str | None = None) -> str:
    """
    Build prompt for 'report' command.

    Args:
        finding: Security finding to document
        mockup_context: Optional context from mockup data

    Returns:
        Formatted prompt string
    """
    prompt = f"{SYSTEM_PROMPT}\n\n"
    prompt += f"Write a brief security report (2-3 paragraphs) for: {finding}\n\n"
    prompt += "Include:\n"
    prompt += "1. Vulnerability: What was found\n"
    prompt += "2. Impact: What an attacker could do\n"
    prompt += "3. Mitigation: How to fix it\n"
    prompt += "\nUse professional but clear language.\n"

    if mockup_context:
        prompt += f"\nReference information:\n{mockup_context}\n"

    return prompt


def build_quiz_prompt(topic: str, mockup_context: str | None = None) -> str:
    """
    Build prompt for 'quiz' command.

    Args:
        topic: Topic for quiz questions
        mockup_context: Optional context from mockup data

    Returns:
        Formatted prompt string
    """
    prompt = f"{SYSTEM_PROMPT}\n\n"
    prompt += f"Create 2-3 quiz questions about: {topic}\n\n"
    prompt += "Format each as:\n"
    prompt += "Q: [Question]\n"
    prompt += "A: [Answer with brief explanation]\n"
    prompt += "\nFocus on practical knowledge, not trivia.\n"

    if mockup_context:
        prompt += f"\nBased on:\n{mockup_context}\n"

    return prompt


# Prompt builder dispatcher
PROMPT_BUILDERS = {
    "explain": build_explain_prompt,
    "tip": build_tip_prompt,
    "plan": build_plan_prompt,
    "assist": build_assist_prompt,
    "report": build_report_prompt,
    "quiz": build_quiz_prompt,
}


def build_prompt(
    command: str, query: str, mockup_context: str | None = None
) -> str:
    """
    Build prompt for any command type.

    Args:
        command: Command name (explain, tip, plan, etc.)
        query: User's query/topic
        mockup_context: Optional mockup data context

    Returns:
        Formatted prompt string

    Raises:
        ValueError: If command is unknown
    """
    builder = PROMPT_BUILDERS.get(command)
    if not builder:
        raise ValueError(
            f"Unknown command: {command}. "
            f"Valid commands: {', '.join(PROMPT_BUILDERS.keys())}"
        )

    return builder(query, mockup_context)
