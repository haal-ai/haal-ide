[CmdletBinding()]
param(
  [string]$RepoUrl,
  [string]$Branch,
  [string]$SourceOlauf = "$env:USERPROFILE\.olaf",
  [switch]$Force
)

$ErrorActionPreference = 'Stop'

function Write-Log {
  param([string]$Message, [string]$Level = 'INFO')
  $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  Write-Host "[$timestamp] [$Level] $Message"
}

function Get-RepoRoot {
  $root = (& git rev-parse --show-toplevel 2>$null)
  if ($LASTEXITCODE -eq 0 -and $root) {
    return $root.Trim()
  }
  return (Resolve-Path (Join-Path $PSScriptRoot '..\\..')).Path
}

function Get-ConfigDefaults {
  param([string]$RepoRoot)

  $configPath = Join-Path $RepoRoot '_olaf-config.json'
  if (-not (Test-Path -LiteralPath $configPath)) {
    $configPath = Join-Path $RepoRoot 'olaf-config.json'
  }
  if (-not (Test-Path -LiteralPath $configPath)) {
    return @{}
  }

  try {
    return (Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json)
  } catch {
    return @{}
  }
}

function Get-RawBaseUrl {
  param(
    [Parameter(Mandatory = $true)][string]$RepoUrl,
    [Parameter(Mandatory = $true)][string]$Branch
  )

  $repoUrlTrim = $RepoUrl.TrimEnd('/')

  if ($repoUrlTrim -match '^https://github.com/(?<org>[^/]+)/(?<repo>[^/]+)$') {
    return "https://raw.githubusercontent.com/$($Matches.org)/$($Matches.repo)/$Branch"
  }

  throw "Unsupported RepoUrl format for raw downloads: $RepoUrl"
}

function Get-OwnerRepo {
  param([Parameter(Mandatory = $true)][string]$RepoUrl)

  $repoUrlTrim = $RepoUrl.TrimEnd('/')
  if ($repoUrlTrim -match '^https://github.com/(?<org>[^/]+)/(?<repo>[^/]+)$') {
    return "$($Matches.org)/$($Matches.repo)"
  }

  throw "Unsupported RepoUrl format for owner/repo: $RepoUrl"
}

function Invoke-FileDownload {
  param(
    [Parameter(Mandatory = $true)][string]$Url,
    [Parameter(Mandatory = $true)][string]$OutFile
  )

  Write-Log "Downloading: $Url"
  Invoke-WebRequest -Uri $Url -OutFile $OutFile -UseBasicParsing
}

$repoRoot = Get-RepoRoot
$config = Get-ConfigDefaults -RepoRoot $repoRoot

if (-not $RepoUrl) {
  $RepoUrl = $config.'registry-repo'
}
if (-not $RepoUrl) {
  $RepoUrl = 'https://github.com/haal-ai/haal-ide'
}

if (-not $Branch) {
  $Branch = $config.branch
}
if (-not $Branch) {
  $Branch = 'main'
}

Write-Log "Repo root: $repoRoot"
Write-Log "Source repo: $RepoUrl@$Branch"

$rawBase = Get-RawBaseUrl -RepoUrl $RepoUrl -Branch $Branch
$ownerRepo = Get-OwnerRepo -RepoUrl $RepoUrl

$tempDir = Join-Path $env:TEMP (Join-Path 'olaf-init' ([Guid]::NewGuid().ToString('N')))
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

$installerPath = Join-Path $tempDir 'install_olaf.py'
$selectCollectionPath = Join-Path $tempDir 'select-collection.py'

try {
  if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python not found on PATH. Install Python 3.12+ and retry."
  }

  Invoke-FileDownload -Url "$rawBase/.olaf/tools/install_olaf.py" -OutFile $installerPath
  Invoke-FileDownload -Url "$rawBase/.olaf/tools/select-collection.py" -OutFile $selectCollectionPath

  Write-Log 'Running installer (install_olaf.py)...'
  & python $installerPath --repo $ownerRepo --branch $Branch --target $SourceOlauf --local $repoRoot
  if ($LASTEXITCODE -ne 0) {
    throw "install_olaf.py failed ($LASTEXITCODE)"
  }

  Write-Log 'Running select-collection...'
  & python $selectCollectionPath
  if ($LASTEXITCODE -ne 0) {
    throw "select-collection.py failed ($LASTEXITCODE)"
  }

  Write-Log 'Done.' 'SUCCESS'
}
finally {
  if (Test-Path -LiteralPath $tempDir) {
    Remove-Item -LiteralPath $tempDir -Recurse -Force -ErrorAction SilentlyContinue
  }
}
