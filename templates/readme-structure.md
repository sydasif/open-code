---
name: readme-structure
description: Standard README.md template for Python projects with uv toolchain
---

# README.md

Standard project README. Adapt the sections to your project:

````markdown
# Project Title

Brief description of the project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [License](#license)

## Installation

```bash
# Clone the repository
git clone https://github.com/username/repo.git
cd repo

# Install dependencies using uv
uv sync
```

## Usage

Brief explanation of how to use the project.

```bash
# Example command
uv run python -m your_module
```

## Development

### Prerequisites

- [uv](https://github.com/astral-sh/uv) (for package management)
- Python 3.10+

### Setting up development environment

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks on existing code (optional but recommended)
pre-commit run --all-files
```

### Code Quality

This project uses the following tools for code quality:

- **Ruff** for linting and formatting
- **MyPy** for static type checking
- **Bandit** for security analysis
- **Safety** for dependency vulnerability scanning
- **pytest** for testing

To run checks manually:

```bash
# Linting and formatting
uv run ruff check . --fix
uv run ruff format .

# Type checking
uv run mypy src/

# Security analysis
uv run bandit -r src/
uv run safety check
uv run uv-secure scan

# Testing
uv run pytest
```

### Making changes

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Ensure all tests pass
4. Run pre-commit checks: `pre-commit run --all-files`
5. Submit a pull request

## Testing

Run the test suite:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=src --cov-branch
```

Generate HTML coverage report:

```bash
uv run pytest --cov=src --cov-report=html
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
````

## Usage

Copy the content above into `README.md` at your project root. Adjust installation, usage, and testing sections to match your project specifics.
