#!/bin/bash
# 在 Cursor 中打开 Notebook 的辅助脚本
# 注意：此脚本只是显示提示信息，实际打开需要在 Cursor 中操作

NOTEBOOK_FILE="$1"

if [ -z "$NOTEBOOK_FILE" ]; then
    echo "📓 可用的 Notebook 文件："
    echo ""
    ls -1 notebooks/research/*.ipynb 2>/dev/null | xargs -n1 basename | nl
    echo ""
    echo "💡 使用方法："
    echo "   1. 在 Cursor 中按 Ctrl+P"
    echo "   2. 输入文件名（例如: 06_market_visualization.ipynb）"
    echo "   3. 回车打开"
    echo ""
    echo "或者运行: $0 <notebook文件名>"
    exit 0
fi

NOTEBOOK_PATH="notebooks/research/$NOTEBOOK_FILE"

if [ ! -f "$NOTEBOOK_PATH" ]; then
    echo "❌ 文件不存在: $NOTEBOOK_PATH"
    echo ""
    echo "可用的文件："
    ls -1 notebooks/research/*.ipynb 2>/dev/null | xargs -n1 basename
    exit 1
fi

echo "📓 Notebook 文件路径："
echo "   $NOTEBOOK_PATH"
echo ""
echo "✅ 在 Cursor 中打开步骤："
echo "   1. 按 Ctrl+P (Mac: Cmd+P)"
echo "   2. 输入: $NOTEBOOK_FILE"
echo "   3. 回车打开"
echo ""
echo "🔧 首次打开时需要："
echo "   1. 点击顶部 'Select Kernel' 按钮"
echo "   2. 选择: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python"
echo ""
echo "⚡ 运行代码快捷键："
echo "   • Shift + Enter：运行并移到下一个单元格"
echo "   • Ctrl + Enter：运行当前单元格但不移动"
