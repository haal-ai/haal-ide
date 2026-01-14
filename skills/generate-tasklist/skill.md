---
name: generate-tasklist
description: Generate structured tasklists with iteration-task-subtask hierarchy and status tracking
license: Apache-2.0
metadata:
  olaf_tags: [tasklist, planning, project, iteration, tasks]
---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full [id:condensed_framework].

CRITICAL: Skill-local resource resolution: if this prompt references `templates/...`, `kb/...`, `docs/...`, `tools/...`, or `scripts/...`, you MUST search for and resolve those paths within THIS SAME SKILL directory. Concretely, resolve them relative to this skill root directory (the parent folder of `prompts/`).

## Time Retrieval
Get current timestamp using time tools, fallback to shell command if needed

## Input Parameters

**IMPORTANT**: When you don't have entries provided, ask the USER to provide them.
- **project_purpose**: string - Brief description of the overall goal or project
- **iteration_type**: single|multiple - Whether project has single or multiple iterations
- **iterations_list**: array - List of iteration names/descriptions (if multiple)
- **major_tasks**: array - High-level tasks for each iteration

## Process
1. **Gather Requirements**:
   - Ask: "What is the purpose of this tasklist?"
   - Ask: "Single or multiple iterations?"
   - If multiple: "Please list iteration names/descriptions"
   - Ask: "What are the major tasks for each iteration?"
2. **Generate Tasklist Structure**:
   - Use template: `templates/project-manager/tasklist-template.md.md`
   - Apply status prefixes: todo, wip, done, dump
   - Follow iteration-task-subtask hierarchy
   - Enforce constraints: max 7 tasks per iteration, max 7 subtasks per task
3. **Present for Review**:
   - Display proposed tasklist structure
   - Request user amendments
   - Apply modifications as requested

## Output Format

Follow template structure: `templates/project-manager/tasklist-template.md.md`

## Output to USER
- Present proposed tasklist for review
- Request amendments and modifications
- Confirm final structure
