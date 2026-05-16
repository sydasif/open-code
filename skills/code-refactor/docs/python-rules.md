---
name: python-rules
description: Python-specific code best practices.
---

# Python Code Review Rules

These are Python-specific code review rules. Follow these guidelines to maintain high-quality Python code.

---

## Rule 1: Google-Style Docstrings (PEP 257)

All public modules, classes, and functions must have Google-style docstrings.

**Forbidden:**

- Missing docstrings on public entities
- "One-liner" descriptions for complex functions
- Sphinx/reST or NumPy style (unless explicitly re-configured)

**Required:**

- Triple quotes `"""`
- `Args:` section for parameters
- `Returns:` section for return values
- `Raises:` section for known exceptions
- Module-level docstrings for all modules
- Class docstrings explaining the class purpose

**Example:**

```python
def fetch_user(user_id: int) -> dict:
    """Fetches a user profile from the database.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        A dictionary containing the user's profile data.

    Raises:
        ValueError: If user_id is negative.
        ConnectionError: If the database is unreachable.
    """
    ...
```

---

## Rule 2: Strict Type Hints (PEP 484, PEP 526, PEP 544)

No escape hatches. Use precise type hints for all function arguments and return values.

**Forbidden:**

- Missing type hints
- `Any` (unless absolutely necessary and justified)
- Bare `list` or `dict` without generics (use `list[str]`, `dict[str, int]`)
- Unused imports that cause circular dependency workarounds
- Inconsistent use of Union syntax (mixing `Union[A, B]` and `A | B`)

**Required:**

- Full signatures: `def func(a: int, b: str) -> bool:`
- `Optional[T]` or `T | None` for nullable values (Python 3.10+)
- `Union` or `|` for multiple types (Python 3.10+), prefer `|` syntax
- Variable annotations: `count: int = 0`
- Generic types: `list[int]`, `dict[str, Any]` (Python 3.9+) or `List[int]`, `Dict[str, Any]` for older versions
- Use `Protocol` for structural subtyping: `class Drawable(Protocol): def draw(self) -> None: ...`
- Use `TypeVar` for generic functions: `T = TypeVar('T', bound=str)`
- Use `Literal` for exact values: `mode: Literal['r', 'w', 'a']`
- Use `TypedDict` for dictionary structures with known keys
- Use `Final` for constants: `MAX_SIZE: Final = 100`
- Use `NoReturn` for functions that never return: `def die() -> NoReturn: ...`

---

## Rule 3: No Print Statements in Production

Production code must use the `logging` module, not standard output.

**Forbidden:**

- `print(...)`
- `pprint(...)`
- `sys.stdout.write(...)`
- `sys.stderr.write(...)` for application messages

**Required:**

- `import logging`
- `logger = logging.getLogger(__name__)`
- `logger.info(...)`, `logger.warning(...)`, `logger.error(...)`, `logger.debug(...)`
- Structured logging with relevant context

---

## Rule 4: Explicit Error Handling

Never swallow errors blindly. Handle specific exceptions.

**Forbidden:**

- Bare `except:`
- `except Exception:` (without re-raising or logging extensively)
- `pass` inside an except block without a comment
- Silent failure without proper error propagation

**Required:**

- Catch specific exceptions: `except ValueError:`
- `try/finally` or `with` statements for resource cleanup
- Proper exception chaining: `raise CustomException("msg") from original_exc`
- Log exceptions with context before handling

---

## Rule 5: PEP 8 Naming Conventions

Follow standard Python naming conventions to maintain idiomatic code.

**Forbidden:**

- camelCase for functions/variables (`myFunction`, `myVariable`)
- PascalCase for functions/variables
- snake_case for classes (`my_class`)
- Single character variable names (except for loop counters)

**Required:**

- `snake_case` for functions, variables, modules
- `PascalCase` (CapWords) for classes and exceptions
- `UPPER_CASE` for constants
- Descriptive names that clearly indicate purpose
- Private attributes with leading underscore: `_private_attr`

---

## Rule 6: Import Organization and Best Practices

Structure imports according to PEP 8 standards.

**Forbidden:**

- Wildcard imports: `from module import *`
- Relative imports for same package
- Imports inside functions (except for conditional imports)
- Multiple imports per line

**Required:**

- Standard library imports first
- Third-party imports second
- Local application/library imports third
- Blank lines between import groups
- Absolute imports preferred over relative
- Specific imports: `from module import specific_function`

**Example:**

```python
import os
import sys
from pathlib import Path

import requests
import yaml

from myapp.models import User
from myapp.utils import helper_function
```

---

## Rule 7: Security Best Practices

Implement secure coding practices to prevent vulnerabilities.

**Forbidden:**

- Hardcoded secrets, API keys, or passwords
- Direct use of `eval()`, `exec()`, or `compile()` with user input
- Unsanitized input in SQL queries (use parameterized queries)
- Insecure deserialization (pickle) with untrusted data
- Using `input()` or similar functions without validation in production
- Importing modules from untrusted sources

**Required:**

- Store secrets in environment variables, secure vaults, or use libraries like `python-dotenv` with proper .gitignore
- Use parameterized queries or ORM to prevent SQL injection
- Validate and sanitize all user inputs using libraries like `validators` or custom validation
- Use secure random generators for tokens: `secrets` module instead of `random`
- Hash passwords with bcrypt, Argon2, or similar: `bcrypt.hashpw(password.encode(), bcrypt.gensalt())`
- Use `urllib.parse` for URL parsing and validation
- Implement proper input length limits to prevent buffer overflow attacks
- Use `html.escape()` when displaying user-generated content to prevent XSS
- Regularly update dependencies and scan for vulnerabilities with tools like `safety` or `pip-audit`
- Use `defusedxml` instead of standard XML libraries to prevent XXE attacks

---

## Rule 8: Modern Python Features and Best Practices

Leverage modern Python features for cleaner, more efficient code.

**Forbidden:**

- Outdated Python 2 compatibility code
- Manual file handling without context managers
- Manual string formatting (old `%` style or `.format()`)

**Required:**

- Context managers: `with open(file) as f:`
- f-strings for string formatting: `f"Hello {name}"`
- Walrus operator (Python 3.8+) where appropriate: `if (n := len(a)) > 10:`
- Type hints and generics
- Dataclasses for simple data containers
- Pathlib for path manipulation

---

## Rule 9: Performance and Memory Best Practices

Write efficient code that minimizes resource consumption.

**Forbidden:**

- Loading entire large files into memory unnecessarily
- Repeated expensive operations in loops
- Creating unnecessary intermediate lists

**Required:**

- Use generators for large datasets: `(x for x in items if condition)`
- Use `itertools` for efficient iteration patterns
- Consider `functools.lru_cache` for expensive pure functions
- Use `collections.defaultdict` to avoid repeated key checking

---

## Rule 10: Asynchronous Programming Patterns (asyncio)

Use appropriate patterns for handling asynchronous operations efficiently.

**Forbidden:**

- Blocking the event loop with synchronous operations
- Using `threading` or `multiprocessing` when asyncio would be more appropriate
- Mixing synchronous and asynchronous code without proper bridges
- Forgetting to await coroutines

**Required:**

- Use `async`/`await` syntax for asynchronous operations: `async def fetch_data():`
- Proper error handling with try/catch in async functions
- Use `asyncio.gather()` for concurrent operations: `await asyncio.gather(task1, task2)`
- Use `asyncio.create_task()` to schedule concurrent tasks
- Use `asyncio.timeout()` (Python 3.11+) or `asyncio.wait_for()` for timeouts
- Implement proper cleanup with async context managers: `async with`
- Avoid `asyncio.run()` in libraries; reserve for main entry points
- Use `asyncio.sleep()` instead of `time.sleep()` in async functions

---

## Rule 11: Dependency and Execution Best Practices

Always use modern, reproducible dependency management and execution patterns.

**Forbidden:**

- Using `pip install` directly in projects
- Running Python scripts with `python script.py` without proper environment
- Using `pip` for project dependencies (in favor of modern tools)
- Direct execution without proper environment isolation
- Committing `requirements.txt` when using modern tools like Poetry or uv

**Required:**

- Use `uv` for fast dependency management and execution (recommended)
- Use `Poetry` or `PDM` for project dependency management with lock files
- Always use `uv run` or `poetry run` to execute Python scripts and commands
- For ad-hoc Python execution, use `uv run python -c "your code"` or `poetry run python -c "your code"`
- Use virtual environments for project isolation
- Use `pyproject.toml` for project configuration and dependency specifications
- Pin dependencies in lock files (`uv.lock`, `poetry.lock`, or `pdm.lock`)
- Scan dependencies for security vulnerabilities with `pip-audit`, `safety`, or similar tools
- Use `uv pip compile` or `poetry export` to generate requirements files for deployment

---

## Review Procedure

For each Python file:

1. **Read complete file**
2. **Search for violations**
3. **Report findings** with file:line references

---

## Report Format

### If violations found

```text
FAIL

Violations:
1. [GOOGLE-STYLE DOCSTRINGS] - src/users.py:42
   Issue: Missing 'Args' section in docstring
   Fix: Add Args section describing 'user_id' parameter

2. [NO PRINT STATEMENTS] - src/main.py:15
   Issue: Used print() for debugging
   Fix: Replace with logger.info()
```

### If no violations

```text
PASS

File meets all semantic requirements.
```
