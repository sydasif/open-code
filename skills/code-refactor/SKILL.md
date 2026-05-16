---
name: code-refactor
description: Modernize legacy Python code with best practices, type hints, and efficient patterns.
---

# Python Refactoring Specialist

> **Prerequisite**: Run the `code-cleanup` skill before this one if the codebase hasn't been pruned recently.
> This skill modernizes code that _should exist_ — not code that should be deleted.
> Cleanup first, refactor second.

This skill transforms legacy Python code into modern, maintainable, and efficient implementations following current best practices.

## Python style

Follow the project's canonical Python style rules defined in `rules/python-style.md`.
Those rules are always loaded and take precedence. This skill applies them mechanically
during refactoring — it does not restate them here.

---

## Refactoring Process

### 1. Assessment

1. Identify legacy patterns in the code
2. Prioritize refactoring based on impact and risk
3. Check for existing tests — ensure they exist and pass before refactoring anything

### 2. Safe Refactoring Steps

1. Run existing tests to establish a baseline
2. Apply one refactoring pattern at a time
3. Run tests after each change
4. Verify functionality remains identical

### 3. Modernization Checklist

**String and data handling**

- [ ] All string formatting uses f-strings (replace `%` and `.format()`)
- [ ] Path operations use `pathlib` (replace `os.path.*`)
- [ ] Config parsing uses `tomllib` (3.11+) or `tomli` where `configparser` is overkill

**Type system**

- [ ] Function signatures have type hints on inputs and return values
- [ ] Keyword-only arguments used where callers should not rely on positional order
- [ ] `TypedDict` or dataclasses used for structured dicts passed between functions

**Classes and data structures**

- [ ] Simple attribute-only classes replaced with `@dataclass`
- [ ] Boilerplate methods (`__init__`, `__repr__`, `__eq__`) removed where dataclass covers them
- [ ] `__slots__` added to hot-path dataclasses where memory efficiency matters

**Control flow**

- [ ] Long `if/elif` chains over a single variable replaced with `match` statements (Python 3.10+)
- [ ] Complex lambda functions moved to named functions
- [ ] Iterations use appropriate patterns: `enumerate`, list/dict/set comprehensions, `zip`

**Resource and error handling**

- [ ] Context managers handle all file, socket, and connection resources
- [ ] Exception handling is specific — no bare `except:` or `except Exception:` without re-raise
- [ ] `print` statements for diagnostics replaced with `logging` calls at appropriate levels

**Async (if applicable)**

- [ ] `asyncio` patterns are consistent — no mixing of sync blocking calls inside async functions
- [ ] `async with` and `async for` used where available on async-capable resources

**Imports**

- [ ] Imports organized in standard groups: stdlib → third-party → local
- [ ] No unused imports (should already be clear after `code-cleanup` pass)

---

## Quality Assurance

For detailed tool commands, see the project's `AGENTS.md` or the `code-cleanup` and `code-review` skills.

### Before Refactoring

Run type checking, linting, and tests to establish baseline:

```
uv run mypy <target>
uv run ruff check <target>
uv run pytest --tb=short
uv run pytest --cov=<target> --cov-report=term-missing
```

Record the baseline pass/fail counts. Any test that was already failing before refactoring is not your regression to fix — flag it and leave it.

### After Refactoring

Verify refactored code passes all checks:

- Type checking (no new mypy errors)
- Linting (no new lint violations)
- Unit tests (same or better pass rate as baseline)
- Coverage (no meaningful drop from baseline)

---

## Common Refactoring Scenarios

### Scenario 1: Migrate to f-strings

```python
# Before
msg = "Host %s unreachable after %d retries" % (host, retries)
msg = "Host {} unreachable after {} retries".format(host, retries)

# After
msg = f"Host {host} unreachable after {retries} retries"

# Preserve alignment options where needed
msg = f"{'Interface':<20} {'Status':>10}"
```

### Scenario 2: Migrate to dataclasses

```python
# Before
class DeviceInfo:
    def __init__(self, hostname, ip, platform):
        self.hostname = hostname
        self.ip = ip
        self.platform = platform

    def __repr__(self):
        return f"DeviceInfo({self.hostname}, {self.ip}, {self.platform})"

# After
from dataclasses import dataclass

@dataclass
class DeviceInfo:
    hostname: str
    ip: str
    platform: str
```

### Scenario 3: Migrate to pathlib

```python
# Before
import os
config_path = os.path.join(base_dir, "config", "devices.yaml")
if os.path.exists(config_path):
    with open(config_path) as f:
        ...

# After
from pathlib import Path
config_path = Path(base_dir) / "config" / "devices.yaml"
if config_path.exists():
    with config_path.open() as f:
        ...
```

### Scenario 4: Migrate to match statements

```python
# Before
if platform == "ios":
    driver = IOSDriver()
elif platform == "eos":
    driver = EOSDriver()
elif platform == "nxos":
    driver = NXOSDriver()
else:
    raise ValueError(f"Unknown platform: {platform}")

# After (Python 3.10+)
match platform:
    case "ios":
        driver = IOSDriver()
    case "eos":
        driver = EOSDriver()
    case "nxos":
        driver = NXOSDriver()
    case _:
        raise ValueError(f"Unknown platform: {platform}")
```

### Scenario 5: Replace print with logging

```python
# Before
print(f"Connecting to {host}...")
print(f"ERROR: timeout on {host}")

# After
import logging
logger = logging.getLogger(__name__)

logger.debug("Connecting to %s", host)
logger.error("Timeout on %s", host)
```

### Scenario 6: Migrate dict to TypedDict

```python
# Before
def process_user(user_data):
    name = user_data["name"]
    age = user_data["age"]
    active = user_data.get("active", False)
    return f"{name} ({age}) - Active: {active}"

# After
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    active: bool

def process_user(user_data: User) -> str:
    name = user_data["name"]
    age = user_data["age"]
    active = user_data.get("active", False)
    return f"{name} ({age}) - Active: {active}"
```

### Scenario 7: Convert positional args to keyword-only

```python
# Before
def create_user(name, age, active=True, admin=False):
    return {"name": name, "age": age, "active": active, "admin": admin}

# After
def create_user(name: str, age: int, *, active: bool = True, admin: bool = False):
    """Create a new user.

    Args:
        name: User's full name
        age: User's age
        active: Whether the user is active
        admin: Whether the user has admin privileges
    """
    return {"name": name, "age": age, "active": active, "admin": admin}
```

### Scenario 8: Replace index loops and manual accumulators

```python
# Before
items = ["apple", "banana", "cherry"]
for i in range(len(items)):
    print(f"{i}: {items[i]}")

total = 0
for num in numbers:
    total += num

filtered = []
for num in numbers:
    if num > 0:
        filtered.append(num * 2)

# After
for i, item in enumerate(items):
    print(f"{i}: {item}")

total = sum(numbers)

filtered = [num * 2 for num in numbers if num > 0]
```

### Scenario 9: Use specific exceptions with exception chaining

```python
# Before
def divide(a, b):
    try:
        result = a / b
    except:
        return None

# After
def divide(a: float, b: float) -> float:
    """Divide a by b.

    Args:
        a: Dividend
        b: Divisor

    Returns:
        The result of a / b

    Raises:
        ZeroDivisionError: If b is zero
        TypeError: If a or b are not numeric
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ZeroDivisionError(f"Cannot divide {a} by zero") from e
    except TypeError as e:
        raise TypeError(f"Invalid operand types: {type(a).__name__}, {type(b).__name__}") from e
```

---

Use this skill to modernize legacy Python code into clean, maintainable, and efficient implementations using contemporary Python features and best practices — after the codebase has been pruned with `code-cleanup`.
