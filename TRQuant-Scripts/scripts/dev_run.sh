#!/usr/bin/env bash
# 开发模式启动脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 设置开发模式
export JQQUANT_DEV_MODE=1

# 激活虚拟环境（如果存在）
if [ -f "${PROJECT_ROOT}/venv/bin/activate" ]; then
    source "${PROJECT_ROOT}/venv/bin/activate"
fi

# 运行应用
cd "${PROJECT_ROOT}"
exec python3 JQQuant.py "$@"
