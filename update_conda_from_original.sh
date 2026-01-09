#!/bin/bash
# 从原始 venv 同步包到 Conda base 环境

set -e

ORIGINAL_VENV="/home/taotao/dev/QuantTest/TRQuant/venv"

echo "🔄 从原始 venv 更新 Conda base 环境"
echo "="*60
echo "原始位置: $ORIGINAL_VENV"
echo "目标环境: Conda base"
echo ""

# 检查原始 venv 是否存在
if [ ! -d "$ORIGINAL_VENV" ]; then
    echo "❌ 原始 venv 不存在: $ORIGINAL_VENV"
    exit 1
fi

# 导出原始 venv 的包列表
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS_FILE="$SCRIPT_DIR/original_requirements.txt"

echo "📦 步骤 1: 导出原始 venv 的包列表..."
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "✅ 使用已有的包列表: $REQUIREMENTS_FILE"
    package_count=$(wc -l < "$REQUIREMENTS_FILE")
else
    $ORIGINAL_VENV/bin/python3 -m pip freeze > "$REQUIREMENTS_FILE"
    package_count=$(wc -l < "$REQUIREMENTS_FILE")
    echo "✅ 已导出 $package_count 个包到 $REQUIREMENTS_FILE"
fi
echo ""

# 初始化 conda
echo "📦 步骤 2: 激活 Conda base 环境..."
eval "$(conda shell.bash hook)"
conda activate base

echo "⬆️  步骤 3: 升级 pip..."
pip install --upgrade pip setuptools wheel

echo ""
echo "📦 步骤 4: 安装包（这可能需要一些时间，请耐心等待）..."
echo "   将从原始 venv 安装 $package_count 个包到 conda base 环境"
echo ""

# 询问确认
read -p "是否继续? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⏭️  已取消"
    exit 0
fi

# 安装包
pip install -r "$REQUIREMENTS_FILE"

echo ""
echo "✅ Conda base 环境更新完成！"
echo ""
echo "📝 验证:"
echo "   conda activate base"
echo "   pip list | wc -l  # 应该显示约 $package_count 个包"
echo ""
echo "🔍 检查特定包:"
echo "   python3 -c \"import graphviz, networkx, TA-Lib, akshare; print('✅ 核心包已安装')\""
echo ""
echo "📄 包列表文件: $REQUIREMENTS_FILE"

