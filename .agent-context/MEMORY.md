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

## Learnings
- 2026-02-21: OpenClaw has 512 known vulnerabilities, 8 critical. Do not run
  without full VM isolation. SandVault or ClodPod recommended if experimenting.
- 2026-02-21: Claude Code Pro plan gives ~45 prompts per 5-hour window.
  Max plans scale up to 20x. API usage averages ~$6/dev/day.
