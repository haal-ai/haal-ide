
# HAAL Branching Strategy

This document outlines the branching strategy for all HAAL repositories to ensure clear development workflows and maintain code quality across the HAAL ecosystem.

## Branch Overview

### `main` - Minimal Production Branch (Protected)
- **Purpose**: Bare minimum HAAL framework for core functionality
- **Content**: Essential framework components only
- **Status**: Always functional and tested
- **Usage**: Base framework for users who want minimal installation
- **Protection**: Protected - no direct commits, only via pull requests from `integration`

### `integration` - Main Integration Branch (Protected)
- **Purpose**: Integration testing for features destined for `main`
- **Status**: Functional but may contain new features under final validation
- **Usage**: Testing ground for core framework features before they reach main
- **Workflow**: Receives pull requests from `develop` and feature branches, merges to `main` after validation

### `develop` - Development Branch
- **Purpose**: Personal development and experimentation
- **Status**: Work-in-progress, may contain incomplete features
- **Usage**: Individual developer workspace
- **Protection**: Unprotected - allows direct commits for development freedom

## Contribution Workflow

### For All Contributors

1. **Create Feature Branch**: Create your own branch from `develop`
   ```
   git checkout develop
   git pull origin develop
   git checkout -b feature-your-feature-name
   ```

2. **Development**: Work on your contributions in your feature branch

3. **Submit Pull Request**: 
   - Target `integration` for all changes
   - Ensure PR includes clear description and testing

4. **Review Process**: Pull requests are reviewed before integration
   - Requires approval from code owner (@pjmp020564)
   - Stale approvals are dismissed on new commits

5. **Integration**: After approval, changes are merged to `integration`

6. **Production Release**: `integration` branch is periodically merged to `main`

## Branch Protection Rules

- **main**: Protected - requires pull request approval and code owner review
- **integration**: Protected - requires pull request approval and code owner review
- **develop**: Unprotected - allows direct commits for development
- **feature-***: No protection - development freedom

### Protection Settings
- Required approving reviews: 1
- Dismiss stale reviews: Enabled
- Require code owner reviews: Enabled (@pjmp020564)
- Allow force pushes: Disabled
- Allow deletions: Disabled
- Block creations: Enabled

## Best Practices

1. **Always use Pull Requests** - No direct commits to `main` or `integration`
2. **Clear Branch Naming** - Use descriptive names like `feature-new-cli-command` or `fix-skills-loading`
3. **Target Integration Branch** - All PRs should target `integration`
4. **Test Before PR** - Ensure your contributions work as expected
5. **Document Changes** - Include clear descriptions in pull requests
6. **Update Documentation** - Keep docs in sync with code changes
7. **Respect Protection Rules** - Follow the established branch protection policies

---

**Last Updated**: January 7, 2026
**Applies to**: All HAAL repositories
