# =========================================================
# VS Code Custom Agents Installer
# Install agents from git cloud to any project
# =========================================================
# Usage:
#   .\install-agents.ps1 -RepoUrl "https://github.com/user/repo.git" -TargetDir ".github"
#   .\install-agents.ps1 -RepoUrl "https://github.com/user/repo.git" -AgentsOnly
# =========================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl,
    
    [string]$TargetDir = ".github",
    
    [switch]$AgentsOnly,
    
    [switch]$SkillsOnly,
    
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

function Install-AgentsFromGit {
    param(
        [string]$Url,
        [string]$Target,
        [string]$BranchName
    )
    
    # Create temp directory for cloning
    $tempDir = Join-Path $env:TEMP "vscode-agents-temp-$(Get-Random)"
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
    
    try {
        Write-Host "📥 Cloning repository..." -ForegroundColor Cyan
        
        # Shallow clone for speed
        git clone --depth 1 --branch $BranchName $Url $tempDir
        
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
        $targetPath = $Target
        if (-not (Test-Path $targetPath)) {
            New-Item -ItemType Directory -Force -Path $targetPath | Out-Null
        }
        
        # Copy agents
        $sourceAgents = Join-Path $sourceRoot "agents"
        $targetAgents = Join-Path $targetPath "agents"
        
        if ((Test-Path $sourceAgents) -and (-not $SkillsOnly) -and (-not $AgentsOnly) -or $AgentsOnly) {
            Write-Host "📁 Installing agents..." -ForegroundColor Cyan
            
            # Backup existing agents
            if (Test-Path $targetAgents) {
                $backupPath = "$targetAgents.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
                Write-Host "⚠️  Backing up existing agents to $backupPath" -ForegroundColor Yellow
                Rename-Item -Path $targetAgents -NewName (Split-Path $backupPath -Leaf)
            }
            
            Copy-Item -Path $sourceAgents -Destination $targetPath -Recurse -Force
            Write-Host "✅ Agents installed!" -ForegroundColor Green
        }
        
        # Copy agents.minimal
        $sourceMinimal = Join-Path $sourceRoot "agents.minimal"
        $targetMinimal = Join-Path $targetPath "agents.minimal"
        
        if ((Test-Path $sourceMinimal) -and (-not $SkillsOnly) -and (-not $AgentsOnly) -or $AgentsOnly) {
            Write-Host "📁 Installing agents.minimal..." -ForegroundColor Cyan
            
            if (Test-Path $targetMinimal) {
                Remove-Item -Path $targetMinimal -Recurse -Force
            }
            
            Copy-Item -Path $sourceMinimal -Destination $targetPath -Recurse -Force
            Write-Host "✅ agents.minimal installed!" -ForegroundColor Green
        }
        
        # Copy skills
        $sourceSkills = Join-Path $sourceRoot "skills"
        $targetSkills = Join-Path $targetPath "skills"
        
        if ((Test-Path $sourceSkills) -and (-not $AgentsOnly) -and (-not $SkillsOnly) -or $SkillsOnly) {
            Write-Host "📁 Installing skills..." -ForegroundColor Cyan
            
            if (Test-Path $targetSkills) {
                Remove-Item -Path $targetSkills -Recurse -Force
            }
            
            Copy-Item -Path $sourceSkills -Destination $targetPath -Recurse -Force
            Write-Host "✅ Skills installed!" -ForegroundColor Green
        }
        
        Write-Host ""
        Write-Host "🎉 Installation complete!" -ForegroundColor Green
        Write-Host "   Agents: $targetAgents" -ForegroundColor Gray
        
    }
    finally {
        # Cleanup temp directory
        if (Test-Path $tempDir) {
            Remove-Item -Path $tempDir -Recurse -Force
        }
    }
}

# Run installation
Install-AgentsFromGit -Url $RepoUrl -Target $TargetDir -BranchName $Branch
