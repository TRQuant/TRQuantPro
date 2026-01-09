#!/bin/bash
# 安装剩余缺失的包（跳过有问题的包）

set -e

echo "🚀 安装剩余缺失的包..."
echo "📦 使用 Conda base 环境"
echo ""

# 初始化 conda
eval "$(conda shell.bash hook)"
conda activate base

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip setuptools wheel

# 读取原始 requirements
REQUIREMENTS_FILE="original_requirements.txt"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "❌ 文件不存在: $REQUIREMENTS_FILE"
    exit 1
fi

echo "📦 从 $REQUIREMENTS_FILE 安装包..."
echo "   跳过已知有问题的包（pyqlib 等）"
echo ""

# 创建临时文件，排除有问题的包
TEMP_REQ=$(mktemp)
grep -v "^pyqlib==" "$REQUIREMENTS_FILE" > "$TEMP_REQ"

# 安装包（忽略错误，继续安装其他包）
pip install -r "$TEMP_REQ" || {
    echo ""
    echo "⚠️  部分包安装失败，但会继续安装其他包"
    echo "   失败的包可能因为："
    echo "   - Python 版本不兼容"
    echo "   - 包源不可用"
    echo "   - 依赖冲突"
}

# 清理临时文件
rm -f "$TEMP_REQ"

echo ""
echo "✅ 包安装完成（部分包可能失败）"
echo ""
echo "📝 验证安装:"
python3 check_dependencies.py

