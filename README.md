# OpenCode Configuration

A configuration for [OpenCode](https://opencode.ai) — an AI-powered coding assistant — with structured agent capabilities, LSP integration, and secure tool permissions.

---

## Features

- **Agent system**: Specialized sub-agents for cleanup, refactor, and review
- **External docs**: Instructions loaded from `~/.claude/docs/index.md` via `opencode.json`
- **Skills pipeline**: Symlinked from `~/.claude/skills` — cleanup → refactor → review
- **LSP integration**: Pyright (Python), YAML, and Bash language servers
- **MCP servers**: Web search (`ddg_search`) and network automation (`nornir`)
- **Auto-formatting**: `ruff` for Python, `prettier` for JS/TS/JSON/Markdown/YAML
- **Security-first permissions**: Granular allow/deny/ask rules for bash, edit, and read operations

---

## Quick Start

```bash
git clone <this-repo> ~/.config/opencode
```

---

## Key Files

| Path              | Purpose                                                                          |
| ----------------- | -------------------------------------------------------------------------------- |
| `opencode.json`   | Main config — providers, LSP, MCP, permissions, formatters                       |
| `AGENTS.md`       | Base instructions — discovery, planning, execution, security                     |
| `agents/*.md`     | Specialized sub-agent definitions                                                |
| `skills/`         | Symlink to `~/.claude/skills` — reusable skill capabilities                      |
| `~/.claude/docs/` | External docs referenced by `opencode.json` — Python standards, testing, tooling |

---

## Requirements

- [OpenCode](https://opencode.ai) — the agent runtime
- Node.js (for formatters) — `node` in `$PATH`
- Optional: `uv`, `ruff`, `prettier` — used by formatters and skills
