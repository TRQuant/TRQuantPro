#!/bin/bash
# 停止 Jupyter Notebook 服务器

PID_FILE="/tmp/jupyter_notebook.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "🛑 停止 Jupyter Notebook (PID: $PID)..."
        kill "$PID"
        sleep 1
        
        # 检查是否已停止
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "⚠️  进程仍在运行，强制停止..."
            kill -9 "$PID"
        fi
        
        rm -f "$PID_FILE"
        echo "✅ Jupyter Notebook 已停止"
    else
        echo "⚠️  PID 文件存在但进程未运行，清理 PID 文件"
        rm -f "$PID_FILE"
    fi
else
    echo "⚠️  未找到 PID 文件，尝试查找并停止 Jupyter 进程..."
    PIDS=$(ps aux | grep -E "jupyter.*notebook" | grep -v grep | awk '{print $2}')
    if [ -z "$PIDS" ]; then
        echo "✅ 没有运行中的 Jupyter Notebook 进程"
    else
        echo "找到以下 Jupyter 进程: $PIDS"
        for pid in $PIDS; do
            echo "🛑 停止进程 $pid..."
            kill "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null
        done
        echo "✅ 所有 Jupyter Notebook 进程已停止"
    fi
fi

