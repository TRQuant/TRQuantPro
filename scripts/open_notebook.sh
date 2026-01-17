#!/bin/bash
# 在Cursor中打开Notebook的便捷脚本

NOTEBOOK_FILE="$1"

if [ -z "$NOTEBOOK_FILE" ]; then
    echo "用法: $0 <notebook文件名>"
    echo ""
    echo "可用的notebook:"
    ls -1 /home/taotao/dev/QuantTest/TRQuant/notebooks/templates/*.ipynb 2>/dev/null | xargs -n1 basename
    exit 1
fi

# 构建完整路径
NOTEBOOK_PATH="/home/taotao/dev/QuantTest/TRQuant/notebooks/templates/$NOTEBOOK_FILE"

if [ ! -f "$NOTEBOOK_PATH" ]; then
    echo "❌ 文件不存在: $NOTEBOOK_PATH"
    exit 1
fi

echo "📓 打开notebook: $NOTEBOOK_PATH"

# 尝试使用cursor命令打开
if command -v cursor &> /dev/null; then
    cursor "$NOTEBOOK_PATH"
    echo "✅ 已在Cursor中打开"
elif command -v code &> /dev/null; then
    code "$NOTEBOOK_PATH"
    echo "✅ 已在VS Code中打开"
else
    echo "⚠️  未找到cursor或code命令"
    echo "请手动打开: $NOTEBOOK_PATH"
    # 尝试用系统默认程序打开
    if command -v xdg-open &> /dev/null; then
        xdg-open "$NOTEBOOK_PATH"
    fi
fi
