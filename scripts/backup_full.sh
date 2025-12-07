#!/bin/bash
# TRQuant 完整备份脚本
# 创建项目完整备份到 .backups 目录

set -e

# 获取项目根目录（脚本所在目录的父目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "💾 TRQuant 完整备份"
echo "=========================================="
echo "项目根目录: $PROJECT_ROOT"
echo ""

# 创建备份目录
BACKUP_DIR="$PROJECT_ROOT/.backups"
mkdir -p "$BACKUP_DIR"

# 生成备份时间戳
BACKUP_TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%S-%3N")
BACKUP_NAME="backup-${BACKUP_TIMESTAMP}"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

echo "📁 创建备份目录: $BACKUP_PATH"
mkdir -p "$BACKUP_PATH"

# 创建备份信息文件
cat > "$BACKUP_PATH/backup-info.json" << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")",
  "projectRoot": "$PROJECT_ROOT",
  "backupPath": "$BACKUP_PATH",
  "backupType": "full",
  "description": "完整系统备份 - 主工作台和桌面系统修复后"
}
EOF

echo "📋 备份信息已创建"
echo ""

# 需要排除的目录和文件模式
EXCLUDE_PATTERNS=(
    "--exclude=node_modules"
    "--exclude=.git"
    "--exclude=.backups"
    "--exclude=venv"
    "--exclude=__pycache__"
    "--exclude=.pytest_cache"
    "--exclude=.vscode"
    "--exclude=.cursor"
    "--exclude=*.pyc"
    "--exclude=*.pyo"
    "--exclude=*.log"
    "--exclude=dist"
    "--exclude=build"
    "--exclude=*.vsix"
    "--exclude=.DS_Store"
    "--exclude=*.swp"
    "--exclude=*.swo"
    "--exclude=*~"
)

echo "🔄 开始复制文件..."
echo ""

# 使用 rsync 进行备份（如果可用）
if command -v rsync &> /dev/null; then
    echo "使用 rsync 进行备份..."
    rsync -av --progress \
        "${EXCLUDE_PATTERNS[@]}" \
        "$PROJECT_ROOT/" \
        "$BACKUP_PATH/" \
        --exclude-from=<(find "$PROJECT_ROOT" -name ".gitignore" -exec cat {} \; 2>/dev/null | grep -v "^#" | grep -v "^$" | sed 's|^|--exclude=|')
else
    echo "使用 cp 进行备份（rsync 不可用）..."
    # 创建临时排除列表
    EXCLUDE_FILE=$(mktemp)
    cat > "$EXCLUDE_FILE" << 'EXCLUDES'
node_modules
.git
.backups
venv
__pycache__
.pytest_cache
.vscode
.cursor
*.pyc
*.pyo
*.log
dist
build
*.vsix
.DS_Store
*.swp
*.swo
*~
EXCLUDES
    
    # 使用 find 和 cp 进行备份
    cd "$PROJECT_ROOT"
    find . -type f ! -path "*/node_modules/*" \
        ! -path "*/.git/*" \
        ! -path "*/.backups/*" \
        ! -path "*/venv/*" \
        ! -path "*/__pycache__/*" \
        ! -path "*/.pytest_cache/*" \
        ! -path "*/.vscode/*" \
        ! -path "*/.cursor/*" \
        ! -name "*.pyc" \
        ! -name "*.pyo" \
        ! -name "*.log" \
        ! -path "*/dist/*" \
        ! -path "*/build/*" \
        ! -name "*.vsix" \
        ! -name ".DS_Store" \
        ! -name "*.swp" \
        ! -name "*.swo" \
        ! -name "*~" | while read -r file; do
        target_file="$BACKUP_PATH/$file"
        target_dir=$(dirname "$target_file")
        mkdir -p "$target_dir"
        cp "$file" "$target_file"
    done
    
    rm -f "$EXCLUDE_FILE"
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo "备份位置: $BACKUP_PATH"
echo "备份时间: $(date)"
echo ""
echo "备份内容:"
du -sh "$BACKUP_PATH" 2>/dev/null || echo "无法计算大小"
echo ""
echo "备份信息:"
cat "$BACKUP_PATH/backup-info.json"
echo ""
























