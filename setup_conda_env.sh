#!/bin/bash
# Conda 环境设置脚本
# 使用现有的 Miniconda，创建项目专用的 conda 环境，避免重复安装

set -e  # 遇到错误立即退出

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_NAME="trquant"

echo "🚀 开始设置 Conda 环境..."
echo "📁 项目目录: $PROJECT_ROOT"
echo "🐍 环境名称: $ENV_NAME"

# 检查 conda 是否可用
if ! command -v conda &> /dev/null; then
    echo "❌ 错误: conda 命令未找到"
    echo "请先安装 Miniconda 或 Anaconda"
    echo "下载地址: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda 已安装: $(conda --version)"

# 检查是否已存在环境
if conda env list | grep -q "^${ENV_NAME}\s"; then
    echo "⚠️  环境 ${ENV_NAME} 已存在"
    read -p "是否删除并重建？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  删除现有环境..."
        conda env remove -n $ENV_NAME -y
    else
        echo "✅ 使用现有环境"
        echo "激活环境: conda activate $ENV_NAME"
        exit 0
    fi
fi

# 创建 conda 环境（使用 Python 3.12，匹配现有 venv）
echo "🔨 创建 Conda 环境..."
conda create -n $ENV_NAME python=3.12 -y

# 激活环境（在脚本中）
echo "🔌 激活环境..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip setuptools wheel

# 安装依赖（使用 pip，conda 会复用已下载的包）
echo "📦 安装项目依赖..."
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    pip install -r "$PROJECT_ROOT/requirements.txt"
else
    echo "❌ 错误: requirements.txt 未找到"
    exit 1
fi

# 验证安装
echo "✅ 验证安装..."
python --version
pip list | head -20

echo ""
echo "🎉 Conda 环境设置完成！"
echo ""
echo "📝 使用方法："
echo "  1. 激活环境: conda activate $ENV_NAME"
echo "  2. 运行项目: python main.py"
echo "  3. 退出环境: conda deactivate"
echo ""
echo "💡 提示："
echo "  - Conda 会自动复用已下载的包（在 ~/miniconda3/pkgs/）"
echo "  - 如需更新依赖: conda activate $ENV_NAME && pip install -r requirements.txt --upgrade"
echo "  - 查看环境列表: conda env list"
echo "  - 删除环境: conda env remove -n $ENV_NAME"

