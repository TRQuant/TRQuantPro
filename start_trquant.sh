#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 激活虚拟环境
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "错误: 未找到虚拟环境 'venv'，请先运行 'python3 -m venv venv' 并安装依赖。"
    exit 1
fi

# 确保日志目录存在
mkdir -p "$SCRIPT_DIR/logs"

# 启动Python应用
if pgrep -f "python.*TRQuant.py" > /dev/null; then
    echo "韬睿量化已经在运行中。"
else
    echo "启动韬睿量化..."
    nohup "$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/TRQuant.py" --fast > "$SCRIPT_DIR/logs/trquant_startup.log" 2>&1 &
    echo "韬睿量化已在后台启动。日志文件: $SCRIPT_DIR/logs/trquant_startup.log"
fi
