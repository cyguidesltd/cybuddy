"""Smart suggestion system for command and topic recommendations."""

from typing import List
from difflib import get_close_matches


def get_command_suggestions(unknown_cmd: str, available_commands: List[str], n: int = 3) -> List[str]:
    """
    Get smart suggestions for unknown commands using fuzzy matching.

    Args:
        unknown_cmd: The command that wasn't recognized
        available_commands: List of valid commands
        n: Number of suggestions to return (default: 3)

    Returns:
        List of suggested commands, sorted by similarity
    """
    # Use difflib for fuzzy matching (60% similarity threshold)
    matches = get_close_matches(unknown_cmd.lower(),
                                [c.lower() for c in available_commands],
                                n=n,
                                cutoff=0.6)

    # Map back to original case
    cmd_map = {c.lower(): c for c in available_commands}
    return [cmd_map[m] for m in matches]


def get_topic_suggestions(unknown_topic: str, available_topics: List[str], n: int = 3) -> List[str]:
    """
    Get smart suggestions for unknown topics using fuzzy matching.

    Args:
        unknown_topic: The topic that wasn't found
        available_topics: List of valid topics
        n: Number of suggestions to return (default: 3)

    Returns:
        List of suggested topics, sorted by similarity
    """
    # Use difflib for fuzzy matching (50% similarity threshold for topics)
    matches = get_close_matches(unknown_topic.lower(),
                                [t.lower() for t in available_topics],
                                n=n,
                                cutoff=0.5)

    # Map back to original case
    topic_map = {t.lower(): t for t in available_topics}
    return [topic_map[m] for m in matches]


def get_tool_suggestions(unknown_tool: str, available_tools: List[str], n: int = 3) -> List[str]:
    """
    Get smart suggestions for unknown tools using fuzzy matching.

    Args:
        unknown_tool: The tool name that wasn't found
        available_tools: List of valid tool names
        n: Number of suggestions to return (default: 3)

    Returns:
        List of suggested tools, sorted by similarity
    """
    # Use difflib for fuzzy matching (55% similarity threshold)
    matches = get_close_matches(unknown_tool.lower(),
                                [t.lower() for t in available_tools],
                                n=n,
                                cutoff=0.55)

    # Map back to original case
    tool_map = {t.lower(): t for t in available_tools}
    return [tool_map[m] for m in matches]
