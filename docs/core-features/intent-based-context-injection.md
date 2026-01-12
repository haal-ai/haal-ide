# Intent-Based Context Injection

OLAF automatically detects user intent and loads relevant context just-in-time, providing specialized knowledge without cluttering the base framework. This system enables efficient, focused AI interactions by injecting domain-specific practices and guidelines exactly when needed.

## How It Works

### **Intent Detection**
The system monitors user requests for specific patterns and automatically loads relevant practice files:

```markdown
User: "I need to commit my changes"
→ Detects: Git operations
→ Loads: .olaf/data/practices/git-guidelines.md
→ Response: "🔄 Git guidelines loaded"
```

### **Supported Intent Categories**

## **Git Operations**
**Trigger Patterns**: `git commit`, `commit`, `stage`, `push`, `pull`, `merge`, `branch`
**Action**: Load `.olaf/data/practices/git-guidelines.md`
**Confirmation**: "🔄 Git guidelines loaded"

## **Code Review**  
**Trigger Patterns**: `review code`, `code review`, `check code`, `coding standards`
**Action**: Load `.olaf/data/practices/code-review-guidelines.md`
**Confirmation**: "👀 Code review guidelines loaded"

## **Code Development**
**Trigger Patterns**: `write code`, `implement`, `develop`, `refactor`, `fix bug`
**Action**: Load `.olaf/data/practices/standards/universal-coding-standards.md`
**Confirmation**: "📋 Coding standards loaded"

## **Testing**
**Trigger Patterns**: `unit test`, `test coverage`, `testing`, `test case`
**Action**: Load `.olaf/data/practices/standards/integration-testing-standards.md`
**Confirmation**: "🧪 Testing standards loaded"

## Architecture

### **Detection Engine**
```markdown
1. Parse user request for intent keywords
2. Match against predefined patterns
3. Identify highest-confidence intent category
4. Load corresponding practice files
5. Inject context into AI agent memory
6. Provide user feedback about loaded context
```

### **Practice File Organization**
```
.olaf/data/practices/
├── git-guidelines.md              # Git workflow best practices
├── code-review-guidelines.md      # Code review standards  
└── standards/
    ├── universal-coding-standards.md    # General coding practices
    └── integration-testing-standards.md # Testing methodologies
```

## Benefits

### **Just-In-Time Loading**
- ✅ **Efficiency**: Only load relevant context when needed
- ✅ **Focus**: Avoid irrelevant information cluttering responses
- ✅ **Performance**: Minimize token usage in base framework
- ✅ **Relevance**: Context precisely matches user intent

### **Dynamic Context Management**
- ✅ **Automatic**: No manual context selection required
- ✅ **Intelligent**: Pattern matching understands user goals
- ✅ **Transparent**: Clear feedback about what context is loaded
- ✅ **Stackable**: Multiple contexts can be loaded for complex tasks

### **Scalable Knowledge Base**
- ✅ **Modular**: Add new practice files without framework changes
- ✅ **Maintainable**: Update domain knowledge independently
- ✅ **Extensible**: Easy to add new intent categories
- ✅ **Portable**: Practice files work across different AI platforms

## Implementation Details

### **Intent Pattern Matching**
```markdown
Git Operations:
- Patterns: ["git commit", "commit", "stage", "push", "pull", "merge", "branch"]
- Case-insensitive matching
- Partial phrase recognition
- Context-aware disambiguation

Code Review:
- Patterns: ["review code", "code review", "check code", "coding standards"] 
- Domain-specific vocabulary recognition
- Activity-based intent classification
```

### **Context Loading Process**
1. **Pattern Recognition**: User input analyzed for intent keywords
2. **Confidence Scoring**: Multiple patterns may match, highest score wins
3. **File Loading**: Relevant practice file loaded from data/practices/
4. **Context Integration**: Practice guidelines integrated into AI memory
5. **User Notification**: Confirmation message with specific emoji indicator
6. **Enhanced Response**: AI responses now include domain-specific knowledge

### **Bootstrap Integration**
The intent-based context injector is automatically activated through OLAF bootstrap:
- **GitHub Copilot**: Loaded via `.github/instructions/intent-based-context-injector.instructions.md`
- **Windsurf**: Activated through bootstrap rule configuration
- **AWS Kiro**: Integrated into steering documents
- **Other Platforms**: Included in condensed framework loading

## Example Scenarios

### **Git Workflow**
```markdown
User: "I want to commit my changes with a good message"
System: 🔄 Git guidelines loaded
AI: Based on git best practices, here's how to create an effective commit message:
- Use imperative mood ("Fix bug" not "Fixed bug")
- Keep first line under 50 characters
- Include detailed explanation if needed
- Reference issue numbers when relevant
[Includes specific guidance from git-guidelines.md]
```

### **Code Review Request**
```markdown
User: "Can you review this code for quality issues?"
System: 👀 Code review guidelines loaded
AI: I'll review your code using our code review standards:
- Checking for readability and maintainability
- Verifying error handling patterns
- Assessing test coverage adequacy
- Evaluating security considerations
[Applies code-review-guidelines.md criteria]
```

### **Development Task**
```markdown
User: "I need to implement this new feature"
System: 📋 Coding standards loaded
AI: I'll help implement this feature following our coding standards:
- Consistent naming conventions
- Proper error handling patterns
- Documentation requirements
- Testing strategy recommendations
[Incorporates universal-coding-standards.md practices]
```

## Configuration

### **Adding New Intent Categories**

1. **Define Intent Patterns**:
   ```markdown
   Documentation: ["write docs", "documentation", "create readme", "generate docs"]
   ```

2. **Create Practice File**:
   ```markdown
   Location: .olaf/data/practices/documentation-standards.md
   Content: Domain-specific guidelines and best practices
   ```

3. **Update Intent Detector**:
   ```markdown
   Add pattern matching rule in intent detection system
   Define confirmation message with appropriate emoji
   ```

4. **Test Integration**:
   ```markdown
   Verify intent detection works correctly
   Confirm practice file loads as expected
   Validate enhanced AI responses include new context
   ```

### **Practice File Format**
```markdown
# Practice Title

## Guidelines
- Specific, actionable practices
- Clear do/don't examples  
- Context-specific recommendations

## Standards
- Quality criteria
- Compliance requirements
- Measurement approaches

## Examples
- Real-world scenarios
- Before/after comparisons
- Common mistakes to avoid
```

## Performance Considerations

### **Optimization**
- **Lazy Loading**: Context loaded only when intent detected
- **Caching**: Recently loaded practices cached for session
- **Size Limits**: Practice files kept focused and concise
- **Priority**: Most common intents detected first

### **Token Management**
- **Minimal Base**: Core framework stays lightweight
- **Targeted Injection**: Only relevant context loaded
- **Automatic Cleanup**: Unused context expires after session
- **Smart Batching**: Related practices can be loaded together

## Future Enhancements

### **Advanced Intent Detection**
- **Multi-Intent Recognition**: Handle complex requests with multiple intents
- **Context Awareness**: Consider project type and user role for better matching
- **Learning System**: Improve pattern matching based on usage patterns
- **User Customization**: Allow users to define custom intent patterns

### **Enhanced Context Management**
- **Hierarchical Loading**: Load general then specific practices
- **Conflict Resolution**: Handle overlapping or contradictory guidelines
- **Dynamic Updates**: Update practice files without restarting sessions
- **Usage Analytics**: Track which contexts are most valuable

## See Also

- [OLAF Bootstrap](olaf-bootstrap.md) - Platform integration and framework loading
- [Project Organization](organization.md) - Practice file organization structure
- [Core Principles](core-principles-explained.md) - Base behavioral guidelines
- [Framework Management](framework-management.md) - Overall framework architecture