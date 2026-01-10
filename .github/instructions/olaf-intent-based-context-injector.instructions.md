---
description: "Intent-based context injector for GitHub Copilot - auto-detects development intents and loads relevant practices"
applyTo: "**"
---

# Intent-Based Context Injector for GitHub Copilot

**CRITICAL**: This instruction applies to EVERY user request. Execute BEFORE any other processing.

## Mandatory Intent Detection

**BEFORE responding to ANY user request**, you MUST:

1. **Scan the user input AND attached files** for intent patterns
2. **Auto-load** corresponding practice files using `read_file` tool
3. **Announce** which practices were loaded
4. **Apply** the loaded guidelines throughout your response

**Detection Sources:**
- User's message text
- Attached prompt file names (e.g., `olaf-git-add-commit.prompt.md` → git intent)
- Attached prompt file contents
- User's request context

## Intent Patterns & Required Practices

### Git Operations
**Patterns**: ["git", "commit", "add and commit", "git add", "stage", "push", "pull", "merge", "branch"]

**MUST Load**: 
- `.olaf/data/practices/guidances/git/git-guidelines.md`

**Announce**: 
```
📋 Git guidelines loaded (detected: git operations)
```

### Code Review
**Patterns**: ["review code", "code review", "check code", "inspect code", "coding standards"]

**MUST Load**:
- `.olaf/data/practices/guidances/review/code-reviews/code-review-guidelines.md`
- `.olaf/data/practices/standards/universal-coding-standards.md`

**Announce**: 
```
📋 Code review guidelines loaded (detected: code review intent)
```

### Code Actions
**Patterns**: ["write code", "create function", "implement", "develop", "code", "programming", "refactor", "fix bug"]

**MUST Load**:
- `.olaf/data/practices/standards/universal-coding-standards.md`
- `.olaf/data/practices/standards/coding-standards-template.md`

**Announce**: 
```
📋 Coding standards loaded (detected: code action intent)
```

### Unit Testing
**Patterns**: ["unit test", "write test", "test coverage", "testing", "test case", "mock", "assert"]

**MUST Load**:
- `.olaf/data/practices/standards/integration-testing-standards.md`
- `.olaf/data/practices/standards/universal-coding-standards.md`

**Announce**: 
```
📋 Testing standards loaded (detected: testing intent)
```

## Execution Order

**STEP 1**: Scan for intent patterns (user message + attachments)
**STEP 2**: Load ALL matching practice files
**STEP 3**: Announce loaded practices to user
**STEP 4**: Proceed with user request while applying guidelines

## Examples

**Example 1**: User says "olaf git commit the changes"
```
📋 Git guidelines loaded (detected: git operations)
[proceed with commit following git-guidelines.md rules]
```

**Example 2**: Attached file `olaf-git-add-commit.prompt.md`
```
📋 Git guidelines loaded (detected: git-add-commit in attachment)
[proceed following git-guidelines.md rules]
```

**Example 3**: User says "review this code for quality"
```
📋 Code review guidelines loaded (detected: code review intent)
[proceed with review following code-review-guidelines.md]
```