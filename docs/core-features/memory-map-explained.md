# Memory Map

## Overview

The Memory Map is OLAF's navigation system for AI agents. It provides a hierarchical structure of important files and directories using **ID pointers** that enable consistent, maintainable references across all prompts and skills.

**Location:** `reference/memory-map.md`

---

## The ID Pointer System

### What Are ID Pointers?

ID pointers are symbolic references that map to actual file paths. Instead of hardcoding paths, prompts use IDs that resolve to the correct location.

**Format:** `[id:identifier_name]`

**Example:**
```markdown
.olaf/ = `.olaf/`
skills/ = `.olaf/core/skills/`
```

### How Prompts Use Pointers

**Instead of hardcoded paths:**
```markdown
❌ Read the file at skills/review-code/skill.prompt.md
```

**Use ID pointers:**
```markdown
✅ Read the file at skills/review-code/skill.prompt.md
```

---

## Benefits of ID Pointers for Prompts

### 1. **Maintainability**
**Problem:** When directory structure changes, hundreds of prompts need updates.

**Solution:** Update once in memory-map, all prompts automatically use new path.

**Example:**
```markdown
# Memory-map change
skills/ = `.olaf/framework/skills/`  # Structure reorganized

# No prompt changes needed!
# All references to skills/ automatically work
```

### 2. **Readability and Intent**
**Problem:** Hardcoded paths obscure intent.

**Solution:** IDs communicate purpose, not just location.

**Example:**
```markdown
❌ Read .olaf/data/projects/changelog-register.md
✅ Read .olaf/data/projects/changelog-register.md

# Second version clearly indicates WHAT, not WHERE
```

### 3. **Consistency Across Prompts**
**Problem:** Different prompts reference same location differently.

**Solution:** Single canonical reference ensures consistency.

**Example:**
```markdown
# All prompts use same reference
.olaf/data/projects/jobs-register.md = .olaf/data/projects/jobs-register.md

# No variations like:
# - .olaf/data/projects/jobs-register.md
# - ../data/projects/jobs-register.md
# - data/projects/jobs-register.md
```

### 4. **Hierarchical Structure**
**Problem:** Flat paths hide relationships between directories.

**Solution:** Nested IDs show hierarchy clearly.

**Example:**
```markdown
.olaf/ = `.olaf/`
.olaf/data/ = `.olaf/data/`
.olaf/data/projects/ = `.olaf/data/projects/`
.olaf/data/projects/jobs-register.md = `.olaf/data/projects/jobs-register.md`

# Clear parent-child relationships
```

### 5. **Context-Dependent References**
**Problem:** Need to reference both OLAF structure and user's project.

**Solution:** Separate ID namespaces for different contexts.

**Example:**
```markdown
 = Root of target repository (user's project)
.olaf/ = `.olaf/` (OLAF framework)

# Prompts can reference both:
# - User code: src/main.py
# - OLAF data: .olaf/data/projects/jobs-register.md
```

### 6. **Environment Flexibility**
**Problem:** Different operating systems, different path conventions.

**Solution:** IDs abstract away platform differences.

**Example:**
```markdown
# Memory-map handles OS-specific contexts
.olaf/data/context/context-current.md = .olaf/data/context/context-windows-powershell.md
# or
.olaf/data/context/context-current.md = .olaf/data/context/context-linux-bash.md

# Prompts just use .olaf/data/context/context-current.md
```

### 7. **Validation and Error Detection**
**Problem:** Typos in paths cause silent failures.

**Solution:** IDs can be validated against memory-map.

**Example:**
```markdown
❌ [id:sklls_dir]  # Typo - can be detected
✅ skills/  # Valid ID

# Tools can validate all ID references
```

---

## Memory Map Structure

### Core Sections

**Root References:**
```markdown
 = Target repository root (user's project)
.olaf/ = `.olaf/` (OLAF framework)
```

**Framework Components:**
```markdown
[id:ack_dir] = `.olaf/core/`
skills/ = `[id:ack_dir]skills/`
competencies/ = `[id:ack_dir]competencies/`
reference/ = `[id:ack_dir]reference/`
schemas/ = `[id:ack_dir]schemas/`
```

**Data Environment:**
```markdown
.olaf/data/ = `.olaf/data/`
.olaf/data/context/ = `.olaf/data/context/`
.olaf/data/projects/ = `.olaf/data/projects/`
.olaf/data/practices/ = `.olaf/data/practices/`
```

**Key Files:**
```markdown
reference/query-competency-index.md = `reference/query-competency-index.md`
reference/core-principles.md = `reference/core-principles.md`
.olaf/data/projects/jobs-register.md = `.olaf/data/projects/jobs-register.md`
.olaf/data/projects/changelog-register.md = `.olaf/data/projects/changelog-register.md`
```

---

## Usage in Prompts

### Example 1: Reading Framework Files
```markdown
## Instructions
1. Load core principles from reference/core-principles.md
2. Review competency index at reference/query-competency-index.md
3. Check available skills in skills/
```

### Example 2: Writing Output Files
```markdown
## Output
- Save job definition to .olaf/data/projects/jobs-register.md
- Create changelog entry in .olaf/data/projects/changelog-register.md
- Store conversation record in [id:conversation_records_dir]
```

### Example 3: Multi-Context References
```markdown
## Process
1. Analyze code in src/
2. Load coding standards from .olaf/data/practices/standards/
3. Generate report to .olaf/data/product/technical/code-review-YYYYMMDD.md
```

---

## Integration with AI Agents

### Automatic Loading

The memory-map is loaded automatically when OLAF framework is initialized:

**Windsurf/Cascade:**
- Loaded via `.windsurf/team.md`
- Available in all agent sessions

**GitHub Copilot:**
- Loaded via `.github/copilot-instructions.md`
- Available in chat and inline suggestions

**Other Agents:**
- Load via `olaf` command
- Included in framework condensed version

### Fallback Strategy

If ID resolution fails, agents can:
1. Reference memory-map directly at `reference/memory-map.md`
2. Use embedded agent indexing/search capabilities
3. Request explicit path from user

---

## Best Practices for Prompt Authors

### 1. Always Use IDs for OLAF Paths
```markdown
✅ Read from skills/
❌ Read from skills/
```

### 2. Use Descriptive IDs
```markdown
✅ .olaf/data/projects/changelog-register.md
❌ [id:cr]
```

### 3. Document ID Usage in Prompts
```markdown
## File References
This prompt uses the following memory-map IDs:
- .olaf/data/projects/jobs-register.md - Job tracking file
- .olaf/data/practices/ - Best practices directory
```

### 4. Validate IDs Exist
Before using a new ID, verify it exists in memory-map or add it.

### 5. Prefer Higher-Level IDs
```markdown
✅ .olaf/data/projects/jobs-register.md  # Direct file reference
❌ .olaf/data/projects/jobs-register.md  # Manual path construction
```

---

## Summary

The Memory Map's ID pointer system provides:

✅ **Single source of truth** for all OLAF paths  
✅ **Maintainable prompts** that survive restructuring  
✅ **Clear intent** through semantic naming  
✅ **Consistent references** across 90+ skills  
✅ **Hierarchical organization** showing relationships  
✅ **Context flexibility** for different environments  
✅ **Validation support** for error detection  

This system is essential for OLAF's scalability, allowing the framework to grow from 10 to 100+ skills while maintaining prompt integrity and ease of maintenance.
