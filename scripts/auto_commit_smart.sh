#!/bin/bash
# 自动提交脚本（只commit，不push）
# 使用方法：./scripts/auto_commit_smart.sh

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 检查是否有未提交的更改
if ! git status --porcelain | grep -q .; then
    echo "✅ 没有需要提交的更改"
    exit 0
fi

# 生成智能commit message
CHANGED_FILES=$(git status --porcelain | wc -l)
CHANGED_PATHS=$(git status --porcelain | head -5 | awk '{print $2}' | tr '\n' ' ')

# 根据文件类型生成commit message
if echo "$CHANGED_PATHS" | grep -q "code_library"; then
    TYPE="feat"
    MSG="代码库更新"
elif echo "$CHANGED_PATHS" | grep -q "\.md$"; then
    TYPE="docs"
    MSG="文档更新"
elif echo "$CHANGED_PATHS" | grep -q "scripts"; then
    TYPE="chore"
    MSG="脚本更新"
else
    TYPE="chore"
    MSG="代码更新"
fi

COMMIT_MSG="${TYPE}: ${MSG} (${CHANGED_FILES} 个文件)"

# 添加所有更改
git add -A

# 提交
git commit -m "$COMMIT_MSG"

echo "✅ 已提交: $COMMIT_MSG"
echo "📝 提示: 使用 'git push' 手动推送，或积累多个提交后批量推送"
