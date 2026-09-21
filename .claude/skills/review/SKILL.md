---
name: review
description: Disciplined, evidence-driven workflow for reviewing completed software changes — features, bug fixes, architectural implementations, refactoring, API/database changes, security- or performance-sensitive changes, or a set of related commits/working-tree changes — to determine whether they are correct, satisfy the requirement, preserve the existing architecture, are adequately tested, and introduce no significant regression or safety risk. Reusable across languages, frameworks, repositories, and system sizes. NOT for implementing changes, designing architecture from scratch, debugging an unknown failure, pure stylistic preference, or broad unrelated code cleanup.
---

# Review

A disciplined, evidence-driven workflow for reviewing completed software
changes before they are considered ready, reusable across languages,
frameworks, repositories, and system sizes.

**This Skill is a reviewer, not an implementer.** Its responsibility is to
answer: *based on the requirement, repository architecture, implementation,
tests, and available verification evidence, is this change ready to be
considered complete?* It should not silently fix problems it discovers.

**Appropriate for:** reviewing a completed feature or change; a bug fix; an
architectural implementation; refactoring; API or database changes;
security-sensitive changes; performance-sensitive changes; a set of related
commits or working-tree changes.

**NOT for:** implementing changes; designing architecture from scratch;
debugging an unknown failure; pure stylistic preference; broad unrelated
code cleanup.

## Principles

1. Review the actual change, not an imagined implementation.
2. Inspect repository instructions and context before judging the change.
3. Review the diff and surrounding code.
4. Verify the implementation against the stated requirement.
5. Verify that existing architectural boundaries and invariants are preserved.
6. Prefer concrete evidence over assumptions.
7. Distinguish correctness problems from optional improvements.
8. Do not turn personal preferences into review findings.
9. Do not recommend unrelated refactoring.
10. Do not modify application source code while performing the review.
11. Do not modify tests simply to make the implementation appear correct.
12. Never claim that a change is safe merely because tests pass.
13. Consider relevant security, data integrity, compatibility, performance,
    reliability, and operational concerns.
14. Preserve all pre-existing user changes.
15. Do not commit or push changes.
16. If a finding is uncertain, explicitly state the uncertainty and what
    evidence is missing.
17. Review severity should be based on impact and likelihood, not the
    number of findings.

## Workflow

1. **Understand the change**
   - Identify what the change is intended to accomplish.
   - Read the user's requirement or implementation request.
   - Identify functional and non-functional expectations.
   - Identify explicitly stated constraints.
   - If the requirement is ambiguous, identify the ambiguity rather than
     silently assuming.

2. **Establish repository context**
   - Read CLAUDE.md or equivalent repository instructions.
   - Inspect relevant repository structure.
   - Identify the affected modules and architectural boundaries.
   - Inspect relevant existing implementations and patterns.
   - Inspect relevant tests.
   - Inspect configuration, dependencies, schemas, migrations, or API
     contracts when applicable.
   - Use recent git history when it provides useful context.

3. **Establish the change boundary**
   - Run `git status` before beginning the review.
   - Establish the review baseline before inspecting implementation changes.
   - Treat changes already present before the review as out of scope unless the
      user explicitly includes them in the review target.
   - Inspect the relevant git diff.
   - Identify files changed by the implementation.
   - Distinguish pre-existing user changes from changes belonging to the
     implementation under review.
   - Never overwrite, revert, discard, or modify pre-existing user changes.
   - If the review target is unclear, state exactly what cannot be
     reliably reviewed.

4. **Review implementation correctness.** Verify:
   - The implementation actually satisfies the requirement.
   - Control flow and data flow are correct.
   - State transitions are correct.
   - Error handling is appropriate.
   - Edge cases are handled where required.
   - External integrations are used correctly.
   - Persistence and transaction behavior are correct where relevant.
   - Concurrency behavior is safe where relevant.
   - Resource lifecycle is handled correctly where relevant.

5. **Review architectural consistency.** Verify:
   - Existing architectural boundaries are respected.
   - Dependency direction remains appropriate.
   - Responsibilities are located in the correct modules.
   - Existing abstractions are reused where appropriate.
   - No unnecessary abstraction or architectural complexity was introduced.
   - Framework-independent logic remains appropriately separated when the
     architecture requires it.
   - Security, persistence, API, and integration boundaries remain intact.

6. **Review tests.** Verify:
   - Appropriate behavior is covered by tests.
   - Important regression cases are covered.
   - Tests validate behavior rather than implementation details where
     appropriate.
   - Tests are meaningful and not artificially weakened.
   - Existing tests remain valid.
   - Relevant integration, contract, or end-to-end coverage exists when
     required by the change.
   - Do not require a specific test type when the repository's
     architecture does not justify it.

7. **Review risk areas.** Consider only risks relevant to the change:
   - Security
   - Authentication/authorization
   - Data integrity
   - API compatibility
   - Database migration safety
   - Backward compatibility
   - Performance
   - Reliability
   - Concurrency
   - Observability
   - Deployment/rollback
   - Dependency changes
   - Configuration/environment behavior

8. **Check for unnecessary changes.** Identify:
   - Unrelated modifications
   - Accidental formatting changes
   - Debug logging
   - Dead code
   - Temporary workarounds
   - Unnecessary dependencies
   - Scope expansion
   - Opportunistic refactoring

   Do not flag harmless differences merely because they are different from
   personal preference.

9. **Verify the implementation.** Run the smallest relevant verification
   available in the repository:
   - Focused tests first
   - Then broader tests when appropriate
   - Formatting/lint/type checks when provided by the project
   - Build or other verification when relevant

   If verification fails:
   - Determine whether the failure was caused by the change.
   - Distinguish implementation regressions from pre-existing/environment
     failures.
   - Do not suppress or ignore failures.
   - Do not modify tests merely to make verification pass.
   - Report unresolved relevant failures clearly.

10. **Classify findings** using:

    **Critical**
    - Security vulnerability
    - Data corruption/loss
    - Severe correctness issue
    - Breaking production behavior
    - Other issues that make the change unsafe to accept

    **High**
    - Significant functional defect
    - Important regression risk
    - Serious compatibility, reliability, or architectural problem

    **Medium**
    - Meaningful correctness, maintainability, testing, or operational
      concern
    - Should generally be addressed before considering the change complete

    **Low**
    - Minor issue with limited impact

    **Suggestion**
    - Optional improvement that does not materially affect correctness,
      safety, or maintainability

    Do not manufacture findings merely to populate every category.

11. **Determine review outcome.** The final outcome should be one of:

    **Approve**
    - No material issues found and relevant verification is satisfactory.

    **Approve with suggestions**
    - No material correctness or safety issues found, but optional
      improvements exist.

    **Changes requested**
    - One or more material issues should be addressed before the change is
      considered complete.

    Do not use the outcome as a subjective quality score.

12. **Final verification.** Before reporting:
    - Re-check the final diff.
    - Confirm findings are actually supported by repository evidence.
    - Ensure no finding is based solely on personal preference.
    - Confirm pre-existing user changes were preserved.
    - Confirm unresolved verification failures are reported.
    - Do not claim a clean review if material issues remain.

## Output format

Use this structure:

### Review Summary
Brief description of what was reviewed and the overall outcome.

### Scope Reviewed
List:
- Requirement/change reviewed
- Relevant files/modules
- Tests/checks executed
- Any review limitations
- If the available evidence is insufficient to verify an important property,
  do not infer that the property is correct. Report the limitation and what
  evidence would be required to verify it.

### Findings

For each finding:

**[Severity] — Short title**
- Location: file/path and relevant symbol or line when available
- Evidence: what the code/repository shows
- Impact: why it matters
- Recommendation: what should change

Order findings by severity. If there are no material findings, explicitly
state that.

### Verification
List the checks performed and their results. Clearly distinguish:
- Passed
- Failed because of the change
- Failed for unrelated/pre-existing/environment reasons
- Not run and why

### Positive Observations
Mention important aspects that are correctly implemented when they provide
useful evidence, but do not turn this into generic praise.

### Remaining Risks
Only include meaningful unresolved risks.

### Review Outcome
One of: Approve / Approve with suggestions / Changes requested. Include a
concise evidence-based reason.

## Rules

- Inspect before judging.
- Review the actual diff and surrounding code.
- Read CLAUDE.md or equivalent instructions.
- Check `git status` before analysis.
- Preserve all pre-existing user changes.
- Never overwrite, revert, discard, or modify pre-existing changes.
- Do not modify application source code during review.
- Do not modify tests to make the implementation pass review.
- Do not invent requirements.
- Do not invent repository architecture.
- Do not treat personal coding preferences as defects.
- Do not recommend unrelated refactoring.
- Do not recommend unnecessary dependencies or abstractions.
- Prefer repository conventions over generic best practices.
- Distinguish facts, assumptions, risks, and suggestions.
- Use evidence for every material finding.
- Consider security and data integrity when relevant.
- Consider backward compatibility when relevant.
- Consider performance only when the change makes it relevant.
- Do not optimize for theoretical scale without evidence.
- Do not require unnecessary test types.
- Do not suppress, ignore, or hide failed verification.
- Distinguish environment failures from implementation failures.
- Do not claim a change is correct solely because tests pass.
- Do not claim a change is broken solely because it differs from a
  preferred implementation.
- Do not commit or push changes.
- Do not modify CLAUDE.md or other project instructions unless explicitly
  requested.
- Do not create additional Skills as part of this Skill.
- Do not automatically invoke the `implement` or `debug` Skill.
- If changes are requested, clearly describe what needs to be addressed so
  the appropriate implementation/debug workflow can be used separately.

## Final review discipline

A good review should be: evidence-driven, specific, severity-aware,
concise, actionable, consistent with the repository, and focused on
material risks. Do not produce a generic code-review checklist as the
final output.
