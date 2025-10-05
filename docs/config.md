# Configuration

SecBuddy reads `~/.secbuddy/config.toml` if present. Keys:

- history.enabled = true|false
- history.path = "~/.secbuddy/history.jsonl"
- todo.path = "~/.secbuddy/todo.json"
- output.truncate_lines = 60
- approvals.require_exec = true
- approvals.ai_consent = false
- ai.enabled = false
- ai.provider = "openai"  # or "claude", "gemini", "custom"
- ai.redact = true
- ai.max_tokens = 300
- history.verbatim = false

Print resolved config:

- secbuddy config
