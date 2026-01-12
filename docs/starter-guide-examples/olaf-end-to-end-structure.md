# OLAF End-to-End Structure

**Target Audience:** New OLAF users and developers  
**Purpose:** Understand how OLAF components work together from individual prompts to enterprise registries

---

## How OLAF Structures Skills

OLAF treats each **skill** as a self-contained bundle: standardized prompts, their templates, optional helper scripts, and supporting documentation. 

A single skill can participate in multiple **competencies**, such as the "research and report" competency that orchestrates several research-focused skills to deliver a full report for a developer or business analyst.

Competencies are grouped into **collections** (for example, an "Engineer" collection tailored to a specific organization), and a single competency can appear in multiple collections to support different teams. 

Collections live in **OLAF registries**, which are GitHub repositories that can be public or private depending on how teams want to share their capabilities. Multiple registries can expose the same collections when organizations collaborate or reuse shared playbooks. 

Nothing is opinionated—every layer can be adapted to match your own workflows.

Enterprise registries can chain to other registries in a preferred order and, when policy allows, terminate their chain with the public open-source OLAF registry. This chaining model lets organizations blend internal capabilities with shared community skills.

---

## Visual Architecture Overview

### Diagram 1: Prompts, skills, and competencies
```
+---------+     +---------+     +-----------------+
| Prompt  | --> | Skill   | --> | Competency      |
+---------+     +---------+     +-----------------+
```
**Reuse notes:** a prompt can power multiple skills, and a skill can participate in many competencies.

### Diagram 2: Competencies, collections, and registries
```
+-----------------+     +-------------+     +-----------------+
| Competency      | --> | Collection  | --> | OLAF Registry   |
+-----------------+     +-------------+     +-----------------+
         ^                     ^                     |
         |                     |                     v
    (many-to-many)         (shared)           chained registries
```
**Sharing notes:** Registries can be chained, with enterprise registries optionally falling back to the open-source OLAF registry.

### Diagram 3: Registry chaining workflow
```
+-------------------+     +---------------------+     +--------------------+
| Seed Registry     | +-> | Internal/External   | --> | Open Source OLAF   |
| (Company Start)   |     | Registry Chain      |     | Registry (if auth) |
+-------------------+     +---------------------+     +--------------------+
         ^                         ^                          ^
         |                         |                          |
    First lookup           Additive registries         Company policy gate
```

The OLAF CLI starts with your company's seed registry, then adds capabilities from the configured chain of internal and external registries, ending with the public registry only if company policy permits.

The order of registry chaining is significant: earlier registries take precedence, allowing organizations to override or extend shared capabilities with their own custom skills.

---

## Key Benefits of This Structure

- **Modularity**: Each layer can be developed, tested, and shared independently
- **Reusability**: Skills and competencies can be mixed and matched across teams
- **Governance**: Organizations control what capabilities are available at each level
- **Flexibility**: Nothing is opinionated—adapt every layer to your workflows
- **Security**: Company policy gates control access to external capabilities

---

*This structure enables OLAF to scale from individual developer productivity to enterprise-wide AI capability management.*