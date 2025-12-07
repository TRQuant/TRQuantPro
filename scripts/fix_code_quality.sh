#!/bin/bash
# TRQuant 代码质量自动修复脚本
# 安全地自动修复代码格式和简单问题

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "TRQuant 代码质量自动修复"
echo "=========================================="
echo ""

# 激活虚拟环境
if [ -d "extension/venv" ]; then
    source extension/venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "错误: 未找到 extension/venv"
    exit 1
fi

# 1. 格式化 Python 代码（排除有问题的文件）
echo ""
echo "1. 格式化 Python 代码..."
python -m black core/ --exclude="data_center.py|strategy_manager.py|ptrade_broker.py|qmt_broker.py" 2>&1 | head -20 || echo "部分文件格式化完成"

# 2. 修复 Python 空白行问题
echo ""
echo "2. 修复 Python 空白行空格..."
python -m ruff check core/ --select=W293,W291 --fix --exclude="data_center.py|strategy_manager.py|ptrade_broker.py|qmt_broker.py" 2>&1 | head -20 || echo "部分文件修复完成"

# 3. 移除不必要的编码声明
echo ""
echo "3. 移除不必要的编码声明..."
find core/ -name "*.py" -type f ! -name "data_center.py" ! -name "strategy_manager.py" ! -name "ptrade_broker.py" ! -name "qmt_broker.py" -exec sed -i '1{/^# -\*- coding: utf-8 -\*-$/d}' {} \; 2>/dev/null || true
echo "✓ 编码声明已清理"

# 4. 格式化 TypeScript 代码
echo ""
echo "4. 格式化 TypeScript 代码..."
cd extension
npx prettier --write "src/**/*.ts" 2>&1 | head -20 || echo "格式化完成"
cd ..

# 5. 自动修复 ESLint 可修复的问题
echo ""
echo "5. 自动修复 ESLint 问题..."
cd extension
npx eslint "src/**/*.ts" --fix 2>&1 | head -30 || echo "修复完成"
cd ..

echo ""
echo "=========================================="
echo "自动修复完成！"
echo "=========================================="
echo ""
echo "⚠️  注意：以下问题需要手动修复："
echo ""
echo "1. 超大文件需要拆分："
echo "   - core/strategy_manager.py (119K 行)"
echo "   - core/ptrade_broker.py (110K 行)"
echo "   - core/data_center.py (108K 行)"
echo "   - core/qmt_broker.py (108K 行)"
echo ""
echo "2. 未使用的变量需要手动删除或标记"
echo ""
echo "3. require 需要手动替换为 import"
echo ""
echo "4. Case 块需要手动添加块作用域"
echo ""
echo "5. any 类型需要手动替换为具体类型"
echo ""
echo "详细问题请查看: docs/CODE_QUALITY_ANALYSIS.md"
echo ""







