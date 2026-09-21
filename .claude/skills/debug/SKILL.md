---
name: debug
description: Disciplined, evidence-driven workflow for diagnosing and fixing software defects, failing tests, runtime errors, unexpected behavior, and regressions. Reusable across languages, frameworks, and repositories. Use whenever the user reports a bug, failure, or unexpected behavior — not for implementing new features or pure code review.
---

# Debug

A disciplined, evidence-driven workflow for diagnosing and fixing software
defects, failing tests, runtime errors, unexpected behavior, and
regressions — reusable across languages, frameworks, and repositories.

## Workflow

1. **Understand the symptom**
   - Identify the expected behavior.
   - Identify the actual behavior.
   - Identify the exact error, failing test, stack trace, or reproduction steps.
   - Do not assume the reported cause is the root cause.

2. **Inspect before changing**
   - Read the relevant repository instructions such as CLAUDE.md.
   - Inspect the affected code path.
   - Inspect relevant tests.
   - Inspect configuration and dependencies when relevant.
   - Check recent git changes when they could explain a regression.
   - Do not modify code during initial investigation unless a tiny diagnostic
     change is genuinely necessary.

3. **Reproduce the problem**
   - Run the smallest command/test that demonstrates the failure.
   - Capture the actual failure.
   - If reproduction is not possible, explicitly state that and continue only
     with evidence available from logs, tests, or code.

4. **Trace the failure.** Follow the execution path from symptom toward root
   cause. Consider:
   - input/state
   - control flow
   - data transformations
   - dependencies
   - configuration/environment
   - concurrency/state management
   - persistence/network boundaries
   - error handling

5. **Identify the root cause.** Distinguish:
   - symptom
   - contributing factors
   - root cause

   Do not declare a root cause based only on correlation or a plausible
   guess. Support the diagnosis with evidence from the code, tests, logs, or
   reproducible behavior.

6. **Propose the smallest appropriate fix**
   - Prefer fixing the root cause rather than masking the symptom.
   - Preserve existing architecture and conventions.
   - Avoid unrelated refactoring.
   - Avoid introducing dependencies unless necessary.
   - For non-trivial fixes, briefly explain the proposed approach before editing.

7. **Implement the fix.**

8. **Add or improve regression coverage**
   - Add a test that reproduces the bug when practical.
   - The test should fail before the fix and pass after the fix when feasible.
   - Never weaken or delete a test merely to obtain a passing result.

9. **Verify**
   - Reproduce the original scenario again.
   - Run the smallest relevant test suite.
   - Run broader tests when the change could affect other areas.
   - Run project-provided formatting, linting, and type checks when relevant.

10. **Inspect the final diff**
    - Verify only intended files changed.
    - Remove accidental formatting, debug code, or unrelated changes.
    - Confirm the fix addresses the root cause rather than merely hiding
      the failure.

11. **Report.** Provide:
    - symptom
    - root cause
    - evidence supporting the diagnosis
    - fix implemented
    - files changed
    - tests/checks run and results
    - regression coverage added
    - remaining risks or limitations

## Rules

- Never guess the root cause when it can be investigated.
- Do not repeatedly apply speculative fixes.
- Do not change multiple unrelated things just to see whether the failure
  disappears.
- Do not modify tests merely to make them pass.
- Do not suppress, ignore, or downgrade legitimate errors.
- Do not introduce unrelated refactoring.
- Preserve existing architectural boundaries.
- Follow the repository's CLAUDE.md instructions.
- Do not commit or push unless explicitly requested.
- If the failure is caused by the environment rather than the code, clearly
  distinguish that from an application defect.
- If the available evidence is insufficient to determine the root cause,
  explicitly state what is known, what is unknown, and what additional
  evidence would resolve it.
- Do not claim the bug is fixed until the original failure has been
  successfully verified.
- Before making a fix, check `git status` and preserve any pre-existing user changes.
- Never overwrite or revert user changes that are unrelated to the bug being investigated.

## Verification gate

If a relevant test, lint, type check, build, or reproduction still fails:

1. Determine whether the failure is caused by the change.
2. Fix legitimate regressions.
3. Do not ignore or suppress the failure.
4. Clearly report unrelated pre-existing failures.
5. Do not claim the debugging task is complete while the original issue
   remains unresolved.
