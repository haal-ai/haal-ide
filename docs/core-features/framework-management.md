# Framework Management

## Overview

OLAF uses structured framework management to enable AI agents to load, validate, and apply core principles and protocols consistently. The framework combines XML section tagging with a condensed format for efficient loading and execution.

---

## The Condensed Framework

### What Is It?

The condensed framework (`olaf-framework-condensed.md`) is a self-contained, minimal file that includes all essential OLAF components in one place.

**Location:** `.olaf/core/reference/.condensed/olaf-framework-condensed.md`

### Purpose

- **Fast Loading**: Single file load gives agents complete framework context
- **Self-Sufficient**: Contains all necessary components (memory map, protocols, principles)
- **Portable**: Can be loaded in any environment
- **Versioned**: Exactly 119 lines (as of current version) for validation

### What's Included

The condensed framework embeds:

1. **Session Initialization** - Critical first-step instructions
2. **Protocol Hierarchy** - Competency search and execution flow
3. **Interaction Protocols** - Act, Propose-Act, Propose-Confirm-Act
4. **Memory Map** - Compact ID pointer mappings (embedded inline)
5. **Core Principles** - Mandatory behavioral rules
6. **Role and Behavior** - Expert domain guidance
7. **Framework Validation** - Self-check mechanism
8. **Work Instructions** - Execution directives

### Loading Strategy

**When to Load:**
- Start of any OLAF session (via `olaf` command)
- Agent initialization (`.github/copilot-instructions.md`, `.windsurf/team.md`)
- Before executing any competency

**How It's Loaded:**
```markdown
1. Agent reads .olaf/core/reference/.condensed/olaf-framework-condensed.md
2. Validates line count (119 lines expected)
3. If incomplete, reloads with endLine=-1
4. Framework components become active in agent context
```

---

## XML Section Tagging

### Purpose

XML tags provide structured anchors for LLMs to reference specific framework sections, enabling precise context loading and validation.

### Tag Structure

```xml
<olaf-session-initialization>
## Session Initialization
[Content for initializing OLAF sessions]
</olaf-session-initialization>

<olaf-protocol-hierarchy>
## Protocol Hierarchy & Execution
[Content defining how competencies are discovered and executed]
</olaf-protocol-hierarchy>

<olaf-interaction-protocols>
## Interaction Protocols
[Act, Propose-Act, Propose-Confirm-Act definitions]
</olaf-interaction-protocols>

<core-principles>
[Mandatory behavioral rules and formatting conventions]
</core-principles>

<olaf-general-role-and-behavior>
## Role and Behavior
[Expert domain approach and communication guidelines]
</olaf-general-role-and-behavior>

<olaf-framework-validation>
## Framework Validation
[Self-check mechanism for complete loading]
</olaf-framework-validation>

<olaf-work-instructions>
[Execution directives for tasks]
</olaf-work-instructions>
```

### Benefits of XML Tags

**For AI Models:**
- **Precise Referencing**: Can target specific sections by tag name
- **Partial Loading**: Load only needed sections when appropriate
- **Validation**: Verify section presence and completeness

**For Framework Maintenance:**
- **Clear Structure**: Tags define logical boundaries
- **Searchability**: Easy to find and update specific sections
- **Consistency**: Standardized across all framework components

---

## Framework Validation

### Self-Validation Mechanism

The condensed framework includes built-in validation:

```markdown
<olaf-framework-validation>
## Framework Validation

**CRITICAL LOADING CHECK**: This framework is EXACTLY 119 lines. 
If you see less than 119 lines, YOU MUST reload using read_file 
with endLine=-1 to get the complete framework.
</olaf-framework-validation>
```

### Why Validation Matters

**Problem:** AI agents sometimes truncate file reads, missing critical framework components.

**Solution:** 
1. Framework declares expected line count
2. Agent checks actual lines loaded
3. If mismatch, agent re-reads complete file
4. Ensures no missing protocols or principles

### What Gets Validated

- ✅ Complete framework loaded (119 lines)
- ✅ All XML sections present
- ✅ Memory map embedded correctly
- ✅ Core principles included
- ✅ Interaction protocols defined

---

## Framework Components in Detail

### 1. Protocol Hierarchy

Defines how OLAF processes user requests:

1. **Competency Search**: Match user intent to competency triggers
2. **Direct Execution**: Single match → execute with appropriate protocol
3. **Match Resolution**: Multiple matches → present options to user
4. **Request Triage**: No match → search all competencies
5. **Request Clarification**: Still no match → explain understanding
6. **User Consent Gate**: All propose protocols require explicit agreement

### 2. Interaction Protocols

Three safety levels for different action types:

**Act Protocol** (Default):
- Direct execution
- No user confirmation needed
- For safe, read-only operations

**Propose-Act Protocol**:
- Present plan first
- Wait for user agreement
- Execute after approval

**Propose-Confirm-Act Protocol**:
- Multi-step confirmation process
- Detailed plan review
- Final sign-off before execution
- For modifications and critical changes

### 3. Memory Map (Embedded)

Compact inline version of full memory map:

```markdown
core_olaf_dir=.olaf/
ack_dir=[core_olaf_dir]core/
skills_dir=[ack_dir]skills/
competency_index=[reference_dir]query-competency-index.md
jobs_register=[projects_dir]jobs-register.md
```

Provides essential ID pointers without loading separate file.

### 4. Core Principles

Non-negotiable behavioral rules:

- **Job Creation**: Only on explicit user instruction
- **Naming Conventions**: kebab-case, verb-entity-complement pattern
- **Timestamp Format**: YYYYMMDD-HHmm in CEDT timezone
- **Tool Selection Hierarchy**: OLAF → Native → MCP → Custom
- **No Unsolicited Files**: Don't create summaries without request

### 5. Role and Behavior

Expert domain guidance:

- Act as domain expert
- Reason carefully before responding
- State "I don't know" when uncertain
- Provide sources for factual claims
- Be concise and focused
- No explanation unless using propose protocols

---

## Usage in Practice

### For AI Agents

**Initialization:**
```markdown
1. Load: Read .olaf/core/reference/.condensed/olaf-framework-condensed.md
2. Validate: Check 119 lines loaded
3. Parse: Extract XML sections
4. Apply: Use protocols, principles, memory map in all operations
```

**During Execution:**
```markdown
1. Check <olaf-protocol-hierarchy> for request handling
2. Apply <olaf-interaction-protocols> for safety level
3. Use <core-principles> for formatting and tool selection
4. Follow <olaf-general-role-and-behavior> for communication
```

### For Users

**Starting OLAF:**
- Type `olaf` to trigger framework loading
- Agent becomes OLAF-aware with all protocols active

**Observing Framework:**
- Agent follows concise communication (core-principles)
- Uses appropriate protocol (Act/Propose-Act/Propose-Confirm-Act)
- References correct file locations (memory map)

---

## Framework vs. Individual Components

### When to Load Full Components

Some operations need detailed documentation beyond condensed framework:

**Full Memory Map** (`.olaf/core/reference/memory-map.md`):
- Complete ID definitions with descriptions
- Hierarchical structure with examples
- Use when creating new skills that need all path references

**Full Core Principles** (`.olaf/core/reference/core-principles.md`):
- Detailed explanations of each principle
- Examples and rationale
- Use when onboarding or training

**Competency Index** (`.olaf/core/reference/query-competency-index.md`):
- Complete catalog of all competencies
- Trigger phrases and descriptions
- Use for competency discovery

### Condensed Framework Advantages

- **Speed**: One file load vs. multiple
- **Completeness**: Self-contained, no missing references
- **Consistency**: Same framework version for all agents
- **Validation**: Built-in self-check mechanism

---

## Framework Evolution

### Versioning

The condensed framework is versioned and tracked:

```markdown
<metadata>
version: 1.7.0
last_updated: 2025-11-17
purpose: LLM navigation aid - consolidated OLAF framework
</metadata>
```

### When Framework Updates

1. Line count may change (update validation)
2. XML sections may be added/modified
3. Memory map paths may be updated
4. Core principles may be refined

**Critical:** All agents must reload framework after updates.

---

## Summary

OLAF framework management combines:

✅ **Condensed Format** - Single file with all essentials (119 lines)  
✅ **XML Section Tags** - Structured, referenceable components  
✅ **Self-Validation** - Built-in completeness checking  
✅ **Embedded Components** - Memory map, protocols, principles in one place  
✅ **Efficient Loading** - Fast initialization for AI agents  
✅ **Consistent Execution** - Same framework across all sessions  

This architecture ensures every OLAF session starts with complete, validated context, enabling reliable and consistent AI assistance.
- Consistent time retrieval wording

No user action is required for migration - all updates are backward compatible.

## See Also

- [Interaction Protocols](interaction-protocols-explained.md)
- [Core Principles](core-principles-explained.md)
- [Memory Map](memory-map-explained.md)
- [Competency-Driven Workflow](competency-driven-workflow.md)
