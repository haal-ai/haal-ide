# Implementation guidance (SOLID + TDD/BDD)

This document is the reference standard for implementing Kanban cards in this repo.

## SOLID (practical application)

- **Single Responsibility**: keep packages and functions focused. Prefer splitting “do everything” functions into small units.
- **Open/Closed**: extend behavior via new types/functions; avoid modifying core logic when adding a feature.
- **Liskov**: if you introduce interfaces (FS/HTTP/Clock), test substitutes must behave like the real ones.
- **Interface Segregation**: small interfaces (e.g. `ReadFile`, `WriteFile`, `Stat`) over a large “god interface”.
- **Dependency Inversion**: core logic depends on interfaces; wire real implementations in `main`.

### Recommended boundaries for this project

- **Pure decision logic** (easy to test):
  - path mapping
  - update decision (needsUpdate)
  - argument parsing
- **Side effects** (wrap behind interfaces):
  - filesystem reads/writes
  - HTTP calls (GitHub)
  - time/clock

## TDD (default)

Use TDD for any non-trivial logic or anything that can break silently.

Cycle:
1. **Red**: write a small failing test.
2. **Green**: implement the minimum to pass.
3. **Refactor**: cleanup with tests staying green.

Rules:
- One behavior per test.
- Tests must use temp dirs and never touch real user home/`~/.olaf`.

## BDD (for user-visible behavior)

For each Kanban card, express the main scenario(s) as:
- **Given** …
- **When** …
- **Then** …

Map acceptance criteria directly to these scenarios.

## Definition of Done (DoD)

A card is “Done” only when:

- **Acceptance criteria** met.
- **Tests**:
  - Relevant unit tests added/updated.
  - `go test ./...` passes.
  - Tests run safely (temp dirs only).
- **Safety**:
  - No accidental writes outside intended target dirs.
  - No deletion of user data unless explicitly required.
- **Quality**:
  - Clear error messages.
  - No dead code.
- **Traceability**:
  - `kanban-learnings.txt` updated.
  - `kanban-progress.txt` updated.
  - A commit exists for the card.
