#!/bin/bash
# 运行主线因子组合测试GUI

cd "$(dirname "$0")/.."

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行测试GUI
python tests/test_mainline_factor_combination_gui.py

