# Project Memory

## Architecture Decisions
- Using Claude Code's native CLAUDE.md system as the agent configuration layer
- Structured after OpenClaw's 7-file architecture, adapted for safety
- Custom slash commands replace OpenClaw's agent chains

## Known Issues & Gotchas
- Claude Code sessions are ephemeral — this file bridges session gaps
- Keep this file under 500 lines to avoid bloating context
- Update this file at the end of each significant work session

## Patterns & Conventions
- Agent routing rules are in .agent-context/AGENTS.md
- Per-task docs go in dev-docs/{task-name}/
- Custom workflows are in .claude/commands/

## Session Log
- 2026-02-21: Initial framework creation. Researched OpenClaw architecture,
  security risks, Mac Mini isolation strategies, and token limits.
  Created full template structure with CLAUDE.md, agent-context files,
  and custom slash commands.
- 2026-02-21: Expanded MAC_MINI_ISOLATION.md with Layer 5 (Seatbelt/sandbox-runtime),
  Feb 2026 OAuth ban policy, API spend tiers, comparison table, quick-start guide.
- 2026-02-21: Researched Slack/Telegram as real-time feedback channels for agents.
  Findings saved to CHAT_INTEGRATION.md. Key result: both work today — Slack has
  first-party support (Claude Code in Slack), Telegram has strong community tools.
- 2026-02-21: Researched Skill Seekers (yusufkaraaslan/Skill_Seekers) for tool-specific
  skill generation. Findings saved to dev-docs/skill-seekers/RESEARCH.md.
  Key: converts docs/repos/PDFs into Claude skills (SKILL.md + references/ ZIP).
  25 MCP tools, --enhance-local uses local Claude CLI (no API cost on Max plan).
  Skills install to ~/.claude/skills/{name}/. Default target is Claude.

## Learnings
- 2026-02-21: OpenClaw has 512 known vulnerabilities, 8 critical. Do not run
  without full VM isolation. SandVault or ClodPod recommended if experimenting.
- 2026-02-21: Claude Code Pro plan gives ~45 prompts per 5-hour window.
  Max plans scale up to 20x. API usage averages ~$6/dev/day.
- 2026-02-21: Anthropic banned subscription OAuth in third-party tools (Feb 19, 2026).
  OpenClaw/Cline/etc must use API keys with per-token billing.
- 2026-02-21: For human-in-the-loop agent workflows via chat:
  - Slack: AskOnSlackMCP (MCP), HumanLayer (SDK), CodeInbox (hooks)
  - Telegram: claude-code-telegram, Tryb, hooks + Bot API curl
  - Claude Code hooks (Notification, Stop, PreToolUse) are the simplest entry point
  - Security: Anthropic's original Slack MCP server had a data exfiltration vuln
    via link unfurling. Use Slack's official MCP server instead.
- 2026-02-21: Skill Seekers (github.com/yusufkaraaslan/Skill_Seekers):
  - pip install skill-seekers[mcp] for MCP integration (25 tools)
  - `skill-seekers install --config {name} --enhance-local` is the one-liner
  - Skills = ZIP of SKILL.md (YAML frontmatter) + references/ markdown files
  - --target flag: claude (default), gemini, openai, markdown
  - 11 presets in-repo, 24+ via SkillSeekersWeb.com API
  - Security: spawns subprocesses, downloaded content is unsandboxed,
    community configs need validation before use
