# CyBuddy 🛡️

Your friendly cybersecurity learning companion. Built for students, CTF players, and anyone learning offensive security.

## What is CyBuddy?

Think of it as a helpful mentor who's always available when you're stuck during a CTF, lab, or pentest exercise. Instead of Googling "how does nmap work" for the 10th time, just ask CyBuddy.

## Quick Start

```bash
# Manual install
python -m venv .venv
source .venv/bin/activate
pip install -e .
cybuddy guide --tui
```

You're now in the interactive learning interface.

## The 7 Commands You Need

Once inside, you have exactly 7 simple commands:

### 1. **explain** - Learn what commands do
```
❯ explain 'nmap -sV target.local'
→ Breaks down the flags, tells you when to use it, warns about IDS noise
```

### 2. **tip** - Quick study guide
```
❯ tip 'SQL injection'
→ Common payloads, where to look, quick wins
```

### 3. **help** - Troubleshoot errors
```
❯ help 'connection refused'
→ "Target might be down, check your IP, is Docker running?"
```

### 4. **report** - Practice writeups
```
❯ report 'Found SQLi on login'
→ Gives you a 2-3 line template: Vulnerability, Impact, Mitigation
```

### 5. **quiz** - Test yourself
```
❯ quiz 'Buffer Overflow'
→ Flashcard-style Q&A to check your understanding
```

### 6. **plan** - Get unstuck
```
❯ plan 'found port 80 open'
→ Here are your next 3 steps...
```

### 7. **exit** - Leave
```
❯ exit
→ Good luck! Document your steps and be safe.
```

## Why CyBuddy?

### Problem
You're doing a CTF. You find a weird service on port 8080. You Google "how to enumerate port 8080". You get 50 tabs of Stack Overflow, blog posts from 2015, and tool documentation that assumes you already know what you're doing.

### Solution
```bash
❯ plan 'found unknown service on port 8080'
→ 1. Check banner with nc
→ 2. Try nmap service detection
→ 3. Search exploit-db for the version
```

Clean. Fast. No 50 tabs.

## Features

✅ **Simple** - 7 commands. That's it.
✅ **Fast** - No waiting. Type → Get answer.
✅ **Offline-first** - Built-in heuristics work without internet.
✅ **Session tracking** - Keeps history so you can review what you tried.
✅ **Safe defaults** - Won't suggest dangerous commands without warnings.
✅ **CTF-friendly** - Designed for the flow of CTF challenges.

## Real Example

You're stuck on a web challenge:

```bash
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

You just went from stuck → understanding → action in 3 commands. No browser tabs needed.

## Additional Features

### Checklists for Common Tasks
```bash
cybuddy checklist web
cybuddy checklist recon
cybuddy checklist crypto
cybuddy checklist forensics
```

### TODO Tracking
```bash
cybuddy todo add "Enumerate SMB shares"
cybuddy todo list
cybuddy todo done 1
```

### Command History
```bash
cybuddy history
cybuddy history --clear
```

### Dry-run Tool Execution
```bash
cybuddy run nmap "-sV target.local"
# Shows safety warnings + what the command does
# Add --exec to actually run it
```

## Optional: AI Mode

Want smarter answers? Enable AI (requires API key):

```bash
# Create ~/.config/cybuddy/config.yaml (optional)
tui:
  theme: default
  show_tips: true

cli:
  color: true
  verbose: false

ai:
  enabled: true
  provider: openai
  api_key: sk-...
  model: gpt-4o-mini
```

Then use `--send` flag:
```bash
cybuddy explain "nmap -A target" --send
```

**Default:** Built-in heuristics (no API needed)
**With AI:** More detailed, context-aware responses

## Configuration

CyBuddy works out of the box with no configuration needed. All settings have sensible defaults.

For advanced users, create `~/.config/cybuddy/config.yaml`:

```yaml
tui:
  theme: default  # or 'dark', 'light'
  show_tips: true

cli:
  color: true
  verbose: false

data:
  mock_mode: true  # v1.0 is always mock

ai:
  enabled: false
  provider: openai
  redact: true
  max_tokens: 300
```

## Why CyBuddy?

Most security tools are:
- **Complex** - 100 flags, 50 modes, steep learning curve
- **Fragmented** - Different tool for every task
- **Overwhelming** - Too many options when you just want an answer

CyBuddy is:
- **Simple** - 7 commands, one interface
- **Focused** - Built for learning, not production pentesting
- **Helpful** - Like a mentor who explains things clearly

## Who Is This For?

✅ Students learning cyber security
✅ CTF players who want quick hints
✅ Lab learners (HTB, TryHackMe, PentesterLab)
✅ Anyone who Googles "how does X work" while hacking

❌ Production penetration testers (use real tools)
❌ People who want automated exploitation (that's not the point)


## FAQ

**Q: Is this better than just using nmap/gobuster/etc directly?**
A: No. This is a *learning tool*. Use real tools for real work.

**Q: Does it replace Google?**
A: For quick hints and common tasks, yes. For deep dives, no.

**Q: Why only 7 commands?**
A: Because 7 commands is all you need to learn. More = confusion.

**Q: Can I use this during exams/CTFs?**
A: Check your rules. Built-in heuristics = usually OK. AI mode = maybe not.

**Q: Is my data sent anywhere?**
A: Only if you enable AI mode and use --send. Otherwise everything is local.

---

**Built for learners. By someone who remembers being stuck at 2am during a CTF.**

Start learning: `cybuddy guide --tui`
