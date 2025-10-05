"""
Natural Language Query Parser for CyBuddy.

Converts natural language queries into structured commands:
- "how do I scan ports?" → ("explain", "nmap")
- "tips on sql injection" → ("tip", "sql injection")
- "what should I do after getting a shell?" → ("plan", "got shell")
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Dict, List, Tuple, Pattern


class NLParser:
    """Optimized Natural Language Parser with compiled patterns and caching."""
    
    def __init__(self):
        # Compile regex patterns once for better performance
        self._compiled_patterns = self._compile_patterns()
        self._keyword_sets = self._build_keyword_sets()
    
    def _compile_patterns(self) -> Dict[str, List[Pattern[str]]]:
        """Compile all regex patterns once for better performance."""
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
        
        return {
            command: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for command, patterns in intents.items()
        }
    
    def _build_keyword_sets(self) -> Dict[str, set]:
        """Build keyword sets for faster lookup."""
        return {
            'tools': {
                'nmap', 'burp', 'sqlmap', 'metasploit', 'wireshark',
                'hydra', 'john', 'hashcat', 'gobuster', 'ffuf',
                'nikto', 'dirb', 'wfuzz', 'netcat', 'nc', 'ssh',
                'tcpdump', 'masscan', 'enum4linux', 'smbclient'
            },
            'attacks': {
                'xss', 'sqli', 'sql injection', 'csrf', 'ssrf', 'xxe',
                'rce', 'lfi', 'rfi', 'ssti', 'deserialization',
                'privilege escalation', 'privesc', 'buffer overflow',
                'format string', 'race condition', 'injection'
            },
            'scenarios': {
                'found', 'got', 'have', 'discovered', 'see', 'seeing',
                'stuck', 'after', 'next', 'shell', 'port', 'vulnerability',
                'target', 'enumeration', 'foothold'
            }
        }
    
    def parse(self, text: str) -> Tuple[str, str]:
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
        if not text or not text.strip():
            return 'explain', ''
        
        text_lower = text.lower().strip()
        
        # Check for direct command usage first (but only if it's a standalone command)
        # This prevents "help me plan" from being treated as "help" command
        direct_commands = ['explain', 'tip', 'report', 'quiz', 'plan']
        for cmd in direct_commands:
            if text_lower == cmd or text_lower.startswith(cmd + ' '):
                query = text[len(cmd):].strip()
                return cmd, query

        # Intent detection patterns (order matters - more specific first)
        for command, patterns in self._compiled_patterns.items():
            for pattern in patterns:
                match = pattern.match(text_lower)
                if match:
                    query = match.group(1).strip()
                    # Clean up common filler words
                    query = self._clean_query(query)
                    return command, query

        # Keyword detection fallback
        return self._keyword_fallback(text_lower, text)
    
    def _keyword_fallback(self, text_lower: str, original_text: str) -> Tuple[str, str]:
        """Fallback to keyword-based detection."""
        # Check for tool keywords first (most specific)
        if any(tool in text_lower for tool in self._keyword_sets['tools']):
            return 'explain', original_text
        
        # Check for attack technique keywords
        if any(keyword in text_lower for keyword in self._keyword_sets['attacks']):
            return 'tip', original_text
        
        # Check for scenario keywords
        if any(keyword in text_lower for keyword in self._keyword_sets['scenarios']):
            return 'plan', original_text
        
        # Default: treat as "explain" query
        return 'explain', original_text
    
    @staticmethod
    def _clean_query(query: str) -> str:
        """Remove filler words and clean up the extracted query."""
        if not query:
            return query
            
        # Remove leading articles and common filler words
        stopwords = {
            'the', 'a', 'an', 'to', 'for', 'with', 'about', 'on',
            'in', 'at', 'by', 'from', 'of', 'and', 'or'
        }

        words = query.split()
        # Remove stopwords from the beginning only
        while words and words[0].lower() in stopwords:
            words.pop(0)

        cleaned = ' '.join(words)
        return cleaned if cleaned else query


# Global parser instance for performance
_parser = NLParser()


def parse_natural_query(text: str) -> Tuple[str, str]:
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
    return _parser.parse(text)


# Legacy function for backward compatibility
def _clean_query(query: str) -> str:
    """Remove filler words and clean up the extracted query."""
    return NLParser._clean_query(query)


@lru_cache(maxsize=128)
def extract_topic(text: str) -> str:
    """
    Extract main topic/keywords from natural language query.

    Useful for fuzzy matching against knowledge base.
    """
    if not text or not text.strip():
        return ''
    
    # Compile patterns once for better performance
    question_patterns = [
        re.compile(r'^how (?:do|can) i\s+', re.IGNORECASE),
        re.compile(r'^how to\s+', re.IGNORECASE),
        re.compile(r'^what is\s+', re.IGNORECASE),
        re.compile(r'^what\'s\s+', re.IGNORECASE),
        re.compile(r'^tell me about\s+', re.IGNORECASE),
        re.compile(r'^explain\s+', re.IGNORECASE),
        re.compile(r'^tips? on\s+', re.IGNORECASE),
        re.compile(r'^help me\s+', re.IGNORECASE),
    ]

    text_lower = text.lower()
    for pattern in question_patterns:
        text_lower = pattern.sub('', text_lower)

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
    if not text or not text.strip():
        return False
        
    text_lower = text.lower()
    words = text_lower.split()
    
    # Single word commands are typically not natural language
    if len(words) == 1:
        # Only consider single words as natural language if they're question words
        question_words = {'how', 'what', 'why', 'when', 'where', 'who', 'which'}
        return words[0] in question_words

    # Explicit question
    if '?' in text:
        return True

    # Question words
    question_words = {'how', 'what', 'why', 'when', 'where', 'who', 'which'}
    first_word = words[0] if words else ''
    if first_word in question_words:
        return True

    # Command words that indicate natural language intent (but only if followed by content)
    command_words = {'explain', 'tip', 'help', 'report', 'quiz', 'plan'}
    if first_word in command_words and len(words) > 1:
        return True

    # Common natural language patterns (compiled for performance)
    nl_patterns = [
        re.compile(r'i (?:found|got|have|see|need|want)', re.IGNORECASE),
        re.compile(r'tips? (?:on|for)', re.IGNORECASE),
        re.compile(r'tell me', re.IGNORECASE),
        re.compile(r'show me', re.IGNORECASE),
        re.compile(r'help me', re.IGNORECASE),
        re.compile(r'can you', re.IGNORECASE),
        re.compile(r'should i', re.IGNORECASE),
    ]

    if any(pattern.search(text_lower) for pattern in nl_patterns):
        return True

    # Multiple words might indicate natural language (reduced threshold)
    word_count = len(words)
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
