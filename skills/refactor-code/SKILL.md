---
name: refactor-code
description: >
  Modernize legacy Python code with best practices, type hints,
  and efficient patterns. Use after cleanup-code has pruned dead code.
---

# Python Refactoring Specialist

> **Prerequisite**: Run the `cleanup-code` skill before this one.
> This skill modernizes code that _should exist_ — not code that should
> be deleted. Cleanup first, refactor second.

## Python Version

Before any refactoring, determine the project's minimum Python version:

1. Read `pyproject.toml` (`requires-python`), `setup.cfg`, or
   `.python-version`
2. If unknown, infer from CI config or ask the user
3. Only apply patterns available in that version:

| Version | Available patterns                                               |
| ------- | ---------------------------------------------------------------- |
| 3.9     | dataclasses, f-strings, pathlib, walrus operator                 |
| 3.10    | match statements, `X \| Y` unions, keyword-only dataclass fields |
| 3.11    | tomllib, `Self` type, exception groups                           |
| 3.12    | type alias syntax, improved f-string nesting                     |

## Python Style

Follow the canonical Python style rules defined in @rules/python-style.md.

---

## Risk Levels

**Safe — apply directly:**

- f-string conversions
- pathlib conversions
- Import organization
- Adding type hints to internal (non-public) functions
- Replacing index loops with enumerate/comprehensions
- Narrowing bare `except` to specific exception types (preserving contract)

**Needs care — confirm before applying:**

- dataclass conversions (see caveats in Scenario 2)
- Adding keyword-only arguments to existing functions
- Adding `__slots__` (breaks pickle, dynamic attributes, some inheritance)
- Type hints on public APIs (exposes types that become hard to change)
- Exception handling changes that alter the error contract

**Skip — document why:**

- Any change to code with no test coverage
- Converting public API class constructors (breaks external callers)
- match statements on simple equality chains (no clarity gain over if/elif)
- Async refactoring without a clear concurrency model
- Code that is stable, untested, and about to be replaced

---

## Refactoring Process

### 1. Assessment

1. Determine minimum Python version (see above)
2. Identify legacy patterns in the code
3. Prioritize refactoring based on impact and risk
4. Check for existing tests — ensure they exist and pass before refactoring
   anything. If no tests exist, escalate and skip.

### 2. Safe Refactoring Steps

1. Create a branch: `git checkout -b refactor/<module>-<pattern>`
2. Run existing tests to establish a baseline. Record pass/fail counts.
   Any test already failing is not your regression — flag it and leave it.
3. Apply one refactoring pattern at a time
4. Run tests after each change
5. Review `git diff` before declaring the pass complete
6. Verify functionality remains identical

### 3. If a regression occurs

1. `git checkout -- <module>` to discard changes
2. Do NOT attempt partial fixes on a broken refactoring
3. Report the failure — some refactorings are only safe with better
   test coverage

---

## Modernization Checklist

**String and data handling**

- [ ] All string formatting uses f-strings (replace `%` and `.format()`)
      **Exception**: logging calls use `%` formatting for lazy evaluation.
      `logger.debug("Value: %s", val)` — not `f"Value: {val}"`. F-strings
      construct the string even when the log level is suppressed.
- [ ] Path operations use `pathlib` (replace `os.path.*`)
- [ ] Config parsing uses `tomllib` (3.11+) or `tomli` where
      `configparser` is overkill

**Type system**

- [ ] Function signatures have type hints on inputs and return values
- [ ] `from __future__ import annotations` used where forward references
      are needed (3.9–3.11; unnecessary in 3.12+)
- [ ] Keyword-only arguments used where callers should not rely on
      positional order
- [ ] `TypedDict` or dataclasses used for structured dicts passed between
      functions. Note: TypedDict is static-only — it does not validate at
      runtime.

**Classes and data structures**

- [ ] Simple attribute-only classes replaced with `@dataclass`
      (see Scenario 2 for caveats)
- [ ] Boilerplate methods (`__init__`, `__repr__`, `__eq__`) removed
      where dataclass covers them
- [ ] `__slots__` added to hot-path dataclasses only where memory
      efficiency matters and pickle/inheritance are not concerns

**Control flow**

- [ ] `match` statements used where they genuinely improve clarity:
      structural pattern matching, nested destructuring, or guards.
      Simple equality chains over a single variable are often clearer
      as `if/elif` — do not convert those.
- [ ] Complex lambda functions moved to named functions
- [ ] Iterations use appropriate patterns: `enumerate`, comprehensions,
      `zip`

**Resource and error handling**

- [ ] Context managers handle all file, socket, and connection resources
- [ ] Exception handling is specific — no bare `except:` or
      `except Exception:` without re-raise. **Preserve the existing error
      contract** (return-None vs. raise) — changing it is a behavior change,
      not a refactoring.
- [ ] `print` statements for diagnostics replaced with `logging` calls
      at appropriate levels (using lazy `%` formatting)

**Async (if applicable)**

- [ ] `asyncio` patterns are consistent — no mixing of sync blocking
      calls inside async functions
- [ ] `async with` and `async for` used where available on async-capable
      resources

**Imports**

- [ ] Imports organized in standard groups: stdlib → third-party → local
- [ ] No unused imports (should already be clear after `cleanup-code`)

---

## Quality Assurance

### Before Refactoring

```bash
uv run mypy <target>
uv run ruff check <target>
uv run pytest --tb=short
uv run pytest --cov=<target> --cov-report=term-missing
```

Record the baseline. Any test already failing is not your regression.

### After Refactoring

- Type checking: no new mypy errors
- Linting: no new ruff violations
- Unit tests: same or better pass rate as baseline
- Coverage: no meaningful drop from baseline. If coverage drops,
  investigate — it may indicate a behavior change.

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

⚠️ **Verify before converting:**

- No code uses identity checks (`is`) on instances — dataclass `__eq__`
  compares values, not identity. Objects that were unequal may become equal.
- No subclasses override `__init__` — dataclass generates its own.
- No code relies on pickling format — dataclass pickle output differs.
- If immutability is intended, use `@dataclass(frozen=True)`.
- If the class has complex inheritance, test thoroughly after conversion.
- If the class is part of a public API, this is a breaking change — skip
  unless you control all callers.

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

### Scenario 4: Use match statements (only where they improve clarity)

```python
# Good candidate — structural pattern matching
match event:
    case {"type": "connect", "host": host, "port": port}:
        handle_connect(host, port)
    case {"type": "disconnect", "reason": reason}:
        handle_disconnect(reason)
    case _:
        handle_unknown(event)

# Bad candidate — simple equality, no clarity gain over if/elif
# Do NOT convert this:
if platform == "ios":
    driver = IOSDriver()
elif platform == "eos":
    driver = EOSDriver()
```

### Scenario 5: Replace print with logging

```python
# Before
print(f"Connecting to {host}...")
print(f"ERROR: timeout on {host}")

# After
import logging
logger = logging.getLogger(__name__)

# Use lazy % formatting in logging — NOT f-strings
logger.debug("Connecting to %s", host)
logger.error("Timeout on %s", host)
```

### Scenario 6: Migrate dict to TypedDict

```python
# Before
def process_user(user_data):
    name = user_data["name"]
    age = user_data["age"]
    return f"{name} ({age})"

# After
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    active: bool

def process_user(user_data: User) -> str:
    name = user_data["name"]
    age = user_data["age"]
    return f"{name} ({age})"
```

Note: TypedDict is a **static analysis tool only**. It does not validate
data at runtime. If runtime validation is needed, use pydantic or a
validation function.

### Scenario 7: Convert positional args to keyword-only

```python
# Before
def create_user(name, age, active=True, admin=False):
    return {"name": name, "age": age, "active": active, "admin": admin}

# After
def create_user(name: str, age: int, *, active: bool = True, admin: bool = False) -> dict:
    return {"name": name, "age": age, "active": active, "admin": admin}
```

⚠️ This changes the function's calling convention. Any caller passing
`active` or `admin` positionally will break. Check all call sites first.

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

### Scenario 9: Narrow exception handling (preserve contract)

```python
# Before — catches everything
def divide(a, b):
    try:
        result = a / b
    except:
        return None

# After — catches only expected errors, SAME contract
def divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except (ZeroDivisionError, TypeError):
        return None
```

⚠️ Changing from return-None to raise-exception is a **behavior change**,
not a refactoring. Preserve the existing error contract. If you want to
change it, that's a separate design decision — flag it, don't implement it.

---

## Progress Tracking

`refactor-progress.md` at the repo root. Create on first pass. Update
after each module.

```markdown
# Refactor Progress

## Python Version

Minimum: [version determined from pyproject.toml / other]

## Analyzed

- [module]: [date] — [patterns found, risk levels]

## Refactored

- [module]: [patterns applied, tests verified]

## Pending

- [module]: [patterns found but not yet applied, with reasons]

## Skipped

- [module/pattern]: [reason — no tests, public API, etc.]

## Unresolved Risks

- [description of anything uncertain or flagged for design review]
```

---

## Reporting

**Important**: All refactoring tasks must adhere to the global "Required Output" format defined in `CLAUDE.md` (Discovery Report → Strategic Plan → Assumptions & Risks → Proposed Changes → Skipped Candidates → Verification Pyramid). The following skill-specific reports should be integrated into those sections.

### Review mode (before changes)

```markdown
## Refactoring Assessment

### Pre-flight

- Python version: [3.x]
- Git status: [clean / uncommitted changes]
- Branch: [refactor/<module>-<pattern> / in-place]
- Test baseline: [N passed, M failed, X% coverage]
- Project overrides: [none / list any]

### Candidates

- [file:line] Pattern → Modern form — safe / needs care / skip

### Safe refactorings

Changes ready to apply.

### Risky refactorings

Changes needing confirmation, with specific caveats.

### Skipped

Items evaluated but not actioned, with reasons.

### Verification plan

Type check / lint / test commands. Coverage comparison.
```

### After changes

```markdown
## What changed

[summary scoped to module, listing each pattern applied]

## What was verified

[git diff summary, mypy output, ruff output, test results,
coverage comparison]

## Residual risks

[skipped items, coverage drops, public API concerns,
dataclass conversion caveats, changes that need design review]
```
