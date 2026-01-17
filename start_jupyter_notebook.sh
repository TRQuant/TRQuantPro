#!/bin/bash
# 启动 Jupyter Notebook 在独立浏览器中（简化版）

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTEBOOK_DIR="${PROJECT_ROOT}/notebooks"
PID_FILE="/tmp/jupyter_notebook.pid"
LOG_FILE="/tmp/jupyter_notebook.log"

# 初始化 conda
eval "$(conda shell.bash hook)"
conda activate base

# 检查 Jupyter 是否已安装
if ! command -v jupyter &> /dev/null; then
    echo "📦 正在安装 Jupyter Notebook..."
    pip install --quiet jupyter notebook ipykernel
fi

# 创建 notebooks 目录
mkdir -p "$NOTEBOOK_DIR"

# 检查是否已经运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "⚠️  Jupyter Notebook 已经在运行 (PID: $PID)"
        echo "🔗 URL: http://localhost:8888"
        echo "💡 如果需要停止，运行: kill $PID 或 ./stop_jupyter_notebook.sh"
        exit 0
    else
        rm -f "$PID_FILE"
    fi
fi

# 启动 Jupyter Notebook
echo "🚀 启动 Jupyter Notebook..."
echo "📁 Notebook 目录: $NOTEBOOK_DIR"
echo "🔗 URL: http://localhost:8888"

cd "$NOTEBOOK_DIR"
nohup jupyter notebook \
    --no-browser \
    --notebook-dir="$NOTEBOOK_DIR" \
    --ip=127.0.0.1 \
    --port=8888 \
    --NotebookApp.open_browser=True \
    --NotebookApp.token='' \
    --NotebookApp.password='' \
    > "$LOG_FILE" 2>&1 &

echo $! > "$PID_FILE"

# 等待服务器启动
sleep 3

# 打开浏览器
echo "🌐 在浏览器中打开..."
xdg-open http://localhost:8888 2>&1 || \
google-chrome http://localhost:8888 2>&1 || \
firefox http://localhost:8888 2>&1 || \
echo "💡 请在浏览器中手动打开: http://localhost:8888"

echo ""
echo "✅ Jupyter Notebook 已启动"
echo "📋 PID: $(cat "$PID_FILE")"
echo "📝 日志: $LOG_FILE"
echo "🛑 停止: ./stop_jupyter_notebook.sh 或 kill $(cat "$PID_FILE")"

