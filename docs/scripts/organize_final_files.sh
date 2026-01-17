#!/bin/bash
# 整理最后剩余的文件和目录

DOCS_DIR="/home/taotao/dev/QuantTest/TRQuant/docs"
cd "$DOCS_DIR"

move_file() {
    local src="$1"
    local dst="$2"
    local desc="$3"
    
    if [ -f "$src" ] || [ -d "$src" ]; then
        mkdir -p "$(dirname "$dst")"
        if [ -f "$dst" ] || [ -d "$dst" ]; then
            echo "⚠️  目标已存在，跳过: $dst"
        else
            mv "$src" "$dst"
            echo "✓ $desc: $(basename "$src") -> $(dirname "$dst")/"
        fi
    else
        echo "✗ 不存在: $src"
    fi
}

echo "整理最后剩余的文件和目录..."
echo ""

# 1. 开发指南相关文件
move_file "Cursor规则制定建议.mhtml" "02_development_guides/Cursor规则制定建议.mhtml" "Cursor规则建议"

# 2. 测试报告JSON文件
move_file "project_rules_report.json" "06_testing_reports/project_rules_report.json" "项目规则报告JSON"

# 3. 模块设计方案TXT文件
move_file "五维评分系统设计方案_提取.txt" "03_modules/五维评分系统设计方案_提取.txt" "五维评分设计方案"
move_file "热度评分设计方案.txt" "03_modules/热度评分设计方案.txt" "热度评分设计方案"

# 4. 工作站的CSV文件（如果根目录还有）
if [ -f "workstation.csv" ] && [ ! -f "09_legacy/workstation.csv" ]; then
    move_file "workstation.csv" "09_legacy/workstation.csv" "工作站CSV"
fi

# 5. ExtentionDev目录（如果根目录还有）
if [ -d "ExtentionDev" ] && [ ! -d "02_development_guides/ExtentionDev" ]; then
    echo "合并 ExtentionDev 目录..."
    cp -r ExtentionDev/* 02_development_guides/ExtentionDev/ 2>/dev/null || true
    rm -rf ExtentionDev
    echo "✓ ExtentionDev -> 02_development_guides/ExtentionDev/"
fi

# 6. project_guides目录（如果根目录还有）
if [ -d "project_guides" ] && [ ! -d "02_development_guides/project_guides" ]; then
    echo "合并 project_guides 目录..."
    cp -r project_guides/* 02_development_guides/project_guides/ 2>/dev/null || true
    rm -rf project_guides
    echo "✓ project_guides -> 02_development_guides/project_guides/"
fi

# 7. Ptrade_coding目录
if [ -d "Ptrade_coding" ]; then
    move_file "Ptrade_coding" "04_platform_integration/Ptrade_coding" "PTrade编码文档"
fi

# 8. standards目录（如果根目录还有）
if [ -d "standards" ] && [ ! -d "02_development_guides/standards" ]; then
    echo "合并 standards 目录..."
    cp -r standards/* 02_development_guides/standards/ 2>/dev/null || true
    rm -rf standards
    echo "✓ standards -> 02_development_guides/standards/"
fi

echo ""
echo "完成！"
