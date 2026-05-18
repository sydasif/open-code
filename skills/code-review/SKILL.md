---
name: code-review
description: Final-gate review of completed changes using a systematic, fresh-eyes verification approach. Run after code-cleanup and/or code-refactor passes to catch errors, verify completeness, and confirm quality standards before submitting work.
---

# Code Review — Final Gate

> **When to use**: After completing a `code-cleanup`, `code-refactor`, or any significant implementation task.
> This skill is the last check before work is considered done. It does not make changes — it surfaces problems.

---

## Purpose

Provide a structured, code-aware methodology for reviewing completed work to catch errors, verify correctness, confirm completeness, and ensure nothing was silently broken or left unresolved.

---

## Input Handling

Based on the input provided, determine which type of review to perform:

1. **No arguments (default)**: Review all uncommitted changes
   - Run: `git diff` for unstaged changes
   - Run: `git diff --cached` for staged changes
   - Run: `git status --short` to identify untracked (net new) files
2. **Commit hash** (40-char SHA or short hash): Review that specific commit
   - Run: `git show <hash>`
3. **Branch name**: Compare current branch to the specified branch
   - Run: `git diff <branch>...HEAD`
4. **PR URL or number**: Review the pull request
   - Run: `gh pr view <number>` to get PR context
   - Run: `gh pr diff <number>` to get the diff

---

## Review Process

### 1. Orient to the Work & Gather Context

**Diffs alone are not enough.** Read the entire file(s) being modified to understand the full context. Code that looks wrong in isolation may be correct given surrounding logic—and vice versa.

- **Task Context**: What task was completed? (cleanup, refactor, feature, fix)
- **File Identification**: Use the diff to identify which files changed.
- **Untracked Files**: Use `git status --short` to identify untracked files, then read their full contents.
- **Patterns**: Read the full file to understand existing patterns, control flow, and error handling. Use the `@explore` subagent to search the codebase for relevant patterns if needed.
- **Guidelines**: Check for existing style guide or conventions files (`CONVENTIONS.md`, `AGENTS.md`, `.editorconfig`, etc.).
- **Residual Risks**: Are there residual risk notes from a prior `code-cleanup` or `code-refactor` pass? Review those first.
- **Scope**: What is the stated scope? Flag anything in the diff that falls outside it.

### 2. Structural Verification

Inspect the file system to confirm expected outputs:

- All expected files and directories are present.
- No files were accidentally deleted or left with placeholder content.
- No unintended new files were created outside the stated scope.
- Import paths, relative links, and cross-references still resolve correctly.

### 3. What to Look For

**Bugs — Primary Focus**

- Logic errors, off-by-one mistakes, incorrect conditionals.
- If-else guards: missing guards, incorrect branching, unreachable code paths.
- Edge cases: null/empty/undefined inputs, error conditions, race conditions.
- Security issues: injection, auth bypass, data exposure.
- Broken error handling that swallows failures, throws unexpectedly, or returns error types that are not caught.

**Structure**

- Does it follow existing patterns and conventions?
- Are there established abstractions it should use but doesn't?
- Excessive nesting that could be flattened with early returns or extraction.

**Performance** (Only flag if obviously problematic)

- O(n²) on unbounded data, N+1 queries, blocking I/O on hot paths.

**Behavior Changes**

- If a behavioral change is introduced, raise it (especially if it's possibly unintentional).

### 4. Code-Specific Checklist

Work through this checklist against the actual diff, not from memory.

**Correctness**

- [ ] Logic changes preserve the original behavior (or the deviation is intentional and documented)
- [ ] Edge cases are handled: empty inputs, None, zero, out-of-range values
- [ ] Error handling is specific — no new bare `except:` blocks introduced
- [ ] No silent failures: errors surface rather than being swallowed

**Public contracts**

- [ ] No public function signatures changed without explicit user approval
- [ ] No exported names renamed or removed
- [ ] No config key names or environment variable names changed
- [ ] API response shapes preserved

**Tests**

- [ ] All tests pass at the same rate as the pre-change baseline
- [ ] No tests were deleted, weakened, or skipped to make the diff pass
- [ ] New helpers or changed shared utilities have test coverage
- [ ] Coverage did not meaningfully drop from baseline

> **Note**: Test execution requires bash access that this agent does not have by default.
> If test results are not available in the diff context (e.g. CI output, prior run logs),
> mark this section as **unverified** rather than assumed-pass.

**Dead code and hygiene**

- [ ] No new unused imports were introduced
- [ ] No debug `print` statements or commented-out code left in
- [ ] No TODO/FIXME comments introduced without a tracking reference

**Documentation and references**

- [ ] Inline comments reflect current behavior, not prior behavior
- [ ] Any updated public APIs are reflected in docstrings
- [ ] Cross-skill references (`code-cleanup`, `code-refactor` notes) are resolved or explicitly deferred

**Security and safety (flag, do not fix)**

- [ ] No secrets, tokens, or credentials appear in the diff
- [ ] No new shell injection vectors (unescaped user input in subprocess calls, etc.)
- [ ] No new file path traversal risks
- [ ] Dependencies added or upgraded are from known, maintained sources

### 5. Fresh-Perspective Questions

Answer each question based on evidence in the code, not intuition:

- Does this solve the original problem completely, or partially?
- Is there anything in the diff that is surprising — behavior that doesn't match the task description?
- Is the implementation something a new team member could follow without needing to ask questions?
- Did the change stay within its stated scope, or did it drift?
- Are there any residual risks from the prior pass that were flagged but not resolved?

---

## Guidance: Before You Flag Something

**Be certain.** If you're going to call something a bug, you need to be confident it actually is one.

- Only review the changes — do not review pre-existing code that wasn't modified.
- Don't flag something as a bug if you're unsure — investigate first. Use `@explore` to search for context.
- Don't invent hypothetical problems — if an edge case matters, explain the realistic scenario where it breaks.
- If you need to verify correct library/API usage, use the `exa-code-context` skill.

**Don't be a zealot about style.**

- Verify the code is _actually_ in violation. Don't complain about else statements if early returns are already being used correctly.
- Some "violations" are acceptable when they're the simplest option. A `let` statement is fine if the alternative is convoluted.
- Excessive nesting is a legitimate concern regardless of other style choices.
- Don't flag style preferences as issues unless they clearly violate established project conventions.

---

## Tools

Use these to inform your review — in order of preference:

- **`@explore` subagent** — Find how existing code handles similar problems. Check patterns, conventions, and prior art before claiming something doesn't fit.
- **`exa-code-context` skill** — Verify correct usage of libraries/APIs before flagging something as wrong.
- **`ddg-search` skill** — Research best practices if you're unsure about a pattern.

_If you're uncertain about something and can't verify it with these tools, say "I'm not sure about X" rather than flagging it as a definite issue._

---

## Output Format

Always produce a structured review report — do not summarize in prose only.

```markdown
## Code Review Report

### Orientation

- Task type: [cleanup / refactor / feature / fix / other]
  -L Files changed: [count and list or reference to git diff]
- Prior pass residual risks reviewed: [yes / no / none present]

### Checklist Results

- Correctness: [pass / issues found]
- Public contracts: [pass / issues found]
- Tests: [pass / issues found / unverified — no bash access]
- Dead code and hygiene: [pass / issues found]
- Documentation: [pass / issues found]
- Security flags: [none / list any]

### Issues Found

For each issue:

- File and line reference
- Description of the problem
- Severity: [blocking / should fix / minor]
- Recommended action
```

### Tone and Clarity Guidance

1. If there is a bug, be direct and clear about why it is a bug.
2. Clearly communicate severity of issues. Do not overstate severity.
3. Critiques should clearly and explicitly communicate the scenarios, environments, or inputs that are necessary for the bug to arise. The comment should immediately indicate that the issue's severity depends on these factors.
4. Your tone should be matter-of-fact and not accusatory or overly positive. It should read as a helpful AI assistant suggestion without sounding too much like a human reviewer.
5. Write so the reader can quickly understand the issue without reading too closely.
6. **AVOID flattery.** Do not give any comments that are not helpful to the reader. Avoid phrasing like "Great job ...", "Thanks for ...".

### Final Verdict

```markdown
### Verdict

[ ] Ready to submit — no blocking issues found
[ ] Needs fixes — blocking issues listed above
[ ] Needs discussion — questions that require user input before proceeding
```

---

## Notes for Agentic Operation

- This skill **does not make changes**. If issues are found, report them. Do not fix them inline during review — that conflates review with implementation and makes the diff harder to reason about.
- Always produce the **full report** before stopping. If a blocking issue is found, mark the verdict as **Needs fixes** and surface it prominently — do not truncate the report.
- If the review uncovers scope drift (the diff contains changes outside what was asked), flag it explicitly rather than silently accepting it.
- Security flags are always reported, even if they appear minor. Do not evaluate severity yourself — surface them for the user.
- If the input type is PR number and `gh` commands fail, report that PR review is unavailable and fall back to reviewing any locally staged/unstaged changes instead.
