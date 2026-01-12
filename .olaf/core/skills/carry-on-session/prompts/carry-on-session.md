---
name: carry-on-session
description: Load the latest carry-over note and propose the immediate next action for session continuation
tags: [session, carry-on, continuation, workflow]
---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full ~/.olaf/core/reference/.condensed/olaf-framework-condensed.md.

# Carry On Session

## Purpose
Load the latest carry-over note and propose the immediate next action. Wait for user approval before doing anything.

## Rules
- Do NOT auto-run workflows or competencies.
- Do NOT modify files until the user approves.

## Instructions1. Find latest carry-over file in `[id:carryover_dir]` matching `carry-over-YYYYMMDD-HHmm.txt` (most recent by timestamp).
2. Parse sections:
   - `## NEXT PROMPT` (required)
   - `## FILES NEEDED` (optional)
   - `## OPTIONAL - Brief Context` (optional)
3. Present a concise proposal and ask for approval. Do not take any action until the user approves.

## Output Template
```text
## Resuming from Carry-Over
- Carry-Over File: [filename]
- Session Date: [YYYY-MM-DD HH:mm]

### Proposed Plan (from NEXT PROMPT)
[Paste NEXT PROMPT verbatim]

### Files To Open
[List each absolute path from FILES NEEDED]

Confirm: Proceed with the proposed plan? (Yes/No)
If No, please specify adjustments.
```
