# OpenCode Configuration

A configuration for [OpenCode](https://opencode.ai) — an AI-powered coding assistant — with structured agent capabilities, LSP config for the future V2 runtime, and secure tool permissions.

---

## Features

- **Agent system**: Specialized sub-agents for cleanup, refactor, and review
- **Local docs**: Python development standards in `docs/` — style, testing, typing, tooling
- **Skills pipeline**: Skills in `skills/` — cleanup → refactor → review
- **LSP config**: Pyright, Ruff, TypeScript, YAML, and Bash server entries — reserved for the future V2 runtime (accepted, not yet executed)
- **MCP servers**: Web search (`research`), docs lookup (`context7`), codebase context (`repomix`)
- **Formatter config**: `uv run ruff format` for Python, `prettier` for JS/TS/JSON/Markdown/YAML — reserved for the future V2 runtime (accepted, not yet executed)
- **Security-first permissions**: Deny rules for secret files (`.env`, `.pem`, `.key`, `.secret`, `*credentials*`)

---

## Quick Start

```bash
git clone <this-repo> ~/.config/opencode
```

---

## Key Files

| Path            | Purpose                                                                      |
| --------------- | ---------------------------------------------------------------------------- |
| `opencode.json` | Main config — LSP, MCP, permissions, formatters                              |
| `AGENTS.md`     | Base instructions — discovery, planning, execution, security                 |
| `skills/`       | Local skills — reusable skill capabilities (cleanup, refactor, review, etc.) |
| `commands/`     | Custom slash commands (`/analyze-library`, `/review-structure`, etc.)        |
| `docs/`         | Python development standards — style, testing, typing, tooling, security     |

---

## Requirements

- [OpenCode](https://opencode.ai) — the agent runtime
- Node.js (for formatters) — `node` in `$PATH`
- Optional: `uv`, `ruff`, `prettier` — used by formatters and skills
