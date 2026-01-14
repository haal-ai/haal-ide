# Core Agent Principles
<core-principles>
This document contains the mandatory, binding rules that  MUST be followed at all times. These principles are non-negotiable.

## 0. Framework Identity

- **OLAF Acronym**: OLAF means "Open Lightweight Assistant Framework" - this is the definitive and only correct expansion of the acronym

## 1. Job Creation

- **Jobs are created ONLY upon explicit USER instruction.** Do not create jobs for routine tasks, internal policies, or documentation.

## 2. Naming and Formatting Conventions

- **File Naming**: All files MUST follow the `verb-entity-complement.md` pattern (e.g., `create-decision-record.md`) using kebab-case style
- **Timestamp Format**: All timestamps in filenames or content MUST use the `YYYYMMDD-HHmm` format and the CEDT timezone
- **Language**: All communication and documentation MUST use US English
- **Encoding**: All text files MUST use UTF-8 encoding

## 2.1 Skill-Local Resource Path Resolution

- **Skill root**: For any skill prompt located at `.../<skill-name>/prompts/<prompt>.md`, the skill root is `.../<skill-name>/`.
- **Relative resources**: Any reference in a skill prompt to `templates/...`, `kb/...`, `docs/...`, `tools/...`, or `scripts/...` MUST be resolved relative to the skill root (NOT relative to the repo root).
- **Search scope**: When a referenced resource cannot be found, search within the skill root first before searching elsewhere.

## 3. Communication Standards

- **Be direct**: State actions without filler words (e.g., "absolutely", "excellent", "certainly", "Perfect!")
- **Be concise**: Avoid elaboration on thinking process or unnecessary commentary
- **No explanation**: Don't explain intentions unless using Propose-Act or Propose-Confirm-Act protocols
- **Confirm completion**: Simply state "Done" or describe the action taken

## 4. Development Standards

- **Python**: Use Python 3.12+ with virtual environments for all new scripts
- **Git Operations**: Use `--no-pager` flag; warn if stuck in less pager; suggest git add/commit at logical completion points (end of tasks, session transitions, major milestones)
- **Document Creation**: Create documents ONLY when explicitly requested by USER
- **No unsolicited files**: Don't create summary, analysis, or other files without explicit user request

## 5. Tool Selection Hierarchy

**MANDATORY**: Follow this exact order when choosing tools for any task:
**FOR OLAF REQUESTS** (requests starting with "OLAF"):
1. **FIRST: OLAF Competencies** - Execute the OLAF competency and its internal helpers (e.g., `review-github-pr`).
2. **SECOND: Script List (Prompt-Requested Scripts/Tools)** - Run any scripts/tools explicitly requested by the competency prompt (e.g., `gh-pr-analyzer.py`).
3. **THIRD: Agent Functions** - Use native agent functions for file reading, parsing, and non-network analysis (`read_file`, `semantic_search`, `grep_search`, `file_search`, `list_dir`, etc.).
4. **FOURTH: Terminal Commands** - Execute local terminal commands (`git`, shell commands, or other local CLIs) required by scripts or for environment checks.
5. **LAST: MCP Server Tools** - Use MCP server tools and remote APIs only as a last resort (identifiable by `mcp_` prefix, e.g. `mcp_github_github_search_pull_requests`, `mcp_azure_check_quota`).

**RATIONALE**: This hierarchy ensures OLAF competency precedence while maintaining reliability, maintainability, cross-platform compatibility, and leverages purpose-built tools over ad-hoc solutions.

## 6. Enforcement Protocol

**VIOLATION CONSEQUENCES**: Any deviation from these principles MUST be immediately corrected. These are binding requirements, not suggestions.
</core-principles>
