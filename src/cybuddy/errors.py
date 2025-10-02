"""Smart error handling with helpful suggestions."""


from .suggestions import (
    get_command_suggestions,
    get_tool_suggestions,
    get_topic_suggestions,
)


def handle_unknown_command(cmd: str, available_commands: list[str]) -> int:
    """
    Handle unknown command errors with smart suggestions.

    Args:
        cmd: The unknown command
        available_commands: List of valid commands

    Returns:
        Exit code (1 for error)
    """
    suggestions = get_command_suggestions(cmd, available_commands)

    print(f"Unknown command: {cmd}")

    if suggestions:
        print("\nDid you mean one of these?")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    else:
        print(f"\nAvailable commands: {', '.join(sorted(available_commands))}")

    print("\nRun 'cybuddy --help' for usage information.")
    return 1


def handle_unknown_topic(topic: str, available_topics: list[str]) -> int:
    """
    Handle unknown topic errors with smart suggestions.

    Args:
        topic: The unknown topic
        available_topics: List of valid topics

    Returns:
        Exit code (1 for error)
    """
    suggestions = get_topic_suggestions(topic, available_topics)

    print(f"Unknown topic: {topic}")

    if suggestions:
        print("\nDid you mean one of these?")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    else:
        print(f"\nAvailable topics: {', '.join(sorted(available_topics))}")

    return 1


def handle_unknown_tool(tool: str, available_tools: list[str]) -> int:
    """
    Handle unknown tool errors with smart suggestions.

    Args:
        tool: The unknown tool
        available_tools: List of valid tools

    Returns:
        Exit code (1 for error)
    """
    suggestions = get_tool_suggestions(tool, available_tools)

    print(f"Unknown tool: {tool}")

    if suggestions:
        print("\nDid you mean one of these?")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    else:
        print("\nRun 'cybuddy explain <tool>' to learn about security tools.")

    return 1


def handle_missing_argument(cmd: str, arg_name: str, example: str = "") -> int:
    """
    Handle missing argument errors with helpful examples.

    Args:
        cmd: The command that's missing an argument
        arg_name: Name of the missing argument
        example: Optional example of correct usage

    Returns:
        Exit code (1 for error)
    """
    print(f"Missing argument: {arg_name}")
    print(f"\nUsage: cybuddy {cmd} <{arg_name}>")

    if example:
        print("\nExample:")
        print(f"  {example}")

    return 1
