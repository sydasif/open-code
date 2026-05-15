---
name: code-cleanup
description: Codebase cleanup workflow applying YAGNI, DRY, and KISS principles. Use when asked to review, simplify, refactor, or remove dead/leftover code, duplicated logic, over-abstraction, or stale docs.
---

# Code Cleanup

## The Three Rules

- **KISS**: prefer direct, readable code over clever abstractions.
- **YAGNI**: remove code with no current use — unused, dead, or leftover.
- **DRY**: reduce duplication only when it lowers real maintenance cost.

When rules conflict, apply them in this order: KISS → YAGNI → DRY.

---

## Before You Start

### 1. Check git status

Run `git status`. If there are uncommitted changes, confirm scope with the user before touching anything.

### 2. Check test coverage

If coverage is thin or absent, escalate all findings to "needs care" and warn the user. Cleanup without tests can silently break behavior.

### 3. Read project guidance

Read `AGENTS.md`, `README.md`, and any contribution or style docs. Project-level rules override this skill. Note any conflicts.

---

## What to Look For

### Dead and leftover code (YAGNI)

- Unused imports, helpers, parameters, config keys, validators, adapters
- Functions or classes with zero call sites
- Code behind flags or conditions that can never be true
- "Future-proof" logic with no tests, docs, or callers
- Stale comments describing behavior that was removed
- Docs referencing files, functions, or structure that no longer exist

### Duplicated logic (DRY)

- Identical or near-identical branches across modules
- Repeated error mapping, serialization, validation, or result shaping
- Tests reimplementing the same fixture or async fake multiple times
- **Rule of three**: tolerate one duplicate; extract on the third occurrence

### Unnecessary complexity (KISS)

- One-use helpers that wrap a single direct call
- Overly defensive branching around impossible states
- Abstractions with vague names that obscure simple behavior
- Tests asserting implementation details instead of behavior

---

## Risk Levels

**Safe — act directly:**

- Unused imports and dead helpers with zero call sites
- Byte-for-byte duplicated branches
- Stale comments and docs describing removed code or structure

**Needs care — confirm before acting:**

- Exported names, public APIs, documented behavior
- Config formats with potential external consumers
- Anything with thin or no test coverage

**Skip — document why:**

- Tiny duplication that is clearer inline than abstracted
- Abstractions encoding a real domain boundary
- Compatibility shims with known external users

---

## How to Clean

- Work one module or layer per pass. Don't sweep the whole codebase at once.
- Don't mix style changes with behavior changes in the same diff.
- Don't introduce a new abstraction unless it removes real complexity across multiple call sites.
- Preserve existing naming, error shape, and test style.
- If a removal forecloses an obvious future extension point, flag it instead of deleting silently.

After each pass: run lint and tests. Fix failures before continuing. Never weaken a failing test to make cleanup pass.

---

## Reporting

### Review mode (before changes)

```
## Findings

### Pre-flight
- Git status: [clean / uncommitted changes]
- Test coverage: [adequate / thin / unknown]
- Project overrides: [none / list any]

### Candidates
- [file:line] Description — safe / needs care / skip

### Safe cleanup
Low-risk changes ready to apply.

### Risky cleanup
Changes needing confirmation.

### Skipped
Items evaluated but not actioned, with reasons.

### Verification plan
Lint/test commands. Doc sections to update.
```

### After changes

```
## What changed
[summary scoped to module or layer]

## What was verified
[lint/test output, or reason skipped]

## Residual risks
[skipped items, thin coverage areas, public API concerns]
```

---

## Agentic Notes

- Leave a `cleanup-progress.md` at the repo root tracking: what was analyzed, changed, pending, and any unresolved risks.
- Batch changes by module. Never accumulate a multi-module diff.
- If a change introduces a regression you can't resolve, revert and report.
