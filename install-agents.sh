#!/bin/bash
# =========================================================
# VS Code Custom Agents Installer
# Install agents and skills from source repository
# Source: https://github.com/pxuanbach/VS-Code-Custom-Agents
# =========================================================
# Usage:
#   ./install-agents.sh
# =========================================================

set -e

# Source repository (hardcoded - this repo)
SOURCE_REPO="https://github.com/pxuanbach/VS-Code-Custom-Agents.git"
SOURCE_BRANCH="main"

# Target directory (current directory's .github)
TARGET_DIR=".github"

# Create temp directory for cloning
TEMP_DIR=$(mktemp -d)
TEMP_DIR="$TEMP_DIR/vscode-agents-temp-$$"

echo "📥 Cloning agents repository..."
echo "   URL: $SOURCE_REPO"
echo "   Branch: $SOURCE_BRANCH"

# Clone into temp directory (shallow clone for speed)
git clone --depth 1 --branch "$SOURCE_BRANCH" "$SOURCE_REPO" "$TEMP_DIR"

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

# Install all (agents, agents.minimal, skills)
install_agents
install_agents_minimal
install_skills

echo ""
echo "🎉 Installation complete!"
echo "   Target: $TARGET_DIR"

# Cleanup temp directory
rm -rf "$TEMP_DIR"
