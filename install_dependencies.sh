#!/bin/bash
# 安装项目依赖包

set -e

echo "🚀 开始安装项目依赖包..."
echo "📦 使用 Conda base 环境"
echo ""

# 初始化 conda
eval "$(conda shell.bash hook)"
conda activate base

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip setuptools wheel

# 核心依赖包列表（按安装顺序）
CORE_PACKAGES=(
    "numpy>=1.24.0"
    "pandas>=2.0.0"
    "matplotlib>=3.7.0"
    "scikit-learn>=1.3.0"
)

VISUALIZATION_PACKAGES=(
    "plotly>=5.14.0"
    "seaborn>=0.12.0"
)

GUI_PACKAGES=(
    "PyQt6>=6.4.0"
    "pyqtgraph>=0.13.0"
)

WEB_PACKAGES=(
    "flask>=2.3.0"
    "flask-cors>=4.0.0"
    "fastapi>=0.104.0"
    "uvicorn>=0.24.0"
    "pydantic>=2.5.0"
)

TOOL_PACKAGES=(
    "python-dotenv>=1.0.0"
    "pyyaml>=6.0"
    "tqdm>=4.65.0"
    "requests>=2.31.0"
    "watchdog>=3.0.0"
    "pyperclip>=1.8.0"
)

SPECIAL_PACKAGES=(
    "jqdatasdk>=1.9.0"
)

# 安装核心依赖
echo "📦 安装核心依赖包..."
pip install "${CORE_PACKAGES[@]}"

# 安装可视化包
echo "📦 安装可视化包..."
pip install "${VISUALIZATION_PACKAGES[@]}"

# 安装 GUI 包
echo "📦 安装 GUI 包..."
pip install "${GUI_PACKAGES[@]}"

# 安装 Web 包
echo "📦 安装 Web 包..."
pip install "${WEB_PACKAGES[@]}"

# 安装工具包
echo "📦 安装工具包..."
pip install "${TOOL_PACKAGES[@]}"

# 安装特殊包（聚宽API）
echo "📦 安装特殊包..."
pip install "${SPECIAL_PACKAGES[@]}"

echo ""
echo "✅ 所有依赖包安装完成！"
echo ""
echo "📝 验证安装:"
python3 check_dependencies.py

