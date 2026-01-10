---
name: research-and-report-master
description: Master coordinator for structured research with comprehensive reporting
tags: [research, reporting, web-search, analysis, documentation, master-chain]
pattern: session-chained-master
---

# Research and Report - Master Chain Coordinator

## Master Chain Protocol

**CRITICAL EXECUTION RULES**:
- ALWAYS display the complete task list at the start of execution
- Execute tasks in STRICT SEQUENTIAL ORDER
- Load only ONE task prompt at a time
- Pass context between tasks via simple variables
- NO anticipation or optimization across tasks
- Each task must complete fully before next

**STARTUP REQUIREMENT**:
Before executing any tasks, MUST display:
```
Research and Report - Task Chain
=================================
Task 0: Retrieve timestamp
Task 1: Validate research topic
Task 2: Create research plan [USER APPROVAL]
Task 3: Conduct research chapter (ITERATIVE) [USER APPROVAL per chapter]
Task 4: Validate sources
Task 5: Finalize report
=================================
```

## Task Chain Definition

```yaml
task_chain:
  - id: "retrieve-timestamp"
    name: "Retrieve timestamp"
    prompt: "../../common/tasks/retrieve-timestamp.md"
    required: true
    
  - id: "validate-research-topic"
    name: "Validate research topic"
    prompt: "../tasks/validate-research-topic.md"
    required: true
    depends_on: ["retrieve-timestamp"]
    
  - id: "create-research-plan"
    name: "Create research plan"
    prompt: "../tasks/create-research-plan.md"
    required: true
    depends_on: ["validate-research-topic"]
    approval_required: true
    approval_type: "plan_approval"
    
  - id: "conduct-research-chapter"
    name: "Conduct research chapter"
    prompt: "../tasks/conduct-research-chapter.md"
    required: true
    depends_on: ["create-research-plan"]
    iterative: true
    iteration_condition: "current_chapter_index < total_chapters"
    approval_required: true
    approval_type: "chapter_approval"
    
  - id: "validate-sources"
    name: "Validate sources"
    prompt: "../tasks/validate-sources.md"
    required: true
    depends_on: ["conduct-research-chapter"]
    
  - id: "finalize-report"
    name: "Finalize report"
    prompt: "../tasks/finalize-report.md"
    required: true
    depends_on: ["validate-sources"]
```

## State Management

### Simple Context Passing
Context is passed between tasks using simple variables:

**Session Initialization**:
- `timestamp`: Session timestamp (YYYYMMDD-HHMMSS)
- `session_id`: Unique session identifier
- `output_dir`: Output directory path
- `skill_path`: Path to skill directory

**User Input Variables**:
- `research_topic`: Specific topic or question to research
- `scope_boundaries`: What is included and excluded (optional)
- `expected_outcomes`: Expected deliverables and audience (optional)
- `timeline`: Research and writing timeline (optional)

**Task 1 Outputs** (validate-research-topic):
- `validated_topic`: Clear, validated topic statement
- `scope_statement`: {included: [list], excluded: [list]}
- `key_questions`: Array of specific research questions
- `information_needs`: {source_types: [list], priority_areas: [list]}
- `clarification_needed`: Boolean - if user input required
- `clarification_questions`: Array of questions for user

**Task 2 Outputs** (create-research-plan):
- `research_plan_file`: Path to saved research plan
- `chapter_structure`: Array of chapter metadata
- `total_chapters`: Integer - number of chapters
- `source_strategy`: Object - source types per chapter
- `plan_approved`: Boolean - set after user approval

**Task 3 Outputs** (conduct-research-chapter - ITERATIVE):
- `current_chapter_index`: Integer - current chapter (0-based)
- `chapter_sources`: Array - sources for current chapter
- `all_sources`: Array - cumulative sources from all chapters
- `report_file`: Path to cumulative report file
- `chapter_approved`: Boolean - set after user approval
- `chapters_complete`: Boolean - true when all done

**Task 4 Outputs** (validate-sources):
- `validated_sources`: Array - sources with validation metadata
- `source_validation_report`: String - validation report text
- `validation_warnings`: Array - list of warnings
- `validation_passed`: Boolean - true if no critical issues

**Task 5 Outputs** (finalize-report):
- `final_report_file`: Path to finalized report
- `completion_summary`: String - summary text
- `report_statistics`: Object - report stats
- `task_complete`: Boolean - true

## Master Execution Protocol

### 1. Initialize Session

**Display Task List** (mandatory startup - shown above)

**Get User Input**:
```
Research and Report
===================

Please provide the following information:

1. Research Topic (required):
   [What specific topic or question should be researched?]

2. Scope Boundaries (optional):
   [What should be included/excluded from research?]

3. Expected Outcomes (optional):
   [What deliverables are expected? Who is the audience?]

4. Timeline (optional):
   [Any deadlines or time constraints?]
```

**Retrieve Timestamp**:
- Execute Task 0: retrieve-timestamp
- Store `timestamp`, `session_id`
- Set `output_dir` from OLAF environment

### 2. Execute Task Chain Loop

For each task in task_chain:

1. **Load Task Prompt**: Read task-specific prompt file
2. **Check Dependencies**: Verify required context variables exist
3. **Execute Task**: Run task with available context
4. **Handle Approval** (if required): Wait for user approval before proceeding
5. **Handle Iteration** (if iterative): Loop until condition false
6. **Pass Context**: Make results available to next task
7. **Continue to Next**: Move to next task in chain

### 3. Task Execution Template

```markdown
**EXECUTING TASK: [task_name]**

**Context Available**:
- Session Timestamp: [timestamp]
- Previous Results: [available variables]

**Task-Specific Instructions**:
[load_and_execute_task_prompt]

**Context Updates**: 
- Store results in simple variables for next tasks
```

### 4. Approval Handling

**For tasks with approval_required = true**:

1. **Propose**: Display deliverable to user
2. **Confirm**: Wait for explicit approval
   - "approve" or "yes": Proceed to next task
   - "revise" or "no": Request specific changes
   - If revisions requested: Re-execute current task with feedback
3. **Act**: Only proceed when approved

**Approval Checkpoints**:
- **Task 2** (create-research-plan): Plan must be approved before research begins
- **Task 3** (conduct-research-chapter): Each chapter must be approved before next

### 5. Iteration Handling

**For Task 3 (conduct-research-chapter)**:

```python
# Initialize iteration
current_chapter_index = 0

# Iteration loop
while current_chapter_index < total_chapters:
    # Execute task with current index
    execute_task("conduct-research-chapter", context)
    
    # Wait for chapter approval
    if chapter_approved:
        current_chapter_index += 1
    else:
        # Re-execute with revision feedback
        continue
    
# Set completion flag
chapters_complete = True
```

### 6. Error Handling

- **Task Failure**: Stop chain, report error with context
- **Missing Dependencies**: Show clear dependency requirements
- **Missing User Input**: Prompt for required information
- **Approval Timeout**: Remind user of pending approval
- **Validation Failures**: Display warnings, allow user to decide continuation

## Input Parameters

**IMPORTANT**: When entries are not provided, ask the USER to provide them.

**Required**:
- `research_topic`: String - Specific topic or question to research

**Optional**:
- `scope_boundaries`: String - What is included and excluded from research
- `expected_outcomes`: String - Expected deliverables and target audience
- `timeline`: String - Research and writing timeline

## Output Format

1. **Research Plan**: `[output_dir]/research-plan-[timestamp].md`
2. **Research Report**: `[output_dir]/research-report-[timestamp].md`
3. **Completion Summary**: Displayed to user with file paths and statistics

## Execution Instructions

When invoked, execute this pattern:

1. **Display Task List** (mandatory startup)
2. **Get User Input** (research topic and optional parameters)
3. **Execute Task 0**: Load and run retrieve-timestamp task
4. **Execute Task 1**: Load and run validate-research-topic task
5. **Execute Task 2**: Load and run create-research-plan task
   - **WAIT FOR USER APPROVAL** before proceeding
6. **Execute Task 3**: Load and run conduct-research-chapter task
   - **ITERATE** for each chapter in chapter_structure
   - **WAIT FOR USER APPROVAL** after each chapter
   - Continue until `current_chapter_index >= total_chapters`
7. **Execute Task 4**: Load and run validate-sources task
8. **Execute Task 5**: Load and run finalize-report task
9. **Display Completion Summary** with file paths and statistics

**NO SHORTCUTS**: Load each task prompt individually and execute completely before next task.

## Research Rules

- Rule 1: Research plan MUST be approved by user before any research begins
- Rule 2: Each chapter MUST be presented for user approval before proceeding to next
- Rule 3: All file paths and naming conventions must follow specified timestamp format
- Rule 4: Use Propose-Confirm-Act protocol for all major deliverable approvals
- Rule 5: **Web search current information** whenever researching tools, market conditions, or rapidly changing topics
- Rule 6: **MANDATORY URL COLLECTION** - Every source MUST have full URL, reject generic references
- Rule 7: **Source validation** - All sources must be accessible and current (prefer 2024-2025 content)

## Success Criteria

- Research plan approved by user
- All chapters researched and approved
- All sources include specific, accessible URLs
- Information is current and validated against web sources
- Final report compiled with TOC and appendices
- User confirms deliverable meets expectations

## OLAF Framework Context

**Current Local Time**: Use timestamp from Task 0

**Available OLAF Directories**:
- **Output Dir**: Use from OLAF environment (default: .olaf/work/staging)
- **Project Root**: Current working directory

**Available Tools**:
- **http_request**: For web research and URL validation
- **file_read**: Read templates and existing files
- **file_write**: Create and update report files
- **editor**: Advanced file editing if needed

## OLAF Conventions
- Use US English
- Follow `verb-entity-complement.md` naming pattern
- Use `YYYYMMDD-HHMMSS` timestamp format
- Save results to output directory
