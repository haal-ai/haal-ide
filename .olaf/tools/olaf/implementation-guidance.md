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

### Filesystem abstraction (required for testability)

Installer logic must not call `os.*` directly in deep code paths. Define a minimal filesystem interface and inject it.

Guidelines:
- Keep interfaces tiny (interface segregation).
- Prefer a dedicated adapter for the OS filesystem.
- Unit tests must use temp dirs and/or a fake FS.

### Error handling (required)

- Never ignore returned errors.
- Wrap errors with context: `fmt.Errorf("<action>: %w", err)`.
- Print user-facing errors to **stderr**.

### CLI structure (run() + exit code)

Use a `run()` function that returns an error, and make `main()` only handle exit codes:

- `main()`:
  - calls `run()`
  - prints error to stderr
  - `os.Exit(1)` on failure

### Output conventions

- **stdout**: normal user-facing output (success/info)
- **stderr**: errors and verbose/debug output
- Add `--verbose` (or env var) to enable debug logs.

### Embedded file timestamps caveat

When using `embed.FS`, file `ModTime()` values typically reflect **build time**, not the original source file timestamp.

Therefore:
- Use **checksum-first** update detection for correctness.
- If `mtime` is used, treat it as a hint only (never the only source of truth).

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
