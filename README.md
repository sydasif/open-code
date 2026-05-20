# Opencode Python Setup

A customized Opencode environment optimized for professional Python development.

## Structure

```
~/.config/opencode/
├── opencode.json                 # Main configuration
├── AGENTS.md                     # Core agent guidelines
├── README.md
├── rules/                        # Language-specific rules
│   ├── python-style.md
│   └── python-testing.md
├── agents/                       # Subagent definitions
│   ├── research.md
│   ├── cleanup.md
│   ├── refactor.md
│   └── review.md
└── skills/                       # Specialized workflows
    ├── code-cleanup/
    ├── code-refactor/
    ├── code-review/
    ├── ddg-search/
    ├── mcp-builder/
    └── repomix/
```

## Core Components

### Agents

Defined in `agents/`, these agents handle specialized tasks:

- **Research**: Deep-dive exploration and documentation lookup.
- **Cleanup**: Applying YAGNI, DRY, and KISS principles.
- **Refactor**: Modernizing legacy Python code.
- **Review**: Final-gate verification of completed changes.

### Skills

On-demand invokable workflows in `skills/` that provide specialized instructions and bundled scripts.

### Rules

Located in `rules/`, providing strict guidelines for Python style, toolchain usage, and testing standards.

## Configuration

The setup is driven by `opencode.json`, which manages:

- **Model Assignments**: Different models for different agent roles.
- **Toolchain Integration**: Configured formatters (e.g., `uv` with `ruff`).
- **Permission System**: Granular control over file access and bash commands.

## Adaptation

To adapt this setup for another language:

1. Replace `rules/*.md` with language-specific style and testing guides.
2. Update `skills/` with relevant workflows.
3. Configure `opencode.json` with the appropriate toolchain and models.
