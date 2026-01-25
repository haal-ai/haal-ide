# Integration with Agents

## Core Files
The essential files for agent integration are located in `reference/`:

- `reference/memory-map.md` - provides the LLM with key context pointers (files or structure)
- `reference/core-principles.md` - contains fundamental OLAF principles
- `reference/query-competency-index.md` - competency mapping and skills index

These files should be loaded by the LLM at the start of each interaction. This is why we rely on the agent's capabilities to do so (e.g., through `.windsurf/team.md` for Windsurf, or similar agent-specific configuration files).

The contents of these files are loaded into the context windows of the LLM when the interaction begins. Therefore, it is crucial to keep the information concise and provide clear context.

## Agent-Specific Setup

### Windsurf Integration
- Use `.windsurf/team.md` to reference the core files
- Configure context loading to include `reference/memory-map.md`

### Other Agents
- Configure your agent to load the core reference files from `reference/`
- Ensure the memory-map file is prioritized for context injection

## Competency Access

Agents should be configured to access:
- **Skills**: Located in `skills/`
- **Competencies**: Located in `competencies/`
- **Reference Materials**: Located in `reference/`

The framework provides structured access to these through the competency index and registry files.
