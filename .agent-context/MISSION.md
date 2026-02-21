# Mission

## Current Phase
- Phase: Initial Setup
- Started: 2026-02-21
- Goal: Establish agent framework template

## Priorities (ordered)
1. Create reusable project template with agent configuration files
2. Document the framework and its mapping from OpenClaw concepts
3. Provide security guidance for running AI agents

## Decisions Log
- 2026-02-21: Chose Claude Code native CLAUDE.md over OpenClaw due to security concerns
- 2026-02-21: Adopted configuration-driven approach from OpenClaw without the runtime
- 2026-02-21: Skipped HEARTBEAT.md equivalent — autonomous daemons are a security risk

## Non-Goals
- Running OpenClaw directly
- Building a custom agent runtime
- Autonomous scheduled execution (use cron/launchd for that)
