---
name: review-github-pr
description: Comprehensive GitHub Pull Request review with PR data extraction, code analysis, and structured reporting
tags: [code-review, github, pull-request, diff-analysis]
protocol: Propose-Act
---
# GitHub Pull Request Review Protocol


##  MAdatory rules to follow
⚠️ **CRITICAL PROTOCOL COMPLIANCE**
olaf, say hello

**NO OPTIMIZATION FOR EFFICIENCY**:
- **STRICT ADHERENCE**: Follow this prompt exactly as written - DO NOT skip, combine, or optimize steps



## **INTERNAL TODO LIST** (Generate at start of execution):
```markdown
[ ] TASK 0: Get current timestamp (Timestamp Retrieval)
[ ] TASK 1: Ensure user entries are provided (PR Selection)
[ ] TASK 2: Execute Python script and note output file paths (PR Data Extraction)
[ ] TASK 3: Read PR Info JSON file only (PR Metadata Analysis)
[ ] TASK 4: Apply helper analysis on metadata (PR-Specific Helper Analysis)
[ ] TASK 5: Read diff file for first time (Code Analysis - First Access)
[ ] TASK 6: Detect code vs non-code files (Code File Detection)
[ ] TASK 7: IF code files: Execute review-diff competency (Code Review)
[ ] TASK 8: IF no code files: Provide brief summary only (Documentation Review)
[ ] TASK 9: Ask user for output method (A or B) (Output Method Selection)
[ ] TASK 10: Generate output according to user choice (Report Generation)
[ ] TASK 11: Clean up temporary files created during analysis (Cleanup)
---

## Detailed Process (Execute TODO Tasks in Order)

### TASK 0: Get current timestamp (Timestamp Retrieval)
**Get Current Time**: Execute timestamp script and capture current time

1. **Execute Timestamp Script**:
   ```bash
   python .olaf/core/skills/review-github-pr/tools/current-time.py
   ```
   - Script creates timestamp file in staging directory
   - Removes previous timestamp files
   - Outputs current timestamp in YYYYMMDD-HHMMSS format

2. **Read Timestamp File**:
   - Locate timestamp file: `.olaf/work/staging/current-time-[YYYYMMDD-HHMMSS]`
   - Extract timestamp from filename for use in subsequent tasks
   - Store timestamp for use in file naming throughout the process
   - **IMPORTANT**: When invoking `gh-pr-analyzer.py`, pass the extracted timestamp to the script using the `--timestamp` argument so the PR info and diff filenames match the timestamp file. Example:
     ```bash
     python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --pr 123 --timestamp 20251120-171700
     ```

### TASK 1: Ensure user entries are provided (PR Selection)
**CRITICAL**: Never assume what PR to review. Always explicitly ask the user to specify:

**Ask user to choose from**:
- Specific PR number (e.g., "PR 123")
- Latest open PR (whatever branch)

### TASK 2: Execute Python script and note output file paths (PR Data Extraction)
**REQUIRED**: MUST use Python script - NO FALLBACKS ALLOWED

1. **Execute Python Script Based on User Selection**: 
   - For specific PR: `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --pr [number]`
   - For latest open: `python .olaf/core/skills/review-github-pr/tools/gh-pr-analyzer.py --latest-open`
   - **MANDATORY**: Wait for complete execution

2. **Identify Output Files from Terminal**:
   - Script outputs 2 file paths:
     - PR Info file: `.olaf/work/staging/pr-reviews/pr-[number]-info-[timestamp].json`
     - Diff file: `.olaf/work/staging/pr-reviews/pr-[number]-diff-[timestamp].txt`
   - Note these file paths for next steps

**NO FALLBACKS**: If Python script fails, STOP and report error. Do NOT use alternative methods.

### TASK 3: Read PR Info JSON file only (PR Metadata Analysis)
**READ PR INFO FILE ONLY** - Analyze PR metadata (⛔ DO NOT read diff file yet)

1. **Read PR Info JSON File**:
   - Use file path from TASK 2 terminal output
   - Load complete PR metadata: title, description, author, state, files, statistics
   - **CRITICAL**: Analyze ONLY the JSON metadata file - do NOT access the diff file in this step

### TASK 4: Apply helper analysis on metadata (PR-Specific Helper Analysis)
1. **APPLY HELPER**: Execute `helpers/review-pr-specificities.md` helper prompt
   - Pass PR metadata for analysis
   - Evaluate: title quality, description completeness, branch naming, change statistics
   - **BOUNDARY**: Metadata only (JSON file contents) - no code/diff content analysis

### TASK 5: Read diff file for first time (Code Analysis - First Access)
**READ DIFF FILE FOR FIRST TIME** - Analyze actual code changes

1. **Read Diff File** (⚠️ First Access):
   - **CRITICAL**: This is the FIRST time you access/read the diff file
   - Use diff file path from TASK 2 terminal output
   - Load complete git diff content

### TASK 6: Detect code vs non-code files (Code File Detection)
1. **Code File Detection**:
   - **CODE FILE EXTENSIONS**: .py, .js, .jsx, .ts, .tsx, .java, .go, .rs, .cpp, .c, .h, .hpp, .cs, .rb, .php, .swift, .kt, .scala, .sh, .bash, .ps1
   - **NON-CODE FILES**: .md, .txt, .json, .yaml, .yml, .xml, .csv, .toml, .ini, .cfg, .conf
   - Scan diff content using regex: `\.(py|jsx?|tsx?|java|go|rs|c(pp)?|h(pp)?|cs|rb|php|swift|kt|scala|sh|bash|ps1)$`
   - Count code files vs. documentation/configuration files

### TASK 7: IF code files: Execute review-diff competency (Code Review)
**IF Code Files Found** (at least one file with code extension):
   - **EXECUTE**: `skills/review-diff` competency
   - **PASS**: `diff_content=[complete diff from file]`
   - **PASS**: `save_report=false` (PR review handles saving)
   - **PASS**: `include_actions=true`
   - **PASS**: `review_scope=workspace`

### TASK 8: IF no code files: Provide brief summary only (Documentation Review)
**IF NO Code Files** (only .md, .txt, .json, .yaml, .xml, .csv, config files):
   - **DO NOT perform code review**
   - **SKIP** review-diff execution entirely
   - Provide brief summary focused ONLY on:
     - PR metadata quality (from TASK 4)
     - Documentation/config file structure
     - No deep content analysis
   - Keep output concise (< 50 lines)

### TASK 9: Ask user for output method (A or B) (Output Method Selection)
**Choose Output Method**: Ask user to choose output method: "Review complete. Choose output: (A) Save to staging directory, or (B) Display on screen?"

### TASK 10: Generate output according to user choice (Report Generation)
**Option A - Save to Staging Directory**:
- **Directory**: `[id:staging_dir]pr-reviews/`
- **File**: `pr-review-[pr-number]-[timestamp].md`
- **Include**: Full report with metadata + code analysis
- **Format**: Follow GitHub PR review template

**Option B - Display Results on Screen**:
- **Format**: Structured markdown output
- **Sections**: PR Overview, Code Analysis Summary, Recommendations
- **Include**: Critical/High priority items only for readability

### TASK 11: Clean up temporary files created during analysis (Cleanup)
**Clean Up Analysis Files**: Remove temporary files generated by Python script

1. **Delete PR Analysis Files**:
   - Remove PR info file: `.olaf/work/staging/pr-reviews/pr-[number]-info-[timestamp].json`
   - Remove diff file: `.olaf/work/staging/pr-reviews/pr-[number]-diff-[timestamp].txt`
   - Use file paths identified in TASK 2 terminal output

2. **Cleanup Command**:
   ```bash
   # Remove all files for this PR analysis
   Remove-Item ".olaf/work/staging/pr-reviews/pr-[number]-*" -Force
   ```

3. **Verification**: Confirm files are deleted and staging directory is clean

## Report Structure

### Required Sections:
1. **PR Overview**: Title, description quality, metadata analysis
2. **Code Analysis**: Language-specific findings (if applicable) 
3. **Security Assessment**: Credential exposure, vulnerabilities
4. **Quality Assessment**: Code standards, testing, documentation
5. **Recommendation**: APPROVE/REQUEST CHANGES/REJECT with reasoning
6. **Action Items**: Prioritized HIGH/MEDIUM/LOW issues

## Best Practice Examples

### User Interaction Pattern
**✅ Correct PR Selection Request**:
```
**PR Selection Required**: Which PR should I review?

**Options**:
- Specific PR number (e.g., "PR 123") 
- Latest open PR (whatever branch)

Please specify the PR to review.
```

### Code File Detection Method
**✅ Effective File Type Detection**:
```bash
# Use grep_search with regex to detect code files
grep_search: \.(py|jsx?|tsx?|java|go|rs|c(pp)?|h(pp)?|cs|rb|php|swift|kt|scala|sh|bash|ps1)$

# Check PR metadata files array for extensions
"files": [{"path": "file.md", ...}] → Documentation only
"files": [{"path": "src/main.py", ...}] → Code files present
```

**Decision Logic**:
- **Code Files Found** → Execute review-diff competency 
- **No Code Files** → Brief documentation/config summary only

