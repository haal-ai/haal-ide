# Project Memory Map
<metadata>
version: 1.7.0
last_updated: 2025-11-17
purpose: LLM navigation aid - consolidated OLAF framework
changes: "Updated memory map to match current .olaf structure: corrected data paths, added missing directories (bundles, docs, orphan-collector, your-data, your-repos), updated context structure with OS-specific files, added olaf-registry.json, corrected product directory structure with functional/technical separation"
</metadata>

<olaf-memory-map>
## Project Structure and Paths

### Target Repository [id:core_dir] = Root of the target repository on which a skill is currently working
# This is a context-dependent reference to the user's project being analyzed/developed (not OLAF itself)
# Used by developer and workflow prompts to reference the codebase under analysis

### Core solution [id:core_olaf_dir] = `.olaf/`
# Repo-local OLAF folder (workspace-scoped)
# Example usage:
# [id:core_olaf_dir]core/reference/query-competency-index.md → refers to .olaf/core/reference/query-competency-index.md

### Global OLAF [id:global_olaf_dir] = `~/.olaf/`

### Additional Directories
- **Docs Directory** [id:docs_dir] = `[id:core_olaf_dir]docs/`
- **Work Directory** [id:work_dir] = `[id:core_olaf_dir]work/`
- **Staging Directory** [id:staging_dir] = `[id:work_dir]staging/`
- **Carry-Over Directory** [id:carryover_dir] = `[id:work_dir]carry-over/`
- **Stash Directory** [id:stash_dir] = `[id:work_dir]stash/`

### Core Framework [id:ack_dir] = `[id:core_olaf_dir]core/`
# Example usage:
# [id:ack_dir]README.md → refers to .olaf/core/README.md
# [id:skills_dir]create-prompt/prompts/create-prompt.md → refers to .olaf/core/skills/create-prompt/prompts/create-prompt.md
- **Competencies Directory** [id:competencies_dir] = `[id:ack_dir]competencies/`
- **Skills Directory** [id:skills_dir] = `[id:ack_dir]skills/`

### Skills Resolution
- **Local Skills Directory** [id:local_skills_dir] = `[id:core_olaf_dir]core/skills/`
- **Global Skills Directory** [id:global_skills_dir] = `[id:global_olaf_dir]core/skills/`
- **Schemas Directory** [id:schemas_dir] = `[id:ack_dir]schemas/`
- **Reference Directory** [id:reference_dir] = `[id:ack_dir]reference/`
- **OLAF Registry** [id:olaf_registry] = `[id:reference_dir]olaf-registry.json`
- **Competency Collections** [id:competency_collections] = `[id:reference_dir]competency-collections.json`
- **Condensed Framework Directory** [id:condensed_dir] = `[id:reference_dir].condensed/`
- **Condensed Framework** [id:condensed_framework] = `[id:condensed_dir]olaf-framework-condensed.md`
- **Competency Index** [id:competency_index] = `[id:reference_dir]query-competency-index.md`
# CRITICAL: [id:competency_index] MUST always resolve to the repo-local .olaf/ tree via [id:core_olaf_dir]. Never load this index from [id:global_olaf_dir].
- **Core Principles** [id:core_principles] = `[id:reference_dir]core-principles.md`
- **Team Delegation** [id:team_delegation] = `[id:reference_dir]team-delegation.md`
- **Memory Map** [id:memory_map] = `[id:reference_dir]memory-map.md`
- **LLM vs IDE Task Guide** [id:llm_vs_ide_task_guide] = `[id:reference_dir]llm-vs-ide-task-guide.md`

### Data Environment [id:data_dir] = `[id:core_olaf_dir]data/`
- **Context Directory** [id:context_dir] = `[id:data_dir]context/`
  - **Context Default** [id:context_default] = `[id:context_dir]context-default.md`
  - **Context Current** [id:context_current] = `[id:context_dir]context-current.md`
- **Peoples** [id:peoples_dir] = `[id:data_dir]peoples/`
- **Projects** [id:projects_dir] = `[id:data_dir]projects/`
  - **Jobs Register** [id:jobs_register] = `[id:projects_dir]jobs-register.md` 
- **Product** [id:product_dir] = `[id:data_dir]product/`
  - **Functional Directory** [id:functional_dir] = `[id:product_dir]functional/`
  - **Technical Directory** [id:technical_dir] = `[id:product_dir]technical/`
  - **Decision Records** [id:decision_records_dir] = `[id:product_dir]decision-records/` 
  - **Documentation** [id:documentations_dir] = `[id:product_dir]documentations/` 
- **Practices** [id:practices_dir] = `[id:data_dir]practices/`
  - **Standards Directory** [id:standards_dir] = `[id:practices_dir]standards/` 
  - **Handover Document** [id:handover] = `[id:data_dir]handover-conversation*.md`
</olaf-memory-map>
