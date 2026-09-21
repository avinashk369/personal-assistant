---
name: implement
description: Disciplined workflow for implementing a requested software change in any language or framework — understand the requirement, inspect the existing code/tests/conventions, make the smallest appropriate change, verify it, and report back. Use whenever the user asks to add, fix, or change behavior in code (not for pure Q&A, review-only, or planning-only requests).
---

# Implement

A repeatable workflow for turning a requested software change into a small,
verified, well-reported diff — independent of language, framework, or project
layout. Follow the repository's own `CLAUDE.md` (or equivalent) first; this
skill fills in the process around it, not a replacement for it.

## Workflow

1. **Understand the requirement.** Restate the change in your own terms:
   what behavior should exist that doesn't (or shouldn't exist and does).
   If genuinely ambiguous in a way that could materially change the
   implementation or is hard to reverse, ask before proceeding. Otherwise,
   pick the least surprising interpretation the repository's own evidence
   supports and continue.

2. **Inspect the repository.** Don't assume structure, framework, build
   commands, or conventions — look. Read the project's own instructions file
   if one exists, skim the directory layout, and open the files most likely
   to be touched.

3. **Identify relevant tests and conventions.** Find the tests that already
   cover this area (if any) and the patterns the codebase uses nearby:
   naming, error handling, layering, module boundaries. Match them rather
   than introducing a new style.

4. **Determine the smallest appropriate implementation.** Prefer extending
   existing code over adding new files, layers, or abstractions. Scope the
   change to exactly what was requested.

5. **For non-trivial changes, explain the approach before editing.** A
   one-line fix doesn't need a preamble. Anything touching multiple files,
   changing an interface, or affecting architecture does — state the plan
   briefly and proceed (only pause for explicit confirmation if the decision
   is ambiguous and hard to reverse, per step 1).

6. **Implement the change.**

7. **Add or update tests for the new behavior.** New behavior gets new
   coverage; changed behavior gets updated coverage. Never edit an existing
   test's assertions just to make it pass — if a test's premise is now
   wrong, say so explicitly and explain why, rather than quietly loosening it.

8. **Run the smallest relevant test suite.** Prefer a scoped run (single
   file/module/package) over the full suite when the project supports it;
   run the full suite if that's the only option or the change is broad.

9. **Run formatting/lint/type checks when the project provides them.**
   Detect these from the project's own config/scripts rather than assuming a
   toolchain — don't add a linter or formatter that wasn't already there.

   ### Verification gate

   If tests, linting, formatting, or type checks fail:

   1. Determine whether the failure is caused by your change.
   2. Fix legitimate regressions.
   3. Do not ignore or suppress failures.
   4. If failures are unrelated to your change, clearly report them instead of attempting unrelated fixes.

   Do not claim the task is complete while relevant checks are failing.

10. **Inspect the final `git diff`.** Read through the actual change, not
    just your memory of what you did. If the final diff contains accidental formatting, debug code, or unrelated edits,
   remove them before considering the implementation complete.

11. **Check for unrelated changes.** Anything in the diff that isn't part of
    the requested change — stray file touches, incidental formatting of
    untouched code, leftover debug output — gets reverted before reporting.

12. **Report:**
    - implementation summary
    - files changed
    - tests/checks run (and their results)
    - important design decisions
    - remaining risks or follow-up work

## Rules

- Never modify tests merely to make them pass.
- Never modify unrelated files.
- Never introduce a new dependency without first checking whether an
  existing dependency or the standard library already covers it.
- Follow the repository's `CLAUDE.md` (or equivalent) instructions.
- Do not commit or push unless explicitly requested.
- Do not assume a framework, architecture, command, or file exists —
  inspect before relying on it.
- Do not stop at a suggestion or plan when the user asked for the change to
  be made — implement it.
- Ask for clarification only when ambiguity could materially change the
  implementation or would be costly/irreversible to get wrong; otherwise
  proceed with the least surprising option.
- Preserve the existing architectural style unless the task explicitly requires changing it.
- Avoid opportunistic refactoring while implementing unrelated features.


## Escalation rules

Pause and ask before proceeding when:

- a database migration changes existing data
- a public API contract changes
- authentication or authorization behavior changes
- a security-sensitive workflow changes
- a destructive operation is required
- multiple reasonable implementations exist with materially different tradeoffs

Otherwise proceed with the least surprising implementation supported by repository evidence.