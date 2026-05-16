---
name: pyproject-toml
description: Python project configuration template with ruff, mypy, pytest, coverage, and security tooling
---

# pyproject.toml

Standardized project configuration for Python projects. Drop this into your project root and customize.

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "your-project-name"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = []
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

# Dependencies
dependencies = [
    # Add your runtime dependencies here
    # example: "requests>=2.25.1",
]

[project.optional-dependencies]
dev = [
    "uv>=0.4.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "bandit>=1.8.0",
    "safety>=3.0.0",
    "uv-secure>=0.1.0",
    "pre-commit>=3.0.0",
]

[tool.uv]
dev-dependencies = [
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "bandit>=1.8.0",
    "safety>=3.0.0",
    "uv-secure>=0.1.0",
    "pre-commit>=3.0.0",
]

[tool.ruff]
line-length = 88
target-version = "py310"
select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "W",      # pycodestyle warnings
    "I",      # isort
    "C90",    # mccabe
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "YTT",    # trytond-yaml-templates
    "RET",    # return
    "RUF",    # ruff-specific
    "DTZ",    # django-tz
]
ignore = [
    # Add any specific ignore rules here
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py

[tool.ruff.format]
quote-style = "double"
indent-width = 4

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = false
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true
pretty = true
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--verbose",
    "--tb=short",
    "--strict-markers",
    "--disable-warnings",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
]
minversion = "8.0"
norecursedirs = [".*^build", "dist", "_build", "htmlcov", ".mypy_cache", ".pytest_cache", ".coverage"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
branch = true
source = ["your_project_name"]  # Change to your package name
omit = [
    "*/tests/*",
    "*/migrations/*",
    "__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
show_missing = true
skip_covered = false
skip_empty = false
precision = 2

[tool.bandit]
exclude = ["tests/", "*/migrations/*"]

[tool.uv-secure]
# Configuration for uv-secure goes here
# See https://github.com/owenlamont/uv-secure for details
```

## Usage

Copy this into `pyproject.toml` at your project root, then:

```bash
uv sync              # Install dependencies
uv run ruff check .  # Lint
uv run pytest        # Test
```
