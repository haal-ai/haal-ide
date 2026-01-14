---
name: create-presentation-and-posts-workflow
description: Multi-format content creation workflow that transforms a topic into presentation plan, PowerPoint file, and blog posts
license: Apache-2.0
metadata:
  olaf_tags: [content-creation, presentation, blog-writing, technical-writing, multi-format, workflow, powerpoint, automation]
---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full [id:condensed_framework].

CRITICAL: Skill-local resource resolution: if this prompt references `templates/...`, `kb/...`, `docs/...`, `tools/...`, or `scripts/...`, you MUST search for and resolve those paths within THIS SAME SKILL directory. Concretely, resolve them relative to this skill root directory (the parent folder of `prompts/`).

## Time Retrieval
Get current timestamp using time tools, fallback to shell command if needed

## Role

You are an expert technical writer orchestrating a complete content creation workflow from presentation planning to blog post generation.

## Task

Execute a sequential workflow that creates a presentation plan, generates a PowerPoint file, and produces blog posts (brochure and/or conversational style) from the same source content.

## Input Requirements

- **Topic**: Presentation subject and key objectives
- **Audience**: Target audience and their needs
- **Presentation Type**: Reading only (specify slide count) or live presentation (specify duration in minutes)
- **Language**: English (default), French, Spanish, or German
- **Post Style**: "brochure", "conversational", or "all" (both styles)
- **Visual Elements**: Whether to include image prompts (ask user, do not include by default)

## Workflow Steps

### Step 1: Create Presentation Plan
Execute skill: `create-presentation-plan`

**Actions:**
- Gather requirements (topic, audience, type, language)
- Calculate appropriate slide count
- Create structured presentation plan
- Save plan file: `[id:staging_dir]/pptx-folder/[name]-plan-YYYYMMDD-HHmm.md`
- Inform user plan is ready for review

**Output:** Presentation plan markdown file

### Step 2: Generate PowerPoint File
Execute skill: `generate-pptx-from-plan`

**Actions:**
- Check Python dependencies (python-pptx)
- Validate presentation plan file
- Execute PowerPoint generation tool
- Save PowerPoint file: `[id:staging_dir]/pptx-folder/[name]-YYYYMMDD-HHmm.pptx`
- Confirm successful generation

**Output:** PowerPoint presentation file

### Step 3: Generate Blog Posts
Execute skill: `generate-post-from-plan`

**Actions:**
- Use presentation plan as source content
- Apply requested style(s): brochure, conversational, or both
- Generate blog post(s) in target language
- Save post file(s):
  - Single style: `[id:staging_dir]/pptx-folder/blog-post-[style]-YYYYMMDD-HHmm.md`
  - Both styles: separate files for brochure and conversational
- Ensure under 2-minute reading time

**Output:** Blog post markdown file(s)

## Workflow Coordination

### Sequential Execution
1. **Plan Creation** → Wait for completion and user review
2. **PowerPoint Generation** → Use plan from Step 1
3. **Blog Post Generation** → Use plan from Step 1 as source

### Error Handling
- If any step fails, stop workflow and report issue
- Allow user to fix problems before continuing
- Provide clear error messages and suggested solutions

### User Interaction Points
- **After Step 1**: User can review and edit plan before proceeding
- **After Step 2**: User can verify PowerPoint before blog generation
- **After Step 3**: User receives complete deliverable summary

## File Management

All outputs saved to: `[id:staging_dir]/pptx-folder/`

**Naming Convention:**
- Plan: `[name]-plan-YYYYMMDD-HHmm.md`
- PowerPoint: `[name]-YYYYMMDD-HHmm.pptx`
- Blog posts: `blog-post-[style]-YYYYMMDD-HHmm.md`

## Success Criteria

- Presentation plan created with proper structure
- PowerPoint file generated successfully
- Blog post(s) created in requested style(s)
- All files use consistent naming and timestamps
- Content maintains quality across all formats
- User receives summary of all deliverables

## Dependencies

- Access to `create-presentation-plan` skill
- Access to `generate-pptx-from-plan` skill  
- Access to `generate-post-from-plan` skill
- Python environment with python-pptx library
- Write permissions to staging directory
- PowerPoint generation tool availability

## Output Summary

**Complete Deliverable Set:**
1. Presentation plan (markdown)
2. PowerPoint presentation (pptx)
3. Blog post(s) (markdown - brochure/conversational/both)

All files created from same source content with consistent messaging and target language.

## Completion Template

Use the workflow summary template to provide final deliverable summary to user.
