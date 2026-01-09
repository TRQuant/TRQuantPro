#!/bin/bash
# 轩辕剑灵开发助手启动脚本
# 使用方法: bash scripts/xuanyuan_start.sh

cd "$(dirname "$0")/.."

# 使用venv中的Python
if [ -f "venv/bin/python" ]; then
    venv/bin/python gui/xuanyuan_main_window.py "$@"
elif [ -f "venv/bin/python3" ]; then
    venv/bin/python3 gui/xuanyuan_main_window.py "$@"
else
    echo "错误: 未找到venv中的Python"
    exit 1
fi

