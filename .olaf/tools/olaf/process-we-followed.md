# OLAF installer planning workflow (what we just did)

This document summarizes the iterative workflow we followed to go from an idea to a structured, executable implementation plan.

## 1) Write a guide (then improve it)

- We started by drafting a **single source of truth** guide describing the desired installer behavior, constraints, and distribution strategy.
- We iterated on correctness and clarity (cross-platform targets, what gets embedded, what gets copied where, update behavior, GitHub Releases update notification, GitHub Pages install page, etc.).
- The guide is meant to capture:
  - Requirements and invariants (e.g. **never copy `.github/.kiro/.windsurf` into `~/.olaf`**)
  - Architecture decisions (two-layer update: framework files vs binary)
  - Example usage and operating modes

**Artifact:**
- `.olaf/tools/olaf/create-go-installer-guide.md`

## 2) Sketch a Kanban plan from the guide

- We translated the guide into a Kanban JSON board:
  - Columns (backlog → todo → in_progress → review → done)
  - Cards with dependencies, effort/priority, subtasks, acceptance criteria
- This produced an implementable backlog instead of a monolithic “do everything” task.

**Artifact:**
- `.olaf/tools/olaf/olaf-kanban.json`

## 3) Estimate and split when needed

- We reviewed cards for **implementation difficulty**.
- When a card was too large / too risky, we **split it** into smaller, similarly-scoped cards.
- Splitting rules we applied:
  - Keep each card deliverable-focused (one main outcome)
  - Make acceptance criteria concrete and testable
  - Preserve dependency ordering to unblock work

Example splits:
- A single “core installer” card was split into:
  - project skeleton + embed wiring
  - fresh install
  - incremental update
  - repo file copy
  - CLI surface
- “Testing matrix” was split into:
  - unit tests for risky logic
  - manual smoke tests

**Artifacts updated:**
- `.olaf/tools/olaf/olaf-kanban.json`
- `.olaf/tools/olaf/kanban-progress.txt`

## 4) Adapt the execution prompt + artifacts to match the Kanban

We created an execution workflow that can be run repeatedly:

- Select the next most important card (priority + dependencies + unblock value)
- Implement end-to-end
- Verify (including tests)
- Log learnings
- Update progress tracker
- Commit

This keeps the work incremental and traceable.

**Artifacts:**
- `.olaf/tools/olaf/olaf-kanban-execute.md` (execution prompt)
- `.olaf/tools/olaf/kanban-progress.txt` (one-line status per card)
- `.olaf/tools/olaf/kanban-learnings.txt` (learnings and decisions log)

## 5) Inject required guidance (SOLID, TDD/BDD, DoD)

- We added implementation standards so each card is implemented with consistent engineering discipline:
  - SOLID-focused design
  - TDD for non-trivial logic
  - BDD framing for user-visible behaviors
  - A clear Definition of Done (tests, safety, docs, commit)

**Preferred approach (yours):** instead of embedding guidance inside the execution prompt, the prompt should **reference** a separate guidance document. We are now adjusting the workflow accordingly.

**Artifacts:**
- `.olaf/tools/olaf/implementation-guidance.md` (referenced guidance)
- `.olaf/tools/olaf/olaf-kanban-execute.md` (references guidance)

## How to use this workflow going forward

1. Open `.olaf/tools/olaf/olaf-kanban.json` and pick the next card.
2. Follow `.olaf/tools/olaf/olaf-kanban-execute.md` step-by-step.
3. Use `.olaf/tools/olaf/implementation-guidance.md` as the standard.
4. After each card, update:
   - `.olaf/tools/olaf/kanban-learnings.txt`
   - `.olaf/tools/olaf/kanban-progress.txt`
5. Commit with a clear message.
