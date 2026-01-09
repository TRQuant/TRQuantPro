#!/bin/bash
# 启动 Jupyter Notebook 在独立浏览器中

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTEBOOK_DIR="${PROJECT_ROOT}/notebooks"

echo "🚀 启动 Jupyter Notebook..."
echo "📁 项目目录: $PROJECT_ROOT"
echo "📂 Notebook 目录: $NOTEBOOK_DIR"

# 初始化 conda（如果还没有）
eval "$(conda shell.bash hook)"

# 检查 jupyter 是否可用
if ! command -v jupyter &> /dev/null; then
    echo "❌ Jupyter 未找到，正在安装..."
    conda activate base
    conda install -y jupyter notebook ipykernel -c conda-forge
fi

# 激活 conda base 环境（或者使用 trquant 环境如果存在）
if conda env list | grep -q "^trquant\s"; then
    echo "✅ 使用 trquant 环境"
    conda activate trquant
    # 确保在 trquant 环境中安装了 jupyter
    if ! python -c "import jupyter" 2>/dev/null; then
        echo "📦 在 trquant 环境中安装 Jupyter..."
        pip install jupyter notebook ipykernel
    fi
else
    echo "✅ 使用 base 环境"
    conda activate base
fi

# 创建 notebooks 目录（如果不存在）
mkdir -p "$NOTEBOOK_DIR"

# 生成 Jupyter 配置文件（如果需要）
JUPYTER_CONFIG_DIR="$HOME/.jupyter"
mkdir -p "$JUPYTER_CONFIG_DIR"

# 检查浏览器命令
if command -v xdg-open &> /dev/null; then
    BROWSER_CMD="xdg-open"
elif command -v google-chrome &> /dev/null; then
    BROWSER_CMD="google-chrome"
elif command -v firefox &> /dev/null; then
    BROWSER_CMD="firefox"
else
    BROWSER_CMD=""
fi

echo ""
echo "🌐 启动 Jupyter Notebook 服务器..."
echo "📝 Notebook 目录: $NOTEBOOK_DIR"
echo "🔗 浏览器将自动打开: http://localhost:8888"
echo ""
echo "💡 提示："
echo "  - 按 Ctrl+C 停止服务器"
echo "  - 默认端口: 8888"
echo "  - 如果需要指定端口: jupyter notebook --port 8889"
echo ""

# 启动 Jupyter Notebook（后台运行，自动打开浏览器）
cd "$NOTEBOOK_DIR"
jupyter notebook \
    --no-browser \
    --notebook-dir="$NOTEBOOK_DIR" \
    --ip=127.0.0.1 \
    --port=8888 \
    --NotebookApp.open_browser=True \
    --NotebookApp.allow_origin='*' \
    --NotebookApp.token='' \
    --NotebookApp.password=''

