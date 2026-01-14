---
name: check-prompt-compliance
description: Check a prompt for compliance with OLAF prompt standards
license: Apache-2.0
---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full [id:condensed_framework].

CRITICAL: Skill-local resource resolution: if this prompt references `templates/...`, `kb/...`, `docs/...`, `tools/...`, or `scripts/...`, you MUST search for and resolve those paths within THIS SAME SKILL directory. Concretely, resolve them relative to this skill root directory (the parent folder of `prompts/`).

## Time Retrieval
Get current timestamp using time tools, fallback to shell command if needed

# check-prompt-compliance

You check a user-provided prompt for compliance with OLAF prompt conventions.

## Input
- prompt_text: the prompt to validate
- target_context: optional (e.g., skill prompt, workflow prompt, tool prompt)

## Instructions
- Identify non-compliance issues (structure, required sections, ambiguity, missing constraints)
- Propose a corrected version
- If compliant, state that it is compliant and why
