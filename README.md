# OpenCode Configuration

A configuration for [OpenCode](https://opencode.ai) — an AI-powered coding assistant — with structured agent capabilities, LSP integration, and secure tool permissions.

---

## Features

- **Agent system**: Specialized sub-agents for cleanup, refactor, and review
- **Local docs**: Python development standards in `docs/` — style, testing, typing, tooling
- **Skills pipeline**: Skills in `skills/` — cleanup → refactor → review
- **LSP integration**: Pyright and Ruff (Python), TypeScript, YAML, and Bash language servers
- **MCP servers**: Web search (`ddg_search`), network automation (`nornir`), docs lookup (`context7`), codebase context (`repomix`)
- **Auto-formatting**: `ruff` for Python, `prettier` for JS/TS/JSON/Markdown/YAML
- **Security-first permissions**: Deny rules for secret files (`.env`, `.pem`, `.key`, `.secret`, `*credentials*`)

---

## Quick Start

```bash
git clone <this-repo> ~/.config/opencode
```

---

## Key Files

| Path              | Purpose                                                                                |
| ----------------- | -------------------------------------------------------------------------------------- |
| `opencode.json`   | Main config — providers, LSP, MCP, permissions, formatters                             |
| `AGENTS.md`       | Base instructions — discovery, planning, execution, security                           |
| `agents/*.md`     | Specialized sub-agent definitions                                                      |
| `skills/`         | Local skills — reusable skill capabilities (cleanup, refactor, review, etc.)           |
| `commands/`       | Custom slash commands (`/analyze-library`, `/review-structure`, etc.)                  |
| `docs/`           | Python development standards — style, testing, typing, tooling, security               |

---

## Requirements

- [OpenCode](https://opencode.ai) — the agent runtime
- Node.js (for formatters) — `node` in `$PATH`
- Optional: `uv`, `ruff`, `prettier` — used by formatters and skills
