# opencode — Configuration

Personal [opencode](https://opencode.ai) configuration — rules, skills, agents, and behavior guidelines for Python development.

## Architecture

### Tier 1: Always-On Constraints

- **Path:** `~/.config/opencode/AGENTS.md`
- **Behavior:** Auto-loaded via `opencode.json` → `instructions`
- **Purpose:** Engineering lifecycle, security rules, authority boundaries, mandatory output structure

### Tier 2: Domain-Specific Rules

- **Path:** `~/.config/opencode/rule/`
- **Behavior:** Loaded alongside AGENTS.md as instruction files
- **Purpose:** Python toolchain (`uv`, `ruff`, `pyright`, `pytest`), testing standards, git conventions, web search

### Tier 3: Actionable Skills

- **Path:** `~/.config/opencode/skills/`
- **Behavior:** Invoked via `skill` tool on intent match
- **Purpose:** Reusable step-by-step procedures (code-cleanup, code-refactor, code-review, docker, mcp-builder, pdf-processing, web-search)

### Tier 4: Specialized Subagents

- **Path:** `~/.config/opencode/agents/`
- **Behavior:** Spawned via `task` tool for isolated subtasks
- **Purpose:** Focused agents (code-reviewer) with defined skills and constraints

---

## Directory Structure

```
~/.config/opencode/
├── AGENTS.md           # Core engineering mandates (auto-loaded)
├── opencode.json       # Provider, MCP, LSP, permissions
├── .opencodeignore     # Context exclusions
├── rule/               # Domain-specific rules
│   ├── python_tools.md
│   ├── testing_rules.md
│   ├── git_rules.md
│   └── web_search.md
├── skills/             # Intent-based workflows
│   ├── code-cleanup/
│   ├── code-refactor/
│   ├── code-review/
│   ├── docker-expert/
│   ├── mcp-builder/
│   ├── pdf-processing/
│   └── web-search/
└── agents/
    └── code-reviewer.md
```

---

## Operational Workflows

### Loading a skill

```bash
Invoke the `code-cleanup` skill on the changed files.
```

### Running a code review

```bash
Use the code-reviewer subagent to analyze the current diff.
```

### Security scanning

```bash
uv run safety check
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

- **License:** MIT
- **Stack:** `uv`, `ruff`, `pyright`, `pytest`, `mypy`
- **Tracking:** All config changes versioned via git
