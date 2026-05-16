# Customizing Opencode for Professional Python Development: My Setup and Why It Works

## Introduction

As a Python developer, I've always sought tools that enhance productivity without compromising code quality. When I discovered Opencode, I was impressed by its flexibility and decided to customize it specifically for Python development.

While this guide focuses on Python customization, the same approach serves as a template that can be adapted for any programming language — simply adjust the toolchain, formatting rules, and testing standards to match your target language.

The same style and testing rules work seamlessly with Claude Code as well, providing a consistent development experience across both platforms. In this post, I'll share my setup, explaining each component and how it contributes to a superior development experience.

## Project Structure

Here's the complete file structure of my customized Opencode Python setup:

```
~/.config/opencode/
├── opencode.json                 # Main configuration file
├── AGENTS.md                     # Agent instructions
├── README.md
├── rules/
│   ├── git.md                    # Git branch naming and commit conventions
│   ├── python-style.md           # Python toolchain, style, and code rules
│   ├── python-testing.md         # Testing standards and patterns
│   └── templates.md              # Project templates reference
├── skills/
│   ├── code-cleanup/             # YAGNI/DRY/KISS cleanup workflow
│   ├── code-refactor/            # Legacy Python modernization
│   ├── code-review/              # Final-gate review workflow
│   ├── ddg-search/               # Web search via DuckDuckGo
│   ├── mcp-builder/              # MCP server creation guide
│   ├── python-testing/           # Testing patterns and coverage
│   └── repomix/                  # Codebase packaging tool
└── templates/                    # Project scaffolding templates
```

This structure serves as a template adaptable to any programming language. Simply replace the language-specific components — rules like `python-style.md`, `python-testing.md`, and the Python toolchain in `opencode.json` — with equivalents for your target language (e.g., `javascript-style.md`, `go-testing.md`, etc.).

## Directory Components Explained

### AGENTS.md

The `AGENTS.md` file defines the core agent guidelines for the Opencode system:

- **Mandate**: Discover → Plan → Execute → Verify
- **Authority**: Proceed & Notify (refactoring, deps, tests) / Propose & Wait (architecture, APIs, new deps) / Do Not Touch (secrets, CI/CD, destructive ops)
- **Process**: Surface assumptions → search patterns → read rules → plan (with non-goals + rollback path) → execute one module per pass (skill chain: @cleanup → @refactor → @review)
- **Always-On Rules**: References `@rules/python-style.md`, `@rules/python-testing.md`, `@rules/git.md`
- **Required Output**: Discovery Report, Strategic Plan, Assumptions & Risks, Proposed Changes, Skipped Candidates, Verification Pyramid
- **Halt & Escalate**: Security vulnerabilities, scope exceeding 5 extra files, contradictory requirements, bypassing architecture, destructive ops, subagent conflicts

### agents/ Directory

Contains subagent definitions, each with its own model assignment, permissions, and invocation instructions:

- `research.md` — Deep-dive research using web search and codebase exploration. Read-only agent (`model: deepseek-v4-flash-free`) with access to `ddg-search` and `repomix` skills. Temperature: 0.2. Invoke for documentation lookups, library understanding, and cross-referencing upstream implementations.
- `cleanup.md` — Codebase cleanup applying YAGNI, DRY, and KISS principles. Edit-capable agent (`model: deepseek-v4-flash-free`) with access to `code-cleanup` skill and ruff/pytest bash permissions. Temperature: 0.1. Invoke to remove dead code, duplicated logic, and over-abstraction.
- `refactor.md` — Modernizes legacy Python code with best practices, type hints, and efficient patterns. Edit-capable agent (`model: minimax-m2.5-free`) with access to `code-refactor` skill and ruff/mypy/pytest bash permissions. Temperature: 0.3. Invoke after a cleanup pass has pruned dead code.
- `review.md` — Final-gate review of completed changes. Read-only agent (`model: deepseek-v4-flash-free`) with access to `code-review`, `ddg-search`, and `repomix` skills. Temperature: 0.2. Invoke before submitting a PR to catch errors and verify completeness.

### skills/ Directory

On-demand invokable workflows, each with specialized instructions and bundled scripts:

- `code-cleanup/` — YAGNI/DRY/KISS cleanup workflow. Removes dead code, deduplicates logic, simplifies over-engineered abstractions. Never introduces new abstractions unless they reduce maintenance cost.
- `code-refactor/` — Legacy Python modernization. Transforms code with f-strings, dataclasses, pathlib, type hints, match statements, and Python 3.10+ idioms. Establishes test baseline before changes.
- `code-review/` — Final-gate verification using fresh-eyes systematic approach. Checks correctness, public contract preservation, test integrity, and hygiene. Produces a structured report with issues, severity, and recommended actions.
- `ddg-search/` — Web search via DuckDuckGo MCP. Enables real-time searches, documentation lookups, and cross-referencing upstream implementations.
- `mcp-builder/` — Guide for creating high-quality MCP (Model Context Protocol) servers using FastMCP (Python) or MCP SDK (TypeScript). Covers tool design, error handling, resource exposure, and testing.
- `python-testing/` — Testing patterns and best practices. Covers AAA pattern, parametrized tests, property-based testing with hypothesis, test fixtures, error condition testing, and coverage thresholds (business logic ≥95%, APIs ≥90%, models ≥85%).
- `repomix/` — Codebase packaging tool. Packs directories into AI-friendly formats (XML, Markdown, JSON, Plain) with tree-sitter compression for efficient token usage.

### templates/ Directory

Ready-to-use project scaffolding templates for new Python projects:

- `github-actions-ci.md` — GitHub Actions CI/CD workflow. Runs lint (ruff), type check (mypy), test (pytest with coverage), security scan (bandit, safety, uv-secure) using `astral-sh/setup-uv` with caching.
- `pre-commit-config.md` — Pre-commit hooks configuration. Integrates ruff (linting + formatting), mypy (type checking), bandit (security), safety (dependency audit), and pytest (test validation).
- `pyproject-toml.md` — Python project configuration template. Pre-configured with ruff, mypy, pytest, coverage, bandit, and uv-secure tooling. Targets Python 3.10+.
- `readme-structure.md` — Standard README template with dev setup, testing sections, and contribution guidelines for Python projects using the uv toolchain.

With this structure in mind, let's explore why customizing Opencode is beneficial.

## Why Customize Opencode for Python?

Opencode is powerful out of the box, but its true strength lies in its configurability. By tailoring it to Python's ecosystem and best practices, I've created a development environment that:

1. Enforces consistent code style and formatting
2. Automates testing and quality checks
3. Integrates seamlessly with Python tooling (uv, ruff, mypy, pytest)
4. Provides security scanning out of the box
5. Reduces cognitive load through automation

The key takeaway is that Opencode's real power comes from its configurability. By tailoring it to your specific language and workflow needs, you can create a development environment that not only catches errors early but also makes the entire development process more enjoyable and productive.

Let's dive into the specifics of my configuration.

## Core Configuration: opencode.json

The foundation of my setup is in `opencode.json`. Here are the key sections I've customized:

### Instructions and Agents

```json
{
  "instructions": ["~/.config/opencode/rules/*.md"],
  "default_agent": "plan",
  "small_model": "opencode/big-pickle",
  "agent": {
    "build": {
      "model": "opencode/minimax-m2.5-free"
    },
    "plan": {
      "model": "opencode/nemotron-3-super-free"
    }
  }
}
```

This configuration:

- Loads all rule files from the rules directory (my Python-specific guidelines)
- Sets the default agent to "plan" for thoughtful problem-solving
- Uses different models for different tasks (smaller model for routine tasks, larger for planning)

### Python-Specific Formatters

```json
"formatter": {
  "prettier": {
    "command": ["npx", "prettier", "--write", "$FILE"],
    "extensions": [".ts", ".js", ".json", ".md", ".yaml", ".yml", ".html"]
  },
  "uv": {
    "command": ["uv", "run", "ruff", "format", "$FILE"],
    "extensions": [".py", ".pyi"]
  }
}
```

I've configured Opencode to use:

- Ruff for Python formatting (via uv run)
- Prettier for other file types
- This ensures consistent formatting across the entire project

### Permission System

```json
"permission": {
  "read": {
    "*": "allow",
    "*.env": "deny",
    // ... other sensitive file patterns
  },
  "edit": {
    "*": "allow",
    "*.env": "deny",
    // ... other sensitive file patterns
  },
  "bash": {
    "git *": "allow",
    "uv run ruff*": "allow",
    "uv run pytest*": "allow",
    "uv run mypy*": "allow",
    "ls *": "allow",
    "wc *": "allow",
    "grep *": "allow",
    // ... other allowed commands
    "*": "ask"
  }
}
```

The permission system is crucial for security:

- Allows read/edit access to most files
- Blocks access to sensitive files (.env, keys, credentials)
- Explicitly allows safe Python development commands (uv, ruff, pytest, mypy)
- Requires approval for potentially dangerous commands (curl, wget, docker)

## Python Style Rules: The Heart of the Setup

The `python-style.md` file contains my comprehensive Python development guidelines. Key aspects include:

### Required Toolchain

I standardized on these tools:

- `uv` for environment management and dependencies
- `ruff` for linting and formatting (replaces flake8, black, isort, etc.)
- `mypy` for static type checking
- `pytest` for testing
- `bandit` for security linting
- `safety` and `uv-secure` for dependency vulnerability scanning

### Standard Workflow

The configuration enforces this workflow:

```bash
uv sync                        # Install dependencies
uv run ruff check --fix .      # Lint and auto-fix
uv run ruff format .           # Format code
uv run mypy src/               # Type check (strict)
uv run pytest                  # Run tests
uv run bandit -r src/          # Security analysis
uv run safety check            # Dependency security
uv run uv-secure scan          # Project security scanning
```

This creates a reliable, repeatable process that catches issues early.

### Code Style Rules

The file details specific Python conventions:

1. **Google-Style Docstrings** - Clear, consistent documentation
2. **Strict Type Hints** - Full signatures with proper nullable types
3. **No Print in Production** - Mandatory use of logging module
4. **Explicit Error Handling** - Specific exception catching, no bare excepts
5. **PEP 8 Naming** - snake_case for functions/variables, PascalCase for classes
6. **Import Organization** - Standard library → third-party → local application
7. **Modern Python Features** - f-strings, pathlib, dataclasses, match/case, etc.
8. **Async Patterns** - Proper async/await usage, no asyncio.run() in libraries
9. **Security Practices** - Environment variables for secrets, parameterized queries
10. **Performance Guidelines** - Appropriate data structures and algorithms
11. **Dependency Management** - Exclusive use of uv, regular updates

## Testing Standards: python-testing.md

My testing configuration ensures high-quality, reliable tests:

### Core Principles

- Use pytest exclusively
- Follow AAA pattern (Arrange → Act → Assert)
- Tests must be fully independent
- Coverage targets: business logic ≥95%, APIs ≥90%, models ≥85%

### Test Patterns

The file provides examples of:

- Basic unit tests
- Parametrized tests
- Property-based testing with hypothesis
- Tests with fixtures
- Error condition testing
- Security testing patterns

### Testing Commands

Standardized commands for running tests:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-branch --cov-fail-under=85

# Show missing coverage lines
uv run pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
```

## MCP Servers: Extending Functionality

I've integrated several MCP (Model Context Protocol) servers to extend Opencode's capabilities:

### DuckDuckGo Search (`ddg_search`)

Enables real-time web searches for documentation and current information.

### Nornir (`nornir`)

For network automation tasks when working with network-related Python projects.

### Bifrost (`Bifrost`)

Provides access to various language models for enhanced AI capabilities.

### Repomix (`repomix`)

Packages codebases into AI-friendly formats for analysis and sharing.

## Benefits of This Setup

After implementing this configuration, I've experienced several benefits:

Customizing Opencode for Python development has transformed my workflow. By integrating Python-specific tooling, enforcing quality standards, and automating routine tasks, I've created an environment where I can focus on solving problems rather than managing tooling.

The investment in setting up a proper development environment pays dividends in code quality and developer satisfaction.

### Improved Code Quality

- Consistent formatting eliminates style debates
- Early bug detection through linting and type checking
- Comprehensive test coverage reduces regressions
- Security scanning catches vulnerabilities before they reach production

### Increased Productivity

- Automated workflows reduce manual steps
- Clear guidelines decrease decision fatigue
- Integrated tooling eliminates context switching
- Pre-configured permissions improve safety

### Better Collaboration

- Standardized setup makes onboarding easier
- Consistent code style improves readability
- Shared quality standards reduce review friction
- Clear documentation of expectations

## How to Adapt This Setup

If you'd like to implement a similar configuration for any programming language, here are the steps:

1. **Install Opencode** if you haven't already

2. **Create the rules directory** and add:
   - `[language]-style.md` (e.g., `python-style.md`, `javascript-style.md`, `rust-style.md` — based on my Python style guide above as a template)
   - `[language]-testing.md` (e.g., `python-testing.md`, `go-testing.md` — based on my Python testing standards above as a template)
   - Other rule files as needed (git.md, templates.md)

3. **Configure opencode.json** with:
   - Your preferred models
   - Formatters for your language (e.g., ruff for Python, prettier for JavaScript, rustfmt for Rust)
   - Appropriate permission settings
   - MCP servers you want to use

4. **Install the required tools** for your language:
   - Package manager (uv for Python, npm for JS, cargo for Rust)
   - Linter/formatter (ruff, eslint, clippy)
   - Type checker (mypy for Python, tsc for TypeScript, rust-analyzer for Rust)
   - Test runner (pytest, vitest, cargo test)
   - Security scanner (bandit, eslint-plugin-security, cargo-audit)
   - Any MCP servers you want to use

5. **Test the setup** on a project to ensure everything works correctly

You can also fork the GitHub repository at [https://github.com/sydasif/open-code.git](https://github.com/sydasif/open-code.git) and amend or add files according to your specific needs. This gives you a ready-to-use starting point that you can customize further for your particular workflow.

I encourage you to experiment with this template in your own projects. Start with the basics—formatters and linters—and gradually add more sophisticated features like type checking, testing integration, and security scanning. Fork the repository, swap the language-specific pieces, and make it your own.

## Conclusion

Have you customized Opencode for your development workflow? I'd love to hear about your setup and any tips you've discovered along the way!
