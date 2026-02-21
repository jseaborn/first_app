# Research: Adopting OpenClaw Agent Concepts in Claude Code Projects

## Executive Summary

OpenClaw's **conceptual architecture** — structured markdown files that define agent personality, mission, tools, and memory — is genuinely powerful. However, OpenClaw **the software** is a severe security risk. This document proposes adopting the best ideas from OpenClaw's configuration-driven agent design into Claude Code's native `CLAUDE.md` system, which provides the same conceptual benefits with dramatically better security properties.

**Bottom line**: Don't run OpenClaw. Steal its best ideas and implement them in Claude Code.

---

## Part 1: OpenClaw Architecture Analysis

### What OpenClaw Gets Right

The core insight is correct: **the setup is the product**. Most people interact with AI agents ad-hoc, providing no structure, personality, or persistent context. OpenClaw's configuration files force you to think about:

| OpenClaw File | Purpose | Why It Matters |
|---|---|---|
| `SOUL.md` | Voice, personality, behavioral philosophy | Consistent outputs across sessions |
| `IDENTITY.md` | Brand details, external presentation | Separation of internal behavior from external persona |
| `AGENTS.md` | Team structure, routing rules | Specialization improves quality |
| `MISSION.md` | Goals, priorities, success criteria | Prevents drift, keeps agents focused |
| `HEARTBEAT.md` | Scheduled tasks, cadences | Autonomous recurring work |
| `MEMORY.md` | Persistent context across sessions | Continuity without re-explaining everything |
| `TOOLS.md` | Environment config, available capabilities | Explicit capability boundaries |
| `USER.md` | Known info about the user | Personalization without repetition |

### What OpenClaw Gets Wrong: Security

OpenClaw has been flagged by **every major cybersecurity vendor** as a critical risk:

- **512 vulnerabilities** identified in security audit, 8 classified as critical
- **CVE-2026-25253** (CVSS 8.8): One-click RCE chain exploitable on localhost instances
- **42,665 exposed instances** found publicly, 93.4% with authentication bypass
- **341+ malicious skills** discovered in ClawHub (12-20% of the registry) delivering macOS stealers
- **Plaintext credential leakage**: Anthropic API keys, Telegram tokens, Slack OAuth credentials, full conversation histories found exposed
- **No trust boundaries**: Untrusted inputs (web content, messages, third-party skills) can directly influence tool invocation without policy mediation

The fundamental problem: OpenClaw requires access to root files, authentication credentials, browser cookies, and your entire filesystem to function as designed. It runs a persistent daemon (heartbeat) with these privileges.

#### Sources on Security Risks
- [Cisco: Personal AI Agents Like OpenClaw Are a Security Nightmare](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)
- [CrowdStrike: What Security Teams Need to Know About OpenClaw](https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/)
- [Palo Alto Networks: Why OpenClaw May Signal the Next AI Security Crisis](https://www.paloaltonetworks.com/blog/network-security/why-moltbot-may-signal-ai-crisis/)
- [Kaspersky: New OpenClaw AI Agent Found Unsafe for Use](https://www.kaspersky.com/blog/openclaw-vulnerabilities-exposed/55263/)
- [VentureBeat: OpenClaw Proves Agentic AI Works — and Your Security Model Doesn't](https://venturebeat.com/security/openclaw-agentic-ai-security-risk-ciso-guide)
- [Permiso: Inside the OpenClaw Ecosystem](https://permiso.io/blog/inside-the-openclaw-ecosystem-ai-agents-with-privileged-credentials)
- [Sophos: The OpenClaw Experiment Is a Warning Shot](https://www.sophos.com/en-us/blog/the-openclaw-experiment-is-a-warning-shot-for-enterprise-ai-security)

---

## Part 2: Adapted Framework for Claude Code

### Why Claude Code Is Safer

Claude Code provides many of the same agentic capabilities but with critical safety differences:

| Property | OpenClaw | Claude Code |
|---|---|---|
| Runs as persistent daemon | Yes (heartbeat) | No (session-based) |
| Holds credentials to external services | Yes (email, calendar, Slack, etc.) | No |
| Executes arbitrary shell commands | Unrestricted | Requires explicit user permission |
| Third-party plugin ecosystem | Yes (20% malicious) | MCP servers (user-configured) |
| Network access | Unrestricted | Sandboxed per configuration |
| Trust boundaries | None | Permission prompts, hooks |
| Open attack surface | 42,000+ exposed instances | Local CLI only |

### The Adapted Architecture

We map OpenClaw's 7 configuration files onto Claude Code's native `CLAUDE.md` hierarchy:

```
project-root/
├── CLAUDE.md                  # Root config (combines SOUL + MISSION + TOOLS)
├── .claude/
│   ├── settings.json          # Tool permissions, MCP config
│   └── commands/              # Custom slash commands (agent chains)
│       ├── research.md        # /research command
│       ├── write.md           # /write command
│       ├── review.md          # /review command
│       └── publish.md         # /publish command
├── .agent-context/
│   ├── IDENTITY.md            # Brand voice, platform details
│   ├── MISSION.md             # Current goals, priorities, success metrics
│   ├── MEMORY.md              # Persistent context, decisions, learnings
│   └── AGENTS.md              # Agent specializations and routing rules
├── dev-docs/                  # Per-task planning docs
│   └── {task-name}/
│       ├── plan.md
│       ├── context.md
│       └── tasks.md
└── src/                       # Your actual code
```

### File-by-File Mapping

#### 1. `CLAUDE.md` ← Replaces SOUL.md + MISSION.md + TOOLS.md

Claude Code's `CLAUDE.md` is automatically loaded at session start — exactly like OpenClaw's SOUL.md. We combine three concepts here because Claude Code uses a single entry point:

```markdown
# Project: [Your Project Name]

## Soul (Voice & Personality)
- Write in [tone]: direct, technical, no fluff
- Prioritize [values]: security, simplicity, correctness
- When uncertain, ask rather than assume
- [Your specific behavioral rules]

## Mission (Current Goals)
- Primary: [What we're building/achieving right now]
- Secondary: [Supporting goals]
- Non-goals: [What we explicitly are NOT doing]
- Success looks like: [Measurable criteria]

## Tools & Environment
- Runtime: Node 22+ / Python 3.12+
- Test command: `npm test` or `pytest`
- Build command: `npm run build`
- Lint: `npm run lint`
- Key directories: src/ for source, tests/ for tests
- Database: [type and connection details if relevant]

## Rules
- Always create a new git branch for each task
- Run tests before committing
- Never modify files in /config/production/
- [Your project-specific rules]
```

#### 2. `.agent-context/IDENTITY.md` ← Replaces IDENTITY.md

Separated from CLAUDE.md because identity details are referenced contextually, not on every prompt:

```markdown
# Identity

## Brand
- Name: [Project/Product Name]
- Tagline: [One-liner]
- Voice: [How we sound to users — formal/casual/technical]

## Platforms
- Website: [URL]
- Repository: [GitHub URL]
- Documentation: [Docs URL]
- Package registry: [npm/PyPI/etc.]

## Audience
- Primary: [Who uses this]
- Technical level: [Beginner/Intermediate/Expert]
- Key use cases: [What they do with it]
```

#### 3. `.agent-context/MISSION.md` ← Replaces MISSION.md (extended)

For projects where mission evolves frequently, keep a separate living document:

```markdown
# Mission

## Current Sprint/Phase
- [What we're working on right now]
- Started: [date]
- Target: [date or milestone]

## Priorities (ordered)
1. [Highest priority task/feature]
2. [Second priority]
3. [Third priority]

## Decisions Log
- [Date]: Decided to [X] because [Y]
- [Date]: Chose [approach A] over [approach B] because [reason]

## Non-Goals (things we are explicitly NOT doing)
- [Feature/approach we consciously rejected]
```

#### 4. `.agent-context/MEMORY.md` ← Replaces MEMORY.md

This is the most powerful concept to adopt. Claude Code sessions are ephemeral — memory.md bridges that gap:

```markdown
# Project Memory

## Architecture Decisions
- Using [framework X] for [reason]
- Database schema follows [pattern] because [reason]
- API authentication uses [method]

## Known Issues & Gotchas
- [Module X] has a quirk where [description]
- Don't use [approach] because [past failure reason]
- [External API] rate limits at [N] requests/minute

## Patterns & Conventions
- Error handling: [how we do it]
- Naming: [conventions]
- File organization: [rules]

## Previous Session Context
- Last worked on: [feature/task]
- Status: [where we left off]
- Next steps: [what to do next]

## Learnings
- [Date]: Discovered that [X] — important for future work
- [Date]: [Library Y] doesn't support [Z], use [alternative] instead
```

#### 5. `.agent-context/AGENTS.md` ← Replaces AGENTS.md

Defines specializations for Claude Code's sub-agent system (`Task` tool):

```markdown
# Agent Specializations

## Researcher
- Role: Explore codebase, read documentation, analyze problems
- Tools: Read, Glob, Grep, WebFetch, WebSearch
- Output: Summary with file references and recommendations
- When to use: Before any implementation work

## Implementer
- Role: Write code, create files, make changes
- Tools: Read, Edit, Write, Bash (build/test only)
- Rules: Always run tests after changes, never skip linting
- When to use: After research phase is complete

## Reviewer
- Role: Review code changes for quality, security, correctness
- Tools: Read, Grep, Bash (git diff only)
- Checklist: Security (OWASP top 10), performance, readability, test coverage
- When to use: After implementation, before commit

## Publisher
- Role: Commit, push, create PRs, update documentation
- Tools: Bash (git commands), Edit (changelog/docs)
- Rules: Descriptive commit messages, PR descriptions with test plans
- When to use: After review approval

## Routing Rules
1. New task → Researcher first
2. Bug report → Researcher → Implementer → Reviewer
3. Feature request → Researcher → Plan → Implementer → Reviewer → Publisher
4. Refactor → Researcher → Reviewer (current state) → Implementer → Reviewer (new state)
```

#### 6. Custom Slash Commands ← Replaces Agent Chains

Instead of OpenClaw's `Researcher → Writer → Reviewer → Publisher` chain, use Claude Code custom commands:

**`.claude/commands/research.md`**:
```markdown
Research the following topic or codebase area: $ARGUMENTS

1. Search the codebase for relevant files and patterns
2. Read and analyze key files
3. Search the web for relevant documentation or solutions if needed
4. Summarize findings with specific file:line references
5. Identify risks, dependencies, and open questions
6. Write findings to dev-docs/{topic}/context.md
```

**`.claude/commands/implement.md`**:
```markdown
Implement the following based on the plan: $ARGUMENTS

1. Read the plan from dev-docs/{feature}/plan.md
2. Read .agent-context/MEMORY.md for relevant context
3. Create a new git branch for this work
4. Implement changes following the plan step by step
5. Run tests after each significant change
6. Update .agent-context/MEMORY.md with any new learnings
7. Do NOT commit — leave that for the review/publish step
```

**`.claude/commands/review.md`**:
```markdown
Review the current changes for quality and correctness: $ARGUMENTS

1. Run git diff to see all changes
2. Check each change against:
   - Correctness: Does it do what was intended?
   - Security: Any injection, XSS, auth issues?
   - Performance: Any obvious bottlenecks?
   - Tests: Are changes covered by tests?
   - Style: Does it follow project conventions?
3. List any issues found with severity (critical/warning/nit)
4. If critical issues exist, do NOT proceed to publish
```

**`.claude/commands/publish.md`**:
```markdown
Publish the current changes: $ARGUMENTS

1. Run the full test suite
2. Run the linter
3. If tests or lint fail, fix issues first
4. Create a descriptive commit message
5. Push to the current branch
6. Create a PR with summary and test plan
7. Update .agent-context/MISSION.md with completion status
```

### What We Skip: HEARTBEAT.md

OpenClaw's heartbeat (autonomous scheduled execution) is deliberately omitted. This is the most dangerous feature — a daemon that acts without user prompting, holding credentials and system access. Claude Code's session-based model is safer: you initiate every interaction. If you need scheduled tasks, use standard cron/launchd jobs that are auditable and don't hold AI agent credentials.

---

## Part 3: Running OpenClaw Safely on Mac Mini (If You Still Want To)

**Strong recommendation**: Use the adapted Claude Code framework above instead. But if you want to experiment with OpenClaw itself, here's how to isolate it.

### Option A: Dedicated macOS User Account (Recommended Minimum)

**Tool: [SandVault](https://github.com/webcoyote/sandvault)**

SandVault creates a limited macOS user account specifically for sandboxing AI agents. It provides:
- A restricted user with no access to your home directory
- Shared workspace at `/Users/Shared/sv-$USER`
- Passwordless account switching (uses `sudo -u`)
- No VM overhead

```bash
# Install SandVault
git clone https://github.com/webcoyote/sandvault.git
cd sandvault
./install.sh

# Run OpenClaw in the sandboxed account
sv openclaw start
```

**Manual setup without SandVault**:
```bash
# Create dedicated user
sudo dscl . -create /Users/aiagent
sudo dscl . -create /Users/aiagent UserShell /bin/zsh
sudo dscl . -create /Users/aiagent UniqueID 599
sudo dscl . -create /Users/aiagent PrimaryGroupID 20
sudo dscl . -create /Users/aiagent NFSHomeDirectory /Users/aiagent
sudo mkdir -p /Users/aiagent
sudo chown aiagent:staff /Users/aiagent

# Create shared workspace (only directory the agent can access)
mkdir -p /Users/Shared/agent-workspace
chmod 770 /Users/Shared/agent-workspace
sudo chown aiagent:staff /Users/Shared/agent-workspace

# Lock down: remove from admin group, restrict sudo
sudo dseditgroup -o edit -d aiagent -t user admin

# Run commands as the agent user
sudo -u aiagent openclaw start --workspace /Users/Shared/agent-workspace
```

**Critical limitations of user-account isolation**:
- The agent user can still make network requests to arbitrary endpoints
- It can still read world-readable files on the system
- It provides no protection against kernel-level exploits
- OpenClaw's own vulnerabilities (CVE-2026-25253) may allow escape

### Option B: Virtual Machine (Stronger Isolation)

**Tool: [ClodPod](https://github.com/webcoyote/clodpod)**

ClodPod creates a macOS VM specifically for running AI agents:

```bash
git clone https://github.com/webcoyote/clodpod.git
cd clodpod
./setup.sh  # Creates macOS VM via Virtualization.framework
```

Benefits over user accounts:
- Full kernel isolation
- Independent filesystem
- Network can be fully restricted
- Snapshot/rollback capability

### Option C: Docker (Linux Containers on Mac)

```bash
# Run OpenClaw in a Docker container with strict limits
docker run -d \
  --name openclaw-sandbox \
  --memory=2g \
  --cpus=1.0 \
  --network=openclaw-net \
  --read-only \
  -v /Users/Shared/agent-workspace:/workspace \
  openclaw/openclaw:latest
```

Create a restricted network that only allows Anthropic API access:
```bash
# Create isolated network
docker network create --internal openclaw-net

# Allow only Anthropic API endpoints
# (requires additional iptables/pf rules on the host)
```

### Network Isolation (All Options)

Use macOS Packet Filter (pf) to restrict the agent's network access:

```bash
# /etc/pf.anchors/aiagent
# Only allow connections to Anthropic API
block out quick on egress proto tcp from any to any user aiagent
pass out quick on egress proto tcp from any to api.anthropic.com port 443 user aiagent
pass out quick on egress proto udp from any to any port 53 user aiagent  # DNS

# Load the rules
sudo pfctl -a aiagent -f /etc/pf.anchors/aiagent
sudo pfctl -e
```

---

## Part 4: Token Limits and Cost Controls

### Using Claude Code Subscription

Claude Code subscriptions (Pro at $20/month, Max at $100-200/month) **cannot directly power third-party frameworks like OpenClaw**. The subscription is tied to the Claude Code CLI. However:

#### For Claude Code Projects (Recommended Path)

| Plan | Capacity | Best For |
|---|---|---|
| Pro ($20/mo) | ~45 prompts per 5-hour window, weekly cap | Individual developers, moderate use |
| Max 5x ($100/mo) | ~5x Pro capacity | Heavy daily use, multi-project work |
| Max 20x ($200/mo) | ~20x Pro capacity | Agencies, intensive automation |

**Built-in cost controls**:
- Dual-layer limits: 5-hour rolling window + 7-day weekly ceiling
- `/cost` command shows real-time token usage in any session
- Automatic throttling when limits approach (no surprise bills)

#### For OpenClaw or Custom Agents (API Required)

If you want to power OpenClaw with Claude, you need a separate **Anthropic API account**:

**API spend controls**:
- **Organization-level spend limits**: Set maximum monthly spend in the Anthropic Console
- **Workspace-level limits**: Create a dedicated workspace with its own budget cap
- **Per-request `max_tokens`**: Cap output tokens per API call (2,000-8,000 recommended for code)
- **Tier system**: Spending is capped by your tier level (Tier 1: $100/mo, Tier 2: $500/mo, etc.)

```bash
# Environment variable to set in OpenClaw's config
export ANTHROPIC_API_KEY="sk-ant-..."

# In openclaw.json, limit token usage:
{
  "llm": {
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514",
    "maxTokens": 4096,
    "temperature": 0.3
  }
}
```

**Cost optimization tips**:
- Use Sonnet instead of Opus for routine tasks (5-10x cheaper)
- Enable prompt caching to reduce input token costs
- Stay under 200K input tokens per message (above this, pricing jumps to $6/$22.50 vs $3/$15)
- Monitor daily: average Claude Code cost is ~$6/developer/day

#### Sources on Cost and Limits
- [Anthropic: Manage Costs Effectively](https://code.claude.com/docs/en/costs)
- [Anthropic: Rate Limits](https://platform.claude.com/docs/en/api/rate-limits)
- [Northflank: Claude Code Rate Limits and Pricing](https://northflank.com/blog/claude-rate-limits-claude-code-pricing-cost)
- [Faros AI: Claude Code Token Limits Guide](https://www.faros.ai/blog/claude-code-token-limits)

---

## Part 5: Recommendations

### Priority 1: Adopt the Framework in Claude Code (Do This)

1. Create the `.agent-context/` directory structure in your projects
2. Write your `CLAUDE.md` with soul + mission + tools sections
3. Create custom slash commands for your workflow chains
4. Maintain `MEMORY.md` across sessions for continuity
5. Use `AGENTS.md` to define specializations for sub-agent tasks

**This gives you 90% of OpenClaw's value with none of the security risk.**

### Priority 2: If You Must Run OpenClaw (Do This Carefully)

1. Use SandVault or ClodPod for isolation on your Mac Mini
2. Never connect it to real email, calendar, or messaging accounts
3. Use a dedicated Anthropic API key with strict spend limits
4. Restrict network access to only the LLM API endpoint
5. Monitor the `/Users/Shared/agent-workspace` directory for unexpected files
6. Keep it on an isolated VLAN if possible

### Priority 3: Don't Do This

1. Don't install OpenClaw on your primary user account
2. Don't give it access to your real credentials
3. Don't install skills from ClawHub without auditing the source
4. Don't expose it to the network (even localhost has been exploited)
5. Don't trust that "local-first" means "secure"
