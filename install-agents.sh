#!/bin/bash
# =========================================================
# VS Code Custom Agents Installer
# Install agents from git cloud to any project
# =========================================================
# Usage:
#   ./install-agents.sh --repo "https://github.com/user/repo.git" --target ".github"
#   ./install-agents.sh --repo "https://github.com/user/repo.git" --agents-only
#   ./install-agents.sh --repo "https://github.com/user/repo.git" --skills-only
# =========================================================

set -e

# Default values
TARGET_DIR=".github"
BRANCH="main"
AGENTS_ONLY=false
SKILLS_ONLY=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --repo)
            REPO_URL="$2"
            shift 2
            ;;
        --target)
            TARGET_DIR="$2"
            shift 2
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        --agents-only)
            AGENTS_ONLY=true
            shift
            ;;
        --skills-only)
            SKILLS_ONLY=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$REPO_URL" ]; then
    echo "Error: --repo is required"
    echo "Usage: $0 --repo <git-url> [--target <dir>] [--branch <branch>] [--agents-only] [--skills-only]"
    exit 1
fi

# Create temp directory for cloning
TEMP_DIR=$(mktemp -d)
TEMP_DIR="$TEMP_DIR/vscode-agents-temp-$$"

echo "📥 Cloning repository..."
echo "   URL: $REPO_URL"
echo "   Branch: $BRANCH"

# Clone into temp directory (shallow clone for speed)
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TEMP_DIR"

if [ $? -ne 0 ]; then
    echo "❌ Git clone failed"
    exit 1
fi

echo "✅ Clone successful!"

SOURCE_ROOT="$TEMP_DIR/.github"

# Check if .github exists in repo
if [ ! -d "$SOURCE_ROOT" ]; then
    echo "❌ Repository does not have .github directory"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Create target directory if not exists
mkdir -p "$TARGET_DIR"

# Install agents
install_agents() {
    local source="$SOURCE_ROOT/agents"
    local target="$TARGET_DIR/agents"
    
    if [ ! -d "$source" ]; then
        return
    fi
    
    echo "📁 Installing agents..."
    
    # Backup existing agents
    if [ -d "$target" ]; then
        backup_path="$target.backup.$(date +'%Y%m%d-%H%M%S')"
        echo "⚠️  Backing up existing agents to $backup_path"
        mv "$target" "$backup_path"
    fi
    
    cp -r "$source" "$TARGET_DIR/"
    echo "✅ Agents installed!"
}

# Install agents.minimal
install_agents_minimal() {
    local source="$SOURCE_ROOT/agents.minimal"
    local target="$TARGET_DIR/agents.minimal"
    
    if [ ! -d "$source" ]; then
        return
    fi
    
    echo "📁 Installing agents.minimal..."
    
    if [ -d "$target" ]; then
        rm -rf "$target"
    fi
    
    cp -r "$source" "$TARGET_DIR/"
    echo "✅ agents.minimal installed!"
}

# Install skills
install_skills() {
    local source="$SOURCE_ROOT/skills"
    local target="$TARGET_DIR/skills"
    
    if [ ! -d "$source" ]; then
        return
    fi
    
    echo "📁 Installing skills..."
    
    if [ -d "$target" ]; then
        rm -rf "$target"
    fi
    
    cp -r "$source" "$TARGET_DIR/"
    echo "✅ Skills installed!"
}

# Run installations based on flags
if [ "$AGENTS_ONLY" = true ]; then
    install_agents
    install_agents_minimal
elif [ "$SKILLS_ONLY" = true ]; then
    install_skills
else
    install_agents
    install_agents_minimal
    install_skills
fi

echo ""
echo "🎉 Installation complete!"
echo "   Agents: $TARGET_DIR/agents"

# Cleanup temp directory
rm -rf "$TEMP_DIR"
