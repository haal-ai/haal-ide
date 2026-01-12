# OLAF Project Organization

## Overview

OLAF follows a modular, skill-based organization pattern where capabilities are structured as atomic skills that can be combined into competencies and organized into collections. This document explains how OLAF organizes its files, skills, and data.

---

## Directory Structure

### Root Structure (`.olaf/`)

```
.olaf/
├── core/           # Framework core components
├── data/           # Structured data and practices
├── docs/           # Documentation
├── work/           # Temporary and staging files
├── bundles/        # Distribution bundles
├── installs/       # Installation packages
├── your-data/      # User-specific data
└── your-repos/     # User repository integrations
```

---

## Core Framework (`core/`)

The core directory contains all framework components:

```
core/
├── skills/         # Individual skill definitions (90+ skills)
├── competencies/   # Skill orchestration and workflows
├── reference/      # Framework documentation and indexes
├── schemas/        # Data structure definitions
└── scripts/        # Build tools and utilities
```

### Skills (`core/skills/`)

Skills are atomic, reusable units containing:
- **Prompts** (`prompts/`) - The AI instruction set (one or more prompt files)
- **Templates** (`templates/`) - Structured templates for consistent output (optional)
- **Documentation** (`docs/`) - Usage guides and examples (optional)
- **Tools** (`tools/`) - Helper scripts and utilities (optional)
- **Knowledge base** (`kb/`) - Supporting materials (optional)
- **Metadata** (`skill-manifest.json`) - Skill configuration

**Example Skill Structure:**
```
core/skills/review-code/
├── prompts/
│   └── review-code.md                    # Main prompt
├── templates/
│   ├── code-review-action-plan-template.md
│   └── developer/
├── docs/
│   └── tutorial.md
├── skill-manifest.json                   # Metadata
└── kb/
    └── code-review-checklist.md
```

**Design Philosophy: Separation of Concerns**

OLAF decouples templates, tools, and knowledge from prompt logic for cleaner design:

- **Templates**: Structured output formats (markdown, JSON, reports) that ensure consistency across skill executions
- **Tools**: Scripts (PowerShell, bash, etc.) that can be generated on the fly for rapid prototyping, then serve as pseudocode for MCP servers
- **Questionnaires**: Optional guided question sets referenced by prompts to gather user input
- **Knowledge Base**: Supporting materials, checklists, and reference documentation

**Benefits:**
- ✅ **Reusability**: Templates/tools shared across similar skills
- ✅ **Maintainability**: Update templates independently of prompt logic
- ✅ **Consistency**: Standardized output formats
- ✅ **Flexibility**: Scripts offer more customization than rigid MCP tools
- ✅ **Rapid Iteration**: Test prompts quickly with generated scripts

**Available Skills** (90+ total):
- **Code Quality**: `review-code`, `improve-cyclomatic-complexity`, `fix-code-smells`
- **Documentation**: `generate-tech-spec-from-code`, `bootstrap-functional-spec-from-code`
- **Testing**: `augment-code-unit-test`, `detect-test-directives`
- **Project Management**: `create-job`, `review-progress`, `create-changelog-entry`
- **Research**: `olaf-help-me`, `should-i-use-ai`
- **Framework**: `create-skill`, `create-prompt`, `import-prompt-unchanged`

### Competencies (`core/competencies/`)

Competencies orchestrate multiple skills to accomplish complex goals. They define:
- **Skill sequence** - Order of execution
- **Data flow** - How outputs become inputs
- **Protocols** - Act/Propose-Act/Propose-Confirm-Act
- **Collections** - Groupings for different contexts

### Reference (`core/reference/`)

Framework documentation and indexes:
- `core-principles.md` - Behavioral guidelines
- `query-competency-index.md` - Complete competency catalog
- Framework condensed versions for quick loading

---

## Data Organization (`data/`)

Structured data following enterprise patterns:

```
data/
├── context/        # Environment-specific configurations
├── peoples/        # Team member records
├── practices/      # Best practices and standards
├── product/        # Product-specific documentation
└── projects/       # Project tracking (jobs, changelogs)
```

### Context (`data/context/`)
Environment-specific settings:
- `context-current.md` - Active context
- `context-windows-powershell.md` - Windows environment
- `context-linux-bash.md` - Linux environment
- `context-macos-zsh.md` - macOS environment

### Practices (`data/practices/`)
Reusable best practices and standards:
- `git-guidelines.md` - Git workflow standards
- `code-review-guidelines.md` - Code review practices
- `standards/` - Coding and testing standards

### Projects (`data/projects/`)
Project tracking and management:
- `jobs-register.md` - Active tasks and jobs
- `changelog-register.md` - Change tracking
- `changelog-register-archive.md` - Historical changes

### Product (`data/product/`)
Product-specific documentation:
- `functional/` - Functional specifications
- `technical/` - Technical documentation
- `decision-records/` - Architecture decision records

---

## Work Directories (`work/`)

Temporary and work-in-progress storage:

```
work/
├── staging/        # Pre-commit work and research outputs
├── carry-over/     # Files to carry between sessions
└── stash/          # Temporary storage for paused work
```

### Staging (`work/staging/`)
Generated outputs before final placement:
- `research/` - Research reports and analysis
- `specs/` - Generated specifications
- `code-review/` - Code review outputs

### Carry-over (`work/carry-over/`)
Session continuity files:
- Conversation context
- Ongoing analysis
- Multi-session work

### Stash (`work/stash/`)
Paused or temporary work:
- Experimental changes
- Alternative approaches
- Work to be resumed later

---

## Documentation (`docs/`)

Framework documentation organized by purpose:

```
docs/
├── README.md                    # Documentation hub
├── core-features/               # Framework capabilities
├── specific-features/           # Specialized functionality
├── starter-guide-examples/      # Tutorials and examples
├── release-notes/               # Version history
└── integration.md               # Agent integration guides
```

---

## Modern Organization Principles

### 1. Skill-Based Architecture
- **Atomic Units**: Each skill is self-contained
- **Composable**: Skills combine into competencies
- **Reusable**: Same skill used in multiple contexts

### 2. Clear Separation of Concerns
- **Core**: Framework components (immutable)
- **Data**: Structured information (version-controlled)
- **Work**: Temporary files (not committed)

### 3. Enterprise-Ready Structure
- **Collections**: Group competencies by context
- **Practices**: Inject best practices at runtime
- **Context**: Environment-specific configurations

### 4. Discovery and Navigation
- **Skill names**: Clear, action-oriented (`review-code`, `create-job`)
- **Indexes**: Queryable catalogs (`query-competency-index.md`)
- **Documentation**: Each component includes usage guides

---

## File Naming Conventions

### Skills
- Lowercase with hyphens: `review-code`, `create-prompt`
- Action-oriented verbs: `generate-`, `create-`, `review-`

### Data Files
- Kebab-case: `changelog-register.md`, `jobs-register.md`
- Descriptive suffixes: `-register`, `-archive`, `-template`

### Documentation
- Lowercase with hyphens: `getting-started.md`, `core-principles.md`
- README.md for directory overviews

---

## Path References

All OLAF components use consistent path patterns:

### Absolute Paths from Repository Root
```
.olaf/core/skills/<skill-name>/
.olaf/data/projects/jobs-register.md
.olaf/work/staging/research/
```

### Relative Paths within Skills
```
../reference/core-principles.md
../../data/practices/git-guidelines.md
```

---

## Summary

OLAF's organization follows a clear hierarchy:
1. **Skills** - Atomic reusable prompts
2. **Competencies** - Orchestrated workflows
3. **Collections** - Context-specific groupings
4. **Data** - Structured information and practices
5. **Work** - Temporary and staging areas

This structure ensures:
- **Discoverability**: Easy to find capabilities
- **Maintainability**: Clear file locations and purposes
- **Scalability**: Add new skills without restructuring
- **Collaboration**: Shared understanding of organization

### Benefits of This Organization

1. **Discoverability**: Users can quickly find prompts relevant to their role or specific technical need
2. **Maintainability**: Related prompts and templates are co-located for easier updates
3. **Consistency**: Templates within categories follow similar patterns and structures
4. **Scalability**: New prompts can be easily categorized using established patterns
5. **Tool Integration**: Scripts and templates are organized alongside their related prompts
6. **Collaboration**: Clear organization aids team members in understanding and contributing to the repository