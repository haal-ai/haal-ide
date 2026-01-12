# Interaction Protocols Explained

OLAF uses three distinct interaction protocols to balance safety and efficiency for AI agent actions. These protocols provide a safe environment for users who may be cautious about AI agent autonomy.

## Purpose

- **Safety Management**: Control how AI agents execute tasks
- **User Confidence**: Provide different levels of confirmation for different action types
- **Risk Mitigation**: Require explicit approval for potentially dangerous operations

## The Three Protocols

### 1. **"Act" Protocol** (Direct Actions)
- **Usage**: Safe, read-only operations, information gathering
- **Behavior**: Agent executes immediately without asking
- **Example**: Reading files, searching, analyzing existing content
- **When to use**: Default protocol for low-risk actions

### 2. **"Propose-Act" Protocol** (Analysis Before Acting)
- **Usage**: Actions that benefit from user review but aren't high-risk
- **Behavior**: Agent describes the action and waits for user agreement before proceeding
- **Example**: Creating documentation, running analysis scripts
- **When to use**: Medium-risk actions requiring user awareness

### 3. **"Propose-Confirm-Act" Protocol** (Modifications)
- **Usage**: Any action that modifies, creates, or deletes files
- **Behavior**: Multi-step process with explicit confirmation gates
- **Steps**:
  1. **Propose**: Present detailed plan to user
  2. **Review**: Wait for user review and feedback
  3. **Confirm**: Ask for final sign-off ("Ready to proceed?")
  4. **Act**: Execute only after receiving final confirmation
- **When to use**: High-risk actions (file modifications, deletions, system changes)

## Configuration

- **Location**: Protocols are defined in `/core/reference/team-delegation.md`
- **Assignment**: Each competency specifies its execution protocol in `query-competency-index.md`
- **Default**: If no protocol is specified, "Act" protocol is used

## Model Compatibility

The effectiveness of these protocols varies by AI model:
- Some models handle all three protocols well
- Others may struggle with the multi-step confirmation process
- Testing with your specific model is recommended

## Benefits

- ✅ **User Control**: Different safety levels for different action types
- ✅ **Transparency**: Users understand what actions will be taken
- ✅ **Safety**: Critical operations require explicit approval
- ✅ **Flexibility**: Can be configured per competency based on risk level

## See Also

- **Implementation**: `/core/reference/team-delegation.md` (actual protocol definitions)
- **Configuration**: `query-competency-index.md` (protocol assignments)
- **Framework**: [Framework Management](framework-management.md) (how protocols integrate)