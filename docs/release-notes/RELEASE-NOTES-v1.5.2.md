# Release v1.5.2 - Enhanced Script Output Processing

**Release Date:** 2025-09-28  
**Tag:** [v1.5.2](https://github.com/AmadeusITGroup/olaf/tree/v1.5.2)

## Overview

This patch release improves OLAF's reliability by enhancing how analysis prompts process script-generated outputs. The focus is on ensuring structured data from Python analysis scripts is properly read and integrated into final reports.

## 🚀 New Features

- **Structured Data Extraction Framework**: All analysis prompts now include detailed instructions for parsing script-generated markdown files with explicit validation steps
- **Mandatory Data Integration Requirements**: Added comprehensive requirements for incorporating script output into final analysis reports with cross-reference validation

## 🔧 Enhancements

- **Enhanced Script Output Processing**: Updated 6 critical analysis prompts with improved parsing capabilities:
  - `analyze-workspace-content-structure.md` - Repository structure tables and dependency mappings
  - `analyze-repo-language-distribution.md` - Language percentages and project type detection  
  - `measure-repo-size-metrics.md` - Size tables and file category breakdowns
  - `identify-code-hotspot-patterns.md` - Hotspot rankings and risk assessments
  - `analyze-critical-contributor-impact.md` - Bus factor analysis and ownership patterns
  - `analyze-cyclomatic-complexity-metrics.md` - Complexity metrics and recommendations

- **Improved Data Processing Reliability**: Added "CRITICAL" instructions to read script output files with structured parsing requirements for tables, statistics, and recommendations

- **Competency Management Cleanup**: Synchronized competency indexes and removed duplicate entries, added missing "release notes" competency

## 🛠️ Technical Changes

- **Prompt Enhancements**: 188 insertions, 112 deletions across 6 analysis prompts with enhanced validation phases and improved Core Logic sections
- **Workflow Streamlining**: Removed research-stage unit test evolution workflow to focus on production-ready features

## 📚 Documentation

- **User Guidance**: Clarified branching strategy - users should use latest release from main branch
- **IDE Support**: Updated platform list and OLAF acronym definition in VSCode extension README

## 🔒 Security

- **Dependency Update**: Updated tar-fs from 2.1.3 to 2.1.4 in VSCode extension addressing security vulnerabilities
- **CI/CD Enhancement**: Added OpenSSF Scorecard workflow for continuous security assessment

## 🔄 Breaking Changes

None - All existing workflows remain fully compatible.

## 💥 Contributors

@ppaccaud, @wherka-ama

## 📝 Upgrade Instructions

No special upgrade steps required. Simply update to the latest version from the main branch.

## 🎯 Impact

This release addresses a critical reliability issue where analysis prompts were launching Python scripts but not properly reading their file outputs. Enhanced parsing capabilities ensure:

- **More Accurate Analysis**: Proper integration of script-generated metrics and recommendations
- **Improved Reliability**: Consistent handling of structured data from analysis tools  
- **Better User Experience**: More comprehensive and accurate analysis reports

---

**Full Changelog**: [v1.5.1...v1.5.2](https://github.com/AmadeusITGroup/olaf/compare/v1.5.1...v1.5.2)

*Generated using OLAF's professional release notes competency*
