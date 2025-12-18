#!/bin/bash
# 智能自动提交和推送脚本
# 用于轩辕剑灵自动执行commit和push

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# 检查是否有未提交的更改
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 没有变更需要提交"
    exit 0
fi

# 生成commit message
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
CHANGES=$(git status --short | head -5 | sed 's/^/  /' | tr '\n' '; ')

# 根据更改类型生成message
if git status --porcelain | grep -q "^A"; then
    TYPE="feat"
    DESC="添加新功能或文件"
elif git status --porcelain | grep -q "^M.*\.md$"; then
    TYPE="docs"
    DESC="更新文档"
elif git status --porcelain | grep -q "^M"; then
    TYPE="fix"
    DESC="修复或更新代码"
else
    TYPE="chore"
    DESC="更新配置或工具"
fi

COMMIT_MSG="${TYPE}: ${DESC} - ${TIMESTAMP}

自动提交更新
时间: ${TIMESTAMP}
更改摘要: ${CHANGES}"

# 添加所有更改
echo "📝 添加更改..."
git add -A

# 提交
echo "💾 提交更改..."
git commit -m "$COMMIT_MSG"

# 推送到TRQuantPro
echo "📤 推送到TRQuantPro..."
if git push trquantpro main-clean:main 2>&1; then
    echo "✅ 推送成功"
else
    echo "⚠️  推送失败，请检查网络或权限"
    exit 1
fi
