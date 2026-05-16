# OpenCode Configuration

Personal OpenCode config at `~/.config/opencode/`.

## Structure

```
~/.config/opencode/
├── opencode.json         # Provider, MCP, LSP, permissions, instructions
├── AGENTS.md             # Session-critical context (always loaded)
├── README.md             # This file
├── rules/                # Always-on constraints
├── agents/               # Subagent definitions with permissions
├── skills/               # On-demand invokable workflows
└── .opencodeignore
```

## Key Config Points

- **Providers**: Bifrost (local proxy to Gemini/Mistral models)
- **MCP servers**: ddg_search, nornir, Bifrost, repomix
- **LSP**: pyright, yaml-ls, bash-language-server
- **Formatters**: prettier (JS/TS/JSON/MD/YAML), ruff (Python)

## Agent Model Assignments

| Agent               | Model                           |
| ------------------- | ------------------------------- |
| build (primary)     | opencode/minimax-m2.5-free      |
| plan (primary)      | opencode/nemotron-3-super-free  |
| research (subagent) | opencode/deepseek-v4-flash-free |
| cleanup (subagent)  | opencode/deepseek-v4-flash-free |
| refactor (subagent) | opencode/minimax-m2.5-free      |
| review (subagent)   | opencode/deepseek-v4-flash-free |

## Skills Auto-Discovery

All skills under `skills/` are auto-discovered by OpenCode. The `python-testing`
skill was promoted from a rule — invoke it explicitly for full test patterns.
