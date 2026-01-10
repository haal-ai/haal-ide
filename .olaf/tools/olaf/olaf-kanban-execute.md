---
description: Execute the next most important OLAF installer Kanban card end-to-end (implement, verify, log learnings, commit)
---

# OLAF Kanban Execution Prompt

## Inputs
- Kanban file: `.olaf/tools/olaf/olaf-kanban.json`
- Progress file: `.olaf/tools/olaf/kanban-progress.txt`
- Learnings file: `.olaf/tools/olaf/kanban-learnings.txt`

## Operating rules
- Always pick the **single most important** Kanban card to do next.
- Work on **one card at a time**.
- Implement end-to-end.
- Verify thoroughly:
  - For filesystem deliverables: confirm folders/files exist and formats are valid.
  - For code: run tests and add unit tests when meaningful.
- Maintain logs:
  - Append to `kanban-learnings.txt` after completing each card.
  - Update `kanban-progress.txt` (one line per card).
- After each card is completed and verified, create a git commit with a clear message.
- You may create new Kanban cards if learnings show missing work; keep them small and explicit.

## Step 1 — Select the next card
1. Open `.olaf/tools/olaf/olaf-kanban.json`.
2. Consider all cards with `column != "done"`.
3. Choose the “most important” card using this heuristic:
   - Highest priority first (`high` > `medium` > `low`).
   - Then dependency readiness (all dependencies done or not present).
   - Then unblock value (unblocks multiple downstream cards).
   - Then effort (prefer smaller if equal priority/unblock).
4. Announce the selected card id/title.

## Step 2 — Create/confirm a safe verification plan
For the chosen card, define:
- Deliverables (files/folders/code changes expected).
- Verification steps (commands, checks).
- Test plan (unit tests where applicable).

## Step 3 — Implement
- Make the minimal set of changes needed to satisfy the acceptance criteria.
- If you discover missing prerequisite work, add a new Kanban card and stop, unless it’s trivial.

## Step 4 — Verify
- Run verification steps.
- For code changes:
  - Run `go test ./...` (or the relevant test command).
  - Add tests if needed.
  - Re-run tests.
- Confirm outputs.

## Step 5 — Log learnings
Append a new entry to `kanban-learnings.txt` with:
- Date/time
- Card id/title
- What was done
- What was learned / decisions made
- Any follow-up tasks or risks

## Step 6 — Update progress tracker
Update `kanban-progress.txt`:
- Ensure there is exactly one line for the card.
- Mark it as `[x]` when done (or `[ ]` if not done).

## Step 7 — Commit
Create a commit after verification:
- Message format:
  - `kanban(<id>): <short summary>`
- Include only the relevant changes for that card.

## Step 8 — Iterate
Repeat from Step 1 until you stop explicitly.
