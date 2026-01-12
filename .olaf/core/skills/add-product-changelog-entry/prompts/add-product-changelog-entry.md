---
name: add-product-changelog-entry
description: Add entries to functional or technical product changelogs with linked detail files
tags: [changelog, product, documentation, functional, technical]
---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full ~/.olaf/core/reference/.condensed/olaf-framework-condensed.md.

## Time Retrieval\s*Get current timestamp in `YYYYMMDD-HHmm` format

## Input Parameters
You MUST request these parameters if not provided by the user:
- **changelog_type**: enum[Functional,Technical] - Type of changelog to update (REQUIRED)
- **entry_description**: string - Concise description of the change (REQUIRED)
- **additional_context**: string - Detailed information for the linked detail file (REQUIRED)
- **subject_name**: string - Brief subject name for the detail file (kebab-case) (OPTIONAL - auto-generated if not provided)

## User Interaction Protocol
You MUST follow the established interaction protocol strictly:
- Use Propose-Act protocol for this competency (file modifications with user review)

## Process

### 1. Validation Phase
You WILL verify all requirements:
- Confirm changelog_type is either "Functional" or "Technical"
- Validate entry_description is concise and clear
- Check additional_context provides sufficient detail
- Auto-generate subject_name from entry_description if not provided

### 2. Execution Phase
You WILL execute these operations:

**Template Loading**:
- Load appropriate template: `templates/[changelog_type-lowercase]-changelog-template.md`
- Parse template for entry format and detail file structure

**File Operations**:
- Read current changelog: `[id:product_dir]changelog-[changelog_type-lowercase].md`
- Determine if date section exists, create if needed
- Insert new entry at top of current date's entries
- Create detail file: `[id:product_dir][changelog_type-lowercase]/[subject_name].md`
- Populate detail file using template structure with additional_context

**Core Logic**: Execute following template requirements
- Apply appropriate entry type from template
- Generate clickable markdown link format: `[Details]([subfolder]/[subject_name].md)`
- Maintain proper date section hierarchy (YYYY-MM format, then YYYY-MM-DD subsections)
- Preserve existing formatting and structure

### 3. Validation Phase
You WILL validate results:
- Confirm entry added to correct changelog file
- Verify detail file created with proper content
- Check markdown link is properly formatted and clickable
- Validate no existing structure was damaged

## Output Format
You WILL generate outputs following this structure:
- Primary deliverable: Updated changelog file with new entry
- Supporting files: Detail file in appropriate subfolder
- Link verification: Confirm clickable markdown links work

## User Communication
You WILL provide these updates to the user:

### Progress Updates
- Confirmation of changelog type selection
- Template loading success
- Date retrieved and formatted
- File operations completed

### Completion Summary
- Entry added to: `changelog-[type].md` with date: [YYYY-MM-DD]
- Detail file created: `[type]/[subject].md`
- Clickable link verified: `[Details]([type]/[subject].md)`
- Entry position: Top of current date section

### Next Steps
You WILL clearly define:
- Changelog entry is live and linked
- Detail file can be edited for additional context
- Files are ready for git commit/web publishing

## Domain-Specific Rules
You MUST follow these constraints:
- Rule 1: Always add new entries to the top of their date section (reverse chronological order)
- Rule 2: Create missing date sections following format: `## YYYY-MM` then `### YYYY-MM-DD`
- Rule 3: Use kebab-case for all detail file names (lowercase, hyphens only)
- Rule 4: Preserve all existing changelog formatting and structure
- Rule 5: Generate clickable markdown links using format: `[Details](subfolder/filename.md)`

## Success Criteria
You WILL consider the task complete when:
- [ ] Changelog type validated and template loaded
- [ ] Current date retrieved using terminal
- [ ] Entry added to correct date section in appropriate changelog
- [ ] Detail file created with template structure and user context
- [ ] Markdown link properly formatted and clickable
- [ ] No existing structure damaged or modified

## Required Actions
1. Validate all required input parameters
2. Load appropriate changelog template
3. Execute file operations following template structure
4. Generate outputs with proper linking
5. Provide user communication and verification

## Error Handling
You WILL handle these scenarios:
- **Invalid Changelog Type**: Re-request with valid options (Functional/Technical)
- **Template Not Found**: Provide error and manual template guidance
- **Date Command Failure**: Provide fallback date determination method
- **File Access Issues**: Check permissions and provide alternative approaches
- **Malformed Existing Changelog**: Attempt repair or request manual intervention
- **Link Generation Failure**: Provide manual link format instructions

?? **Critical Requirements**
- MANDATORY: Follow Propose-Act protocol (propose changes, get approval, then execute)
- NEVER modify files without user approval
- ALWAYS preserve existing changelog structure
- ALWAYS generate clickable markdown links
- ALWAYS create detail files using template structure
- ALWAYS add entries in reverse chronological order within date sections

