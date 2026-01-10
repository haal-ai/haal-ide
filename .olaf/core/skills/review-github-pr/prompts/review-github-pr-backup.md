---

name: review-github-pr

description: Perform a comprehensive code review of GitHub Pull Requests with user-guided selection and automated analysis.

tags: [code-review, github, pull-request, automation, propose-confirm-act]

---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full ~/.olaf/core/reference/.condensed/olaf-framework-condensed.md.

## ⚠️ TERMINAL OUTPUT HANDLING PRINCIPLE

**FUNDAMENTAL RULE**: For EVERY command execution:
1. Use `run_in_terminal` to execute command
2. **ALWAYS WAIT** for command to complete fully
3. Use `terminal_last_command` to read the **COMPLETE OUTPUT**
4. **EXTRACT and USE** the actual data from terminal output
5. **NEVER assume** - always verify actual output content

**This applies to**: timestamp commands, script execution, git commands, ALL terminal operations.

## Time Retrieval
Get current timestamp using time tools, fallback to shell command if needed 
  1. Run the command with `run_in_terminal`
  2. **WAIT** for command to complete fully
  3. Use `terminal_last_command` to read the **COMPLETE output**
  4. **EXTRACT** the actual timestamp value from output
- **SUCCESS = Actual timestamp extracted (e.g., "20251120-1127")**
- **Use the real timestamp value from terminal output for documentation**

## GitHub Data Collection - MANDATORY SEQUENCE

**⚠️ CRITICAL: ALWAYS FOLLOW THIS EXACT ORDER - DO NOT SKIP STEPS**

**🚫 ABSOLUTE PROHIBITION: DO NOT USE MCP SERVER TOOLS FOR DATA COLLECTION UNLESS EXPLICITLY INSTRUCTED BY USER**

### STEP 1: PRIMARY METHOD (REQUIRED FIRST)
**ALWAYS START HERE**: Use GitHub PR Analyzer Script

**MANDATORY COMMAND**: `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --pr [number]`

Located: `.olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py`

**CRITICAL EXECUTION PROCESS**:
1. Run script with `run_in_terminal` tool
2. **WAIT** for script to complete fully (do NOT proceed until finished)
3. Use `terminal_last_command` to read **ALL OUTPUT**
4. **VERIFY** you received structured data (look for "=== GitHub PR Analysis Report ===")
5. **EXTRACT** the complete PR data from terminal output

**Usage Examples**:
- `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --pr 123` - Analyze specific PR
- `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --branch feature/my-branch` - Latest PR for branch  
- `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --latest-open` - Latest open PR

**Script Benefits**:
- Handles GitHub CLI authentication automatically
- Returns comprehensive PR analysis in structured format
- Includes: PR details, diff, files changed, reviews, status checks
- Simplifies all GitHub interactions

**DO NOT PROCEED TO STEP 2 UNLESS THIS SCRIPT FAILS**

### STEP 2: Fallback Method (Only if Python script fails)
**Direct GitHub CLI Commands**:
- `gh auth status` - Check authentication
- `gh pr list --state open` - List open PRs
- `gh pr view [number]` - View PR details
- `gh pr diff [number]` - Get PR changes

**DO NOT PROCEED TO STEP 3 UNLESS GITHUB CLI FAILS**

### STEP 3: Last Resort (Only if GitHub CLI unavailable)
**Local Git Commands**:
- Use git commands for branch comparison
- `git diff main..feature-branch` for changes

**🚫 MCP TOOLS PROHIBITION: NEVER use MCP server tools (github-pull-request_*, activate_*, etc.) for initial data collection unless user explicitly requests their use**

## Input Parameters

**MANDATORY**: You MUST always ask the USER first to specify what to review.

**CRITICAL**: Never assume what PR to review. Always explicitly ask the user to specify:

### PR Selection (Required - Ask User)
- **What to review**: Ask user to choose from:
  - Specific PR number (e.g., "PR 123")  
  - Branch name (e.g., "feature/new-feature")
  - "Latest open PR" 
  - "Current branch changes"

### Repository Context (Optional)
- **repository**: string - Repository in format 'owner/repo' (default: auto-detect from git)

**Note**: All reviews are comprehensive by default, covering all aspects (security, workflow, quality, compliance) automatically.

## Process

**MANDATORY FIRST STEP**: Always ask the user what they want to review before proceeding.

### Phase 1: User Selection & Data Collection

**STEP 1**: Ask User for PR/Branch Selection (MANDATORY FIRST):
   - Ask user to specify: PR number, branch name, "latest open PR", or "current branch changes"
   - Get user's choice before proceeding

**STEP 2**: MANDATORY Data Collection Sequence:

**2A. PRIMARY METHOD - Python Script (ALWAYS TRY FIRST - NO MCP TOOLS)**:
   - **REQUIRED COMMAND**: `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --pr [number]` OR
   - **REQUIRED COMMAND**: `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --branch [branch-name]` OR  
   - **REQUIRED COMMAND**: `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --latest-open`
   - **CRITICAL EXECUTION STEPS**:
     1. Use `run_in_terminal` to execute script
     2. **WAIT** for complete execution (do NOT proceed prematurely)
     3. Use `terminal_last_command` to read **ALL terminal output**
     4. **ANALYZE** the actual output content from terminal
   - **SCRIPT SUCCESS = Find "=== GitHub PR Analysis Report ===" in terminal output**
   - **SCRIPT FAILS = Error messages, command not found, or no structured data in output**
   - **IF SCRIPT SUCCESS**: Extract and use all PR data from terminal output for analysis
   - **IF SCRIPT FAILS**: Proceed to 2B

**2B. FALLBACK METHOD - GitHub CLI (Only if Python script failed)**:
   - **CRITICAL EXECUTION STEPS**:
     1. Run: `gh auth status` with `run_in_terminal`
     2. **WAIT** for complete execution, then use `terminal_last_command` to read output
     3. Run: `gh pr view [number]` with `run_in_terminal` for PR details
     4. **WAIT** and read complete output with `terminal_last_command`
     5. Run: `gh pr diff [number]` with `run_in_terminal` for changes
     6. **WAIT** and read complete output with `terminal_last_command`
   - **IF CLI SUCCESS**: Use complete CLI output from terminal for analysis  
   - **IF CLI FAILS**: Proceed to 2C

**2C. LAST RESORT - Local Git (Only if GitHub CLI failed)**:
   - Run: `git diff main..feature-branch` for changes
   - Use local git data for analysis

**🚫 ABSOLUTE PROHIBITION: NEVER use MCP server tools for data collection unless user explicitly requests them**
### Phase 2: PR-Specific Analysis (Standards-Based)
1. **Load PR Specificities Helper**: Read complete content of `helpers/review-pr-specificities.md`
2. **Execute Standards Loading**: Helper will load all four PR review standards files:
   - `pr-description-standards.md` - PR title/description quality criteria
   - `ci-cd-integration-standards.md` - Build/test/security status interpretation  
   - `review-workflow-standards.md` - Approval/conflict resolution workflows
   - `branch-workflow-standards.md` - Naming conventions/merge strategies
3. **Perform Comprehensive Analysis**:
   - Execute complete PR metadata analysis using all loaded standards
   - Automatically include code analysis for thorough review
   - Cover all focus areas: security, workflow, quality, and compliance
4. **Generate PR-Specific Findings**: Use standards' severity classification (HIGH/MEDIUM/LOW)

### Phase 2.5: Code Files Detection & Analysis (MANDATORY)
**⚠️ CRITICAL: ALWAYS PERFORM THIS CHECK - NEVER SKIP**

1. **MANDATORY Code File Detection**: Analyze PR diff to identify actual code files
   - **Code File Extensions**: `.ts`, `.js`, `.py`, `.java`, `.cs`, `.cpp`, `.c`, `.go`, `.rs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, etc.
   - **Non-Code Files**: Skip if only these file types:
     - Documentation: `.md`, `.txt`, `.doc`, `.pdf`
     - Configuration: `.json`, `.yaml`, `.yml`, `.xml`, `.ini`, `.config`
     - Binary/Assets: `.zip`, `.tar.gz`, `.png`, `.jpg`, `.pdf`, bundles
     - Build/Package: `package.json`, `pom.xml`, `Dockerfile`, manifests
   
2. **MANDATORY Decision Documentation**: 
   - **ALWAYS STATE**: "Code file analysis: [DETECTED/NOT DETECTED]"
   - **List detected code files** if any found
   - **Explain decision**: Why skipping or proceeding with code analysis

3. **IF CODE FILES DETECTED**: Execute review-diff competency
   - **REQUIRED**: Read and execute `[id:skills_dir]review-diff/prompts/review-diff.md` competency
   - **Pass Complete PR Diff**: Provide full diff content as parameter
   - **Integration**: Merge code analysis with PR metadata findings

4. **IF NO CODE FILES**: Document and skip code analysis
   - **STATE**: "No code files detected in PR - focusing on metadata/configuration review only"
   - **Continue**: Proceed with PR metadata analysis only

### Phase 3: Output & Documentation
1. **Determine Analysis Scope**: Based on presence of code files in PR
2. **Generate Appropriate Review**:
   - **With Code**: PR metadata analysis + code diff analysis results  
   - **Without Code**: PR metadata analysis only
3. **Generate Unified Action Plan**: Both PR-level and code-level improvements (if applicable)
4. **Merge Recommendation**: approve/request changes/reject based on combined analysis
5. **Present Review Results**:
   - Show comprehensive analysis from PR metadata and optionally code diff review
   - Highlight critical issues from all sources
   - Provide actionable recommendations
6. **Save Review & Action Plan**:
   - **ALWAYS propose saving results** - Ask user if they want to save the review
   - **If user agrees**, save to: `[id:staging_dir]code-reviews/github-pr-review-YYYYMMDD-HHmm.md`
   - **AFTER SAVING**: Automatically propose creating a curative action plan
   - **Use template**: `templates/code-review-action-plan-template.md`
   - **Save action plan** to: `[id:staging_dir]code-reviews/github-pr-action-plan-YYYYMMDD-HHmm.md`

## Output/Result Format
- GitHub PR review with:
  - Summary of staging
  - File-specific comments
  - Suggested improvements
  - Security recommendations
  - Overall assessment

## Output to USER
1. **Review Summary**:
   - PR overview
   - Key staging
   - Required actions
2. **Detailed Feedback**:
   - Per-file analysis
   - Code suggestions
   - Security concerns
3. **Review Status**:
   - Approval status
   - Blocking issues
   - Next steps

## Domain-Specific Rules
- Rule 1: Respect GitHub review guidelines
- Rule 2: Follow team's coding standards
- Rule 3: Prioritize security issues
- Rule 4: Provide actionable feedback
- Rule 5: Maintain professional tone

## Required Actions

### Pre-Review (Mandatory)
1. **ALWAYS ask user first** what PR/branch to review  
2. **Get user's choice** and proceed with data collection

### Data Collection (Mandatory Sequence)
1. **NEVER USE MCP TOOLS FIRST**: Absolutely prohibited unless user explicitly requests
2. **ALWAYS TRY PYTHON SCRIPT FIRST**: Run `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py` with appropriate arguments
3. **ONLY IF PYTHON FAILS**: Fall back to GitHub CLI commands
4. **ONLY IF CLI FAILS**: Use local git commands  
5. **MCP TOOLS**: Only use if explicitly requested by user

### Review Process (After Data Collection)
1. **Analyze Script/CLI Output**: Review comprehensive data (PR details, diff, files, reviews, status)
   - **CRITICAL: Read complete terminal output content, focus on structured data not exit codes**
   - **Success indicator: Presence of "=== GitHub PR Analysis Report ===" or similar structured output**
2. **PR Metadata Analysis**: Examine PR against all standards (description, CI/CD, workflow, branch)  
3. **MANDATORY Code File Check**: 
   - **ALWAYS ANALYZE**: Check PR diff for actual code files vs config/docs/binaries
   - **DOCUMENT DECISION**: State whether code files detected or not
   - **EXPLAIN REASONING**: Why proceeding with or skipping code analysis
4. **Conditional Code Analysis**: 
   - **IF CODE FILES PRESENT**: Execute `[id:skills_dir]review-diff/prompts/review-diff.md` directly with diff content
   - **IF NO CODE FILES**: Skip code analysis, document this decision
5. **Combine Results**: Merge PR metadata findings with code diff analysis results (if applicable)
6. **Generate Complete Review**: Create structured feedback with severity levels covering all areas
7. **Present Results**: Show comprehensive analysis to user

### Post-Review (Mandatory)
1. **ALWAYS propose saving results** - Ask user if they want to save the review as a file
2. **If user agrees**, save to: `[id:staging_dir]code-reviews/github-pr-review-YYYYMMDD-HHmm.md`
3. **AFTER SAVING**: Automatically propose creating a curative action plan with specific steps
4. **Use template**: `templates/code-review-action-plan-template.md`
5. **Save action plan** to: `[id:staging_dir]code-reviews/github-pr-action-plan-YYYYMMDD-HHmm.md`

⚠️ **Critical Notes**
- Never expose sensitive information
- Follow branch protection rules
- Respect code ownership
- Document review decisions
- Consider CI/CD status