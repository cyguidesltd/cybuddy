"""
AI Provider factory and base class for BYOK integration.

Provides abstraction over OpenAI, Claude, and Gemini APIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class AIProvider(Protocol):
    """Protocol for AI providers."""

    def complete(self, prompt: str, max_tokens: int = 500) -> str:
        """Get completion from AI provider."""
        ...


@dataclass
class OpenAIProvider:
    """OpenAI provider (GPT-4, GPT-3.5)."""

    api_key: str
    model: str = "gpt-4o-mini"
    max_tokens: int = 500

    def complete(self, prompt: str, max_tokens: int | None = None) -> str:
        """Call OpenAI API."""
        try:
            import openai
        except ImportError:
            raise AIProviderError(
                "OpenAI package not installed. Install with: pip install openai"
            )

        client = openai.OpenAI(api_key=self.api_key)
        tokens = max_tokens or self.max_tokens

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise AIProviderError(f"OpenAI API error: {e}")


@dataclass
class ClaudeProvider:
    """Anthropic Claude provider."""

    api_key: str
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 500

    def complete(self, prompt: str, max_tokens: int | None = None) -> str:
        """Call Anthropic Claude API."""
        try:
            import anthropic
        except ImportError:
            raise AIProviderError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )

        client = anthropic.Anthropic(api_key=self.api_key)
        tokens = max_tokens or self.max_tokens

        try:
            message = client.messages.create(
                model=self.model,
                max_tokens=tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            raise AIProviderError(f"Claude API error: {e}")


@dataclass
class GeminiProvider:
    """Google Gemini provider."""

    api_key: str
    model: str = "gemini-1.5-flash"
    max_tokens: int = 500

    def complete(self, prompt: str, max_tokens: int | None = None) -> str:
        """Call Google Gemini API."""
        try:
            import google.generativeai as genai
        except ImportError:
            raise AIProviderError(
                "Google Generative AI package not installed. Install with: pip install google-generativeai"
            )

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        tokens = max_tokens or self.max_tokens

        try:
            # Gemini uses different parameter name
            generation_config = {"max_output_tokens": tokens}
            response = model.generate_content(
                prompt, generation_config=generation_config
            )
            return response.text
        except Exception as e:
            raise AIProviderError(f"Gemini API error: {e}")


class AIProviderError(Exception):
    """Raised when AI provider encounters an error."""

    pass


def get_provider(provider_name: str, api_key: str, config: dict | None = None) -> AIProvider:
    """
    Factory function to get AI provider.

    Args:
        provider_name: "openai", "claude", or "gemini"
        api_key: API key for the provider
        config: Optional config dict with model and max_tokens

    Returns:
        AIProvider instance

    Raises:
        ValueError: If provider_name is unknown
        AIProviderError: If provider package not installed
    """
    config = config or {}
    provider_name = provider_name.lower()

    if provider_name == "openai":
        return OpenAIProvider(
            api_key=api_key,
            model=config.get("model", "gpt-4o-mini"),
            max_tokens=config.get("max_tokens", 500),
        )
    elif provider_name in ("claude", "anthropic"):
        return ClaudeProvider(
            api_key=api_key,
            model=config.get("model", "claude-3-5-sonnet-20241022"),
            max_tokens=config.get("max_tokens", 500),
        )
    elif provider_name == "gemini":
        return GeminiProvider(
            api_key=api_key,
            model=config.get("model", "gemini-1.5-flash"),
            max_tokens=config.get("max_tokens", 500),
        )
    else:
        raise ValueError(
            f"Unknown provider: {provider_name}. "
            f"Supported providers: openai, claude, gemini"
        )
