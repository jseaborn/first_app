# Running AI Agents Safely on Mac Mini

## Threat Model

AI agents like OpenClaw require broad system access to function. The risks:
- **Credential theft**: Agents hold API keys, OAuth tokens, passwords in memory
- **Data exfiltration**: Agents can read your files and send data to external servers
- **Prompt injection**: Malicious content can hijack agent behavior
- **Supply chain attacks**: Third-party plugins/skills may contain malware
- **Lateral movement**: A compromised agent can access everything your user can

## Isolation Strategy (Defense in Depth)

Use multiple layers. No single layer is sufficient.

```
┌─────────────────────────────────────────────┐
│ Layer 4: Network Isolation (pf firewall)     │
│  ┌───────────────────────────────────────┐  │
│  │ Layer 3: Separate macOS User Account   │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │ Layer 2: VM or Container         │  │  │
│  │  │  ┌───────────────────────────┐  │  │  │
│  │  │  │ Layer 1: Token/Spend Caps │  │  │  │
│  │  │  └───────────────────────────┘  │  │  │
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## Layer 1: Token and Spend Caps

### For Claude Code (Subscription)
Your Claude Code subscription has built-in limits:
- **Pro ($20/mo)**: ~45 prompts per 5-hour window + weekly cap
- **Max 5x ($100/mo)**: ~5x capacity
- **Max 20x ($200/mo)**: ~20x capacity

No additional configuration needed — limits are enforced server-side.

### For API Usage (OpenClaw or Custom Agents)
Create a dedicated API workspace with spend limits:

1. Go to https://console.anthropic.com
2. Create a new Workspace called "AI Agents - Sandboxed"
3. Set a monthly spend limit (e.g., $50/month)
4. Generate an API key scoped to this workspace only
5. Set `max_tokens` in your agent config to cap per-request output

```bash
# Environment for the sandboxed agent
export ANTHROPIC_API_KEY="sk-ant-sandbox-..."  # Workspace-scoped key
```

---

## Layer 2: Dedicated macOS User Account

### Quick Setup with SandVault

```bash
# Install
git clone https://github.com/webcoyote/sandvault.git
cd sandvault && ./install.sh

# Run any command in the sandbox
sv <command>

# Run Claude Code in the sandbox
sv claude
```

### Manual Setup

```bash
# 1. Create the agent user
sudo sysadminctl -addUser aiagent -password "$(openssl rand -base64 32)" -home /Users/aiagent

# 2. Remove from admin group
sudo dseditgroup -o edit -d aiagent -t user admin

# 3. Create isolated workspace
sudo mkdir -p /Users/Shared/agent-workspace
sudo chown aiagent:staff /Users/Shared/agent-workspace
sudo chmod 770 /Users/Shared/agent-workspace

# 4. Restrict the agent user's home directory
sudo chmod 700 /Users/aiagent

# 5. Prevent agent from reading YOUR home directory
# (macOS home dirs are readable by default — fix this)
chmod 700 ~/

# 6. Run agent commands as the restricted user
sudo -u aiagent -H bash -c 'cd /Users/Shared/agent-workspace && openclaw start'
```

### What This Protects Against
- Agent cannot read your home directory, Documents, Downloads, etc.
- Agent cannot access your Keychain
- Agent cannot modify system settings
- Agent is limited to /Users/Shared/agent-workspace

### What This Does NOT Protect Against
- Network-based attacks (agent can still reach the internet)
- Kernel exploits (agent shares the same kernel)
- World-readable files outside home directories

---

## Layer 3: Virtual Machine (Stronger)

### Using ClodPod (macOS VM)

```bash
git clone https://github.com/webcoyote/clodpod.git
cd clodpod && ./setup.sh
```

### Using Docker Desktop

```bash
# Create isolated network
docker network create --driver bridge agent-net

# Run agent in container with strict resource limits
docker run -d \
  --name ai-agent \
  --network agent-net \
  --memory=2g \
  --cpus=1.0 \
  --pids-limit=100 \
  --read-only \
  --tmpfs /tmp:size=512m \
  -v /Users/Shared/agent-workspace:/workspace:rw \
  -e ANTHROPIC_API_KEY="$SANDBOX_API_KEY" \
  node:22-slim \
  bash -c "npm install -g openclaw && openclaw start"
```

---

## Layer 4: Network Firewall

Restrict the agent to only reach the LLM API:

### macOS Packet Filter (pf)

Create `/etc/pf.anchors/aiagent.rules`:
```
# Block all outbound traffic from aiagent user
block out quick proto tcp from any to any user aiagent

# Allow DNS (needed for API hostname resolution)
pass out quick proto udp from any to any port 53 user aiagent

# Allow ONLY Anthropic API
pass out quick proto tcp from any to api.anthropic.com port 443 user aiagent

# Allow ONLY OpenAI API (if using GPT models)
# pass out quick proto tcp from any to api.openai.com port 443 user aiagent
```

Load the rules:
```bash
# Add anchor to /etc/pf.conf
echo 'anchor "aiagent"' | sudo tee -a /etc/pf.conf
echo 'load anchor "aiagent" from "/etc/pf.anchors/aiagent.rules"' | sudo tee -a /etc/pf.conf

# Enable packet filter
sudo pfctl -f /etc/pf.conf
sudo pfctl -e
```

### For Docker (simpler)
```bash
# Create internal-only network (no internet)
docker network create --internal agent-isolated

# Use a proxy container to allow only API traffic
# (the agent container has no direct internet access)
```

---

## Recommended Minimum Setup

For experimenting with OpenClaw on your Mac Mini:

1. **Separate user account** (Layer 2) — 10 minutes to set up
2. **Spend-capped API key** (Layer 1) — 5 minutes in Anthropic Console
3. **Network firewall rules** (Layer 4) — 15 minutes with pf

For production or sensitive data environments, add Layer 3 (VM/Docker).

---

## Layer 5: Filesystem Sandboxing (Seatbelt)

Beyond user account isolation, use macOS `sandbox-exec` for process-level restrictions.

### Anthropic's sandbox-runtime (Recommended)

Anthropic provides [sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime),
which sandboxes filesystem and network access without Docker or VMs:

```bash
npm install -g @anthropic-ai/sandbox-runtime
```

Configure `~/.srt-settings.json`:
```json
{
  "network": {
    "allowedDomains": ["api.anthropic.com", "*.anthropic.com"],
    "deniedDomains": []
  },
  "filesystem": {
    "denyRead": ["~/.ssh", "~/.aws", "~/.gnupg", "~/.config/gh"],
    "allowWrite": ["/Users/Shared/agent-workspace", "/tmp"],
    "denyWrite": [".env", "*.pem", "*.key"]
  }
}
```

Run your agent sandboxed:
```bash
srt "your-agent-command-here"
```

### Custom Seatbelt Profile

For maximum control, create a deny-all-default sandbox profile.

Create `agent-sandbox.sb`:
```scheme
(version 1)
(deny default)

;; Allow basic execution
(allow process-exec)
(allow process-fork)

;; System libraries (read-only)
(allow file-read*
  (subpath "/usr/lib")
  (subpath "/usr/bin")
  (subpath "/bin")
  (subpath "/Library/Frameworks")
  (subpath "/System"))

;; Agent workspace (read + write)
(allow file-read* (subpath "/Users/Shared/agent-workspace"))
(allow file-write* (subpath "/Users/Shared/agent-workspace"))
(allow file-write* (subpath "/private/tmp"))

;; Block all other user directories
(deny file-read* (subpath "/Users")
  (require-not (subpath "/Users/Shared/agent-workspace")))

;; Network: HTTPS only
(allow network-outbound (remote ip "*:443"))
(allow network-outbound (remote unix-socket (path-literal "/var/run/mDNSResponder")))

(allow sysctl-read)
(allow mach-lookup)
```

Run with: `sandbox-exec -f agent-sandbox.sb /path/to/agent`

### Application-Level Firewall (GUI Option)

For per-process network monitoring with a visual interface:
- [**LuLu**](https://objective-see.org/products/lulu.html) (free, open-source): blocks unknown outgoing connections
- **Little Snitch** ($59): more polished UI, per-process domain filtering

Both let you create rules like "allow agent to connect to api.anthropic.com:443 only."

---

## Comparison of Isolation Approaches

| Approach | Isolation | Overhead | Setup Time | Best For |
|----------|-----------|----------|------------|----------|
| SandVault (user account) | Medium | Zero | 10 min | Quick setup, CLI agents |
| sandbox-runtime (Seatbelt) | Medium-High | Minimal | 15 min | Claude Code, lightweight agents |
| Docker Desktop | High | Low-Medium | 30 min | Complex agent environments |
| ClodPod (macOS VM) | Very High | Medium | 45 min | Maximum isolation |
| Apple Containers (macOS 26+) | Very High | Low | TBD | Future-proof (VM-per-container) |

---

## Using Your Claude Code Account

### Critical Policy Change (February 2026)

Anthropic has **banned the use of Claude Pro/Max subscription OAuth tokens in
third-party tools**. This includes OpenClaw, Cline, Roo Code, and other
non-Anthropic applications. The policy is clear:

- **Official tools** (Claude Code CLI, claude.ai): use your subscription
- **Third-party tools** (OpenClaw, etc.): must use API keys with per-token billing

Source: [Anthropic Bans Claude Subscription OAuth in Third-Party Apps](https://winbuzzer.com/2026/02/19/anthropic-bans-claude-subscription-oauth-in-third-party-apps-xcxwbn/)

### What This Means for You

| | Claude Code CLI | OpenClaw |
|---|---|---|
| Authentication | Anthropic account (OAuth) | API key (required) |
| Billing | Subscription (Pro/Max) | Pay-per-token (API) |
| Cost control | Built-in dual-layer limits | Workspace spend caps |
| Security model | Sandboxed CLI with permissions | Full system access |
| Policy | Officially supported | Must use separate API key |

### API Spend Tiers

| Tier | Deposit Required | Monthly Spend Cap |
|------|-----------------|-------------------|
| Tier 1 | $5 | $100 |
| Tier 2 | $40 | $500 |
| Tier 3 | $200 | $1,000 |
| Tier 4 | $400 | $5,000 |

**Recommendation**: Stay on Tier 1 ($100/mo cap) when experimenting with OpenClaw.
Set the workspace spend limit even lower (e.g., $50/mo) for safety.

### Monitoring API Costs

```bash
# Check cost breakdown via API
curl https://api.anthropic.com/v1/organizations/cost_report \
  -H "x-api-key: $ANTHROPIC_API_KEY"

# Check token consumption
curl https://api.anthropic.com/v1/organizations/usage_report/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY"
```

Within Claude Code, use `/cost` to see real-time session usage.

---

## Recommended Setup (Quick Start)

### If you want OpenClaw on your Mac Mini (30-minute setup):

```bash
# 1. Install SandVault (sandboxed user account)
brew install sandvault && sv build

# 2. Create spend-capped API key at console.anthropic.com
#    - New workspace: "OpenClaw Sandbox"
#    - Spend limit: $50/month
#    - Generate API key

# 3. Configure sandbox-runtime for filesystem/network restriction
npm install -g @anthropic-ai/sandbox-runtime
# Edit ~/.srt-settings.json (see Layer 5 above)

# 4. Run OpenClaw in the sandbox
sv shell /Users/Shared/sv-$USER -- \
  env ANTHROPIC_API_KEY=sk-ant-sandbox-... openclaw start
```

### If you want the same benefits without OpenClaw (recommended):

Use Claude Code directly with the agent framework in this repository.
See `CLAUDE.md`, `.agent-context/`, and `.claude/commands/`.
