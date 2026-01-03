#!/bin/bash
# docs目录安全整理脚本
# 使用方法: bash organize_docs_safe.sh [dry-run|execute]

set -e

DOCS_DIR="/home/taotao/.cursor/worktrees/TRQuant/ope/docs"
cd "$DOCS_DIR"

MODE=${1:-dry-run}  # 默认dry-run模式，不会实际删除文件

echo "=== docs目录整理脚本 ==="
echo "模式: $MODE"
echo ""

if [ "$MODE" != "execute" ]; then
    echo "⚠️  DRY-RUN模式：只显示操作，不会实际执行"
    echo "要实际执行，请运行: bash organize_docs_safe.sh execute"
    echo ""
fi

# 函数：安全删除目录
safe_remove() {
    local target="$1"
    local description="$2"
    
    if [ "$MODE" = "execute" ]; then
        echo "删除: $target ($description)"
        rm -rf "$target"
    else
        echo "[DRY-RUN] 将删除: $target ($description)"
    fi
}

# 函数：安全移动文件/目录
safe_move() {
    local source="$1"
    local dest="$2"
    local description="$3"
    
    if [ "$MODE" = "execute" ]; then
        if [ -e "$dest" ]; then
            echo "⚠️  目标已存在，跳过: $source → $dest"
        else
            echo "移动: $source → $dest ($description)"
            mv "$source" "$dest"
        fi
    else
        echo "[DRY-RUN] 将移动: $source → $dest ($description)"
    fi
}

# 步骤1: 删除docs/docs/重复目录
echo "步骤1: 删除docs/docs/重复目录 (180M)"
if [ -d "docs" ]; then
    safe_remove "docs" "重复嵌套目录"
else
    echo "✓ docs/docs/ 目录不存在，跳过"
fi
echo ""

# 步骤2: 合并ExtentionDev目录
echo "步骤2: 合并ExtentionDev目录"
if [ -d "ExtentionDev" ]; then
    if [ -d "02_development_guides/ExtentionDev" ]; then
        echo "⚠️  目标目录已存在: 02_development_guides/ExtentionDev/"
        echo "   需要手动对比和合并"
    else
        safe_move "ExtentionDev" "02_development_guides/ExtentionDev" "扩展开发文档"
    fi
else
    echo "✓ ExtentionDev目录不存在，跳过"
fi
echo ""

# 步骤3: 合并Ptrade_coding目录
echo "步骤3: 合并Ptrade_coding目录"
if [ -d "Ptrade_coding" ]; then
    if [ -d "04_platform_integration/Ptrade_coding" ]; then
        echo "⚠️  目标目录已存在: 04_platform_integration/Ptrade_coding/"
        echo "   需要手动对比和合并"
    else
        safe_move "Ptrade_coding" "04_platform_integration/Ptrade_coding" "PTrade编码文档"
    fi
else
    echo "✓ Ptrade_coding目录不存在，跳过"
fi
echo ""

# 步骤4: 统计根目录文件（供后续整理参考）
echo "步骤4: 统计根目录文件"
echo "根目录Markdown文件数量: $(find . -maxdepth 1 -name "*.md" -type f | wc -l)"
echo "根目录文本文件数量: $(find . -maxdepth 1 -name "*.txt" -type f | wc -l)"
echo ""
echo "⚠️  根目录文件整理需要手动分类，建议使用DOCS_ORGANIZATION_PLAN.md中的分类规则"
echo ""

# 步骤5: 清理09_legacy中的backups（可选）
echo "步骤5: 检查09_legacy目录"
if [ -d "09_legacy/backups" ]; then
    echo "09_legacy/backups 目录大小: $(du -sh 09_legacy/backups | cut -f1)"
    echo "⚠️  建议手动审查backups目录，删除过时备份"
else
    echo "✓ 09_legacy/backups 不存在"
fi
echo ""

if [ "$MODE" = "execute" ]; then
    echo "✅ 执行完成！"
    echo ""
    echo "下一步："
    echo "1. 手动整理根目录散乱文件（参考DOCS_ORGANIZATION_PLAN.md）"
    echo "2. 审查和处理重复文件"
    echo "3. 运行 git status 查看更改"
    echo "4. 运行 git add docs/ 添加更改"
else
    echo "✅ DRY-RUN完成！"
    echo ""
    echo "要实际执行，请运行: bash organize_docs_safe.sh execute"
fi

