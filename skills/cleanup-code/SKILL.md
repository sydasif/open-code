---
name: cleanup-code
description: >
  Codebase cleanup workflow applying YAGNI, DRY, and KISS principles.
  Use when asked to review, simplify, refactor, or remove dead/leftover
  code, duplicated logic, over-abstraction, or stale docs.
---

# Code Cleanup

## The Three Rules

- **KISS**: prefer direct, readable code over clever abstractions.
- **YAGNI**: remove code with no current use — unused, dead, or leftover.
- **DRY**: reduce duplication only when it lowers real maintenance cost.

Apply the **rule of three**: tolerate one duplicate; extract on the third
occurrence, and only when it genuinely reduces maintenance cost, not just
line count.

When rules conflict, apply them in this order: **KISS → YAGNI → DRY**.

---

## Before You Start

### 1. Check git status

Run `git status`. If there are uncommitted changes, confirm scope with the
user before touching anything.

### 2. Isolate changes

Create a branch: `git checkout -b cleanup/<module>`. This keeps the working
branch clean and makes rollback trivial. If the user explicitly wants
in-place changes, proceed but note it in the report.

### 3. Check test coverage

If coverage is thin or absent, escalate all findings to "needs care" and
warn the user. Cleanup without tests can silently break behavior.

### 4. Define scope

Confirm with the user what counts as a "module" in this project, or infer
from directory structure. A module is the smallest unit that can be
independently tested and deployed (if applicable). Work one module per pass.

### 5. Read project guidance

Read `AGENTS.md`, `README.md`, and any contribution or style docs.
Project-level rules override this skill. Note any conflicts.

---

## What to Look For

### Dead and leftover code (YAGNI)

- Unused imports, helpers, parameters, config keys, validators, adapters
- Functions or classes with zero call sites **and** zero string references (see "How to Clean" for verification)
- Re-exports in `__init__.py`, `__all__`, or barrel files referencing deleted names
- Code behind flags or conditions that can never be true
- "Future-proof" logic with no tests, docs, or callers
- Stale comments and TODOs/FIXMEs/HACKs describing behavior that was removed
- Docs referencing files, functions, or structure that no longer exist
- Package dependencies only used by code being removed

### Duplicated logic (DRY)

- Identical or near-identical branches across modules
- Repeated error mapping, serialization, validation, or result shaping
- Tests reimplementing the same fixture or async fake multiple times

### Unnecessary complexity (KISS)

- One-use helpers that wrap a single direct call
- Overly defensive branching around impossible states
- Abstractions with vague names that obscure simple behavior
- Tests asserting implementation details instead of behavior

---

## Risk Levels

**Safe — act directly:**

- Unused imports and dead helpers with zero call sites and zero string references
- Byte-for-byte duplicated branches
- Stale comments and docs describing removed code or structure

**Needs care — confirm before acting:**

- Exported names, public APIs, documented behavior
- Config formats with potential external consumers
- Anything with thin or no test coverage
- Package dependency removals (may be used by code outside this module)

**Skip — document why:**

- Tiny duplication that is clearer inline than abstracted
- Abstractions encoding a real domain boundary
- Compatibility shims with known external users
- Code invoked via dynamic dispatch: decorators, registries, plugin entry
  points, reflection, signal handlers, CLI registration, `__subclasses__()`
- Re-exports and `__all__` entries that form a public API surface
- ORM models, migration references, and admin registrations
- Code behind feature flags, environment configs, or A/B toggles that may
  be active in other deployments
- Anything imported by name string or config key

---

## How to Clean

- Work one module or layer per pass. Don't sweep the whole codebase at once.
- Don't mix style changes with behavior changes in the same diff.
- Don't introduce a new abstraction unless it removes real complexity across multiple call sites.
- Preserve existing naming, error shape, and test style.
- If a removal forecloses an obvious future extension point, flag it instead of deleting silently.

### Before marking any name as "unused"

Search for string references, not just call sites:

```bash
grep -r "FunctionName" --include="*.py" --include="*.yaml" --include="*.toml"
```

Zero call sites ≠ zero usages. Dynamic dispatch, registries, config files,
and decorator arguments all leave no visible call graph but are real usages.

### When deleting production code

Delete its tests in the same pass. This is not "weakening" a test — the
tested behavior no longer exists. Confirm the tests only test the deleted
code before removing them.

### When deleting code that uses a library

Check whether the library is still imported anywhere after deletion. If not,
remove it from `pyproject.toml` / `requirements.txt` / `package.json` in the
same pass.

### After each pass

1. Run `git diff` and review the actual change before running tests.
2. Run lint and tests. Fix failures before continuing.
3. Never weaken a failing test to make cleanup pass.

### If a regression occurs

1. `git checkout -- <module>` to discard changes to that module.
2. Do NOT attempt partial fixes on a broken cleanup.
3. Report the failure with the specific test that broke.

---

## Progress Tracking

`cleanup-progress.md` at the repo root. Create it on first pass. Update
after each module. This is the only mechanism for continuity across sessions.

```markdown
# Cleanup Progress

## Analyzed

- [module]: [date] — [safe/needs care/skipped counts]

## Changed

- [module]: [what was removed/simplified]

## Pending

- [module]: [what was found but not yet actioned]

## Unresolved Risks

- [description of anything skipped or uncertain]
```

---

## Reporting

### Review mode (before changes)

```markdown
## Findings

### Pre-flight

- Git status: [clean / uncommitted changes]
- Branch: [cleanup/<module> / in-place]
- Test coverage: [adequate / thin / unknown]
- Scope: [what "module" means in this project]
- Project overrides: [none / list any]

### Candidates

- [file:line] Description — safe / needs care / skip

### Safe cleanup

Low-risk changes ready to apply.

### Risky cleanup

Changes needing confirmation.

### Skipped

Items evaluated but not actioned, with reasons.

### Narrowly avoided

Items that appeared unused but had string references or dynamic dispatch
usages. Document these to prevent future false positives.

### Verification plan

Lint/test commands. Doc sections to update. Dependencies to check.
```

### After changes

```markdown
## What changed

[summary scoped to module or layer]

## What was verified

[git diff summary, lint/test output, dependency check results]

## Residual risks

[skipped items, thin coverage areas, public API concerns,
dependencies that might be unused but couldn't be confirmed]
```

---

## Agentic Notes

- Batch changes by module. Never accumulate a multi-module diff.
- If a change introduces a regression you can't resolve, revert and report.
- When in doubt about whether code is dynamically dispatched, skip it and
  flag it. False negatives (keeping dead code) are cheap; false positives
  (deleting live code) are catastrophic.
