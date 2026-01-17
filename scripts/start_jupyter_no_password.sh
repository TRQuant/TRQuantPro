#!/bin/bash
# 启动 Jupyter Notebook（无需密码/Token）
# 使用方法: ./scripts/start_jupyter_no_password.sh

cd /home/taotao/dev/QuantTest/TRQuant

# 使用项目的虚拟环境
VENV_PYTHON="/home/taotao/dev/QuantTest/TRQuant/venv/bin/python"

# 先停止已运行的 Jupyter（如果存在）
pkill -f "jupyter.*8888" 2>/dev/null
sleep 1

# 启动 Jupyter Notebook，禁用 token 和密码
$VENV_PYTHON -m jupyter notebook \
    --no-browser \
    --port=8888 \
    --notebook-dir=notebooks/research \
    --NotebookApp.token='' \
    --NotebookApp.password='' \
    --NotebookApp.allow_origin='*' \
    --ip=127.0.0.1 \
    2>&1 &

sleep 2
echo "✅ Jupyter Notebook 已启动（无需密码）"
echo "📝 访问地址: http://localhost:8888/tree"
echo "🛑 停止服务: pkill -f 'jupyter.*8888'"
echo ""
echo "⚠️  注意: 已禁用所有认证，仅限本地访问"
