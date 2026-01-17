#!/bin/bash
# EmQuantAPI安装脚本
# 使用venv的Python安装EmQuantAPI

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="${PROJECT_ROOT}/extension/venv/bin/python"
VENV_PIP="${PROJECT_ROOT}/extension/venv/bin/pip"

echo "🔧 EmQuantAPI安装脚本"
echo "项目根目录: ${PROJECT_ROOT}"
echo ""

# 检查venv是否存在
if [ ! -f "${VENV_PYTHON}" ]; then
    echo "❌ 错误: venv不存在，请先创建venv"
    echo "   运行: python3 -m venv extension/venv"
    exit 1
fi

echo "✅ 使用venv Python: ${VENV_PYTHON}"
echo ""

# 方式1: 如果有installEmQuantAPI.py
if [ -f "installEmQuantAPI.py" ]; then
    echo "📦 找到installEmQuantAPI.py，使用官方安装脚本..."
    "${VENV_PYTHON}" installEmQuantAPI.py
    echo "✅ 安装完成"
    exit 0
fi

# 方式2: 如果有wheel文件
WHEEL_FILE=$(find . -maxdepth 3 -name "EmQuantAPI*.whl" -o -name "emquant*.whl" 2>/dev/null | head -1)
if [ -n "${WHEEL_FILE}" ]; then
    echo "📦 找到wheel文件: ${WHEEL_FILE}"
    "${VENV_PIP}" install "${WHEEL_FILE}"
    echo "✅ 安装完成"
    exit 0
fi

# 方式3: 如果有zip文件
ZIP_FILE=$(find . -maxdepth 3 -name "EmQuantAPI*.zip" -o -name "emquant*.zip" 2>/dev/null | head -1)
if [ -n "${ZIP_FILE}" ]; then
    echo "📦 找到zip文件: ${ZIP_FILE}"
    TEMP_DIR=$(mktemp -d)
    unzip -q "${ZIP_FILE}" -d "${TEMP_DIR}"
    
    # 查找setup.py或install脚本
    if [ -f "${TEMP_DIR}"/*/setup.py ]; then
        SETUP_PY=$(find "${TEMP_DIR}" -name "setup.py" | head -1)
        cd "$(dirname "${SETUP_PY}")"
        "${VENV_PYTHON}" setup.py install
    elif [ -f "${TEMP_DIR}"/*/installEmQuantAPI.py ]; then
        INSTALL_SCRIPT=$(find "${TEMP_DIR}" -name "installEmQuantAPI.py" | head -1)
        "${VENV_PYTHON}" "${INSTALL_SCRIPT}"
    else
        echo "⚠️  zip文件中未找到setup.py或installEmQuantAPI.py"
        echo "   请手动解压并安装"
        exit 1
    fi
    
    rm -rf "${TEMP_DIR}"
    echo "✅ 安装完成"
    exit 0
fi

# 如果都没有找到
echo "❌ 未找到EmQuantAPI安装文件"
echo ""
echo "请选择以下方式之一："
echo "1. 从东方财富Choice官网下载安装包"
echo "2. 将installEmQuantAPI.py放在项目根目录"
echo "3. 将.whl或.zip文件放在项目根目录或子目录"
echo ""
echo "然后重新运行此脚本"
exit 1
