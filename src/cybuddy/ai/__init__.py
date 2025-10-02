"""
BYOK (Bring Your Own Key) AI integration for CyBuddy.

Supports:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude (Claude 3.5 Sonnet, etc.)
- Google Gemini (Gemini 1.5 Flash/Pro)
"""

from .provider import AIProvider, get_provider

__all__ = ["get_provider", "AIProvider"]
