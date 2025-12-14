#!/bin/bash
# Git历史清理脚本
# 用于移除Git历史中的大文件（.taorui和.vsix文件）

set -e

echo "=== Git历史清理脚本 ==="
echo ""
echo "⚠️  警告：此操作会重写Git历史，所有提交SHA会改变"
echo "⚠️  建议：先创建完整备份"
echo ""

# 检查是否在正确的目录
if [ ! -f ".git/config" ]; then
    echo "❌ 错误：不在Git仓库根目录"
    exit 1
fi

# 询问确认
read -p "是否已创建备份？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "请先创建备份，然后重新运行此脚本"
    exit 1
fi

# 检查git-filter-repo是否安装
if ! command -v git-filter-repo &> /dev/null; then
    echo "安装git-filter-repo..."
    pip install git-filter-repo
fi

echo ""
echo "开始清理Git历史..."
echo ""

# 1. 移除.taorui目录
echo "步骤1: 移除.taorui目录..."
git filter-repo --path .taorui --invert-paths --force

# 2. 移除.vsix文件
echo ""
echo "步骤2: 移除.vsix文件..."
git filter-repo --path-glob '*.vsix' --invert-paths --force
git filter-repo --path-glob 'extension/*.vsix' --invert-paths --force

# 3. 清理引用
echo ""
echo "步骤3: 清理引用..."
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin 2>/dev/null || true
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 4. 显示结果
echo ""
echo "=== 清理完成 ==="
echo ""
echo "仓库大小："
du -sh .git
echo ""
echo "最近5个提交："
git log --oneline -5
echo ""
echo "下一步："
echo "1. 验证清理结果"
echo "2. 推送到远程（需要--force）"
echo "   git push origin main --force"

