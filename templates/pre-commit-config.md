---
name: pre-commit-config
description: Pre-commit hooks configuration for Python projects with ruff, mypy, bandit, safety, and pytest
---

# .pre-commit-config.yaml

Pre-commit hooks configuration that runs ruff (lint+format), mypy, bandit, safety, and core checks on every commit. Place this at your project root.

```yaml
default_language_version:
  python: python3

repos:
  # Core pre-commit hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ["--maxkb=500"]
      - id: check-merge-conflict
      - id: detect-private-key
      - id: check-toml
      - id: check-vcs-permalinks
      - id: debug-statements

  # Ruff for linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # MyPy for type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy
        args: [--strict]
        additional_dependencies: [types-all]

  # Bandit for security scanning
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.2
    hooks:
      - id: bandit
        args: [-ll, -r, src/]
        types: [python]

  # Safety for dependency vulnerability scanning
  - repo: https://github.com/pyupio/safety-pre-commit
    rev: v1.2.2
    hooks:
      - id: safety-db-update
      - id: safety
        additional_dependencies: [django]

  # Pytest for running tests (optional - usually run separately)
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: uv run pytest
        language: system
        types: [python]
        pass_filenames: false
        stages: [commit]
```

## Setup

```bash
# Install pre-commit
uv add --dev pre-commit

# Install the git hooks
pre-commit install

# Run on all files once to verify
pre-commit run --all-files
```

## Commands

| Command                      | Purpose                        |
| ---------------------------- | ------------------------------ |
| `pre-commit install`         | Install hooks (once per clone) |
| `pre-commit run --all-files` | Run all hooks on all files     |
| `pre-commit run <hook-id>`   | Run a single hook              |
| `pre-commit autoupdate`      | Update hook versions           |
| `git commit --no-verify`     | Skip hooks (emergency only)    |
