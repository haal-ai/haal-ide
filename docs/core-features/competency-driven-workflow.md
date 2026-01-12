# OLAF Workflow Architecture

OLAF uses a three-tier architecture: **Skills → Competencies → Collections** to organize and orchestrate AI capabilities.

## Architecture Overview

### 1. **Skills** (Atomic Units)
- **Location**: `/core/skills/`
- **Purpose**: Individual, reusable AI prompts with specific functions
- **Structure**: Each skill contains prompts, templates, tools, documentation
- **Examples**: `review-code`, `create-changelog-entry`, `git-add-commit`

### 2. **Competencies** (Orchestration Layer)  
- **Location**: `/core/competencies/`
- **Purpose**: Group related skills into logical workflows
- **Function**: Define skill sequences, data flow, interaction protocols
- **Examples**: Code review competency (uses review-code + improve-complexity skills)

### 3. **Collections** (Enterprise Organization)
- **Location**: `/core/reference/competency-collections.json`
- **Purpose**: Package competencies for different user personas/contexts
- **Examples**: `developer`, `business-analyst`, `prompt-engineer`, `git-assistant`

## Central Dispatcher

**Query Competency Index** (`/core/reference/query-competency-index.md`):
- Maps user requests to specific skills using pattern matching
- Defines interaction protocols (Act/Propose-Act/Propose-Confirm-Act) per skill
- Contains 78+ entry points across 7 competency collections
- Auto-generated and maintained by collection selection system

## Request Processing Flow

1. **User Request**: "olaf review code"
2. **Pattern Match**: System searches query-competency-index.md for "review code"
3. **Skill Resolution**: Maps to `skills/review-code/prompts/review-code.md`
4. **Protocol Assignment**: Applies "Propose-Act" protocol
5. **Execution**: Loads skill with appropriate safety protocol

## Key Features

- ✅ **Pattern Matching**: Flexible natural language to skill mapping
- ✅ **Protocol Safety**: Different interaction levels per skill type
- ✅ **Modular Design**: Skills can be combined into complex competencies
- ✅ **Enterprise Ready**: Collections allow persona-specific skill sets
- ✅ **Scalable**: Currently 78+ skills across 90+ atomic units

## Modern Capabilities

### Competency Collections
```json
{
  "all": ["my-prompts", "olaf-base-skills", "business-analyst", "common", "developer", "git-assistant", "prompt-engineer"],
  "developer": ["code-quality", "git-operations", "documentation"],
  "business-analyst": ["requirements-analysis", "specification-review"]
}
```

### Skill Organization
```
skills/review-code/
├── prompts/review-code.md          # Main AI instruction
├── templates/action-plan.md        # Output templates  
├── docs/tutorial.md               # Usage documentation
└── skill-manifest.json           # Metadata & config
```

### Protocol Assignment
- **Act**: Safe operations (reading, analysis) - no confirmation
- **Propose-Act**: Medium risk - propose then execute with approval
- **Propose-Confirm-Act**: High risk (file changes) - multi-step confirmation

## Evolution from Legacy

**Previous**: Simple competency → prompt mapping
**Current**: Skills → Competencies → Collections with sophisticated orchestration

This architecture enables:
- **Atomic reusability** of individual skills
- **Complex workflows** through competency orchestration  
- **Enterprise organization** via persona-specific collections
- **Safety protocols** matched to risk levels
- **Scalable growth** from 10 to 100+ skills

## See Also

- [Project Organization](organization.md) - Detailed skill architecture
- [Interaction Protocols](interaction-protocols-explained.md) - Safety protocol details
- [Framework Management](framework-management.md) - How components integrate
