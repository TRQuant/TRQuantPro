#!/bin/bash
# 清理根目录的重复文件

DOCS_DIR="/home/taotao/dev/QuantTest/TRQuant/docs"
cd "$DOCS_DIR"

echo "清理根目录的重复文件..."
echo ""

# 检查并删除重复文件
check_and_remove() {
    local root_file="$1"
    local target_file="$2"
    
    if [ -f "$root_file" ] && [ -f "$target_file" ]; then
        echo "删除重复文件: $root_file (目标已存在: $target_file)"
        rm -f "$root_file"
    elif [ -f "$root_file" ] && [ ! -f "$target_file" ]; then
        echo "移动文件: $root_file -> $target_file"
        mkdir -p "$(dirname "$target_file")"
        mv "$root_file" "$target_file"
    fi
}

# 检查并合并目录
check_and_merge_dir() {
    local root_dir="$1"
    local target_dir="$2"
    
    if [ -d "$root_dir" ]; then
        if [ -d "$target_dir" ]; then
            echo "合并目录: $root_dir -> $target_dir"
            # 复制新文件到目标目录
            find "$root_dir" -type f | while read file; do
                rel_path="${file#$root_dir/}"
                target_file="$target_dir/$rel_path"
                if [ ! -f "$target_file" ]; then
                    mkdir -p "$(dirname "$target_file")"
                    cp "$file" "$target_file"
                    echo "  + $rel_path"
                fi
            done
            rm -rf "$root_dir"
        else
            echo "移动目录: $root_dir -> $target_dir"
            mkdir -p "$(dirname "$target_dir")"
            mv "$root_dir" "$target_dir"
        fi
    fi
}

# 处理文件
check_and_remove "Cursor规则制定建议.mhtml" "02_development_guides/Cursor规则制定建议.mhtml"
check_and_remove "project_rules_report.json" "06_testing_reports/project_rules_report.json"
check_and_remove "workstation.csv" "09_legacy/workstation.csv"
check_and_remove "五维评分系统设计方案_提取.txt" "03_modules/五维评分系统设计方案_提取.txt"
check_and_remove "热度评分设计方案.txt" "03_modules/热度评分设计方案.txt"

# 处理目录
check_and_merge_dir "ExtentionDev" "02_development_guides/ExtentionDev"
check_and_merge_dir "project_guides" "02_development_guides/project_guides"
check_and_merge_dir "standards" "02_development_guides/standards"

echo ""
echo "完成！"
