#!/bin/bash
# 整理参考文档和脚本文件

DOCS_DIR="/home/taotao/dev/QuantTest/TRQuant/docs"
cd "$DOCS_DIR"

echo "整理参考文档和脚本文件..."
echo ""

# 移动参考文档到05_reference_books
move_to_ref() {
    local file="$1"
    if [ -f "$file" ]; then
        mv "$file" "05_reference_books/"
        echo "✓ $file -> 05_reference_books/"
    fi
}

# PDF和DOCX参考文档
move_to_ref "A股主题轮动策略研究：AI主线、国产替代与算力.pdf"
move_to_ref "A 股量化策略开发与演化体系设计.pdf"
move_to_ref "QuantConnect平台策略开发：AI方法与传统策略的比较.docx"
move_to_ref "TRQuant量化系统白皮书（初版）.pdf"
move_to_ref "Ubuntu 24.04 LTS 金融_AI 工作站搭建手册.docx"
move_to_ref "基于 Cursor 的 PTrade 策略模板自动生成指南.pdf"
move_to_ref "小资金投资者的策略探讨.docx"
move_to_ref "目录.docx"
move_to_ref "第六步：策略开发 – AI辅助代码生成与文件管理.pdf"
move_to_ref "高倍股量化投资策略（QuantConnect实现）.docx"

# HTML文件（可能是教程）
if [ -f "index.html" ]; then
    mv "index.html" "02_development_guides/project_guides/"
    echo "✓ index.html -> 02_development_guides/project_guides/"
fi

# 脚本文件
if [ -f "organize_docs.sh" ]; then
    mv "organize_docs.sh" "scripts/"
    echo "✓ organize_docs.sh -> scripts/"
fi

echo ""
echo "完成！"
