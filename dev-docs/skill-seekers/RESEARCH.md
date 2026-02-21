# Skill Seekers — Research Report

**Repository**: [github.com/yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)
**PyPI**: [pypi.org/project/skill-seekers](https://pypi.org/project/skill-seekers)
**Website**: [skillseekersweb.com](https://skillseekersweb.com/)
**Current Version**: 3.0.0 (pyproject.toml), 2.2.0 (latest published on PyPI)
**License**: MIT
**Language**: Python (requires >=3.10)
**Date**: 2026-02-21

---

## What It Is

Skill Seekers is a preprocessing pipeline that converts documentation websites,
GitHub repositories, and PDFs into structured "skills" for AI systems. It targets
16+ platforms including Claude Code, Gemini, OpenAI, Cursor, Windsurf, LangChain,
LlamaIndex, and vector databases (Pinecone, Chroma, FAISS, Qdrant).

**Relevance to this project**: We can use it to generate tool-specific Claude Code
skills from any documentation source — giving our agent deep knowledge of specific
tools (Terraform, Slack API, Kubernetes, etc.) without manual curation.

---

## 1. Claude Skill Generation Pipeline

### The 5-Phase Workflow

```
fetch config → scrape docs → enhance (AI rewrite) → package ZIP → upload/install
```

1. **Scrape** — Crawl documentation using configurable CSS selectors, URL patterns,
   and rate limits. Pages saved as individual JSON files in `output/{name}_data/pages/`.
2. **Organize** — Categorize content into reference markdown files under
   `output/{name}/references/` based on config category rules.
3. **Generate SKILL.md** — Create main skill file with YAML frontmatter.
4. **Enhance** — Local Claude CLI subprocess rewrites SKILL.md from ~75 lines
   to ~500+ lines with step descriptions, troubleshooting, prerequisites, next steps.
5. **Package** — ZIP everything. Upload to platform or install locally.

### What a Claude Skill Looks Like

```
output/{name}/
  SKILL.md              # Main file with YAML frontmatter
  references/
    index.md            # Table of contents
    getting_started.md  # Category-based reference files
    api.md
    scripting.md
    ...
  scripts/              # Optional executables
  assets/               # Optional images/resources
```

**SKILL.md format:**

```markdown
---
name: react
description: React framework knowledge base
version: 1.0.0
---

# React Skill

## When to Use This Skill
[Trigger conditions]

## What's Included
[TOC pointing to reference files]

## Quick Reference
[5-10 practical code examples]

## Navigation
See references/index.md for the full reference guide.
```

### Installation Path

Skills install to: **`~/.claude/skills/{skill_name}/`**

Requires Claude Code restart to pick up new skills.

---

## 2. MCP Integration (25 Tools)

The FastMCP server (`src/skill_seekers/mcp/server_fastmcp.py`) exposes 25 tools:

### Config Tools (3)
| Tool | Description |
|------|-------------|
| `generate_config` | Create scraping config |
| `list_configs` | List available presets |
| `validate_config` | Check config for errors |

### Scraping Tools (9)
| Tool | Description |
|------|-------------|
| `estimate_pages` | Preview page count |
| `scrape_docs` | Full documentation scrape with llms.txt detection |
| `scrape_github` | README, issues, changelog, releases, code structure |
| `scrape_pdf` | Text, code, images from PDFs |
| `scrape_codebase` | Local codebase analysis, API reference extraction |
| `detect_patterns` | Design patterns across 9 languages |
| `extract_test_examples` | Mine test files for real usage patterns |
| `build_how_to_guides` | Convert examples into tutorials |
| `extract_config_patterns` | Analyze config files (DB, API, auth) |

### Packaging Tools (4)
| Tool | Description |
|------|-------------|
| `package_skill` | Package for target platform |
| `upload_skill` | Upload to platform API |
| `enhance_skill` | AI-enhance SKILL.md |
| `install_skill` | Full pipeline end-to-end |

### Splitting Tools (2)
| Tool | Description |
|------|-------------|
| `split_config` | Divide large configs into focused skills |
| `generate_router` | Create routing skill for split docs |

### Source Tools (5)
| Tool | Description |
|------|-------------|
| `fetch_config` | Retrieve configs from API/git/registered sources |
| `submit_config` | Submit to community via GitHub issue |
| `add_config_source` | Register git repo as config source |
| `list_config_sources` | Display registered sources |
| `remove_config_source` | Unregister a source |

### Vector DB Tools (4)
| Tool | Description |
|------|-------------|
| `export_to_weaviate` | Format for Weaviate |
| `export_to_chroma` | Format for Chroma |
| `export_to_faiss` | Format for FAISS |
| `export_to_qdrant` | Format for Qdrant |

### MCP Setup

`setup_mcp.sh` auto-detects installed agents and configures transport:

| Agent | Config Path | Transport |
|-------|-------------|-----------|
| Claude Code | `~/.claude.json` | stdio |
| VS Code + Cline | `~/.config/Code/...cline_mcp_settings.json` | stdio |
| Cursor | `~/.cursor/mcp_settings.json` | HTTP |
| Windsurf | `~/.windsurf/...` | HTTP |
| IntelliJ IDEA | `mcp.xml` in JetBrains dir | HTTP |

---

## 3. CLI Commands

### All Subcommands

| Command | Description |
|---------|-------------|
| `scrape` | Scrape a documentation website |
| `github` | Scrape a GitHub repository |
| `pdf` | Extract from PDF files |
| `unified` | Multi-source scraping (docs + GitHub + PDF) |
| `analyze` | Analyze local codebase |
| `enhance` | AI-powered local enhancement |
| `enhance-status` | Check enhancement status |
| `package` | Package skill into .zip |
| `upload` | Upload skill to platform |
| `estimate` | Estimate page count |
| `extract-test-examples` | Extract usage examples from tests |
| `install-agent` | Install skill to AI agent directories |
| `install` | Full pipeline: fetch → scrape → enhance → package → upload |
| `config` | Configure tokens, API keys, settings |
| `resume` | Resume interrupted scraping |
| `stream` | Streaming ingestion |
| `update` | Incremental updates |
| `multilang` | Multi-language support |
| `quality` | Quality metrics |

### Key Flags for `scrape`

**Configuration:**
- `url` (positional) — Base documentation URL
- `--config` / `-c` — Load config from JSON file
- `--name` — Skill name
- `--description` / `-d` — Skill description
- `--interactive` / `-i` — Interactive mode

**Scraping control:**
- `--max-pages` — Maximum pages
- `--skip-scrape` — Use existing data
- `--dry-run` — Preview only
- `--resume` — Resume from checkpoint
- `--fresh` — Clear checkpoint, start fresh

**Performance:**
- `--async` — Async mode (2-3x faster)
- `--workers` / `-w` — Parallel workers (max 10)
- `--rate-limit` / `-r` — Delay between requests
- `--no-rate-limit` — Disable rate limiting

**Enhancement:**
- `--enhance` — Enhance using Claude API (needs `ANTHROPIC_API_KEY`)
- `--enhance-local` — Enhance using local Claude CLI (no API cost)
- `--interactive-enhancement` — Open terminal window
- `--api-key` — Anthropic API key

**RAG chunking (v2.10.0+):**
- `--chunk-for-rag` — Enable semantic chunking
- `--chunk-size` — Target tokens per chunk (default: 512)
- `--chunk-overlap` — Overlap (default: 50)

### The `--target` Flag

On `package` and `install` commands:

```
--target [claude|gemini|openai|markdown]   (default: "claude")
```

- **claude** — ZIP with SKILL.md + references/ (YAML frontmatter)
- **gemini** — tar.gz with system_instructions.md + gemini_metadata.json
- **openai** — ZIP (OpenAI Assistants format)
- **markdown** — Universal markdown export

---

## 4. The `--enhance-local` Mechanism

Lives in `src/skill_seekers/cli/enhance_skill_local.py`. Does NOT call any cloud API.

### How It Works

1. Reads all reference files from the skill directory
2. Synthesizes a detailed prompt file (current SKILL.md + source analysis + instructions)
3. Spawns a subprocess calling the local `claude` binary (Claude Code Max)
4. Local agent rewrites SKILL.md based on the prompt (~75 → ~500+ lines)

### Supported Local Agents

```
--agent [claude|codex|copilot|opencode|custom]
```

| Agent | Command |
|-------|---------|
| `claude` (default) | `claude {prompt_file}` |
| `codex` | `codex exec --full-auto ...` |
| `copilot` | `gh copilot chat` |
| `opencode` | `opencode` |
| `custom` | User-defined command template |

### Execution Modes

- **Headless** (default): `subprocess.run()`, 10-minute timeout
- **Background**: Threading-based, returns immediately
- **Daemon**: Fully detached via `nohup`, survives terminal close
- **Terminal**: Launches new terminal window

### Smart Summarization

For skills exceeding 30K characters, references auto-summarize to ~30% by keeping:
- First 20% (introductions)
- Up to 5 code blocks
- 10 section headings with initial paragraphs

### Safety

- Creates `SKILL.md.backup` before modification
- Status tracking via JSON files
- `--force` mode (default) skips confirmations

---

## 5. Preset Configurations

### Shipped in Repository (`configs/`)

1. `godot.json` — Godot Engine (docs + GitHub, deep code analysis)
2. `react.json` — React framework
3. `vue.json` — Vue.js
4. `django.json` — Django
5. `fastapi.json` — FastAPI
6. `ansible-core.json` — Ansible Core
7. `claude-code.json` — Claude Code CLI itself (47 start_urls, 9 categories)
8. `blender-unified.json` — Blender (unified multi-source)
9. `astrovalley_unified.json` — AstroValley
10. `httpx_comprehensive.json` — HTTPX
11. `medusa-mercurjs.json` — Medusa/MercurJS

24+ additional presets available via the SkillSeekersWeb.com API.

### Analysis Presets (for `analyze` command)

| Preset | Depth | AI Level | Time |
|--------|-------|----------|------|
| `quick` | surface | none | 1-2 min |
| `standard` | deep | basic | 5-10 min |
| `comprehensive` | full | full AI | 20-60 min |

---

## 6. Installation

```bash
pip install skill-seekers              # CLI only
pip install skill-seekers[mcp]         # + MCP server
pip install skill-seekers[all-llms]    # + Gemini + OpenAI
pip install skill-seekers[all]         # Everything
```

### All Optional Dependency Groups

| Extra | What It Adds |
|-------|-------------|
| `mcp` | mcp, httpx, httpx-sse, uvicorn, starlette, sse-starlette |
| `gemini` | google-generativeai |
| `openai` | openai |
| `all-llms` | google-generativeai, openai |
| `s3` | boto3 |
| `gcs` | google-cloud-storage |
| `azure` | azure-storage-blob |
| `rag-upload` | chromadb, weaviate-client, sentence-transformers |
| `embedding` | fastapi, uvicorn, sentence-transformers, numpy, voyageai |
| `all` | Everything above |

---

## 7. Custom Config Example (Terraform)

```json
{
  "name": "terraform",
  "description": "HashiCorp Terraform IaC. Providers, modules, state, provisioning.",
  "base_url": "https://developer.hashicorp.com/terraform/docs",
  "selectors": {
    "main_content": "article, main, #content-area",
    "title": "h1",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": ["/terraform/docs"],
    "exclude": ["/terraform/tutorials", "/blog", "/changelog"]
  },
  "categories": {
    "getting_started": ["intro", "install", "getting-started"],
    "configuration": ["configuration", "settings", "backend"],
    "providers": ["providers", "registry"],
    "modules": ["modules"],
    "state": ["state", "remote-state"],
    "cli": ["cli", "commands"]
  },
  "rate_limit": 0.5,
  "max_pages": 500
}
```

```bash
skill-seekers scrape --config configs/terraform.json --enhance-local
skill-seekers package output/terraform/ --target claude
```

### Multi-Source (Unified) Config

```json
{
  "name": "terraform",
  "merge_mode": "claude-enhanced",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://developer.hashicorp.com/terraform/docs",
      "max_pages": 500
    },
    {
      "type": "github",
      "repo": "hashicorp/terraform",
      "enable_codebase_analysis": true,
      "code_analysis_depth": "deep",
      "fetch_issues": true,
      "max_issues": 100
    }
  ]
}
```

### Config Resolution Order

1. Exact file path
2. `./configs/` (current directory)
3. `~/.config/skill-seekers/configs/`
4. SkillSeekersWeb.com API (community presets)
5. Registered git-based config sources

---

## 8. Source Code Layout

```
src/skill_seekers/
  __init__.py
  _version.py
  py.typed
  cli/                   # 67 files + 3 subdirectories
    main.py              # CLI entry point (click-based)
    doc_scraper.py       # scrape command
    github_scraper.py    # github command
    pdf_scraper.py       # pdf command
    enhance_skill_local.py  # --enhance-local
    package_skill.py     # package command
    upload_skill.py      # upload command
    install_skill.py     # install (full pipeline)
    install_agent.py     # install-agent command
    adaptors/
      base.py            # SkillAdaptor ABC
      claude.py          # Claude ZIP packaging
      gemini.py          # Gemini tar.gz packaging
      openai.py          # OpenAI packaging
      markdown.py        # Universal markdown
      langchain.py       # LangChain format
      llama_index.py     # LlamaIndex format
      haystack.py        # Haystack format
      weaviate.py        # Weaviate format
      chroma.py          # Chroma format
      faiss_helpers.py   # FAISS format
      qdrant.py          # Qdrant format
  mcp/
    server.py            # Legacy MCP server (18 tools)
    server_fastmcp.py    # FastMCP server (25 tools)
    agent_detector.py    # Auto-detect installed agents
    source_manager.py    # Config source management
    git_repo.py          # Git operations
    tools/
      config_tools.py
      scraping_tools.py
      packaging_tools.py
      splitting_tools.py
      source_tools.py
      vector_db_tools.py
  benchmark/
  embedding/
  sync/
```

---

## How This Fits Our Agent Framework

### Immediate Value

1. **Generate tool skills on demand**: Scrape any tool's docs and produce a
   Claude-ready skill in ~20-45 minutes.
2. **MCP server integration**: Add Skill Seekers' 25 MCP tools to our agent's
   config, enabling it to self-serve skill generation.
3. **Local enhancement via Claude Code**: No API costs if on Max plan — the
   `--enhance-local` flag uses the local CLI binary.

### Integration Points

```
.agent-context/          ← Our framework config
~/.claude/skills/        ← Where Skill Seekers installs generated skills
~/.claude.json           ← MCP server registration (auto-configured by setup_mcp.sh)
```

### Recommended Workflow

```bash
# One-time: Install with MCP support
pip install skill-seekers[mcp]
bash setup_mcp.sh

# Per-tool: Generate and install a skill
skill-seekers install --config terraform --enhance-local
# → scrapes docs → enhances → packages → installs to ~/.claude/skills/terraform/

# Or use MCP from within Claude Code:
# "Generate a skill for the Slack API"  ← agent calls install_skill MCP tool
```

### Security Considerations

- Skill Seekers spawns subprocesses (`claude` CLI) — runs with your user privileges
- Downloaded content is not sandboxed — malicious docs could inject prompt content
- Config files support arbitrary CSS selectors — validate before using community configs
- The `--no-rate-limit` flag can trigger rate limiting or IP bans on target sites
