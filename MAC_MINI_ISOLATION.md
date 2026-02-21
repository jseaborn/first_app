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

## Using Your Claude Code Account

**Claude Code subscription cannot directly power OpenClaw.** They are separate:

| | Claude Code CLI | OpenClaw |
|---|---|---|
| Authentication | Anthropic account (OAuth) | API key |
| Billing | Subscription (Pro/Max) | API usage (pay-per-token) |
| Cost control | Built-in limits | Manual spend caps |
| Security model | Sandboxed CLI with permissions | Full system access |

**Recommendation**: Use Claude Code directly with the framework from this project.
If you also want to experiment with OpenClaw, create a separate API workspace
with a strict spend cap ($20-50/month) and run it in the sandboxed environment
described above.
