# Remove Config File Requirement

**ID:** V1-S2-002
**Epic:** UX Improvements
**Priority:** P0
**Size:** M (2 hours)
**Sprint:** V1 Sprint 2 - Day 2
**Status:** Done

## User Story
As a new user,
I want CyBuddy to work immediately after installation,
So that I don't need to create configuration files.

## Acceptance Criteria
- [ ] CyBuddy works without any config file
- [ ] Use sensible defaults for all settings
- [ ] Optional config file for advanced users
- [ ] Config file location: `~/.config/cybuddy/config.yaml`
- [ ] Auto-migrate existing config if found
- [ ] No errors if config doesn't exist
- [ ] Document optional config in README

## Current Config (to remove requirement)
```yaml
# Current config.yaml (make optional)
tui:
  theme: default
  show_tips: true

cli:
  color: true
  verbose: false

data:
  mock_mode: true
  api_url: null
```

## New Default Behavior
```python
# Default settings (no config needed)
DEFAULT_CONFIG = {
    'tui': {
        'theme': 'default',
        'show_tips': True,
        'history_file': '~/.local/share/cybuddy/history'
    },
    'cli': {
        'color': True,
        'verbose': False
    },
    'data': {
        'mock_mode': True,  # v1.0 is always mock
        'api_url': None
    }
}

def load_config():
    """Load config with fallback to defaults"""
    config = DEFAULT_CONFIG.copy()

    config_path = Path.home() / '.config' / 'cybuddy' / 'config.yaml'
    if config_path.exists():
        with open(config_path) as f:
            user_config = yaml.safe_load(f)
            # Merge user config with defaults
            deep_merge(config, user_config)

    return config
```

## Technical Notes

### File Changes
- `src/secbuddy/config.py` - Add default config
- `src/secbuddy/main.py` - Load config with defaults
- Remove config requirement from setup
- Update README with optional config

### Migration Path
```python
def migrate_old_config():
    """Migrate config from old location if exists"""
    old_path = Path.home() / '.cybuddy' / 'config.yaml'
    new_path = Path.home() / '.config' / 'cybuddy' / 'config.yaml'

    if old_path.exists() and not new_path.exists():
        new_path.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy(old_path, new_path)
        print(f"Migrated config from {old_path} to {new_path}")
```

### Optional Config Documentation
```markdown
## Optional Configuration

CyBuddy works out of the box with no configuration needed.

For advanced users, create `~/.config/cybuddy/config.yaml`:

```yaml
tui:
  theme: default  # or 'dark', 'light'
  show_tips: true

cli:
  color: true
  verbose: false
```

## Definition of Done
- [x] Config is optional, not required
- [x] Defaults work for 99% of users
- [x] Config file migration works
- [x] No errors without config
- [x] README documents optional config
- [x] Test: Fresh install without config works
- [x] Git commit: "feat: make config optional with sensible defaults"

## Testing Checklist
- [x] Fresh install (no config) works
- [x] Existing config still works
- [x] Config migration works
- [x] All commands work without config
- [x] TUI works without config
- [x] CLI works without config

## Time Estimate Breakdown
- Implement default config: 30 mins
- Migration logic: 30 mins
- Update documentation: 30 mins
- Testing: 30 mins

**Total: 2 hours**

## Dev Agent Record

### Agent Model Used
Claude Sonnet 4 (via Cursor)

### Debug Log References
- New config system implemented in `src/cybuddy/config.py`
- CLI integration updated in `src/cybuddy/cli.py`
- README documentation updated with optional config section
- Migration tested with old TOML config files

### Completion Notes List
- ✅ Created new config module with sensible defaults
- ✅ Implemented YAML-based configuration system
- ✅ Added migration logic for existing TOML configs
- ✅ Updated CLI to use new config system with backward compatibility
- ✅ Updated README with clear documentation for optional config
- ✅ Tested fresh install without any config files
- ✅ Tested migration from old config format
- ✅ All functionality works with defaults

### File List
- **Added**: `src/cybuddy/config.py` - New configuration management system
- **Modified**: `src/cybuddy/cli.py` - Updated to use new config system
- **Modified**: `README.md` - Updated documentation for optional config
- **Modified**: `docs/stories/v1-sprint2/V1-S2-002-remove-config.md` - Updated completion status

### Change Log
- **2025-01-12**: Implemented optional configuration system
  - Created new config module with YAML support
  - Added migration logic for existing TOML configs
  - Updated CLI integration with backward compatibility
  - Updated documentation to reflect optional config
  - All acceptance criteria met and tested
