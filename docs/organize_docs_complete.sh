#!/bin/bash
# docs目录完整分类整理脚本（处理剩余文件）
# 将所有文件分门别类整理，重复/过时的文件移动到tmp文件夹

set -e

DOCS_DIR="/home/taotao/.cursor/worktrees/TRQuant/ope/docs"
cd "$DOCS_DIR"

TMP_DIR="tmp_old_files"
mkdir -p "$TMP_DIR"

echo "=== docs目录完整分类整理（处理剩余文件）==="
echo "重复/过时文件将移动到: $TMP_DIR/"
echo ""

# 函数：安全移动文件到tmp
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
        
        echo "移动重复/过时文件: $source → $dest ($reason)"
        mv "$source" "$dest"
    fi
}

# 函数：移动文件到目标目录
move_to_dir() {
    local source="$1"
    local dest_dir="$2"
    local description="$3"
    
    if [ -e "$source" ]; then
        mkdir -p "$dest_dir"
        local basename_file=$(basename "$source")
        local dest="$dest_dir/$basename_file"
        
        if [ -e "$dest" ]; then
            move_to_tmp "$source" "目标目录中已存在"
        else
            echo "移动文件: $source → $dest_dir/ ($description)"
            mv "$source" "$dest"
        fi
    fi
}

# 处理MCP相关文件 → 07_workflow 或 08_ai_tools
echo "步骤: 整理MCP相关文件..."
for file in MCP_*.md; do
    if [ -f "$file" ]; then
        # MCP工作流相关 → 07_workflow
        if [[ "$file" =~ WORKFLOW|FLOW|CALL ]]; then
            move_to_dir "$file" "07_workflow" "MCP工作流"
        # MCP工具相关 → 08_ai_tools
        elif [[ "$file" =~ TOOLS|STANDARD|SPECIFICATION ]]; then
            move_to_dir "$file" "08_ai_tools" "MCP工具"
        else
            move_to_dir "$file" "07_workflow" "MCP相关"
        fi
    fi
done

# 处理工作流程相关文件 → 07_workflow
echo "步骤: 整理工作流程相关文件..."
for file in *WORKFLOW*.md ENGINEERING_WORKFLOW*.md STANDARD*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "07_workflow" "工作流程"
    fi
done

# 处理TENBAGGER相关文件 → 03_modules 或 strategy_kb
echo "步骤: 整理TENBAGGER相关文件..."
STRATEGY_DIR="strategy_kb"
mkdir -p "$STRATEGY_DIR"
for file in TENBAGGER*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "$STRATEGY_DIR" "TENBAGGER策略"
    fi
done

# 处理CODE_EMBEDDING相关文件（多个版本）→ tmp（只保留一个在08_ai_tools）
echo "步骤: 整理CODE_EMBEDDING相关文件（多个版本移到tmp）..."
code_embedding_moved=false
for file in CODE_EMBEDDING*.md; do
    if [ -f "$file" ]; then
        if [ "$code_embedding_moved" = false ] && [ ! -f "08_ai_tools/$file" ]; then
            # 保留第一个版本到08_ai_tools
            move_to_dir "$file" "08_ai_tools" "代码嵌入（保留一个版本）"
            code_embedding_moved=true
        else
            # 其他版本移到tmp
            move_to_tmp "$file" "CODE_EMBEDDING多个版本"
        fi
    fi
done

# 处理GUI相关文件 → 02_development_guides
echo "步骤: 整理GUI相关文件..."
for file in GUI_*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "GUI开发"
    fi
done

# 处理知识库相关文件 → knowledge_base_docs
echo "步骤: 整理知识库相关文件..."
KB_DIR="knowledge_base_docs"
mkdir -p "$KB_DIR"
for file in KB_*.md DATABASE_ARCHITECTURE*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "$KB_DIR" "知识库文档"
    fi
done

# 处理JQData相关文件（剩余）→ jqdata_docs
echo "步骤: 整理JQData相关文件（剩余）..."
JQDATA_DIR="jqdata_docs"
mkdir -p "$JQDATA_DIR"
for file in JQDATA*.md JOINQUANT*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "$JQDATA_DIR" "JQData文档"
    fi
done

# 处理其他开发相关文件 → 02_development_guides
echo "步骤: 整理其他开发相关文件..."
for file in SETUP_*.md INITIALIZATION*.md INSTALLATION*.md MONGODB*.md DATASOURCE*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "开发设置"
    fi
done

# 处理优化和测试相关文件
echo "步骤: 整理优化和测试相关文件..."
for file in OPTIMIZATION*.md TEST*.md TASK_SUMMARY*.md PHASE*.md COMPLETION*.md; do
    if [ -f "$file" ]; then
        if [[ "$file" =~ TEST ]]; then
            move_to_dir "$file" "06_testing_reports" "测试报告"
        else
            move_to_dir "$file" "02_development_guides" "开发相关"
        fi
    fi
done

# 处理研究和分析相关文件
echo "步骤: 整理研究和分析相关文件..."
for file in RESEARCH*.md ANALYSIS*.md CONTEXT*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "研究分析"
    fi
done

# 处理其他杂项文件
echo "步骤: 整理其他文件..."
for file in *.md; do
    if [ -f "$file" ]; then
        # 跳过已经在分类目录中的文件
        if [[ "$file" != "README.md" ]] && [[ "$file" != "DOCS_ORGANIZATION_PLAN.md" ]] && [[ "$file" != "DOCS_CLEANUP_REPORT.md" ]]; then
            # 如果文件名匹配特定模式，移动到相应目录
            if [[ "$file" =~ ^[0-9] ]]; then
                move_to_dir "$file" "09_legacy" "编号文件（可能是旧文件）"
            elif [[ "$file" =~ BACKUP|BACKUP_GUIDE|ORGANIZE ]]; then
                move_to_dir "$file" "09_legacy" "备份相关"
            else
                # 其他文件移动到legacy或保持原样（根据具体情况）
                echo "  未分类文件保留在根目录: $file"
            fi
        fi
    fi
done

echo ""
echo "✅ 整理完成！"
echo ""
echo "统计:"
echo "  tmp_old_files/ 目录大小: $(du -sh $TMP_DIR 2>/dev/null | cut -f1 || echo '0')"
echo "  剩余根目录文件数: $(find . -maxdepth 1 -type f | wc -l)"
echo ""
echo "各分类目录文件数:"
for dir in 01_architecture 02_development_guides 03_modules 04_platform_integration 05_reference_books 06_testing_reports 07_workflow 08_ai_tools jqdata_docs knowledge_base_docs strategy_kb; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -type f | wc -l)
        echo "  $dir: $count 个文件"
    fi
done





