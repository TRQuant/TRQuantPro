#!/bin/bash
# 轩辕剑灵独立GUI启动脚本

# 设置中文输入法环境变量（如果未设置）
if [ -z "$QT_IM_MODULE" ]; then
    if command -v fcitx >/dev/null 2>&1; then
        export QT_IM_MODULE=fcitx
    elif command -v ibus-daemon >/dev/null 2>&1; then
        export QT_IM_MODULE=ibus
    fi
fi

if [ -z "$XMODIFIERS" ]; then
    export XMODIFIERS="@im=fcitx"
fi

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
