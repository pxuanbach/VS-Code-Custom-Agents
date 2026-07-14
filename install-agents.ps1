# =========================================================
# VS Code Custom Agents Installer
# Install agents and skills from source repository
# Source: https://github.com/pxuanbach/VS-Code-Custom-Agents
# =========================================================
# Usage:
#   .\install-agents.ps1
# =========================================================

$ErrorActionPreference = "Stop"

# Source repository (hardcoded - this repo)
$SourceRepo = "https://github.com/pxuanbach/VS-Code-Custom-Agents.git"
$SourceBranch = "main"

# Target directory (current directory's .github)
$TargetDir = ".github"

Write-Host "📥 Cloning agents repository..." -ForegroundColor Cyan

# Create temp directory for cloning
$tempDir = Join-Path $env:TEMP "vscode-agents-temp-$(Get-Random)"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

try {
    # Shallow clone for speed
    git clone --depth 1 --branch $SourceBranch $SourceRepo $tempDir
    
    if ($LASTEXITCODE -ne 0) {
        throw "Git clone failed"
    }
    
    Write-Host "✅ Clone successful!" -ForegroundColor Green
    
    # Source directory in cloned repo
    $sourceRoot = Join-Path $tempDir ".github"
    
    if (-not (Test-Path $sourceRoot)) {
        throw "Repository does not have .github directory"
    }
    
    # Create target directory if not exists
    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
    }
    
    # Copy agents
    $sourceAgents = Join-Path $sourceRoot "agents"
    $targetAgents = Join-Path $TargetDir "agents"
    
    if (Test-Path $sourceAgents) {
        Write-Host "📁 Installing agents..." -ForegroundColor Cyan
        
        # Backup existing agents
        if (Test-Path $targetAgents) {
            $backupPath = "$targetAgents.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
            Write-Host "⚠️  Backing up existing agents to $backupPath" -ForegroundColor Yellow
            Rename-Item -Path $targetAgents -NewName (Split-Path $backupPath -Leaf)
        }
        
        Copy-Item -Path $sourceAgents -Destination $TargetDir -Recurse -Force
        Write-Host "✅ Agents installed!" -ForegroundColor Green
    }
    
    # Copy agents.minimal
    $sourceMinimal = Join-Path $sourceRoot "agents.minimal"
    $targetMinimal = Join-Path $TargetDir "agents.minimal"
    
    if (Test-Path $sourceMinimal) {
        Write-Host "📁 Installing agents.minimal..." -ForegroundColor Cyan
        
        if (Test-Path $targetMinimal) {
            Remove-Item -Path $targetMinimal -Recurse -Force
        }
        
        Copy-Item -Path $sourceMinimal -Destination $TargetDir -Recurse -Force
        Write-Host "✅ agents.minimal installed!" -ForegroundColor Green
    }
    
    # Copy skills
    $sourceSkills = Join-Path $sourceRoot "skills"
    $targetSkills = Join-Path $TargetDir "skills"
    
    if (Test-Path $sourceSkills) {
        Write-Host "📁 Installing skills..." -ForegroundColor Cyan
        
        if (Test-Path $targetSkills) {
            Remove-Item -Path $targetSkills -Recurse -Force
        }
        
        Copy-Item -Path $sourceSkills -Destination $TargetDir -Recurse -Force
        Write-Host "✅ Skills installed!" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "🎉 Installation complete!" -ForegroundColor Green
    Write-Host "   Target: $TargetDir" -ForegroundColor Gray
    
}
finally {
    # Cleanup temp directory
    if (Test-Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force
    }
}
