# OLAF Bootstrap Integration

OLAF automatically integrates with different AI development platforms through bootstrap configurations, ensuring consistent framework behavior across GitHub Copilot, Windsurf, AWS Kiro, and other AI tools.

## Supported Platforms

### **GitHub Copilot**
- **Configuration**: `.github/copilot-instructions.md`
- **Method**: Bootstrap instructions load condensed framework
- **Integration**: Framework loaded via instruction files
- **Activation**: Automatic on repository access

### **Windsurf IDE**  
- **Configuration**: `.windsurf/rules/` directory
- **Method**: OLAF Bootstrap Rules system
- **Integration**: Framework loaded via rule configuration
- **Activation**: Automatic at session start

### **AWS Kiro**
- **Configuration**: `.kiro/steering/` directory  
- **Method**: Steering documents approach
- **Integration**: Framework loaded as steering document
- **Activation**: Integrated into workspace context

### **Other AI Tools**
- **Requirement**: Tool must support initial instruction configuration
- **Method**: Adaptable bootstrap pattern
- **Examples**: Claude Code, Cursor, other AI coding assistants

## Bootstrap Architecture

### **Core Components**

1. **Condensed Framework Loading**
   ```markdown
   Location: .olaf/core/reference/.condensed/olaf-framework-condensed.md
   Purpose: Self-contained framework (119 lines)
   Content: Protocols, memory map, principles, validation
   ```

2. **Platform Detection**
   ```markdown
   Auto-detection of environment (Copilot/Windsurf/Kiro)
   Platform-specific configuration paths
   Fallback mechanisms for unknown platforms
   ```

3. **Bootstrap Instructions**
   ```markdown
   Intent-based context injector instructions
   Framework validation requirements  
   Tool selection hierarchy rules
   Core principle enforcement
   ```

## Bootstrap Process

### **Initialization Flow**
1. **Platform Detection**: AI agent identifies environment (Copilot/Windsurf/Kiro)
2. **Framework Loading**: Condensed framework loaded from bootstrap configuration
3. **Validation Check**: Verify complete framework loading (119 lines expected)
4. **Context Activation**: Memory map, protocols, and principles become active
5. **Ready State**: Agent responds with "🔄 OLAF framework loaded"

### **Configuration Files**

**GitHub Copilot** (`.github/copilot-instructions.md`):
```markdown
# OLAF Bootstrap - GitHub Copilot Integration
Always load OLAF framework first from:
.olaf/core/reference/.condensed/olaf-framework-condensed.md

Include intent-based context injector rules.
```

**Windsurf** (`.windsurf/rules/olaf-bootstrap.md`):
```markdown
# OLAF Bootstrap - Windsurf Integration  
Framework loaded via bootstrap configuration
Automatic initialization at session start
Self-contained operation mode
```

**AWS Kiro** (`.kiro/steering/olaf-bootstrap.md`):
```markdown
# OLAF Bootstrap - AWS Kiro Integration
Framework loaded as steering document
Integrated into workspace context
Persistent across sessions
```

## Benefits

### **Cross-Platform Consistency**
- ✅ Same OLAF behavior regardless of AI platform
- ✅ Consistent competency routing and protocols
- ✅ Unified skill execution across environments

### **Automatic Integration** 
- ✅ Zero manual setup required
- ✅ Framework loads automatically in any supported environment
- ✅ Platform-specific optimizations handled transparently

### **Framework Completeness**
- ✅ Self-contained framework prevents missing components
- ✅ Validation ensures complete loading
- ✅ Fallback mechanisms for partial loads

## Platform-Specific Features

### **GitHub Copilot**
- Integration with VS Code extension ecosystem
- File-based instruction loading
- Repository-wide framework access

### **Windsurf IDE**
- Always-on rule configuration
- Persistent framework state
- IDE-native integration

### **AWS Kiro** 
- Steering document persistence
- Workspace-integrated context
- Multi-session continuity

## Troubleshooting

### **Common Issues**

**Framework Not Loading**:
- Verify bootstrap file exists in correct platform directory
- Check condensed framework file integrity (119 lines)
- Confirm AI tool supports instruction files

**Incomplete Loading**:
- Look for validation messages about line count
- Framework should auto-reload with `endLine=-1` if truncated
- Check for "🔄 OLAF framework loaded" confirmation

**Platform Detection**:
- Bootstrap works across supported platforms automatically
- Manual specification available if auto-detection fails
- Platform-specific configurations can be customized

## Development

### **Adding New Platforms**

1. **Identify Configuration Method**: How the platform loads initial instructions
2. **Create Bootstrap File**: Platform-specific bootstrap configuration  
3. **Test Integration**: Verify framework loading and validation
4. **Add Documentation**: Update this guide with new platform details

### **Bootstrap File Template**
```markdown
# OLAF Bootstrap - [Platform Name]
Load condensed framework from: .olaf/core/reference/.condensed/olaf-framework-condensed.md
Enable intent-based context injection
Validate complete framework loading (119 lines)
Confirm with: "🔄 OLAF framework loaded"
```

## See Also

- [Framework Management](framework-management.md) - Condensed framework details
- [Intent-Based Context Injection](intent-based-context-injection.md) - Just-in-time context loading
- [Project Organization](organization.md) - Overall OLAF structure
- [Interaction Protocols](interaction-protocols-explained.md) - Protocol system details