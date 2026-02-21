# Slack & Telegram Integration for AI Agents

Real-time human-in-the-loop communication channels for agent workflows.

---

## Quick Decision Matrix

| Goal | Best Tool |
|------|-----------|
| Delegate coding tasks from Slack | **Claude Code in Slack** (official) |
| Get notified when agent finishes (Slack) | **CodeInbox** or hooks + webhook |
| Get notified when agent finishes (Telegram) | Hooks + Telegram Bot API |
| Full Claude Code from Telegram (mobile) | **claude-code-telegram** (1.1k stars) |
| Agent pauses, asks human, waits for reply (Slack) | **AskOnSlackMCP** |
| Agent pauses, asks human, waits for reply (Telegram) | **Tryb** (beta) |
| Full approval workflow SDK | **HumanLayer** (Slack/email/Discord) |
| Visual workflow with approval nodes | **n8n** |
| Gate specific tool calls before execution | **PreToolUse hook** + custom script |

---

## The Approval Workflow Pattern

```
Agent runs task
  → detects high-stakes action
  → PAUSES execution
  → sends approval request to Slack/Telegram
  → human taps Approve / Deny / provides feedback
  → agent resumes or aborts
```

---

## Implementation Paths

### Path A: Claude Code Hooks (Simplest)

No extra dependencies. Wire hooks directly to Slack webhooks or Telegram Bot API.

**Slack:**
```json
{
  "hooks": {
    "Notification": [{
      "type": "command",
      "command": "curl -s -X POST -H 'Content-Type: application/json' -d '{\"text\":\"Claude Code needs your attention\"}' https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    }],
    "Stop": [{
      "type": "command",
      "command": "curl -s -X POST -H 'Content-Type: application/json' -d '{\"text\":\"Claude Code finished\"}' https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    }]
  }
}
```

**Telegram:**
```json
{
  "hooks": {
    "Notification": [{
      "type": "command",
      "command": "curl -s 'https://api.telegram.org/botYOUR_TOKEN/sendMessage?chat_id=YOUR_ID&text=Claude+needs+attention'"
    }],
    "Stop": [{
      "type": "command",
      "command": "curl -s 'https://api.telegram.org/botYOUR_TOKEN/sendMessage?chat_id=YOUR_ID&text=Task+complete'"
    }]
  }
}
```

### Path B: MCP Server (AskOnSlackMCP)

Agent gains an `ask_on_slack` tool via MCP. Posts question to Slack, waits 60s for
threaded reply, returns response to agent.

- Repo: https://github.com/trtd56/AskOnSlackMCP
- Works with Claude Desktop and any MCP client
- Best for synchronous Q&A with the agent

### Path C: SDK (HumanLayer)

Wrap high-stakes functions with `@hl.require_approval()`. Execution blocks until
human approves via Slack, email, or Discord.

- Repo: https://github.com/humanlayer/humanlayer
- Python/TypeScript SDK
- Supports escalation chains, timeouts, auto-approve learning
- Free tier: 1,000 ops/month

### Path D: Workflow Platform (n8n)

Visual workflow: Claude API call → HITL approval node → Slack/Telegram notification.
Workflow pauses at approval node. Resumes on human response.

- Docs: https://docs.n8n.io/advanced-ai/human-in-the-loop-tools/

---

## Slack-Specific Tools

### Claude Code in Slack (Official, First-Party)

Launched Dec 8, 2025. `@Claude` in a Slack channel with a coding task:
- Auto-detects coding intent
- Spins up a sandboxed Claude Code session
- Posts progress updates in the Slack thread
- Shares PR link on completion

Requirements:
- Claude plan with Code access (Pro, Max, Team, Enterprise)
- Claude Code browser access enabled in org admin settings
- Claude Slack app installed from App Marketplace
- Works in channels only (not DMs)

### Slack MCP Server (Official from Slack)

- Docs: https://docs.slack.dev/ai/slack-mcp-server/
- Gives Claude Code read/write access to Slack data
- Search channels, send messages, manage Slack

**Security note**: Anthropic's *original* Slack MCP reference server was archived
(May 2025) due to a link-unfurling data exfiltration vulnerability. Use Slack's
own official MCP server instead.

### Community Slack Bot

- mpociot/claude-code-slack-bot: https://github.com/mpociot/claude-code-slack-bot
- Uses Claude Code SDK, supports DMs, threads, streaming, markdown

---

## Telegram-Specific Tools

### claude-code-telegram (Community, 1.1k+ stars)

- Repo: https://github.com/RichardAtCT/claude-code-telegram
- Full Claude Code SDK integration
- Session persistence, git integration, webhook triggers
- Cost tracking, multi-layer auth

### Claudegram

- Site: https://claudegram.com/
- Model switching, session resume
- `/teleport` command to transfer sessions to terminal

### MCP Servers for Telegram

| Server | Repo |
|--------|------|
| Composio Telegram MCP | https://composio.dev/toolkits/telegram/framework/claude-code |
| telegram-mcp (Telethon) | https://github.com/chigwell/telegram-mcp |
| tsgram-mcp (lightweight) | https://github.com/areweai/tsgram-mcp |

### Tryb (Human Relay for Telegram)

- Site: https://tryb.dev/
- Agent calls `ask_human()`, human taps Approve/Deny in Telegram
- Purpose-built for agent approval workflows

---

## Hook Events Reference

| Event | When | Use Case |
|-------|------|----------|
| `Notification` | Permission needed or idle 60s+ | "Waiting for input" alerts |
| `Stop` | Agent finishes responding | "Task complete" notifications |
| `PreToolUse` | Before tool executes | Gate dangerous operations |
| `PostToolUse` | After tool completes | Notify on deploys, commits |

`PreToolUse` can return `{"hookSpecificOutput": {"permissionDecision": "deny"}}` to
block execution — enabling true approval gating.

---

## Recommendation for This Project

1. **Start with hooks → Telegram** for mobile notifications (10 min setup)
2. **Add AskOnSlackMCP** if your team uses Slack for synchronous approvals
3. **Look at HumanLayer** for production workflows with audit trails
4. **Avoid building a custom bot** — the ecosystem is mature enough
