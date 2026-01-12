---
name: carry-over-session
description: Create a simple carry-over note with next prompt and files needed for session continuation
tags: [session, carry-over, continuation, workflow]
---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full ~/.olaf/core/reference/.condensed/olaf-framework-condensed.md.

## Time Retrieval\s*Get current timestamp in `YYYYMMDD-HHmm` format

# Create Carry-Over Session Note

## Purpose
Create a simple carry-over note with TWO items only:
- **Next Prompt**: Exact prompt to continue next session
- **Files Needed**: Absolute paths to open/edit next

## Instructions. **Write Next Prompt**
   - One clear, actionable prompt to resume work
   - Include just enough context to start immediately2. **List Files Needed**
   - Use ABSOLUTE paths from workspace root (e.g., `c:\Users\<user>\coderepos\project\...`)
   - Include all files to read and modify3. **Save File**
   - Path: `[id:carryover_dir]carry-over-YYYYMMDD-HHmm.txt`

## Template
```text
CARRY-OVER - <YYYY-MM-DD HH:mm>
========================

## NEXT PROMPT
<Exact prompt to use next session>

## FILES NEEDED (Absolute Paths)
<c:\Users\<user>\coderepos\project\path\to\file1>
<c:\Users\<user>\coderepos\project\path\to\file2>

## OPTIONAL - Brief Context
<Only if critical: 1–2 lines on current state>
```

## Example
```text
CARRY-OVER - 2025-11-14 14:30
========================

## NEXT PROMPT
Add JWT validation to `AuthService`, update login to return token, and add middleware to protect routes.

## FILES NEEDED (Absolute Paths)
c:\Users\<user>\coderepos\project\src\services\AuthService.ts
c:\Users\<user>\coderepos\project\src\middleware\auth.ts
c:\Users\<user>\coderepos\project\src\routes\api.ts
c:\Users\<user>\coderepos\project\config\jwt.config.ts
c:\Users\<user>\coderepos\project\tests\auth.test.ts
```

