#!/bin/bash
# Git仓库初始化脚本
# 用途：清理旧的Git配置，重新初始化并连接到新仓库 TRQuant_ope

set -e  # 遇到错误立即退出

cd /home/taotao/.cursor/worktrees/TRQuant/ope

echo "=== Git仓库清理和重新配置 ==="
echo ""

# 步骤1: 清理旧的Git配置（彻底清理）
echo "步骤1: 清理旧的Git相关文件和配置..."
echo "  删除.git目录/文件..."

# 删除.git目录（如果是独立仓库）
if [ -d .git ]; then
    rm -rf .git
    echo "  ✅ 已删除.git目录"
fi

# 删除.git文件（如果是worktree）
if [ -f .git ]; then
    rm -f .git
    echo "  ✅ 已删除.git文件"
fi

# 删除其他Git相关隐藏文件（保留.gitignore）
find . -maxdepth 1 -name ".git*" ! -name ".gitignore" -delete 2>/dev/null || true

echo "  ✅ Git清理完成"

echo ""

# 步骤2: 初始化Git仓库
echo "步骤2: 初始化Git仓库..."
git init
echo "  ✅ Git初始化完成"

echo ""

# 步骤3: 配置Remote到新仓库 TRQuant_ope
echo "步骤3: 配置Remote到新仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/TRQuant/TRQuant_ope.git
echo "  ✅ Remote配置完成 (TRQuant_ope)"

echo ""

# 步骤4: 验证配置
echo "步骤4: 验证配置..."
echo ""
echo "Git Remote:"
git remote -v
echo ""
echo "Git状态:"
git status --short | head -20 || echo "  (暂无可跟踪文件)"

echo ""
echo "=== 清理和配置完成 ==="
echo ""
echo "✅ 旧Git配置已清理"
echo "✅ 新Git仓库已初始化"
echo "✅ Remote已配置到: https://github.com/TRQuant/TRQuant_ope.git"
echo ""
echo "下一步操作:"
echo "1. 添加文件: git add ."
echo "2. 提交: git commit -m 'Initial commit: 核心代码和配置文件'"
echo "3. 推送: git push -u origin main (或 master)"
echo ""

