# Release Notes v1.3.0
**Release Date**: August 14, 2025  
**Previous Version**: v1.2.1

## 🎯 Highlights

### ✨ New & Enhanced Workflows
- Added an agentic Unit Test Augmentation workflow that suggests new cases and iteratively expands coverage.
- Refined complexity analysis helpers and reporting for clearer hot-spot detection and remediation steps.
- Introduced standardized code quality review prompts and templates for accessibility (WCAG-minded) and code smells.

### 🧭 Framework & Delegation Protocol
- Delegation Protocol now enforces session initialization checks so the memory map, core principles, and competency index are loaded at the start of each session.
- Competency index updated to include the Unit Test Augmentation competency.

### 🛠 Fixes & Cleanups
- Normalized default "Core solution" path to `my-repo/` across prompts and docs (replacing legacy `roo-code/` used during internal tests).
- Restored the `<olaf-memory-map>` section tag to ensure framework parsing and validation works reliably.
- Minor documentation polish and timestamp housekeeping.

## 📊 Statistics
- Total Commits: 9
- Scope: prompts, workflows, rules (.windsurf), docs

## 🔍 Technical Notes and Compatibility
- Unit Test Augmentation workflow and quality review prompts extend developer tooling for test coverage and static checks.
- Delegation rule at `.windsurf/rules/team-delegation.md` now enforces session initialization.
- Path references standardized to `my-repo/` per `core-knowldege/memory-map.md`.
- No breaking changes; upgrade requires no manual steps.

---
**Full Changelog**: [v1.2.1...v1.3.0](https://github.com/AmadeusITGroup/olaf/compare/v1.2.1...v1.3.0)
