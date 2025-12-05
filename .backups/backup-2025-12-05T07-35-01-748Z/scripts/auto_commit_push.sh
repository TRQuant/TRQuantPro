#!/bin/bash
# -*- coding: utf-8 -*-
# 自动提交并推送脚本
# 保持版本号，自动commit和push到GitHub

set -e

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"
cd "$PROJECT_ROOT"

# 读取版本号
VERSION_FILE="$PROJECT_ROOT/VERSION"
if [ -f "$VERSION_FILE" ]; then
    VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')
else
    VERSION="2.0.0"
fi

# 检查是否有变更
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 没有变更需要提交"
    exit 0
fi

# 生成commit message
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG="chore: auto commit [v$VERSION] - $TIMESTAMP

自动提交更新
版本: v$VERSION
时间: $TIMESTAMP"

# 添加所有变更
git add -A

# 提交
git commit -m "$COMMIT_MSG"

# 推送到远程
echo "📤 推送到GitHub..."
if git push origin main 2>&1; then
    echo "✅ 推送成功 [v$VERSION]"
else
    echo "⚠️  推送失败，可能需要手动处理"
    exit 1
fi

