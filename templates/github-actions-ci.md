---
name: github-actions-ci
description: GitHub Actions CI/CD workflow for Python projects with uv, ruff, mypy, pytest, and security scanning
---

# GitHub Actions CI

Place this at `.github/workflows/ci.yml` in your project. Runs lint, test, security, and build jobs with uv caching and Python matrix.

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  UV_CACHE_DIR: /tmp/.uv-cache

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
          cache-dependency-glob: "uv.lock"

      - name: Set up Python
        run: uv python install

      - name: Install dependencies
        run: uv sync --locked --all-extras --dev

      - name: Lint with ruff
        run: uv run ruff check .

      - name: Check formatting with ruff
        run: uv run ruff format --check .

      - name: Type check with mypy
        run: uv run mypy src/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v6

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
          cache-dependency-glob: "uv.lock"

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --locked --all-extras --dev

      - name: Run tests
        run: uv run pytest --cov=src --cov-branch --cov-report=xml --cov-report=term-missing

      - name: Upload coverage
        uses: codecov/codecov-action@v5
        with:
          files: ./coverage.xml
          fail_ci_if_error: false

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
          cache-dependency-glob: "uv.lock"

      - name: Set up Python
        run: uv python install

      - name: Install dependencies
        run: uv sync --locked --all-extras --dev

      - name: Security scan with bandit
        run: uv run bandit -r src/ || true

      - name: Dependency scan with safety
        run: uv run safety check || true

      - name: Project dependency scan
        run: uv run uv-secure scan || true

  build:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: [lint, test, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
          cache-dependency-glob: "uv.lock"

      - name: Set up Python
        run: uv python install

      - name: Build package
        run: uv build

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

## Structure

| Job        | Runs on      | Purpose                                                            |
| ---------- | ------------ | ------------------------------------------------------------------ |
| `lint`     | push/PR      | ruff check + format check + mypy                                   |
| `test`     | push/PR      | pytest with coverage, matrix across 3.10–3.12                      |
| `security` | push/PR      | bandit + safety + uv-secure                                        |
| `build`    | push to main | uv build + artifact upload (blocked until lint/test/security pass) |

## Cache Notes

Uncached CI runs take ~60s for a small project. With uv caching enabled via `setup-uv`, subsequent runs complete in ~20s on cache hit.
