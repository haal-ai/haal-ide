---
name: learn-from-code
description: Generate newcomer documentation by analyzing code and configuration files with consistent functional and technical sections
tags: [documentation, code-analysis, newcomer-guide, onboarding]
---

## Framework Validation
You MUST apply the <olaf-work-instructions> framework.
You MUST pay special attention to**:
- <olaf-general-role-and-behavior> - Expert domain approach
- <olaf-interaction-protocols> - Appropriate execution protocol
You MUST strictly apply <olaf-framework-validation>.

## Time Retrieval

## Time Retrieval
Get current timestamp using appropriate command in background terminal, then read output:
- **PowerShell**: `Get-Date -Format "yyyyMMdd-HHmm"`
- **Bash**: `date +%Y%m%d-%H%M`


## Input Parameters
You MUST request these parameters if not provided by the user:
- **code_folder_path**: string - Path to the folder containing code and configuration files (REQUIRED)
- **project_name**: string - Name of the project for documentation title (REQUIRED)
- **target_audience**: string - Experience level of newcomers (e.g., "junior developers", "experienced developers new to project") (OPTIONAL, default: "new team members")
- **output_filename**: string - Name for the generated documentation file (OPTIONAL, default: "newcomer-guide-[timestamp].md")

## User Interaction Protocol
You MUST follow the established interaction protocol strictly:
- Act / Propose-Act / Propose-Confirm-Act (defined externally)
- You WILL use Act protocol for this documentation generation task

## Process

### 1. Validation Phase
You WILL verify all requirements:
- Confirm code_folder_path exists and is accessible
- Validate folder contains code and/or configuration files
- Check access to documentation template
- Verify project_name is provided and valid

### 2. Execution Phase

**File Analysis Operations**:
<!-- <code_analysis> -->
You WILL systematically analyze the provided folder:
- Read all code files (.js, .py, .java, .cs, .ts, .php, etc.)
- Read all configuration files (.json, .yaml, .yml, .xml, .ini, .env, etc.)
- Read build/deployment files (package.json, requirements.txt, Dockerfile, etc.)
- Identify project structure and architecture patterns
<!-- </code_analysis> -->

**Template Application**:
<!-- <template_processing> -->
You MUST use template: `[id:templates_dir]/developer/newcomer-documentation-template.md`
You WILL generate documentation following the template structure exactly
<!-- </template_processing> -->

**Core Logic**: Execute following protocol requirements
- You WILL analyze code functionality and business logic for functional section
- You WILL analyze technical architecture, dependencies, and setup for technical section
- You MUST ensure consistent formatting using the template structure
- You WILL provide clear, actionable information for newcomers
- You MUST include setup instructions and common workflows

### 3. Validation Phase
You WILL validate the generated documentation:
- Confirms template structure is followed completely
- Contains both functional and technical sections as required
- Includes actionable setup and workflow instructions
- Uses clear, newcomer-friendly language throughout
- All code references are accurate and up-to-date

## Output Format
You WILL generate outputs following this structure:
- Primary deliverable: Complete newcomer documentation following template `[id:templates_dir]/developer/newcomer-documentation-template.md`
- File location: `[id:ads_dir]staging/[output_filename]`
- Timestamp format: YYYYMMDD-HHmm in filename if using default naming

## User Communication

### Progress Updates
- Confirmation when folder analysis begins
- Status of file types discovered and analyzed
- Confirmation when template is applied successfully
- Location of generated documentation file

### Completion Summary
- Summary of files analyzed (count by type)
- Documentation file created with full path
- Key functional and technical insights discovered
- Any limitations or missing information noted

### Next Steps
You WILL clearly define:
- Documentation ready for newcomer use
- File location: `[id:ads_dir]staging/[output_filename]`
- Recommendation to review and customize for specific team needs
- Suggestion to update documentation as code evolves

## Domain-Specific Rules
You MUST follow these constraints:
- Rule 1: Documentation MUST contain both functional and technical sections (template compliance required)
- Rule 2: All code examples MUST be accurate and reflect actual codebase content
- Rule 3: Setup instructions MUST be complete and testable by newcomers
- Rule 4: Language MUST be accessible to the specified target audience level
- Rule 5: File references MUST use relative paths from project root
- Rule 6: Documentation MUST include common troubleshooting scenarios
- Rule 7: Template structure MUST be followed exactly for consistency

## Success Criteria
You WILL consider the task complete when:
- [ ] Code folder successfully analyzed (all relevant files read)
- [ ] Template loaded and applied correctly
- [ ] Functional section completed with business logic explanation
- [ ] Technical section completed with architecture and setup details
- [ ] Documentation saved in specified location with timestamp
- [ ] All code references validated for accuracy
- [ ] Newcomer-friendly language used throughout
- [ ] Setup instructions are complete and actionable

## Required Actions
1. Validate all required input parameters and folder access
2. Execute comprehensive code and configuration analysis
3. Generate documentation using template structure
4. Provide user communication and file location confirmation
5. Validate output quality and completeness

## Error Handling
You WILL handle these scenarios:
- **Invalid Folder Path**: Request valid path and verify accessibility
- **Empty or No Code Files**: Inform user and request folder with actual code content
- **Template Access Failed**: Provide error message and offer to create basic structure manually
- **Large Codebase**: Inform user of analysis scope and focus on key files/patterns
- **Unrecognized File Types**: Log unknown extensions and focus on standard code/config files
- **Missing Project Context**: Request additional information about project purpose and scope

⚠️ **Critical Requirements**
- MANDATORY: Follow template structure exactly for consistent output format
- MANDATORY: Include both functional and technical sections as specified
- NEVER generate documentation without analyzing actual code content
- NEVER skip validation of code references and examples
- ALWAYS ensure setup instructions are complete and testable
- ALWAYS use newcomer-appropriate language and explanations
- ALWAYS validate template compliance before considering task complete
