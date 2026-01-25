---
description: Start implementation in a worktree
---

# Workflow: Start Implementation in Worktree

This workflow guides you through starting implementation work in a dedicated worktree.

## Steps

1. **Create worktree for implementation**
   ```bash
   git worktree add -b feature/implementation-name ../haal-ide-implementation develop
   ```

2. **Navigate to worktree**
   - Switch to the worktree directory
   - Verify you're on the correct branch

3. **Analyze the implementation requirements**
   - Review the Kanban card or prompt
   - Identify key components using SOLID principles
   - Check acceptance criteria and DoD checklist

4. **Plan with TDD/BDD approach**
   - Write BDD scenarios for user-visible behavior
   - Identify unit tests needed for core logic
   - Plan filesystem abstractions for testability

5. **Set up development environment**
   - Ensure Go dependencies are available
   - Create test directories and temp file handling
   - Set up interfaces for filesystem/HTTP/clock as needed

6. **Implement following SOLID principles**
   - Start with single responsibility functions
   - Use dependency inversion for core logic
   - Wrap side effects behind interfaces
   - Follow error handling conventions (wrap with context, stderr)

7. **Test-driven development cycle**
   - Red: Write failing test
   - Green: Implement minimum to pass
   - Refactor: Clean up with tests green

8. **Validate against DoD**
   - Check acceptance criteria met
   - Run `go test ./...`
   - Verify no accidental writes outside target dirs
   - Update kanban-learnings.txt and kanban-progress.txt

9. **Commit and merge**
   - Commit changes with clear message
   - Switch back to main worktree
   - Merge feature branch when complete

## Usage

Run this workflow when starting implementation work that requires isolation from the main development branch.
