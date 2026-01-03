#!/bin/bash
# 清理 Git worktrees 脚本

PROJECT_ROOT="/home/taotao/dev/QuantTest/TRQuant"
CURSOR_WORKTREES="$HOME/.cursor/worktrees/TRQuant"

echo "=== 清理 Git Worktrees ==="
echo ""

cd "$PROJECT_ROOT" || exit 1

# 1. 统计 worktrees
BEFORE=$(git worktree list 2>/dev/null | wc -l)
echo "当前 Git worktrees 数量：$BEFORE"

# 2. 清理已删除的 worktrees
echo ""
echo "清理已删除的 worktrees..."
git worktree prune

# 3. 清理 Cursor worktrees 目录
if [ -d "$CURSOR_WORKTREES" ]; then
    echo ""
    echo "清理 Cursor worktrees 目录..."
    rm -rf "$CURSOR_WORKTREES"/*
fi

# 4. 清理主仓库的 .git/worktrees
if [ -d "$PROJECT_ROOT/.git/worktrees" ]; then
    echo ""
    echo "清理主仓库的 .git/worktrees..."
    rm -rf "$PROJECT_ROOT/.git/worktrees"/*
fi

# 5. 再次运行 prune
echo ""
echo "最终清理..."
git worktree prune

# 6. 统计结果
AFTER=$(git worktree list 2>/dev/null | wc -l)
echo ""
echo "清理后 Git worktrees 数量：$AFTER"
if [ "$BEFORE" -gt "$AFTER" ]; then
    echo "✅ 清理了 $((BEFORE - AFTER)) 个 worktrees"
else
    echo "⚠️  worktrees 数量未减少，可能需要手动清理"
fi
