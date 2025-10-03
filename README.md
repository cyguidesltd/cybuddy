# CyBuddy 🛡️

**Your AI-powered cybersecurity learning companion** — Get instant answers about security tools, attack techniques, and CTF scenarios. No tabs, no confusion, just fast learning.

## Quick Start

```bash
# Install
pip install cybuddy

# Start learning
cybuddy guide --tui
```

That's it. You're ready to learn cybersecurity.

---

## What is CyBuddy?

**The Problem:** Learning cybersecurity means juggling 50+ browser tabs, outdated blog posts, and tool docs that assume you already know everything. You're stuck at 2am during a CTF, Googling "how to enumerate port 8080" and getting overwhelmed.

**The Solution:** CyBuddy gives you instant, focused answers through 7 simple commands. Ask about tools, techniques, or scenarios — get clear explanations with practical next steps. No browser needed.

**Built for:** Students learning cyber security • CTF players • Lab learners (HTB, TryHackMe) • Anyone who needs quick security answers

---

## The 7 Commands

Once you run `cybuddy guide`, you have exactly 7 commands:

| Command | Purpose | Example |
|---------|---------|---------|
| **explain** | Learn what commands/tools do | `explain 'nmap -sV'` |
| **tip** | Quick study guide for topics | `tip 'SQL injection'` |
| **help** | Troubleshoot errors | `help 'connection refused'` |
| **report** | Practice writing security reports | `report 'Found SQLi in login'` |
| **quiz** | Test your knowledge with flashcards | `quiz 'Buffer Overflow'` |
| **plan** | Get unstuck with next steps | `plan 'found port 80 open'` |
| **exit** | Leave the interactive mode | `exit` |

**Why only 7?** Because 7 commands is all you need to learn effectively. More = confusion.

---

## Real-World Usage

### Scenario: Stuck on a Web CTF Challenge

```bash
❯ cybuddy guide --tui

❯ explain 'gobuster dir -u http://target -w wordlist.txt'
─── Explanation ─────────────────────────────────────
  dir: directory brute-forcing mode
  -u: target URL
  -w: wordlist file
  Use when: looking for hidden endpoints
  Watch out: can be noisy, start with small wordlists
─────────────────────────────────────────────────────

❯ tip 'directory brute forcing'
─── Tip ─────────────────────────────────────────────
  Check robots.txt first
  Common dirs: /admin, /api, /backup
  Use small wordlists in CTFs to avoid rate limits
─────────────────────────────────────────────────────

❯ plan 'gobuster found /admin endpoint'
─── Next Steps ──────────────────────────────────────
  1. Try default credentials (admin/admin, admin/password)
  2. Check for authentication bypass
  3. Look for SQLi in login form
─────────────────────────────────────────────────────
```

**Result:** You went from stuck → understanding → action in 3 commands. Zero browser tabs.

---

## Features

✅ **300+ cybersecurity entries** — Tools, techniques, attack scenarios explained simply
✅ **7 focused commands** — Everything you need, nothing you don't
✅ **Beautiful TUI interface** — Clean, readable, distraction-free
✅ **Zero configuration** — Works out of the box, no setup required
✅ **Offline-first** — Built-in knowledge base works without internet
✅ **Safe defaults** — Won't suggest dangerous commands without warnings
✅ **Session tracking** — Review your learning history
✅ **CTF-optimized** — Designed for the flow of challenges

---

## Command Line Usage (Outside Interactive Mode)

Use CyBuddy commands directly from your terminal:

```bash
# Tool explanations
cybuddy explain "nmap -sV"

# Study tips
cybuddy tip "SQL injection"

# Troubleshooting
cybuddy help "connection refused"

# Report writing practice
cybuddy report "Found XSS in login form"

# Test knowledge
cybuddy quiz "Buffer overflow"

# Next steps guidance
cybuddy plan "found port 80 open"

# Checklists for common tasks
cybuddy checklist web
cybuddy checklist recon
cybuddy checklist crypto
cybuddy checklist forensics
```

---

## Optional: AI Mode (Advanced)

Want deeper, context-aware answers? Enable AI with your own API key:

```bash
# Set your API key (OpenAI, Claude, or Gemini)
export CYBUDDY_API_KEY="sk-..."

# Use --send flag for AI responses
cybuddy explain "nmap -A target" --send
```

**Default mode:** Built-in knowledge base (no API needed)
**AI mode:** Enhanced explanations using your API key (BYOK — Bring Your Own Key)

Create `~/.config/cybuddy/config.yaml` for persistent AI settings:

```yaml
ai:
  enabled: true
  provider: openai  # or 'anthropic' or 'google'
  api_key: sk-...
  model: gpt-4o-mini
```

---

## Configuration (Optional)

CyBuddy works perfectly with **zero configuration**. For advanced customization:

```yaml
# ~/.config/cybuddy/config.yaml
tui:
  theme: default  # 'dark', 'light', 'default'
  show_tips: true

cli:
  color: true
  verbose: false

ai:
  enabled: false  # Set to true for AI mode
  provider: openai
  redact: true
  max_tokens: 300
```

---

## FAQ

**Q: Is this better than using real security tools?**
A: No. CyBuddy is a *learning tool* to help you understand and use real tools effectively.

**Q: Does it replace Google/Stack Overflow?**
A: For quick hints and common tasks, yes. For deep technical dives, no.

**Q: Can I use this during exams/CTFs?**
A: Check your specific rules. Built-in knowledge base is usually OK. AI mode may have restrictions.

**Q: Is my data sent anywhere?**
A: Only if you enable AI mode with `--send`. Otherwise, everything is local.

**Q: What's the difference between TUI and CLI mode?**
A: TUI mode (`--tui`) provides a rich interactive interface. CLI mode (`--cli`) is simple text for any terminal.

**Q: Why is it called CyBuddy?**
A: It's your cybersecurity buddy — always ready to help you learn, no judgment, no confusion.

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Built by learners, for learners.** Someone who remembers being stuck at 2am during a CTF wanted to make learning easier.

---

## License

MIT License - see LICENSE file for details.

---

**Start learning now:**
```bash
pip install cybuddy
cybuddy guide --tui
```
