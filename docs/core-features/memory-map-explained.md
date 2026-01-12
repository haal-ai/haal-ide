# Memory Map

## Overview

The Memory Map is OLAF's navigation system for AI agents. It provides a hierarchical structure of important files and directories using **ID pointers** that enable consistent, maintainable references across all prompts and skills.

**Location:** `.olaf/core/reference/memory-map.md`

---

## The ID Pointer System

### What Are ID Pointers?

ID pointers are symbolic references that map to actual file paths. Instead of hardcoding paths, prompts use IDs that resolve to the correct location.

**Format:** `[id:identifier_name]`

**Example:**
```markdown
[id:core_olaf_dir] = `.olaf/`
[id:skills_dir] = `[id:core_olaf_dir]core/skills/`
```

### How Prompts Use Pointers

**Instead of hardcoded paths:**
```markdown
❌ Read the file at .olaf/core/skills/review-code/skill.prompt.md
```

**Use ID pointers:**
```markdown
✅ Read the file at [id:skills_dir]review-code/skill.prompt.md
```

---

## Benefits of ID Pointers for Prompts

### 1. **Maintainability**
**Problem:** When directory structure changes, hundreds of prompts need updates.

**Solution:** Update once in memory-map, all prompts automatically use new path.

**Example:**
```markdown
# Memory-map change
[id:skills_dir] = `.olaf/framework/skills/`  # Structure reorganized

# No prompt changes needed!
# All references to [id:skills_dir] automatically work
```

### 2. **Readability and Intent**
**Problem:** Hardcoded paths obscure intent.

**Solution:** IDs communicate purpose, not just location.

**Example:**
```markdown
❌ Read .olaf/data/projects/changelog-register.md
✅ Read [id:changelog_register]

# Second version clearly indicates WHAT, not WHERE
```

### 3. **Consistency Across Prompts**
**Problem:** Different prompts reference same location differently.

**Solution:** Single canonical reference ensures consistency.

**Example:**
```markdown
# All prompts use same reference
[id:jobs_register] = [id:projects_dir]jobs-register.md

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
[id:core_olaf_dir] = `.olaf/`
[id:data_dir] = `[id:core_olaf_dir]data/`
[id:projects_dir] = `[id:data_dir]projects/`
[id:jobs_register] = `[id:projects_dir]jobs-register.md`

# Clear parent-child relationships
```

### 5. **Context-Dependent References**
**Problem:** Need to reference both OLAF structure and user's project.

**Solution:** Separate ID namespaces for different contexts.

**Example:**
```markdown
[id:core_dir] = Root of target repository (user's project)
[id:core_olaf_dir] = `.olaf/` (OLAF framework)

# Prompts can reference both:
# - User code: [id:core_dir]src/main.py
# - OLAF data: [id:jobs_register]
```

### 6. **Environment Flexibility**
**Problem:** Different operating systems, different path conventions.

**Solution:** IDs abstract away platform differences.

**Example:**
```markdown
# Memory-map handles OS-specific contexts
[id:context_current] = [id:context_dir]context-windows-powershell.md
# or
[id:context_current] = [id:context_dir]context-linux-bash.md

# Prompts just use [id:context_current]
```

### 7. **Validation and Error Detection**
**Problem:** Typos in paths cause silent failures.

**Solution:** IDs can be validated against memory-map.

**Example:**
```markdown
❌ [id:sklls_dir]  # Typo - can be detected
✅ [id:skills_dir]  # Valid ID

# Tools can validate all ID references
```

---

## Memory Map Structure

### Core Sections

**Root References:**
```markdown
[id:core_dir] = Target repository root (user's project)
[id:core_olaf_dir] = `.olaf/` (OLAF framework)
```

**Framework Components:**
```markdown
[id:ack_dir] = `[id:core_olaf_dir]core/`
[id:skills_dir] = `[id:ack_dir]skills/`
[id:competencies_dir] = `[id:ack_dir]competencies/`
[id:reference_dir] = `[id:ack_dir]reference/`
[id:schemas_dir] = `[id:ack_dir]schemas/`
```

**Data Environment:**
```markdown
[id:data_dir] = `[id:core_olaf_dir]data/`
[id:context_dir] = `[id:data_dir]context/`
[id:projects_dir] = `[id:data_dir]projects/`
[id:practices_dir] = `[id:data_dir]practices/`
```

**Key Files:**
```markdown
[id:competency_index] = `[id:reference_dir]query-competency-index.md`
[id:core_principles] = `[id:reference_dir]core-principles.md`
[id:jobs_register] = `[id:projects_dir]jobs-register.md`
[id:changelog_register] = `[id:projects_dir]changelog-register.md`
```

---

## Usage in Prompts

### Example 1: Reading Framework Files
```markdown
## Instructions
1. Load core principles from [id:core_principles]
2. Review competency index at [id:competency_index]
3. Check available skills in [id:skills_dir]
```

### Example 2: Writing Output Files
```markdown
## Output
- Save job definition to [id:jobs_register]
- Create changelog entry in [id:changelog_register]
- Store conversation record in [id:conversation_records_dir]
```

### Example 3: Multi-Context References
```markdown
## Process
1. Analyze code in [id:core_dir]src/
2. Load coding standards from [id:practices_dir]standards/
3. Generate report to [id:technical_dir]code-review-YYYYMMDD.md
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
1. Reference memory-map directly at `[id:memory_map]`
2. Use embedded agent indexing/search capabilities
3. Request explicit path from user

---

## Best Practices for Prompt Authors

### 1. Always Use IDs for OLAF Paths
```markdown
✅ Read from [id:skills_dir]
❌ Read from .olaf/core/skills/
```

### 2. Use Descriptive IDs
```markdown
✅ [id:changelog_register]
❌ [id:cr]
```

### 3. Document ID Usage in Prompts
```markdown
## File References
This prompt uses the following memory-map IDs:
- [id:jobs_register] - Job tracking file
- [id:practices_dir] - Best practices directory
```

### 4. Validate IDs Exist
Before using a new ID, verify it exists in memory-map or add it.

### 5. Prefer Higher-Level IDs
```markdown
✅ [id:jobs_register]  # Direct file reference
❌ [id:projects_dir]jobs-register.md  # Manual path construction
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
