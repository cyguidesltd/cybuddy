# Configuration

SecBuddy reads `~/.secbuddy/config.toml` if present. Keys:

- history.enabled = true|false
- history.path = "~/.secbuddy/history.jsonl"
- todo.path = "~/.secbuddy/todo.json"
- output.truncate_lines = 60
- approvals.require_exec = true

Print resolved config:

- secbuddy config

