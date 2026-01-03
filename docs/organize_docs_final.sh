#!/bin/bash
# docs目录最终整理脚本（处理剩余未分类文件）

set -e

DOCS_DIR="/home/taotao/.cursor/worktrees/TRQuant/ope/docs"
cd "$DOCS_DIR"

TMP_DIR="tmp_old_files"
mkdir -p "$TMP_DIR"

echo "=== docs目录最终整理（处理剩余文件）==="
echo ""

move_to_tmp() {
    local source="$1"
    local reason="$2"
    
    if [ -e "$source" ]; then
        local basename_file=$(basename "$source")
        local dest="$TMP_DIR/$basename_file"
        
        if [ -e "$dest" ]; then
            local counter=1
            while [ -e "$TMP_DIR/${basename_file}.${counter}" ]; do
                ((counter++))
            done
            dest="$TMP_DIR/${basename_file}.${counter}"
        fi
        
        mv "$source" "$dest" 2>/dev/null && echo "移动重复文件: $source → $dest ($reason)"
    fi
}

move_to_dir() {
    local source="$1"
    local dest_dir="$2"
    local description="$3"
    
    if [ -e "$source" ]; then
        mkdir -p "$dest_dir"
        local basename_file=$(basename "$source")
        local dest="$dest_dir/$basename_file"
        
        if [ -e "$dest" ]; then
            move_to_tmp "$source" "目标已存在"
        else
            mv "$source" "$dest" 2>/dev/null && echo "移动文件: $source → $dest_dir/ ($description)"
        fi
    fi
}

# STRATEGY相关 → strategy_kb
echo "处理STRATEGY相关文件..."
STRATEGY_DIR="strategy_kb"
mkdir -p "$STRATEGY_DIR"
for file in STRATEGY*.md Strategy*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "$STRATEGY_DIR" "策略文档"
    fi
done

# SYSTEM相关 → 01_architecture
echo "处理SYSTEM相关文件..."
for file in SYSTEM*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "01_architecture" "系统架构"
    fi
done

# TASK相关 → 02_development_guides
echo "处理TASK相关文件..."
for file in TASK*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "任务相关"
    fi
done

# TODO相关 → 02_development_guides
echo "处理TODO相关文件..."
for file in TODO*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "TODO相关"
    fi
done

# USAGE相关 → 02_development_guides
echo "处理USAGE相关文件..."
for file in USAGE*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "使用指南"
    fi
done

# UNIFIED相关 → 02_development_guides 或 07_workflow
echo "处理UNIFIED相关文件..."
for file in UNIFIED*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "统一开发"
    fi
done

# WEB/WEBVIEW相关 → 02_development_guides
echo "处理WEB相关文件..."
for file in WEB*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "Web开发"
    fi
done

# WORKBENCH/WORKTREES相关 → 02_development_guides
echo "处理WORKBENCH相关文件..."
for file in WORKBENCH*.md WORKTREES*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "工作环境"
    fi
done

# TRIAL相关 → 02_development_guides
echo "处理TRIAL相关文件..."
for file in TRIAL*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "试用相关"
    fi
done

# SCRIPT相关 → 02_development_guides
echo "处理SCRIPT相关文件..."
for file in SCRIPT*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "脚本相关"
    fi
done

# token相关 → 08_ai_tools
echo "处理token相关文件..."
for file in token*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "08_ai_tools" "Token优化"
    fi
done

# 中文文件名 → 07_workflow（工作流相关）
echo "处理中文文件名..."
for file in *.md; do
    if [ -f "$file" ]; then
        # 检查是否包含中文
        if [[ "$file" =~ [\u4e00-\u9fff] ]] || [[ "$file" =~ [一-龥] ]]; then
            move_to_dir "$file" "07_workflow" "工作流文档（中文）"
        fi
    fi
done

echo ""
echo "✅ 最终整理完成！"
echo ""
echo "最终统计:"
echo "  tmp_old_files/ 目录大小: $(du -sh $TMP_DIR 2>/dev/null | cut -f1)"
echo "  剩余根目录文件数: $(find . -maxdepth 1 -type f \( -name '*.md' -o -name '*.txt' -o -name '*.pdf' -o -name '*.html' \) | wc -l)"

