"""Tests for natural language parser."""
import pytest
from cybuddy.nl_parser import (
    parse_natural_query,
    is_natural_language,
    extract_topic,
    suggest_command_format,
)


class TestParseNaturalQuery:
    """Test natural language query parsing."""

    def test_how_do_i_pattern(self):
        """Test 'how do I...' pattern."""
        cmd, query = parse_natural_query("how do I scan for open ports?")
        assert cmd == "explain"
        assert "scan" in query.lower()

    def test_what_is_pattern(self):
        """Test 'what is...' pattern."""
        cmd, query = parse_natural_query("what is burp suite?")
        assert cmd == "explain"
        assert "burp suite" in query.lower()

    def test_tips_on_pattern(self):
        """Test 'tips on...' pattern."""
        cmd, query = parse_natural_query("tips on sql injection")
        assert cmd == "tip"
        assert "sql injection" in query.lower()

    def test_plan_pattern_found(self):
        """Test 'I found...' pattern maps to plan."""
        cmd, query = parse_natural_query("I found an open port 22")
        assert cmd == "plan"
        assert "22" in query

    def test_plan_pattern_what_should(self):
        """Test 'what should I do...' pattern."""
        cmd, query = parse_natural_query("what should I do after getting a shell?")
        assert cmd == "plan"
        assert "shell" in query.lower()

    def test_report_pattern(self):
        """Test report patterns."""
        cmd, query = parse_natural_query("document xss vulnerability")
        assert cmd == "report"
        assert "xss" in query.lower()

    def test_quiz_pattern(self):
        """Test quiz patterns."""
        cmd, query = parse_natural_query("test me on buffer overflow")
        assert cmd == "quiz"
        assert "buffer overflow" in query.lower()

    def test_assist_pattern(self):
        """Test assist/help patterns."""
        cmd, query = parse_natural_query("why is my scan not working?")
        assert cmd == "assist"
        assert "scan" in query.lower()

    def test_tool_keyword_fallback(self):
        """Test tool keyword detection fallback."""
        cmd, query = parse_natural_query("nmap syntax")
        assert cmd == "explain"
        assert "nmap" in query.lower()

    def test_attack_keyword_fallback(self):
        """Test attack technique keyword fallback."""
        cmd, query = parse_natural_query("xss bypass techniques")
        assert cmd == "tip"
        assert "xss" in query.lower()

    def test_scenario_keyword_fallback(self):
        """Test scenario keyword fallback."""
        cmd, query = parse_natural_query("found vulnerability in target")
        assert cmd == "plan"
        assert "vulnerability" in query.lower()

    def test_default_fallback(self):
        """Test default fallback to explain."""
        cmd, query = parse_natural_query("some random query")
        assert cmd == "explain"
        assert query == "some random query"


class TestIsNaturalLanguage:
    """Test natural language detection."""

    def test_question_mark_indicator(self):
        """Question marks indicate natural language."""
        assert is_natural_language("what is nmap?")

    def test_question_words(self):
        """Question words indicate natural language."""
        assert is_natural_language("how do I scan ports")
        assert is_natural_language("what should I do next")
        assert is_natural_language("why is this failing")

    def test_natural_patterns(self):
        """Common natural language patterns."""
        assert is_natural_language("I found an open port")
        assert is_natural_language("tips on sql injection")
        assert is_natural_language("tell me about metasploit")

    def test_multiple_words(self):
        """Multiple words (4+) suggest natural language."""
        assert is_natural_language("scan for open ports now")

    def test_short_direct_command(self):
        """Short direct commands are not natural language."""
        assert not is_natural_language("nmap -sV")
        assert not is_natural_language("help")


class TestExtractTopic:
    """Test topic extraction."""

    def test_removes_question_words(self):
        """Remove question words from topic."""
        topic = extract_topic("how do I scan ports?")
        assert "how" not in topic.lower()
        assert "scan" in topic.lower()

    def test_removes_punctuation(self):
        """Remove trailing punctuation."""
        topic = extract_topic("what is burp suite?")
        assert "?" not in topic
        assert "burp suite" in topic.lower()

    def test_handles_simple_query(self):
        """Handle simple queries."""
        topic = extract_topic("nmap")
        assert topic == "nmap"


class TestSuggestCommandFormat:
    """Test command suggestion formatting."""

    def test_formats_correctly(self):
        """Test suggestion formatting."""
        suggestion = suggest_command_format("explain", "nmap")
        assert "explain" in suggestion
        assert "nmap" in suggestion
        assert "🤔" in suggestion


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_string(self):
        """Handle empty string."""
        cmd, query = parse_natural_query("")
        assert cmd == "explain"
        assert query == ""

    def test_whitespace_only(self):
        """Handle whitespace-only input."""
        cmd, query = parse_natural_query("   ")
        assert cmd == "explain"

    def test_very_long_query(self):
        """Handle very long queries."""
        long_query = "how do I " + "test " * 100 + "this application"
        cmd, query = parse_natural_query(long_query)
        assert cmd == "explain"
        assert len(query) > 0

    def test_special_characters(self):
        """Handle special characters."""
        cmd, query = parse_natural_query("what is SQL's role?")
        assert cmd == "explain"
        assert "sql" in query.lower()

    def test_mixed_case(self):
        """Handle mixed case input."""
        cmd, query = parse_natural_query("How Do I Scan PORTS?")
        assert cmd == "explain"
        assert "scan" in query.lower()


class TestRealWorldExamples:
    """Test real-world example queries."""

    @pytest.mark.parametrize("query,expected_cmd", [
        ("how do I test for SQL injection?", "explain"),
        ("what should I do after getting shell access?", "plan"),
        ("tips on privilege escalation", "tip"),
        ("I'm getting connection refused error", "assist"),
        ("document the XSS finding", "report"),
        ("quiz me on cryptography", "quiz"),
        ("what is the best way to learn nmap?", "explain"),
        ("help me plan a penetration test", "plan"),
    ])
    def test_real_world_queries(self, query, expected_cmd):
        """Test realistic user queries."""
        cmd, extracted = parse_natural_query(query)
        assert cmd == expected_cmd
        assert len(extracted) > 0
