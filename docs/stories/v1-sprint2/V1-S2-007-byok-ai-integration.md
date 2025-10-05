# AI Integration (BYOK - Bring Your Own Key)

**ID:** V1-S2-007
**Epic:** AI Integration
**Priority:** P0 (Core differentiator)
**Size:** M (2 hours)
**Sprint:** V1 Sprint 2 - Day 2
**Status:** ✅ COMPLETED

## Implementation Summary
- **Commit:** `7699cce feat: add BYOK AI provider integration`
- **Files Created:**
  - `src/cybuddy/ai/provider.py` - AI provider factory (165 lines)
  - `src/cybuddy/ai/prompts.py` - Prompt templates (219 lines)
  - `src/cybuddy/ai/__init__.py` - Module exports
  - Updated `src/cybuddy/config.py` - AI config with env var support
- **Providers:** OpenAI, Claude (Anthropic), Gemini
- **Result:** BYOK AI integration ready, awaiting CLI/TUI integration

## User Story
As a user who wants better answers,
I want to use my own OpenAI/Claude/Gemini API key,
So that I can get AI-powered responses without paying subscription.

## Background: V1 vs V2 Model

### V1 (This Story): BYOK - User Provides API Key
- User brings own API key
- User pays AI provider directly
- Flexible, no vendor lock-in
- No subscription required

### V2 (Future): SaaS - You Provide Backend
- User logs in with OAuth
- You provide AI backend
- $9-19/month subscription
- No user API key needed

## Acceptance Criteria
- [ ] Support 3 AI providers:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic Claude (Claude 3.5 Sonnet, etc.)
  - Google Gemini (Gemini 1.5 Flash/Pro)
- [ ] Config file: `~/.cybuddy/config.toml`
- [ ] Environment variable support: `CYBUDDY_API_KEY`, `CYBUDDY_PROVIDER`
- [ ] Auto-fallback to mockup if:
  - API key not configured
  - API call fails
  - Network error
- [ ] Two modes:
  - Manual: Require `--send` flag
  - Auto: `auto_send = true` in config
- [ ] Show mode indicator:
  - `[Mockup]` - Free local response
  - `[AI-GPT4]` - OpenAI response
  - `[AI-Claude]` - Anthropic response
  - `[AI-Gemini]` - Google response
- [ ] Clear setup instructions in README
- [ ] Works with all 7 commands (explain, tip, help, report, quiz, plan)

## Technical Notes

### Config File Structure
```toml
# ~/.cybuddy/config.toml

[ai]
enabled = true              # Enable AI integration
provider = "openai"         # or "claude" or "gemini"
auto_send = false          # false = require --send flag, true = always use AI

[openai]
api_key = "sk-..."
model = "gpt-4o-mini"      # or "gpt-4", "gpt-3.5-turbo"
max_tokens = 500

[claude]
api_key = "sk-ant-..."
model = "claude-3-5-sonnet-20241022"
max_tokens = 500

[gemini]
api_key = "..."
model = "gemini-1.5-flash"  # or "gemini-1.5-pro"
max_tokens = 500
```

### Environment Variables
```bash
# Quick setup without config file
export CYBUDDY_API_KEY="sk-..."
export CYBUDDY_PROVIDER="openai"  # or "claude" or "gemini"
```

### Implementation

#### AI Provider Factory
```python
# src/secbuddy/ai/provider.py
from typing import Protocol
from dataclasses import dataclass

class AIProvider(Protocol):
    """Protocol for AI providers."""
    def complete(self, prompt: str) -> str:
        """Get completion from AI."""
        ...

@dataclass
class OpenAIProvider:
    api_key: str
    model: str = "gpt-4o-mini"
    max_tokens: int = 500

    def complete(self, prompt: str) -> str:
        """Call OpenAI API."""
        import openai
        openai.api_key = self.api_key

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise AIProviderError(f"OpenAI API error: {e}")

@dataclass
class ClaudeProvider:
    api_key: str
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 500

    def complete(self, prompt: str) -> str:
        """Call Anthropic Claude API."""
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)

        try:
            message = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            raise AIProviderError(f"Claude API error: {e}")

@dataclass
class GeminiProvider:
    api_key: str
    model: str = "gemini-1.5-flash"
    max_tokens: int = 500

    def complete(self, prompt: str) -> str:
        """Call Google Gemini API."""
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise AIProviderError(f"Gemini API error: {e}")


def get_provider(config: dict) -> AIProvider:
    """Factory function to get AI provider."""
    provider_name = config['ai']['provider']

    if provider_name == 'openai':
        return OpenAIProvider(
            api_key=config['openai']['api_key'],
            model=config['openai'].get('model', 'gpt-4o-mini'),
            max_tokens=config['openai'].get('max_tokens', 500)
        )
    elif provider_name == 'claude':
        return ClaudeProvider(
            api_key=config['claude']['api_key'],
            model=config['claude'].get('model', 'claude-3-5-sonnet-20241022'),
            max_tokens=config['claude'].get('max_tokens', 500)
        )
    elif provider_name == 'gemini':
        return GeminiProvider(
            api_key=config['gemini']['api_key'],
            model=config['gemini'].get('model', 'gemini-1.5-flash'),
            max_tokens=config['gemini'].get('max_tokens', 500)
        )
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
```

#### Config Loader
```python
# src/secbuddy/config.py
from pathlib import Path
import os
import tomli  # or toml

def load_config() -> dict:
    """Load config from file or environment variables."""
    config = {
        'ai': {
            'enabled': False,
            'provider': 'openai',
            'auto_send': False
        }
    }

    # Try config file
    config_path = Path.home() / '.cybuddy' / 'config.toml'
    if config_path.exists():
        with open(config_path, 'rb') as f:
            user_config = tomli.load(f)
            config.update(user_config)

    # Override with environment variables
    if os.getenv('CYBUDDY_API_KEY'):
        provider = os.getenv('CYBUDDY_PROVIDER', 'openai')
        config['ai']['enabled'] = True
        config['ai']['provider'] = provider
        config[provider]['api_key'] = os.getenv('CYBUDDY_API_KEY')

    return config
```

#### Integration with Commands
```python
# src/secbuddy/cli.py

def explain_command(query: str, send: bool = False) -> str:
    """Explain command with optional AI."""
    config = load_config()

    # Check if should use AI
    use_ai = send or (config['ai']['enabled'] and config['ai']['auto_send'])

    if use_ai:
        try:
            provider = get_provider(config)
            prompt = f"Explain this security tool/concept for a beginner: {query}"
            response = provider.complete(prompt)

            # Add mode indicator
            provider_name = config['ai']['provider'].upper()
            return f"[AI-{provider_name}] {response}"
        except Exception as e:
            # Fallback to mockup
            print(f"⚠️ AI error: {e}. Falling back to mockup.")

    # Use mockup
    result = explain_fn(query)
    return f"[Mockup] {result}"
```

## Usage Examples

### Mockup Mode (Default - Free)
```bash
$ cybuddy explain "nmap"

[Mockup] Network Mapper - powerful port scanner and service detection tool

Common flags:
  -sV: Version detection
  -Pn: Skip ping
  -A: Aggressive scan
```

### AI Mode with --send Flag
```bash
$ cybuddy explain "nmap" --send

[AI-GPT4] Nmap (Network Mapper) is a sophisticated open-source network
discovery and security auditing tool. It's widely used by security professionals
for network inventory, managing service upgrade schedules, and monitoring host
or service uptime.

Key features:
• Port scanning: Identifies open ports and services
• OS detection: Determines operating system and version
• Version detection: Identifies service versions
• Scripting engine: NSE (Nmap Scripting Engine) for advanced tasks

Best practices:
- Always get authorization before scanning networks
- Start with basic scans (-sV) before aggressive scans (-A)
- Use timing templates (-T0 to -T5) to control scan speed
```

### Auto-Send Mode
```toml
# config.toml with auto_send = true
[ai]
enabled = true
provider = "claude"
auto_send = true
```

```bash
$ cybuddy tip "sql injection"

[AI-Claude] SQL injection is a critical web security vulnerability...
```

### Environment Variable Setup
```bash
# Quick setup
export CYBUDDY_API_KEY="sk-..."
export CYBUDDY_PROVIDER="openai"

$ cybuddy plan "got shell" --send
[AI-GPT4] After obtaining a shell, here's your priority checklist...
```

## File Changes
- `src/secbuddy/ai/` - New directory
  - `provider.py` - AI provider factory
  - `prompts.py` - Prompt templates
- `src/secbuddy/config.py` - Add AI config loading
- `src/secbuddy/cli.py` - Add --send flag, AI integration
- `requirements.txt` - Add openai, anthropic, google-generativeai
- `docs/AI_SETUP.md` - Setup guide

## Dependencies
```txt
# requirements-ai.txt (optional dependencies)
openai>=1.0.0
anthropic>=0.8.0
google-generativeai>=0.3.0
tomli>=2.0.0  # for config parsing
```

## Definition of Done
- [ ] 3 AI providers implemented (OpenAI, Claude, Gemini)
- [ ] Config file support
- [ ] Environment variable support
- [ ] --send flag works
- [ ] auto_send config works
- [ ] Mode indicators show correctly
- [ ] Fallback to mockup on errors
- [ ] Works with all 7 commands
- [ ] README updated with BYOK instructions
- [ ] AI_SETUP.md guide created
- [ ] Git commit: "feat: add BYOK AI integration"

## Testing Checklist
- [ ] OpenAI provider works
- [ ] Claude provider works
- [ ] Gemini provider works
- [ ] Config file loading works
- [ ] Environment variables work
- [ ] --send flag works
- [ ] auto_send config works
- [ ] Fallback to mockup on API error
- [ ] Mode indicators correct
- [ ] Works without API key (mockup only)

## Documentation

### README Section
```markdown
## AI Integration (Optional)

CyBuddy works offline with built-in mockup responses.
For deeper insights, bring your own API key (BYOK):

### Quick Setup
```bash
export CYBUDDY_API_KEY="sk-..."
export CYBUDDY_PROVIDER="openai"  # or "claude" or "gemini"
cybuddy explain "nmap" --send
```

### Config File Setup
Create `~/.cybuddy/config.toml`:
```toml
[ai]
enabled = true
provider = "openai"
auto_send = false  # require --send flag

[openai]
api_key = "sk-..."
model = "gpt-4o-mini"
```

### Supported Providers
- **OpenAI**: GPT-4, GPT-3.5 (api.openai.com)
- **Claude**: Claude 3.5 Sonnet (anthropic.com)
- **Gemini**: Gemini 1.5 (ai.google.dev)

### Cost Control
- Manual mode (default): Use --send flag per query
- Auto mode: Set auto_send = true in config
- Mockup fallback: Free, instant, offline
```

## Time Estimate Breakdown
- AI provider implementation: 45 mins
- Config loading: 30 mins
- CLI/TUI integration: 30 mins
- Documentation: 15 mins

**Total: 2 hours**
