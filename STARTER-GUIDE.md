# HAAL Getting Started Guide

**Target Audience:** New HAAL users and developers

## Overview

HAAL (Human-Agent-Assisted-Learning) is a skill-driven AI agent framework that enables structured, protocol-based interactions with Large Language Model (LLM). This guide demonstrates HAAL's core capabilities through practical examples and real conversation records.

---

## What You'll Learn

This getting started guide walks you through HAAL's key features:

1. **Skill Discovery** - How to find  and useavailable AI capabilities
2. **Conversation Documentation** - How to capture and analyze AI interactions  
3. **Prompt Engineering** - How to create standardized AI prompts

Each section includes:
- ✅ **Live Examples** - Real conversation records showing actual usage
- 🔗 **Linked Resources** - Direct links to prompts, templates, and outputs
- 📋 **Step-by-Step Instructions** - How to replicate the examples
- 🎯 **Best Practices** - Tips for effective usage

---
### How HAAL Structures Skills

For a comprehensive understanding of how HAAL components work together from prompts to enterprise registries, see our dedicated [HAAL End-to-End Structure](.olaf/docs/starter-guide-examples/olaf-end-to-end-structure.md) guide.

In brief: HAAL organizes capabilities as **skills** → **competencies** → **collections** → **registries**, with each layer supporting reuse and enterprise governance.

---

## How to Use HAAL Skills

There are multiple ways to activate HAAL capabilities and use the skills. Choose the method that works best for you:

### 1. Framework Activation
Start any session with `haal` to load the framework:
- **Basic activation**: Type `haal` to load the framework and get context-aware help
- **Direct skill activation**: Type `haal <trigger phrase>` to immediately start a specific skill
- **Pre-defined triggers**: Each skill has standardized trigger phrases (e.g., "list skills", "help me")

### 2. Slash Commands (Repository Integration)
When HAAL is installed in your repository, slash commands are automatically available for quick access:
- Type `/` followed by a few letters to see available HAAL skills
- Example: Type `/list` to see `/haal-list-skills` and other options
- Select the command that matches your needs from the autocomplete list

### 3. Skill Launcher (Universal Skill Access)
Use the special skill launcher to find and run any available skill:
- **Command**: `/haal-user-skill <skill name>` or `/haal-user-skill <trigger word>`
- **What it does**: Searches for the specified skill and runs it automatically if found
- **Benefits**: Single command to access any skill without remembering exact trigger phrases

### 4. Context Help
Get personalized assistance based on your current situation:
- **Command**: `haal help me` or `/haal-help-me`
- **What it does**: Analyzes your current context and suggests relevant actions
- **Examples**: Code review, research, documentation, project management

### 5. Direct File Access (IDE Integration)
Browse and execute skill files directly from your IDE:
- **Search**: Use your IDE's file search (e.g., Ctrl+P in VS Code) and type part of a skill name
- **Select**: Click on the skill file to view its prompt and documentation
- **Execute**: Copy the prompt content and paste it into your AI agent to run the skill

## Quick Start: Try These Commands

Once HAAL is installed in your repository, try these basic commands to get started:

- **Discover skills**: Type `/` followed by a few letters to see `/haal-list-skills` in the autocomplete list. Select it to view all available skills in your repository.

- **Load framework**: Type `haal` to load the HAAL framework into your context and get immediate access to all capabilities.

- **Get help**: Type `haal help me` to receive personalized suggestions based on your current context. HAAL will analyze your situation and recommend the most relevant skills.

- **Challenge yourself**: Type `haal challenge me` to engage in a structured thinking exercise. HAAL will ask about your topics of interest (implementation ideas, documentation goals, etc.) and guide you through 3-4 cycles of challenging questions designed to deepen your thinking. The entire process and outcomes are automatically saved for future reference.

---

## Advanced Features: Documenting AI Conversations

### The "Store Conversation" Competency

One of HAAL's most powerful features is automatic conversation documentation using the **"store conversation"** competency.

**What the competency captures:**
- **Timeline**: Exact timestamps of each interaction
- **Actions Taken**: Every file read, search performed, and output created
- **Files Created/Modified**: Complete audit trail of all changes
- **User Interactions**: Full conversation flow with context

**How to use it:**
1. At the end of any AI session, simply say: **" haal store conversation" or /haal-store-conversation**
2. HAAL automatically:
   - Finds the store-conversation competency
   - Retrieves current timestamp
   - Creates a detailed narrative record
   - Saves it to the conversations directory

**Generated Output Location:**
```
data/product/documentations/conversations/
└── conversation-record-YYYYMMDD-HHmm.md
```

**Why this matters:**
- **Accountability**: Full audit trail of AI assistance
- **Knowledge Transfer**: Share exactly what was accomplished
- **Session Continuity**: Resume work across multiple sessions
- **Learning**: Understand how competencies work in practice

---

## Section 3: Structured Knowledge Research

### The "Search and Learn" Competency

The **"search and learn"** competency demonstrates HAAL's ability to conduct focused research using web search capabilities.

**How it works:**
1. **Competency Detection**: HAAL finds the competency in its library using trigger phrases like "search and learn"
2. **Parameter Collection**: Requests essential information if not provided:
   - Research topic/question
   - Scope and focus areas
   - Target audience level
3. **Web Research**: Uses the agent's web search tools to gather current information
4. **Report Generation**: Creates a structured report with staging and sources

**Key Features:**
- **Current Information**: Always searches for up-to-date web sources
- **Source Documentation**: Provides full URLs and citations
- **Structured Output**: Organized staging with clear sections
- **Scope Management**: Focuses research based on user requirements

**Example Usage:**
```
User: "search and learn about microservices architecture patterns"

HAAL Response:
1. Identifies the search-and-learn competency
2. Requests any missing parameters (scope, audience)
3. Conducts web searches for current information
4. Creates structured report with staging
5. Saves report to staging directory
```

**Output Location:**
```
work/staging/research/
└── research-report-YYYYMMDD-HHmm.md
```

---

## Section 4: Advanced Research with User Review

### The "Research and Report" Competency

For complex research requiring user oversight, HAAL provides the **"research and report"** competency with the **Propose-Confirm-Act** protocol.


**Protocol Flow:**
1. **Propose**: Creates detailed research plan with scope, questions, and chapter structure
2. **Confirm**: Waits for user approval before proceeding
3. **Act**: Executes research systematically, updating progress

**Key Benefits:**
- **User Control**: Review and modify research scope before execution
- **Structured Approach**: Organized chapter-by-chapter execution
- **Progress Tracking**: Clear milestones and deliverables
- **Session Continuity**: Can pause and resume across multiple sessions

**Generated Outputs:**
```
work/staging/research/
├── research-plan-YYYYMMDD-HHmm.md      # Approved research plan
└── research-report-YYYYMMDD-HHmm.md    # Final comprehensive report
```

**When to use this competency:**
- Complex research requiring multiple sources
- Technical analysis for decision-making
- Competitive analysis and market research
- Any research where you want to review the approach first

---

## Section 5: Creating Custom AI Prompts

### The "Create Prompt" Competency

HAAL enables you to create standardized AI prompts that follow framework principles and templates.

**How it works:**
1. **Template-Based**: Uses standardized templates
2. **Role Organization**: tries  to  categorize prompts by role (developer, researcher, etc.)
3. **Consistency**: Ensures all prompts follow HAAL core principles
4. **Deduplication**: Checks for existing similar prompts to avoid duplicates

**Prompt Structure Analysis:**

All HAAL prompts follow this standardized structure:

```markdown
---
name: prompt-name
description: Brief description of what the prompt does
tags: [relevant, tags, for, categorization]
---

## Framework Validation
[Standard HAAL framework requirements]

## Time Retrieval  
[Timestamp handling instructions]

## Input Parameters
[Required and optional parameters]

## User Interaction Protocol
[Act/Propose-Act/Propose-Confirm-Act specification]

## Process
[Step-by-step execution instructions]

## Output Format
[Expected deliverables and file locations]

## Success Criteria
[Checklist for completion validation]
```

**Example: Finding Created Prompts**

After using the "create prompt" competency, you can find your new prompt in:
```
.olaf/core/skills/<your-new-skill>/
```

Your prompt becomes a standalone skill that can be attached to a competency or used independently. By default, new prompts are organized into a competency called "my-prompts" for easy management.


---

## Section 6: Understanding HAAL Protocols

### Interaction Protocols Explained

HAAL uses three distinct interaction protocols to balance safety and efficiency:

#### **Act Protocol** (Direct Execution)
- **When used**: Safe, read-only operations
- **Behavior**: Executes immediately without asking
- **Examples**: Reading files, listing directories, searching code
- **User experience**: Fast, efficient, minimal interruption

#### **Propose-Act Protocol** (Analysis Before Action)  
- **When used**: Actions requiring user agreement
- **Behavior**: Presents plan, waits for approval, then executes
- **Examples**: Code modifications, file creation, research execution
- **User experience**: One confirmation step, maintains control

#### **Propose-Confirm-Act Protocol** (Multi-Step Validation)
- **When used**: Complex, multi-step operations with significant impact
- **Behavior**: 
  1. **Propose**: Present detailed plan
  2. **Review**: Wait for user feedback
  3. **Confirm**: Ask for final sign-off  
  4. **Act**: Execute only after confirmation
- **Examples**: Large research projects, system modifications, complex analysis
- **User experience**: Maximum control, suitable for complex tasks

**Protocol Selection:**
Each competency specifies its protocol in the competency index. This ensures consistent behavior and appropriate safety levels.

---

## Section 7: File Organization and Memory Map

### Understanding HAAL's Structure

HAAL uses a modernized file organization system focused on competencies and collections:

#### **Core Framework** (`core/`)
- **Skills**: `core/skills/<skill-name>/` - Individual skill definitions with prompts and documentation
- **Competencies**: `core/competencies/<role>/` - Competency definitions that reference one or more skills
- **Collections**: `core/reference/competency-collections.json` - Single file defining collections that group competencies in desired order
- **Reference**: `core/reference/` - Core principles and guides

#### **Committed Work Environment** (`data/`)
These are folders and files that store persistent project data:
- **Projects**: `data/projects/` - Jobs register, changelogs, project tracking
- **Product**: `data/product/` - Decision records, documentation, functional and technical specifications
- **Context**: `data/context/` - Environment-specific context files for different platforms
- **Practices**: `data/practices/` - Development guidelines, standards, and best practices
- **Peoples**: `data/peoples/` - Team member information

#### **Uncommitted and Temporary Work** (`work/`)
These are folders for temporary and work-in-progress files:
- **Staging**: `work/staging/` - Research outputs, analysis results, and pre-commit work
- **Carry-over**: `work/carry-over/` - Files that need to be carried forward between sessions
- **Stash**: `work/stash/` - Temporary storage for work that may be resumed later


#### **Modern Organization Pattern**
The new structure separates concerns clearly:
- **Skills** are atomic units containing prompts and logic
- **Competencies** orchestrate multiple skills to achieve specific goals
- **Collections** define groupings and ordering of competencies for different contexts

This system ensures:
- **Consistency**: Same references across all prompts and documentation
- **Maintainability**: Easy to update paths in one location
- **Clarity**: Clear understanding of file locations

---

## Next Steps

### Getting Started Checklist

- [ ] **Try `/list-skills`** - Discover available AI capabilities
- [ ] **Use "store conversation"** - Document your first AI session  
- [ ] **Experiment with "search and learn"** - Conduct focused research
- [ ] **Try "research and report"** - Experience the Propose-Confirm-Act protocol
- [ ] **Create a custom prompt** - Build your own AI competency
- [ ] **Explore the file structure** - Understand HAAL's organization

### Advanced Usage

Once comfortable with basics:
- **Create Jobs**: Use project management competencies for task tracking
- **Code Analysis**: Leverage developer competencies for code review and improvement
- **Documentation**: Use technical writer competencies for comprehensive documentation
- **Team Collaboration**: Share conversation records and research reports

### Getting Help

- **Competency Index**: Check `core/reference/query-competency-index.md` for all available capabilities
- **Core Principles**: Review `core/reference/core-principles.md` for framework guidelines
- **Examples**: Explore `.olaf/docs/starter-guide-examples/` for real usage examples

---

## Summary

HAAL transforms AI interactions from ad-hoc conversations into structured, documented, and repeatable processes. By using competencies, protocols, and standardized templates, you can:

- **Discover** AI capabilities systematically
- **Document** all AI interactions automatically  
- **Research** complex topics with proper oversight
- **Create** standardized AI prompts and workflows
- **Collaborate** effectively using shared conversation records

The framework ensures consistency, safety, and knowledge preservation across all AI-assisted work.

**Ready to start?** Try `/list-skills` in your next AI conversation!

---

*This documentation was generated using HAAL competencies and demonstrates the framework's capabilities through real examples and conversation records.*
