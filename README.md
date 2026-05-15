# opencode — Configuration

![Python](https://img.shields.io/badge/python-3.12+-blue.svg) ![Tooling](https://img.shields.io/badge/tooling-uv%20%7C%20ruff-orange.svg) ![opencode](https://img.shields.io/badge/opencode-powered-black.svg) ![Docs](https://img.shields.io/badge/docs-opencode.ai-blueviolet.svg) ![Maintenance](https://img.shields.io/badge/maintenance-active-brightgreen.svg)

Personal [opencode](https://opencode.ai) configuration — rules, skills, agents, and behavior guidelines for Python development.

## Architecture

### Tier 1: Always-On Constraints

- **Path:** Global persona settings via `~/.config/opencode/AGENTS.md`
- **Behavior:** Auto-loaded at startup
- **Purpose:** Engineering lifecycle, security rules, authority boundaries, mandatory output structure

### Tier 2: Domain-Specific Rules

- **Path:** Global rule settings via `~/.config/opencode/rules/*.md`
- **Behavior:** Loaded alongside `AGENTS.md` as instruction
- **Purpose:** Personal preferences, testing standards, git conventions, and etc

### Tier 3: Actionable Skills

- **Path:** Domain-specific skill definitions via `~/.config/opencode/skills/`
- **Behavior:** Invoked via `skill` tool on intent match or explicit request
- **Purpose:** Reusable step-by-step procedures (code-cleanup, code-refactor, code-review, docker, mcp-builder, pdf-processing, ddg-search, repomix)

### Tier 4: Specialized Subagents

- **Path:** Domain-specific agent definitions via `~/.config/opencode/agents/`
- **Behavior:** Spawned via `@cleanup`, `@refactor`, or `@review` tools for isolated subtasks
- **Purpose:** Focused agents (cleanup, refactor, review) with defined skills and constraints

---

## opencode.json — Configuration Deep Dive

Every opencode instance starts by reading `opencode.json` to understand what tools, models, and permissions are available. Here's what each section does and why I configured it this way.

### `$schema` — The Safety Net

```json
"$schema": "https://opencode.ai/config.json"
```

This tells your IDE (VS Code, etc.) the shape of valid configuration. You'll get autocomplete and inline validation when editing the file. It's optional but incredibly helpful for catching typos before runtime.

### `instructions` — Loading Your Rules

```json
"instructions": ["~/.config/opencode/rules/*.md"]
```

This glob pattern loads every rule file in your `rules/` directory at startup. Think of it as injecting your personal preferences directly into the agent's context. Mine includes Python tooling standards, testing requirements, git conventions, and web search behavior.

**Why not list them individually?** Using `*.md` means any new rule file automatically gets picked up—no config edits required when you add a new domain.

### `default_agent` & `small_model` — Choosing the Right Tool

```json
"default_agent": "plan",
"small_model": "opencode/big-pickle"
```

- **`default_agent: plan`** — When you don't specify which agent to use, `plan` handles it. This is your general-purpose workhorse.

- **`small_model`** — For quick, isolated tasks (e.g., "find all occurrences of X"), this lightweight model keeps latency low and cost minimal. It's also what powers the explore subagent.

### `agent` — Task-Specific Model Routing

```json
"agent": {
  "build": { "model": "bifrost/gemini/gemma-4-31b-it" },
  "plan": { "model": "opencode/minimax-m2.5-free" }
}
```

Different tasks need different capabilities. My `build` agent gets the heavyweight Gemma-4-31b for complex implementation work, while `plan` uses MiniMax for reasoning and planning. This separation keeps costs in check—you don't need a 31B model to decide _what_ to build.

### `formatter` — On-Save Auto-Formatting

```json
"formatter": {
  "prettier": { "extensions": [".ts", ".js", ".json", ".md", ...] },
  "uv": { "extensions": [".py", ".pyi"] }
}
```

When you save a file, opencode checks its extension and runs the appropriate formatter. No more arguing about tabs vs spaces or imports ordering—it's handled automatically.

- **Prettier** — Web stack (TypeScript, JavaScript, YAML, HTML...)
- **Ruff** — Python via `uv run ruff format` for consistent formatting + linting in one pass

### `permission` — Security Boundaries

```json
"permission": {
  "read": { "*": "allow", "*.env": "deny", "*.pem": "deny", ... },
  "write": { ...same rules... }
}
```

This is your security layer. The agent can read/write anywhere by default, except:

- **Secrets files:** `*.env`, `*.pem`, `*.key`, `*.secret`, `*credentials*` — blocked to prevent accidental exposure
- **`*.env.example`: allow** — Templates are safe to read (and write, for new projects)

The read and write rules are identical here—you generally don't want the agent modifying your secrets either.

### `mcp` — External Tool Integrations

```json
"mcp": {
  "duck": { "type": "local", "command": ["web-search-mcp"], "enabled": true },
  "nornir": { "type": "local", "command": ["nornir-mcp"], "enabled": true },
  "Bifrost": { "type": "remote", "url": "http://localhost:8080/mcp", "enabled": true }
}
```

MCP (Model Context Protocol) brings external capabilities into opencode:

| Tool        | Type   | Purpose                                |
| ----------- | ------ | -------------------------------------- |
| **duck**    | Local  | Web search & live data retrieval       |
| **nornir**  | Local  | Network automation & device management |
| **Bifrost** | Remote | Custom LLM backend (local GPU serving) |

The `enabled: true` flag means these load automatically at startup. `type: local` spawns the process; `type: remote` connects to an already-running server.

### `lsp` — Language Server Protocol

```json
"lsp": {
  "pyright": { "command": ["pyright-langserver", "--stdio", "--no-implicit-any"] },
  "yaml-ls": { "command": ["yaml-language-server", "--stdio"] },
  "bash": { "command": ["bash-language-server", "start"] }
}
```

Language servers provide real-time diagnostics, goto-definition, and autocomplete. My setup:

- **pyright** with `--no-implicit-any` — Strict Python type checking (no `Any` implied)
- **yaml-ls** — YAML validation for configs
- **bash-language-server** — Shell script support

### `provider` — LLM Backends

```json
"provider": {
  "bifrost": {
    "npm": "@ai-sdk/openai-compatible",
    "options": { "baseURL": "http://localhost:8080/v1" },
    "models": { ... }
  }
}
```

This defines where your models actually come from. I'm using Bifrost (a self-hosted OpenAI-compatible server) running locally on port 8080. The `models` map gives each model a friendly alias for display in logs and UI.

---

**How to override per-project:** Drop an `opencode.json` in your project root and it merges with (or replaces) these global defaults. Priority: global → project.

---

## Directory Structure

```
~/.config/opencode/
├── AGENTS.md           # Core engineering mandates (auto-loaded)
├── opencode.json       # Provider, MCP, LSP, permissions
├── .opencodeignore     # Context exclusions
├── rules/               # Domain-specific rules
│   ├── python_tools.md
│   └── git_rules.md
├── skills/             # Intent-based workflows
│   ├── code-cleanup/
│   ├── code-refactor/
│   ├── code-review/
│   ├── docker-expert/
│   ├── mcp-builder/
│   ├── pdf-processing/
│   ├── python-rules/
│   ├── python-testing/
│   ├── ddg-search/
│   └── repomix/
└── agents/
    ├── cleanup.md
    ├── refactor.md
    ├── research.md
    └── review.md
```

---

## Operational Workflows

### Loading a skill

```bash
Invoke the `code-cleanup` skill on the changed files.
```

### Running a code review

```bash
Use the `review` subagent to analyze the current diff.
```

### Security scanning

```bash
uv run safety scan
uv run bandit -r src/
```

---

## Configuration Resolution

| Priority | Scope   | Location                     | Purpose                       |
| :------- | :------ | :--------------------------- | :---------------------------- |
| 1        | Config  | `~/.config/opencode/`        | Personal style, safety, tools |
| 2        | Project | `./opencode.json` (optional) | Project-level overrides       |

---

## Maintenance

- **License:** ![License](https://img.shields.io/badge/license-MIT-blue.svg)
- **Stack:** `uv`, `ruff`, `pyright`, `pytest`, `mypy`
- **Tracking:** All config changes versioned via git
