# HAAL Skill Discovery Demo: BMS Expertise Example

## Overview

This example demonstrates HAAL's intelligent skill discovery workflow, showing how the system automatically routes user requests to specialized skills rather than using generic approaches.

## Demo Scenario

**User Request**: "haal tell me about bms"

**HAAL Response**: Instead of using the generic "tell me" skill, HAAL discovered and activated the specialized "get-bms-expertise" skill, providing expert-level knowledge of Amadeus' Build Management System.

## Skill Discovery Workflow

### 1. Framework Loading
HAAL first loads the condensed framework and current context to establish the operational environment.

### 2. Competency Index Query
The system searches `query-competency-index.md` for pattern matches:
- **Pattern Matched**: ["bms expert", "bms help", "load bms expertise"]
- **Skill Found**: `skills/get-bms-expertise/prompts/get-bms-expertise.md`
- **Protocol**: "Act" (direct execution)

### 3. Expertise Activation
HAAL loads the BMS expert persona with deep knowledge of:
- Component-based C/C++ architecture
- Binary compatibility management
- Build/test/delivery workflows
- Dependency resolution and Forest workspaces

### 4. Specialized Response
The BMS expert provides detailed, domain-specific information that generic skills cannot match.

## Conversation Recording

### Staging Location
The conversation record is saved to:
```
.olaf/work/staging/conversation-records/conversation-record-20260108-0829.md
```

### Why Staging Folder?
- **Non-committed**: Files in staging are not automatically committed to version control
- **Review Process**: Users can review, edit, and approve content before committing
- **Flexibility**: Allows modification of conversation records as demonstrated in this example
- **Temporary Storage**: Staging serves as a holding area for work-in-progress documentation

### Record Benefits
- **Complete Dialogue**: Captures full user-AI interaction without summarization
- **Action Documentation**: Records all tool calls and file operations
- **Skill Discovery Evidence**: Shows how HAAL matched specific skills to user requests
- **Knowledge Transfer**: Provides examples for training and documentation

## Key Demonstration Points

### 1. Intelligent Skill Routing
HAAL's competency index contains 86+ entry points across multiple collections. The system:
- Analyzes user requests for pattern matches
- Prioritizes specialized skills over generic ones
- Provides domain-expert level responses
- Maintains context of available capabilities

### 2. Expertise Depth
The BMS expert skill contains:
- 242 lines of specialized knowledge
- Specific command references and examples
- Troubleshooting scenarios and solutions
- Integration with knowledge base resources
- Behavioral guidelines and quality standards

### 3. Documentation Workflow
The conversation record demonstrates:
- Real-time capture of interactions
- Structured formatting for readability
- File operation tracking
- Timestamp and metadata preservation
- Post-creation editing capabilities

## Comparison: Generic vs Specialized

### Generic "tell me" Skill
- Broad knowledge search
- Web resource fetching
- General information synthesis
- Suitable for external topics

### Specialized "get-bms-expertise" Skill
- Domain-specific expertise
- Internal knowledge base integration
- Detailed technical guidance
- Context-aware recommendations
- Best practices and troubleshooting

## Usage Patterns

### When to Use This Demo
- **Training**: Show new users how HAAL skill discovery works
- **Documentation**: Illustrate competency-driven workflow benefits
- **Development**: Guide skill creation and pattern matching
- **Evaluation**: Demonstrate HAAL's intelligence over generic AI

### Key Takeaways
1. **Skill Discovery**: HAAL automatically finds the most appropriate skill for any request
2. **Expertise Access**: Specialized skills provide deeper knowledge than generic approaches
3. **Documentation**: Conversation records preserve interactions for future reference
4. **Flexibility**: Staging allows review and modification before finalizing

## File Structure

```
.olaf/
├── work/staging/conversation-records/
│   └── conversation-record-20260108-0829.md  # Demo conversation record
├── core/skills/get-bms-expertise/
│   └── prompts/get-bms-expertise.md          # Specialized BMS skill
└── core/reference/
    └── query-competency-index.md             # Skill discovery index
```

## Reproducing the Demo

1. **Request**: Ask HAAL about a specific domain (e.g., "haal tell me about bms")
2. **Observe**: Watch HAAL search competency index and load specialized skill
3. **Record**: Use "haal store conversation" to capture the interaction
4. **Review**: Examine the conversation record in staging folder
5. **Modify**: Edit the record if needed before committing

This example showcases HAAL's core value proposition: intelligent skill discovery that provides expert-level assistance while maintaining complete documentation of the interaction.
