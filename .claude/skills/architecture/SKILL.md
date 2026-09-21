---
name: architecture
description: Disciplined workflow for analyzing an existing software system and designing architectural changes before implementation — new modules/services, significant feature design, schema/API/auth changes, infrastructure changes, cross-cutting concerns, significant refactoring, performance/scalability changes, or anything touching multiple architectural boundaries. Reusable across languages, frameworks, repositories, and system sizes. NOT for simple bug fixes, small isolated features, pure code review, or implementation-only requests.
---

# Architecture

A disciplined workflow for analyzing an existing software system and
designing architectural changes before implementation, reusable across
languages, frameworks, repositories, and system sizes.

**This Skill is for:** new modules or services; significant feature design;
database/schema changes; API/interface changes; authentication/authorization
architecture; infrastructure changes; cross-cutting concerns; significant
refactoring; performance/scalability changes; changes that affect multiple
architectural boundaries.

**This Skill is NOT for:** simple bug fixes; small isolated features; pure
code review; implementation-only requests.

## Workflow

1. **Understand the requirement.** Identify: desired outcome, functional
   requirements, non-functional requirements, constraints, assumptions, and
   explicitly stated out-of-scope areas. If important information is
   genuinely missing and could materially change the architecture, identify
   it explicitly rather than silently assuming it.

2. **Establish repository context.** Before proposing architecture: read
   CLAUDE.md or equivalent project instructions; inspect the repository
   structure; identify the application's architectural style; locate
   relevant modules, services, interfaces, models, repositories,
   configuration, and tests; inspect existing implementations that solve
   similar problems; inspect relevant database schemas and migrations when
   applicable; inspect API contracts when applicable; check dependency and
   build configuration; check recent git history when it provides useful
   architectural context. Do not design against an imagined architecture.

3. **Map the current architecture.** Describe only what is supported by
   repository evidence. Identify: major components, responsibilities,
   dependency direction, data flow, integration boundaries, persistence
   boundaries, external dependencies, important architectural invariants.
   Clearly distinguish observed architecture from assumptions.

4. **Identify constraints and risks.** Consider: backward compatibility,
   data migration, API compatibility, security, performance, scalability,
   reliability, concurrency, observability, deployment, operational
   complexity, testing complexity, dependency impact, failure modes. Only
   discuss risks relevant to the proposed change.

5. **Identify affected areas.** Determine which existing components are
   likely to change. Separate them into: must change, may change, should
   remain unchanged. Avoid expanding the scope unnecessarily.

6. **Develop architectural options.** When there are meaningful design
   choices, provide 2–3 viable options. For each option describe:
   architecture; how data/control flows through it; affected components;
   advantages; disadvantages; migration complexity; operational
   implications; testing implications. Do not create artificial
   alternatives when one approach clearly follows the existing architecture.

7. **Evaluate the options.** Compare options against the actual
   requirements and repository constraints. Consider: correctness,
   simplicity, maintainability, consistency with the existing architecture,
   performance, scalability, reliability, security, migration risk,
   operational cost, implementation complexity, reversibility and ease of
   rollback. Do not optimize for theoretical scale when the requirements do
   not justify it.

8. **Recommend an approach.** Recommend one architecture when the evidence
   supports a clear choice. Explain: why it fits the existing system; why it
   satisfies the requirements; important trade-offs; what is intentionally
   not being solved. Do not recommend a rewrite merely because a different
   architecture would be cleaner in isolation.

9. **Define the implementation plan.** Produce a concrete implementation
   plan containing: components/files likely to change; new components only
   when necessary; interfaces/contracts; data model/schema changes; API
   changes; migration strategy; test strategy; rollout considerations when
   relevant; verification steps. Order the plan so implementation can
   proceed incrementally.

10. **Identify architectural invariants.** Explicitly list things that must
    remain true after implementation — for example: dependency direction,
    transaction boundaries, security boundaries, API compatibility,
    framework-independent core logic, local/cloud boundaries, data
    consistency guarantees.

11. **Stop before implementation.** This Skill is a design/planning Skill.
    Complete the architecture analysis and present the decision gate.
    Do not modify application source code during architecture analysis.
    After user approval, hand off the approved implementation plan to the
    `implement` Skill rather than implementing it within this Skill.

## Output format

Use this structure:

### Architecture Summary
Brief description of the proposed approach.

### Current Architecture
Relevant existing components and data flow.

### Evidence

List the repository evidence that materially influenced the architectural
decision. Clearly distinguish observed facts from assumptions.

This section must be based on actual repository evidence rather than generic
best practices or assumptions.

### Requirements & Constraints
Functional and non-functional requirements that influence the design.

### Affected Components
- Must change
- May change
- Should remain unchanged

### Options
Only include multiple options when meaningful architectural trade-offs exist.

### Recommended Approach
The selected approach and why it fits the system.

### Design
Describe components, responsibilities, dependencies, data flow, interfaces,
and important boundaries.

### Data / API Changes
Describe schema, migration, API, or contract changes when applicable.

### Implementation Plan
Ordered, incremental implementation steps.

### Testing Strategy
Unit, integration, contract, performance, or other relevant verification.

### Risks & Trade-offs
Important risks, limitations, and decisions intentionally left out of scope.

### Architectural Invariants
Properties that implementation must preserve.

## Rules

- Inspect before designing.
- Do not invent repository structure, services, interfaces, or constraints.
- Prefer extending the existing architecture over introducing a new architecture.
- Prefer the simplest design that satisfies the actual requirements.
- Avoid premature abstraction.
- Avoid speculative scalability.
- Avoid unnecessary microservices.
- Avoid unnecessary dependencies.
- Avoid unrelated refactoring.
- Preserve existing architectural boundaries unless there is a concrete reason
  to change them.
- Treat security, data integrity, and backward compatibility as first-class
  architectural concerns when relevant.
- Distinguish facts observed in the repository from assumptions and proposed
  design decisions.
- Do not present theoretical benefits as guaranteed outcomes.
- Do not modify source code while performing architecture analysis.
- Follow the repository's CLAUDE.md instructions.
- Do not commit or push changes.
- If critical information is missing, state exactly what is missing and why it
  matters.
- Do not produce an architecture document filled with generic best practices;
  ground recommendations in the actual repository and requirements.
- Check `git status` before analysis and preserve all pre-existing user changes.
- Never overwrite, revert, or discard changes that were present before the Skill started.
- Prefer incremental and reversible architectural changes when they satisfy the requirements. Clearly identify decisions that would be expensive or difficult to reverse.

## Decision gate

Before implementation, explicitly state:

- what decision needs to be made
- what approach is recommended
- what important trade-offs remain
- whether the change is safe to implement incrementally

If the user approves the approach, stop architecture analysis and recommend
using the `implement` Skill to execute the approved implementation plan.
Do not begin implementation automatically unless the user explicitly asks
to proceed.
