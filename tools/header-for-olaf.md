CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full ~/.olaf/reference/.condensed/olaf-framework-condensed.md.

CRITICAL: Skill-local resource resolution: if this prompt references `templates/...`, `kb/...`, `docs/...`, `tools/...`, or `scripts/...`, you MUST search for and resolve those paths within THIS SAME SKILL directory. Concretely, resolve them relative to this skill root directory (the parent folder of `prompts/`).

## Time Retrieval
Get current timestamp using time tools, fallback to shell command if needed

