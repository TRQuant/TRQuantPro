#!/bin/bash
# TRQuant回测 GUI 启动脚本

cd "$(dirname "$0")/.."
python3 -m gui.main_window_v2 "$@"
