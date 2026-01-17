#!/bin/bash
# 从原始位置同步包到当前位置的 venv 和 conda base 环境

set -e

ORIGINAL_VENV="/home/taotao/dev/QuantTest/TRQuant/venv"
CURRENT_VENV="/home/taotao/.cursor/worktrees/TRQuant/ope/venv"

echo "🔄 同步包从原始位置到当前位置"
echo "="*60
echo "原始位置: $ORIGINAL_VENV"
echo "当前位置: $CURRENT_VENV"
echo ""

# 检查原始 venv 是否存在
if [ ! -d "$ORIGINAL_VENV" ]; then
    echo "❌ 原始 venv 不存在: $ORIGINAL_VENV"
    exit 1
fi

# 1. 导出原始 venv 的包列表
echo "📦 步骤 1: 导出原始 venv 的包列表..."
$ORIGINAL_VENV/bin/python3 -m pip freeze > /tmp/original_requirements.txt
echo "✅ 已导出 $(wc -l < /tmp/original_requirements.txt) 个包到 /tmp/original_requirements.txt"

# 2. 同步到当前 venv（如果存在）
if [ -d "$CURRENT_VENV" ]; then
    echo ""
    echo "📦 步骤 2: 同步到当前 venv..."
    read -p "是否更新当前 venv? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        $CURRENT_VENV/bin/python3 -m pip install --upgrade pip
        $CURRENT_VENV/bin/python3 -m pip install -r /tmp/original_requirements.txt
        echo "✅ 当前 venv 已更新"
    else
        echo "⏭️  跳过当前 venv 更新"
    fi
else
    echo "⚠️  当前 venv 不存在，跳过"
fi

# 3. 同步到 conda base 环境
echo ""
echo "📦 步骤 3: 同步到 Conda base 环境..."
read -p "是否更新 conda base 环境? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    eval "$(conda shell.bash hook)"
    conda activate base
    
    echo "⬆️  升级 pip..."
    pip install --upgrade pip setuptools wheel
    
    echo "📦 安装包（这可能需要一些时间）..."
    pip install -r /tmp/original_requirements.txt
    
    echo "✅ Conda base 环境已更新"
else
    echo "⏭️  跳过 conda base 环境更新"
fi

echo ""
echo "✅ 同步完成！"
echo ""
echo "📝 验证:"
echo "   - 原始 venv 包列表: /tmp/original_requirements.txt"
echo "   - 检查当前 venv: $CURRENT_VENV/bin/python3 -m pip list"
echo "   - 检查 conda base: conda activate base && pip list"

