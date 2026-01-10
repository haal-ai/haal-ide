#!/usr/bin/env pwsh
<#
.SYNOPSIS
    OLAF Repository Installer
.DESCRIPTION
    Installs OLAF framework components from global ~/.olaf to current repository
    with selective copying based on specified requirements.
.PARAMETER SourceOlauf
    Path to global OLAF installation (default: ~/.olaf)
.PARAMETER Force
    Overwrite existing files
#>

param(
    [string]$SourceOlauf = "$env:USERPROFILE\.olaf",
    [switch]$Force
)

# Error handling
$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

function Test-SourcePath {
    if (-not (Test-Path $SourceOlauf)) {
        Write-Log "Source OLAF path not found: $SourceOlauf" "ERROR"
        exit 1
    }
    Write-Log "Source OLAF path found: $SourceOlauf"
}

function Initialize-TargetStructure {
    Write-Log "Initializing target OLAF structure..."
    
    # Create .olaf directory structure
    $targetDirs = @(
        ".olaf",
        ".olaf\core",
        ".olaf\core\competencies",
        ".olaf\core\reference"
    )
    
    foreach ($dir in $targetDirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Log "Created directory: $dir"
        }
    }
}

function Copy-OlaufCoreCompetencies {
    Write-Log "Copying OLAF core competencies..."
    
    $sourceCompetencies = Join-Path $SourceOlauf "core\competencies"
    $targetCompetencies = ".olaf\core\competencies"
    
    if (Test-Path $sourceCompetencies) {
        # Copy only team competency manifest.json files
        Get-ChildItem -Path $sourceCompetencies -Directory | ForEach-Object {
            $competencyDir = $_
            $targetDir = Join-Path $targetCompetencies $competencyDir.Name
            
            # Create competency directory if it doesn't exist
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                Write-Log "Created competency directory: $targetDir"
            }
            
            # Copy only manifest.json if it doesn't exist or Force is specified
            $manifestFile = Join-Path $competencyDir.FullName "competency-manifest.json"
            $targetManifest = Join-Path $targetDir "competency-manifest.json"
            
            if ((Test-Path $manifestFile) -and (-not (Test-Path $targetManifest) -or $Force)) {
                Copy-Item -Path $manifestFile -Destination $targetManifest -Force
                Write-Log "Copied competency manifest: $($competencyDir.Name)"
            }
        }
    }
}

function Copy-OlaufCoreReference {
    Write-Log "Copying OLAF core reference..."
    
    $sourceReference = Join-Path $SourceOlauf "core\reference"
    $targetReference = ".olaf\core\reference"
    
    if (Test-Path $sourceReference) {
        # Copy only query-competency-index.md if it doesn't exist
        $queryIndex = Join-Path $sourceReference "query-competency-index.md"
        $targetQueryIndex = Join-Path $targetReference "query-competency-index.md"
        
        if ((Test-Path $queryIndex) -and (-not (Test-Path $targetQueryIndex) -or $Force)) {
            Copy-Item -Path $queryIndex -Destination $targetQueryIndex -Force
            Write-Log "Copied query-competency-index.md"
        }
    }
}

function Copy-OlaufData {
    Write-Log "Copying OLAF data subfolders..."
    
    $sourceData = Join-Path $SourceOlauf "data"
    $targetData = ".olaf\data"
    
    if (Test-Path $sourceData) {
        # Create data directory if it doesn't exist
        if (-not (Test-Path $targetData)) {
            New-Item -ItemType Directory -Path $targetData -Force | Out-Null
        }
        
        # Copy all subfolders
        Get-ChildItem -Path $sourceData -Directory | ForEach-Object {
            $sourceSubDir = $_
            $targetSubDir = Join-Path $targetData $sourceSubDir.Name
            
            if (-not (Test-Path $targetSubDir) -or $Force) {
                Copy-Item -Path $sourceSubDir.FullName -Destination $targetSubDir -Recurse -Force
                Write-Log "Copied data subfolder: $($sourceSubDir.Name)"
            }
        }
    }
}

function Copy-OlaufWork {
    Write-Log "Copying OLAF work contents..."
    
    $sourceWork = Join-Path $SourceOlauf "work"
    $targetWork = ".olaf\work"
    
    if (Test-Path $sourceWork) {
        # Create work directory if it doesn't exist
        if (-not (Test-Path $targetWork)) {
            New-Item -ItemType Directory -Path $targetWork -Force | Out-Null
        }
        
        # Copy all contents
        Get-ChildItem -Path $sourceWork | ForEach-Object {
            $sourceItem = $_
            $targetItem = Join-Path $targetWork $sourceItem.Name
            
            if (-not (Test-Path $targetItem) -or $Force) {
                Copy-Item -Path $sourceItem.FullName -Destination $targetItem -Recurse -Force
                Write-Log "Copied work item: $($sourceItem.Name)"
            }
        }
    }
}

function Copy-OlaufGithubFiles {
    Write-Log "Copying GitHub olaf- prefixed files..."
    
    $githubDirs = @(
        ".github\instructions",
        ".github\prompts"
    )
    
    foreach ($dir in $githubDirs) {
        if (Test-Path $dir) {
            Get-ChildItem -Path $dir -File | Where-Object { $_.Name -like "olaf-*" } | ForEach-Object {
                $sourceFile = $_.FullName
                # Files are already in place, just log them
                Write-Log "GitHub olaf file exists: $($_.Name)"
            }
        }
    }
}

function Copy-OlaufWindsurfFiles {
    Write-Log "Copying Windsurf olaf- prefixed files..."
    
    $windsurfDirs = @(
        ".windsurf\rules",
        ".windsurf\workflows"
    )
    
    foreach ($dir in $windsurfDirs) {
        if (Test-Path $dir) {
            Get-ChildItem -Path $dir -File | Where-Object { $_.Name -like "olaf-*" } | ForEach-Object {
                $sourceFile = $_.FullName
                # Files are already in place, just log them
                Write-Log "Windsurf olaf file exists: $($_.Name)"
            }
        }
    }
}

function Copy-OlaufKiroFiles {
    Write-Log "Copying Kiro olaf- prefixed files..."
    
    $kiroDirs = @(
        ".kiro\hooks",
        ".kiro\steering"
    )
    
    foreach ($dir in $kiroDirs) {
        if (Test-Path $dir) {
            Get-ChildItem -Path $dir -File | Where-Object { $_.Name -like "olaf-*" } | ForEach-Object {
                $sourceFile = $_.FullName
                # Files are already in place, just log them
                Write-Log "Kiro olaf file exists: $($_.Name)"
            }
        }
    }
}

function Invoke-SelectCollection {
    Write-Log "Launching select-collection.py..."
    
    # Look for select-collection.py in global ~/.olaf/tools directory
    $selectCollectionScript = Join-Path $SourceOlauf "tools\select-collection.py"
    
    if (Test-Path $selectCollectionScript) {
        try {
            Write-Log "Found select-collection.py at: $selectCollectionScript"
            Write-Log "Launching select-collection.py..."
            
            # Launch the Python script
            & python $selectCollectionScript
            
            if ($LASTEXITCODE -eq 0) {
                Write-Log "select-collection.py completed successfully" "SUCCESS"
            } else {
                Write-Log "select-collection.py exited with code: $LASTEXITCODE" "WARNING"
            }
        }
        catch {
            Write-Log "Failed to launch select-collection.py: $($_.Exception.Message)" "ERROR"
        }
    }
    else {
        Write-Log "select-collection.py not found at: $selectCollectionScript" "WARNING"
        Write-Log "Skipping select-collection.py launch"
    }
}

# Main execution
try {
    Write-Log "Starting OLAF Repository Installer..."
    Write-Log "Source: $SourceOlauf"
    Write-Log "Target: $(Get-Location)"
    
    Test-SourcePath
    Initialize-TargetStructure
    Copy-OlaufCoreCompetencies
    Copy-OlaufCoreReference
    Copy-OlaufData
    Copy-OlaufWork
    Copy-OlaufGithubFiles
    Copy-OlaufWindsurfFiles
    Copy-OlaufKiroFiles
    
    Write-Log "OLAF Repository Installer completed successfully!" "SUCCESS"
    
    # Launch select-collection.py after installation
    Invoke-SelectCollection
}
catch {
    Write-Log "Installer failed: $($_.Exception.Message)" "ERROR"
    exit 1
}
