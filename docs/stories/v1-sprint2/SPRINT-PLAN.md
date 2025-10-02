# V1 Sprint 2 - Day 2: UX Improvements

**Duration:** 8-10 hours (Day 2)
**Goal:** Enhance user experience with smart features and polish
**Team Capacity:** 1 developer

## Sprint Goals
- Implement auto-detect TUI/CLI mode
- Remove config file requirement
- Add syntax highlighting in TUI
- Implement smart error messages
- Add command history
- Add natural language chat parser
- Add BYOK AI integration (OpenAI/Claude/Gemini)

## Story Summary
| ID | Story | Size | Priority | Status | Commit |
|----|-------|------|----------|--------|--------|
| V1-S2-001 | Auto-detect TUI/CLI Mode | M | P0 | ✅ DONE | `09d6d19` |
| V1-S2-002 | Remove Config Requirement | M | P0 | ✅ DONE | `aabc0e4` |
| V1-S2-003 | Syntax Highlighting | S | P1 | ✅ DONE | `d5ac80f` |
| V1-S2-004 | Smart Error Messages | S | P1 | ✅ DONE | `73e5c02` |
| V1-S2-006 | Natural Language Chat | M | P0 | ✅ DONE | `a3f90f1` |
| V1-S2-007 | BYOK AI Integration | M | P0 | ✅ DONE | `7699cce` |
| V1-S2-005 | Command History | S | P2 | ⏭️ DEFERRED | Sprint 3 |

**Progress:** 6/7 stories complete (86%)**
**Deferred:** V1-S2-005 (Command History) moved to Sprint 3 - P2 priority, not critical for v1.0 release

## Sprint Schedule

### Morning (4 hours)
- 08:00-10:00: V1-S2-001 (Auto-detect mode)
- 10:00-12:00: V1-S2-002 (Remove config)

### Afternoon (4 hours)
- 13:00-14:30: V1-S2-003 (Syntax highlighting)
- 14:30-16:00: V1-S2-004 (Smart errors)
- 16:00-17:00: V1-S2-006 (Natural language)
- 17:00-18:00: V1-S2-007 (BYOK AI)
- Buffer: V1-S2-005 (Command history) if time remains

### Buffer
- 17:30-18:00: Testing across platforms

## Success Criteria
- [x] Zero-config installation works (V1-S2-002 ✅)
- [x] TUI auto-launches on supported terminals (V1-S2-001 ✅)
- [x] CLI fallback works on all platforms (V1-S2-001 ✅)
- [x] Error messages are helpful and actionable (V1-S2-004 ✅)
- [x] Natural language works for 80%+ queries (V1-S2-006 ✅)
- [x] BYOK AI works with OpenAI/Claude/Gemini (V1-S2-007 ✅)
- [ ] Command history persists across sessions (V1-S2-005 ⏭️ Deferred to Sprint 3)

## Dependencies
- ✅ Sprint 1 complete (100+ entries added)
- ✅ Terminal capability detection library (auto-detect mode)
- ⏳ Create `src/secbuddy/nl_parser.py` for NL parsing
- ⏳ Create `src/secbuddy/ai/provider.py` for BYOK AI
- ⏳ Create `src/secbuddy/cli.py` for CLI entry point
- ⏳ Create `src/secbuddy/tui.py` for TUI mode
- ⏳ Create `src/secbuddy/engine.py` for query processing

## Completed Work (4/7 Stories)

### ✅ V1-S2-001: Auto-detect TUI/CLI Mode
- **Commit:** `09d6d19 feat: auto-detect TUI/CLI mode`
- **Files:** Mode detection logic implemented
- **Result:** Automatic mode selection based on terminal capabilities

### ✅ V1-S2-002: Remove Config Requirement
- **Commit:** `aabc0e4 feat: make config optional with sensible defaults`
- **Files:** Configuration system with defaults
- **Result:** Zero-config installation works

### ✅ V1-S2-003: Syntax Highlighting
- **Commit:** `d5ac80f feat: add syntax highlighting for code blocks`
- **Files:** 4 files modified (cli.py, tui.py, tui/app.py, formatters.py)
- **Result:** Rich library integration with smart language detection

### ✅ V1-S2-004: Smart Error Messages
- **Commit:** `73e5c02 feat: smart error messages with suggestions`
- **Files:** `errors.py`, `suggestions.py` created
- **Result:** Helpful error messages with fuzzy matching suggestions

## Remaining Work (3/7 Stories)

### ⏳ V1-S2-006: Natural Language Chat (P0 - NEXT)
- **Priority:** Critical - core differentiator
- **Files to Create:**
  - `src/secbuddy/nl_parser.py` - Natural language parser
  - `src/secbuddy/engine.py` - Query processing engine
  - `src/secbuddy/cli.py` - CLI entry point
  - `src/secbuddy/tui.py` - TUI mode
  - `tests/test_nl_parser.py` - Unit tests
- **Acceptance:** Parse queries like "how do I scan ports?" → explain "nmap"

### ⏳ V1-S2-007: BYOK AI Integration (P0 - CRITICAL)
- **Priority:** Critical - enables AI features without subscription
- **Files to Create:**
  - `src/secbuddy/config.py` - Config management
  - `src/secbuddy/ai/provider.py` - AI provider factory
  - `src/secbuddy/ai/openai.py` - OpenAI integration
  - `src/secbuddy/ai/anthropic.py` - Claude integration
  - `src/secbuddy/ai/gemini.py` - Gemini integration
  - `src/secbuddy/ai/prompts.py` - Prompt templates
  - `tests/test_ai_provider.py` - AI tests
- **Acceptance:** Works with OpenAI/Claude/Gemini using --send flag

### 📋 V1-S2-005: Command History (P2 - OPTIONAL)
- **Priority:** Enhancement - nice to have
- **Files to Create:**
  - `src/secbuddy/history.py` - History manager
  - Update TUI/CLI for navigation
  - `tests/test_history.py` - History tests
- **Acceptance:** Persistent history with up/down navigation

## Risks & Mitigation
- **Risk:** Terminal detection edge cases
  - **Mitigation:** Graceful fallback to CLI mode
- **Risk:** Platform-specific issues
  - **Mitigation:** Test on Linux, macOS, Windows
