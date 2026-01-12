# Selective PR (Design Notes)

This document describes the “selective PR” workflow used in this repository.

Selective PR is a workflow to copy only a curated list of paths from one ref/branch into another ref/branch and create a PR branch.

## Files

- Script: `scripts/create-selective-pr.ps1`
- Path lists:
  - `scripts/pr-paths-develop-to-integration.txt`
  - `scripts/pr-paths-integration-to-main.txt`

## Usage

### Develop → Integration

```powershell
pwsh -NoProfile -File .\scripts\create-selective-pr.ps1 -Flow develop-to-integration -SourceRef develop -BaseRef integration
```

### Integration → Main

```powershell
pwsh -NoProfile -File .\scripts\create-selective-pr.ps1 -Flow integration-to-main -SourceRef integration -BaseRef main
```

### Explicit path file override

```powershell
pwsh -NoProfile -File .\scripts\create-selective-pr.ps1 -PathsFile scripts\pr-paths-develop-to-integration.txt -SourceRef develop -BaseRef integration
```

## Notes

- `-PathsFile` is optional; if omitted, `-Flow` selects the default paths file.
- The script requires a clean working tree because it creates and removes a temporary worktree.
