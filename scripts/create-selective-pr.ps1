[CmdletBinding()]
param(
  # Text file containing repo-relative paths (one per line)
  [Parameter(Mandatory = $true)]
  [string]$PathsFile,

  # Source ref to copy paths from (usually develop)
  [Alias('From', 'FromRef')]
  [string]$SourceRef = 'develop',

  # Base branch/ref the PR targets (usually integration)
  [Alias('To', 'ToRef')]
  [string]$BaseRef = 'integration',

  # Remote name
  [string]$Remote = 'origin',

  # Name of the new PR branch to create
  [string]$BranchName,

  # Commit message for the selective changes
  [string]$CommitMessage,

  # Push branch to remote
  [switch]$Push,

  # Create PR using GitHub CLI (gh)
  [switch]$OpenPr,

  # Keep the temporary worktree directory (for debugging)
  [switch]$KeepWorktree,

  # Only print planned actions; don’t modify anything
  [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Git {
  param(
    [Parameter(Mandatory = $true)]
    [string[]]$Args,
    [string]$WorkingDirectory
  )

  $render = ($Args | ForEach-Object {
      if ($_ -match '\s') { '"' + ($_ -replace '"', '\\"') + '"' } else { $_ }
    }) -join ' '

  if ($WorkingDirectory) {
    Write-Host "git $render  (cwd: $WorkingDirectory)"
  } else {
    Write-Host "git $render"
  }

  if ($DryRun) {
    return ''
  }

  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    if ($WorkingDirectory) {
      $lines = & git -C $WorkingDirectory @Args 2>&1
    } else {
      $lines = & git @Args 2>&1
    }
    $output = ($lines | ForEach-Object { "$_" }) -join "`n"
  }
  finally {
    $ErrorActionPreference = $prevEap
  }

  if ($LASTEXITCODE -ne 0) {
    throw "git failed ($LASTEXITCODE): git $render`n$output"
  }

  return $output
}

function Require-Command {
  param([Parameter(Mandatory = $true)][string]$Name)
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Required command not found: $Name"
  }
}

function Get-RepoRoot {
  $root = (& git rev-parse --show-toplevel 2>$null)
  if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($root)) {
    throw 'Not inside a git repository.'
  }
  return $root.Trim()
}

function Assert-CleanWorkingTree {
  param([Parameter(Mandatory = $true)][string]$RepoRoot)

  if ($DryRun) {
    Write-Host '(dry-run) skipping clean working tree check'
    return
  }

  $status = & git -C $RepoRoot status --porcelain -uall 2>$null
  if ($LASTEXITCODE -ne 0) {
    throw 'Failed to check git status.'
  }

  $statusText = ($status | Out-String).Trim()
  if (-not [string]::IsNullOrWhiteSpace($statusText)) {
    throw "Working tree is not clean. Commit/stash/revert changes (including untracked files) before running this script.\n\n$statusText"
  }
}

function Get-PathList {
  param([Parameter(Mandatory = $true)][string]$File)

  if (-not (Test-Path -LiteralPath $File)) {
    throw "Paths file not found: $File"
  }

  $lines = Get-Content -LiteralPath $File -ErrorAction Stop
  $paths = @()
  foreach ($line in $lines) {
    $safeLine = if ($null -eq $line) { '' } else { [string]$line }
    $trimmed = $safeLine.Trim()
    if ([string]::IsNullOrWhiteSpace($trimmed)) { continue }
    if ($trimmed.StartsWith('#')) { continue }
    $paths += $trimmed
  }

  if ($paths.Count -eq 0) {
    throw "No paths found in $File"
  }

  return $paths
}

function Ensure-RefExists {
  param(
    [Parameter(Mandatory = $true)][string]$Ref,
    [string]$Label
  )

  $labelText = if ($Label) { $Label } else { $Ref }

  if ($DryRun) {
    Write-Host "(dry-run) verifying ref exists: $labelText ($Ref)"
    return
  }

  & git rev-parse --verify "$Ref^{commit}" *> $null
  if ($LASTEXITCODE -ne 0) {
    throw "Git ref not found or not a commit: $labelText ($Ref)"
  }
}

function Resolve-Ref {
  param(
    [Parameter(Mandatory = $true)][string]$Ref,
    [Parameter(Mandatory = $true)][string]$Remote,
    [string]$Label
  )

  if ($DryRun) {
    return $Ref
  }

  & git rev-parse --verify "$Ref^{commit}" *> $null
  if ($LASTEXITCODE -eq 0) {
    return $Ref
  }

  $remoteCandidate = "$Remote/$Ref"
  & git rev-parse --verify "$remoteCandidate^{commit}" *> $null
  if ($LASTEXITCODE -eq 0) {
    return $remoteCandidate
  }

  $labelText = if ($Label) { $Label } else { $Ref }
  throw "Git ref not found (tried '$Ref' and '$remoteCandidate'): $labelText"
}

function Assert-PathsExistInRef {
  param(
    [Parameter(Mandatory = $true)][string]$Ref,
    [Parameter(Mandatory = $true)][string[]]$Paths
  )

  if ($DryRun) {
    Write-Host "(dry-run) verifying paths exist in $Ref"
    return
  }

  $missing = @()
  foreach ($p in $Paths) {
    # For both files and directories, ls-tree will return matches if they exist.
    $out = & git ls-tree -r --name-only $Ref -- $p 2>$null
    $outText = ($out | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($outText)) {
      $missing += $p
    }
  }

  if ($missing.Count -gt 0) {
    $msg = "These paths were not found in '$Ref':`n- " + ($missing -join "`n- ")
    throw $msg
  }
}

Require-Command git
$repoRoot = Get-RepoRoot
Assert-CleanWorkingTree -RepoRoot $repoRoot

$pathsFileFull = if ([System.IO.Path]::IsPathRooted($PathsFile)) { $PathsFile } else { Join-Path $repoRoot $PathsFile }
$paths = Get-PathList -File $pathsFileFull

if (-not $BranchName) {
  $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $BranchName = "pr/$BaseRef-selective-$timestamp"
}

# Worktree dir under %TEMP% to avoid polluting the repo
$safeBranchForPath = ($BranchName -replace '[\\/:*?"<>|]', '-')
$worktreeDir = Join-Path $env:TEMP (Join-Path 'haal-ide-worktrees' $safeBranchForPath)

Write-Host "Repo root: $repoRoot"
Write-Host "Paths file: $pathsFileFull"
Write-Host "SourceRef: $SourceRef"
Write-Host "BaseRef: $BaseRef (remote: $Remote)"
Write-Host "PR branch: $BranchName"
Write-Host "Worktree: $worktreeDir"
Write-Host "Selected paths:" 
$paths | ForEach-Object { Write-Host "- $_" }

Invoke-Git -Args @('fetch', $Remote)

$resolvedSourceRef = Resolve-Ref -Ref $SourceRef -Remote $Remote -Label 'SourceRef'
$resolvedBaseRef = Resolve-Ref -Ref $BaseRef -Remote $Remote -Label 'BaseRef'

Assert-PathsExistInRef -Ref $resolvedSourceRef -Paths $paths

# Create the worktree + branch based on remote base
if (-not (Test-Path -LiteralPath $worktreeDir)) {
  if (-not $DryRun) {
    New-Item -ItemType Directory -Path $worktreeDir -Force | Out-Null
  } else {
    Write-Host "(dry-run) mkdir $worktreeDir"
  }
}

Invoke-Git -Args @('worktree', 'add', '-B', $BranchName, $worktreeDir, $resolvedBaseRef)

try {
  # Copy only the requested paths from source into this worktree
  Invoke-Git -Args (@('restore', "--source=$resolvedSourceRef", '--') + $paths) -WorkingDirectory $worktreeDir

  # Stage only those paths
  Invoke-Git -Args (@('add', '-f', '--') + $paths) -WorkingDirectory $worktreeDir

  $status = if ($DryRun) { '' } else { (& git -C $worktreeDir status -sb | Out-String) }
  if (-not $DryRun) {
    Write-Host $status
  }

  if (-not $CommitMessage) {
    if ($DryRun) {
      $CommitMessage = "chore: Selective sync to $BaseRef"
    } else {
      $CommitMessage = Read-Host -Prompt 'Enter commit message for the selective PR'
    }
  }

  if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
    throw 'Commit message cannot be empty.'
  }

  # Commit (will fail if nothing staged)
  Invoke-Git -Args @('commit', '-m', $CommitMessage) -WorkingDirectory $worktreeDir

  if ($Push) {
    Invoke-Git -Args @('push', '-u', $Remote, $BranchName) -WorkingDirectory $worktreeDir
  }

  if ($OpenPr) {
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
      throw "OpenPr requested but 'gh' (GitHub CLI) is not installed or not on PATH. Install it or run without -OpenPr."
    }

    if (-not $Push) {
      throw 'OpenPr requested but branch was not pushed. Re-run with -Push -OpenPr.'
    }

    # Title defaults to first line of commit message
    $title = ($CommitMessage -split "`r?`n")[0]
    $body = "Selective PR: copy listed paths from '$resolvedSourceRef' into '$BaseRef'."

    Write-Host "gh pr create --base $BaseRef --head $BranchName"
    if (-not $DryRun) {
      & gh pr create --base $BaseRef --head $BranchName --title $title --body $body
      if ($LASTEXITCODE -ne 0) {
        throw "gh pr create failed ($LASTEXITCODE)"
      }
    }
  }

  Write-Host 'Done.'
}
finally {
  if (-not $KeepWorktree) {
    Invoke-Git -Args @('worktree', 'remove', '--force', $worktreeDir)
  } else {
    Write-Host "Kept worktree at: $worktreeDir"
  }
}
