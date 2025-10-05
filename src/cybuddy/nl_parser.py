"""
Natural Language Query Parser for CyBuddy.

Converts natural language queries into structured commands:
- "how do I scan ports?" → ("explain", "nmap")
- "tips on sql injection" → ("tip", "sql injection")
- "what should I do after getting a shell?" → ("plan", "got shell")
"""

from __future__ import annotations

import re


def parse_natural_query(text: str) -> tuple[str, str]:
    """
    Parse natural language into (command, query).

    Examples:
        "how do I scan for open ports?" → ("explain", "port scanning")
        "what is burp suite?" → ("explain", "burp suite")
        "tips on privilege escalation" → ("tip", "privilege escalation")
        "I found an open port 8080" → ("plan", "found open port 8080")

    Returns:
        Tuple of (command_name, extracted_query)
    """
    text_lower = text.lower().strip()
    
    # Handle direct command usage (e.g., "explain nmap -Pn")
    command_words = ['explain', 'tip', 'help', 'report', 'quiz', 'plan']
    for cmd in command_words:
        if text_lower.startswith(cmd + ' '):
            query = text[len(cmd):].strip()
            return cmd, query

    # Intent detection patterns (order matters - more specific first)
    intents = {
        'explain': [
            r'how (?:do|can) i (.*)',
            r'how to (.*)',
            r'explain (.*)',
            r'what is (.*)',
            r'what\'s (.*)',
            r'tell me about (.*)',
            r'describe (.*)',
            r'show me (.*)',
        ],
        'plan': [
            r'what should i do (?:after|when|if) (.*)',
            r'what(?:\'s| is) (?:the )?next (?:step|after) (.*)',
            r'next steps (?:for|after) (.*)',
            r'i (?:found|got|have|see) (.*)',
            r'what to do (?:with|about) (.*)',
            r'help (?:me )?(?:with|plan) (.*)',
        ],
        'tip': [
            r'tips? (?:on|for|about) (.*)',
            r'guide (?:for|to|on) (.*)',
            r'(?:how to )?learn (?:about )?(.*)',
            r'techniques? (?:for|on) (.*)',
            r'best practices? (?:for )?(.*)',
        ],
        'assist': [
            r'i\'?m getting (?:an? )?(.*)',
            r'(?:error|problem|issue):? (.*)',
            r'why (?:is|does|am|can\'t) (.*)',
            r'(?:how to )?fix (.*)',
            r'troubleshoot (.*)',
        ],
        'report': [
            r'document (.*)',
            r'write (?:a )?(?:up |report (?:for|on) )?(.*)',
            r'report (.*)',
            r'create (?:a )?report (?:for )?(.*)',
        ],
        'quiz': [
            r'test me (?:on )?(.*)',
            r'quiz (?:me )?(?:on |about )?(.*)',
            r'question(?:s)? (?:on |about )?(.*)',
            r'practice (.*)',
        ],
    }

    # Try to match intent patterns
    for command, patterns in intents.items():
        for pattern in patterns:
            match = re.match(pattern, text_lower)
            if match:
                query = match.group(1).strip()
                # Clean up common filler words
                query = _clean_query(query)
                return command, query

    # Keyword detection fallback
    # If the query contains tool names, assume "explain"
    tool_keywords = [
        'nmap', 'burp', 'sqlmap', 'metasploit', 'wireshark',
        'hydra', 'john', 'hashcat', 'gobuster', 'ffuf',
        'nikto', 'dirb', 'wfuzz', 'netcat', 'nc', 'ssh',
        'tcpdump', 'masscan', 'enum4linux', 'smbclient'
    ]

    if any(tool in text_lower for tool in tool_keywords):
        return 'explain', text

    # Attack technique keywords → tip
    attack_keywords = [
        'xss', 'sqli', 'sql injection', 'csrf', 'ssrf', 'xxe',
        'rce', 'lfi', 'rfi', 'ssti', 'deserialization',
        'privilege escalation', 'privesc', 'buffer overflow',
        'format string', 'race condition', 'injection'
    ]

    if any(keyword in text_lower for keyword in attack_keywords):
        return 'tip', text

    # Scenario/situation keywords → plan
    scenario_keywords = [
        'found', 'got', 'have', 'discovered', 'see', 'seeing',
        'stuck', 'after', 'next', 'shell', 'port', 'vulnerability',
        'target', 'enumeration', 'foothold'
    ]

    if any(keyword in text_lower for keyword in scenario_keywords):
        return 'plan', text

    # Default: treat as "explain" query
    return 'explain', text


def _clean_query(query: str) -> str:
    """Remove filler words and clean up the extracted query."""
    # Remove leading articles and common filler words
    stopwords = [
        'the', 'a', 'an', 'to', 'for', 'with', 'about', 'on',
        'in', 'at', 'by', 'from', 'of', 'and', 'or'
    ]

    words = query.split()
    # Remove stopwords from the beginning only
    while words and words[0] in stopwords:
        words.pop(0)

    cleaned = ' '.join(words)
    return cleaned if cleaned else query


def extract_topic(text: str) -> str:
    """
    Extract main topic/keywords from natural language query.

    Useful for fuzzy matching against knowledge base.
    """
    # Remove question words and common phrases
    question_patterns = [
        r'^how (?:do|can) i\s+',
        r'^how to\s+',
        r'^what is\s+',
        r'^what\'s\s+',
        r'^tell me about\s+',
        r'^explain\s+',
        r'^tips? on\s+',
        r'^help me\s+',
    ]

    text_lower = text.lower()
    for pattern in question_patterns:
        text_lower = re.sub(pattern, '', text_lower)

    # Remove trailing question marks and punctuation
    text_lower = re.sub(r'[?.!]+$', '', text_lower)

    return text_lower.strip()


def is_natural_language(text: str) -> bool:
    """
    Determine if input looks like natural language vs direct command.

    Natural language indicators:
    - Contains question marks
    - Has question words (how, what, why, etc.)
    - Has multiple words (3+)
    - Contains verbs like "do", "can", "should"
    - Starts with command words like "explain", "tip", "help", etc.
    """
    text_lower = text.lower()

    # Explicit question
    if '?' in text:
        return True

    # Question words
    question_words = ['how', 'what', 'why', 'when', 'where', 'who', 'which']
    if any(text_lower.startswith(word + ' ') for word in question_words):
        return True

    # Command words that indicate natural language intent
    command_words = ['explain', 'tip', 'help', 'report', 'quiz', 'plan']
    if any(text_lower.startswith(word + ' ') for word in command_words):
        return True

    # Common natural language patterns
    nl_patterns = [
        r'i (?:found|got|have|see|need|want)',
        r'tips? (?:on|for)',
        r'tell me',
        r'show me',
        r'help me',
        r'can you',
        r'should i',
    ]

    if any(re.search(pattern, text_lower) for pattern in nl_patterns):
        return True

    # Multiple words might indicate natural language (reduced threshold)
    word_count = len(text.split())
    if word_count >= 3:
        return True

    return False


def suggest_command_format(command: str, query: str) -> str:
    """
    Format the suggested command for display to user.

    Returns formatted string like:
    "🤔 I think you mean: explain 'nmap'"
    """
    return f"🤔 I think you mean: {command} '{query}'"


# Convenience function for testing
def demo():
    """Demo the natural language parser."""
    test_queries = [
        "how do I scan for open ports?",
        "what is burp suite?",
        "tips on sql injection",
        "I found an open port 22",
        "what should I do after getting a shell?",
        "document xss vulnerability",
        "test me on buffer overflow",
        "why is my scan not working?",
        "how to learn metasploit",
    ]

    print("Natural Language Parser Demo")
    print("=" * 50)

    for query in test_queries:
        command, extracted = parse_natural_query(query)
        suggestion = suggest_command_format(command, extracted)
        print(f"\nQuery: {query}")
        print(f"  → {suggestion}")


if __name__ == "__main__":
    demo()
