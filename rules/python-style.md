---
name: python-style
description: Python toolchain, style, and code review rules (single canonical source)
---

# Python Style & Toolchain

> Single canonical source — for all Python style and toolchain rules

---

## Required Toolchain

| Tool      | Purpose                                                                 |
| --------- | ----------------------------------------------------------------------- |
| `uv`      | Environment management + dependencies                                   |
| `ruff`    | Linting + formatting                                                    |
| `pyright` | Static type checking — new projects                                     |
| `mypy`    | Static type checking — existing projects or legacy library dependencies |
| `pytest`  | Test runner                                                             |

## Type Checker Selection

| Situation                                                             | Use                                                          |
| --------------------------------------------------------------------- | ------------------------------------------------------------ |
| New project, no existing type config                                  | `pyright --strict`                                           |
| Existing project already configured with `mypy`                       | Keep `mypy` — do not migrate mid-project                     |
| `pyrightconfig.json` present                                          | `pyright`                                                    |
| `mypy.ini` or `[tool.mypy]` in `pyproject.toml` present               | `mypy`                                                       |
| Using Pydantic v1, Django, SQLAlchemy legacy, Netmiko, NAPALM, NORNIR | Prefer `mypy` — pyright stub coverage is thinner for these   |
| Using Pydantic v2, FastAPI, modern stdlib only                        | Either works; `pyright` preferred                            |
| Both configs present                                                  | Follow `pyproject.toml` — do not introduce the other checker |

Never add a second type checker to a project that already has one configured.

## Standard Workflow

```bash
uv sync                        # Install dependencies
uv run ruff check --fix .      # Lint and auto-fix
uv run ruff format .           # Format code

# New projects
uv run pyright src/            # Type check (strict)

# Existing projects
uv run mypy src/               # Type check

uv run pytest                  # Run tests
```

## Security Scans

```bash
uv run safety scan            # Check for vulnerable dependencies
uv run bandit -r src/          # Static security analysis
```

- **safety scan**: Medium+ severity = blocking. Halt until user confirms.
- **bandit**: HIGH severity or HIGH confidence = blocking. Everything else = report, do not auto-fix.
- Never suppress or ignore security scan output. If a known false positive, document why.

---

## Code Style Rules

### 1. Google-Style Docstrings (PEP 257)

All public modules, classes, and functions must have Google-style docstrings.

**Forbidden:** Missing docstrings on public entities. Sphinx/reST or NumPy style (unless reconfigured).

**Required:** Triple quotes, `Args:` section, `Returns:` section, `Raises:` section for known exceptions, module-level and class docstrings.

```python
def fetch_user(user_id: int) -> dict:
    """Fetches a user profile from the database.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        A dictionary containing the user's profile data.

    Raises:
        ValueError: If user_id is negative.
    """
    ...
```

### 2. Strict Type Hints (PEP 484, 526, 544)

**Forbidden:** Missing type hints, `Any` (unless justified), bare `list`/`dict`, mixing `Union[A, B]` and `A | B`.

**Required:** Full signatures, `T | None` for nullable (3.10+, prefer `|`), variable annotations, generic types, `Protocol`, `TypeVar`, `Literal`, `TypedDict`, `Final`, `NoReturn`.

### 3. No Print in Production

Use `logging` module.

**Forbidden:** `print()`, `pprint()`, `sys.stdout.write()`, `sys.stderr.write()` for app messages.

**Required:** `import logging; logger = logging.getLogger(__name__)`, use `logger.info()`, `.warning()`, `.error()`, `.debug()`.

### 4. Explicit Error Handling

**Forbidden:** Bare `except:`, `except Exception:` without re-raise or logging, `pass` in except without comment.

**Required:** Catch specific exceptions, `try/finally` or `with` for resources, `raise ... from original_exc`, log with context.

### 5. PEP 8 Naming

| Element                       | Convention            |
| ----------------------------- | --------------------- |
| Functions, variables, modules | `snake_case`          |
| Classes, exceptions           | `PascalCase`          |
| Constants                     | `UPPER_CASE`          |
| Private attributes            | `_leading_underscore` |

### 6. Import Organization

1. Standard library
2. Third-party
3. Local application

Blank lines between groups. Absolute imports preferred. `from module import name` over `import module.name`.

### 7. Modern Python

- f-strings over `%`/`.format()`
- `pathlib` over `os.path`
- `@dataclass` for simple data containers
- `match`/`case` for long `if/elif` chains over a single variable (3.10+)
- Walrus operator `:=` where it clarifies
- Context managers for all resources

### 8. Async Patterns

`async`/`await`, `asyncio.gather()` for concurrency, `asyncio.create_task()`, `asyncio.timeout()` (3.11+), `async with` for cleanup. Never `asyncio.run()` in libraries.

### 9. Security

**Forbidden:** Hardcoded secrets, `eval()`/`exec()` with user input, unsanitized SQL, pickle from untrusted sources.

**Required:** Env vars for secrets, parameterized queries, input validation, bcrypt/Argon2 for passwords.

### 10. Performance

Generators for large data, `itertools`, `functools.lru_cache`, `collections.defaultdict`.

### 11. Dependency Management

Use `uv`. No direct `pip install`. Use `pyproject.toml`. Pin in `uv.lock`.

---

## See Also

- `python-testing` skill — Test patterns, coverage thresholds
