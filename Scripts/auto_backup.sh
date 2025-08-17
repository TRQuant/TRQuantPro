#!/bin/bash
# 自动备份脚本
# 用法: ./auto_backup.sh [backup_name]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 获取备份名称
BACKUP_NAME=${1:-"backup_$(date +%Y%m%d_%H%M%S)"}
BACKUP_DIR="backups/$BACKUP_NAME"

print_info "开始自动备份: $BACKUP_NAME"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 1. Git提交当前更改
print_info "1. 提交Git更改..."
if python3 Scripts/git_manager.py status | grep -q "修改的文件"; then
    python3 Scripts/git_manager.py auto-commit --force
    print_success "Git提交完成"
else
    print_info "没有需要提交的更改"
fi

# 2. 创建Git备份分支
print_info "2. 创建Git备份分支..."
python3 Scripts/git_manager.py backup-branch --message "$BACKUP_NAME"
print_success "Git备份分支创建完成"

# 3. 备份重要配置文件
print_info "3. 备份重要配置文件..."
IMPORTANT_FILES=(
    "config.json"
    "lean.json"
    "qc.code-workspace"
    "QuantConnect_Research_Start.md"
    "Scripts/README.md"
)

for file in "${IMPORTANT_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/"
        print_success "备份: $file"
    else
        print_warning "文件不存在: $file"
    fi
done

# 4. 备份脚本文件
print_info "4. 备份脚本文件..."
if [ -d "Scripts" ]; then
    cp -r Scripts "$BACKUP_DIR/"
    print_success "备份: Scripts目录"
fi

# 5. 备份笔记本（不包括输出）
print_info "5. 备份笔记本文件..."
find . -name "*.ipynb" -not -path "./backups/*" -not -path "./data/*" | while read -r notebook; do
    # 创建相对路径目录
    notebook_dir=$(dirname "$notebook")
    backup_notebook_dir="$BACKUP_DIR/notebooks/$notebook_dir"
    mkdir -p "$backup_notebook_dir"
    
    # 复制笔记本（清理输出）
    python3 Scripts/notebook_manager.py clean "$notebook" 2>/dev/null || true
    cp "$notebook" "$backup_notebook_dir/"
    print_success "备份: $notebook"
done

# 6. 生成备份报告
print_info "6. 生成备份报告..."
cat > "$BACKUP_DIR/backup_report.md" << EOF
# 备份报告

**备份时间**: $(date '+%Y-%m-%d %H:%M:%S')
**备份名称**: $BACKUP_NAME
**备份目录**: $BACKUP_DIR

## 备份内容

### 配置文件
$(for file in "${IMPORTANT_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "- $file"
    fi
done)

### 脚本文件
- Scripts/ (完整目录)

### 笔记本文件
$(find . -name "*.ipynb" -not -path "./backups/*" -not -path "./data/*" | wc -l) 个笔记本文件

## Git状态
\`\`\`
$(git status --porcelain 2>/dev/null || echo "Git状态获取失败")
\`\`\`

## 系统信息
- 操作系统: $(uname -s)
- 主机名: $(hostname)
- 用户: $(whoami)
- 工作目录: $(pwd)

## 恢复说明

1. 恢复配置文件:
   \`\`\`bash
   cp $BACKUP_DIR/config.json ./
   cp $BACKUP_DIR/lean.json ./
   cp $BACKUP_DIR/qc.code-workspace ./
   \`\`\`

2. 恢复脚本:
   \`\`\`bash
   cp -r $BACKUP_DIR/Scripts ./
   \`\`\`

3. 恢复笔记本:
   \`\`\`bash
   cp -r $BACKUP_DIR/notebooks/* ./
   \`\`\`

4. 恢复Git分支:
   \`\`\`bash
   git checkout $BACKUP_NAME
   \`\`\`
EOF

print_success "备份报告生成完成"

# 7. 压缩备份
print_info "7. 压缩备份文件..."
cd backups
tar -czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME"
rm -rf "$BACKUP_NAME"
print_success "备份压缩完成: ${BACKUP_NAME}.tar.gz"

# 8. 清理旧备份（保留最近5个）
print_info "8. 清理旧备份..."
BACKUP_COUNT=$(ls -1 *.tar.gz 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 5 ]; then
    ls -t *.tar.gz | tail -n +6 | xargs rm -f
    print_success "清理了 $((BACKUP_COUNT - 5)) 个旧备份"
fi

print_success "自动备份完成！"
print_info "备份文件: backups/${BACKUP_NAME}.tar.gz"
print_info "备份报告: backups/${BACKUP_NAME}/backup_report.md" 