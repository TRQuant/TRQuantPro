#!/bin/bash
# 安全的文件恢复脚本 - 在恢复前自动备份
set -e

echo "⚠️  安全恢复脚本 - 会在恢复前自动备份"
echo ""

# 检查是否有未提交的更改
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "检测到未提交的更改，正在自动备份..."
    BACKUP_NAME="backup_before_restore_$(date '+%Y%m%d_%H%M%S')"
    git stash push -m "$BACKUP_NAME"
    echo "✅ 已保存到stash: $BACKUP_NAME"
    echo "   恢复命令: git stash show -p stash@{0}"
    echo ""
fi

# 执行恢复
echo "执行恢复操作..."
git restore "$@"
echo "✅ 恢复完成"
echo ""
echo "如果需要恢复备份，运行:"
echo "  git stash list  # 查看备份列表"
echo "  git stash show -p stash@{0}  # 查看最新备份内容"
echo "  git stash apply stash@{0}  # 应用最新备份"
