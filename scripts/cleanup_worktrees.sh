#!/bin/bash
# 清理 Cursor worktrees 脚本

WORKTREES_DIR="$HOME/.cursor/worktrees/TRQuant"

echo "=== 清理 Cursor Worktrees ==="
echo ""

if [ -d "$WORKTREES_DIR" ]; then
    COUNT=$(ls -1 "$WORKTREES_DIR" 2>/dev/null | wc -l)
    if [ "$COUNT" -gt 0 ]; then
        echo "发现 $COUNT 个 worktrees"
        echo "正在清理..."
        rm -rf "$WORKTREES_DIR"/*
        echo "✅ 已清理所有 worktrees"
    else
        echo "✅ worktrees 目录为空"
    fi
else
    echo "✅ worktrees 目录不存在"
fi

echo ""
echo "建议："
echo "1. 完全关闭 Cursor"
echo "2. 使用工作区文件打开项目："
echo "   File > Open Workspace from File..."
echo "   选择：/home/taotao/dev/QuantTest/TRQuant/TRQuant.code-workspace"
