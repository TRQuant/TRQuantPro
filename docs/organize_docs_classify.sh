#!/bin/bash
# docs目录分类整理脚本
# 将文件分门别类整理，重复/过时的文件移动到tmp文件夹

set -e

DOCS_DIR="/home/taotao/.cursor/worktrees/TRQuant/ope/docs"
cd "$DOCS_DIR"

TMP_DIR="tmp_old_files"
mkdir -p "$TMP_DIR"

echo "=== docs目录分类整理 ==="
echo "重复/过时文件将移动到: $TMP_DIR/"
echo ""

# 函数：安全移动文件到tmp（如果目标已存在）
move_to_tmp() {
    local source="$1"
    local reason="$2"
    
    if [ -e "$source" ]; then
        local basename_file=$(basename "$source")
        local dest="$TMP_DIR/$basename_file"
        
        # 如果tmp中已存在，添加序号
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

# 函数：移动文件到目标目录（如果目标不存在）
move_to_dir() {
    local source="$1"
    local dest_dir="$2"
    local description="$3"
    
    if [ -e "$source" ]; then
        mkdir -p "$dest_dir"
        local basename_file=$(basename "$source")
        local dest="$dest_dir/$basename_file"
        
        if [ -e "$dest" ]; then
            # 如果目标已存在，移动到tmp
            move_to_tmp "$source" "目标目录中已存在: $dest"
        else
            echo "移动文件: $source → $dest_dir/ ($description)"
            mv "$source" "$dest"
        fi
    fi
}

# 步骤1: 处理ExtentionDev目录
echo "步骤1: 处理ExtentionDev目录"
if [ -d "ExtentionDev" ] && [ -d "02_development_guides/ExtentionDev" ]; then
    echo "  发现重复的ExtentionDev目录，移动到tmp"
    move_to_tmp "ExtentionDev" "02_development_guides/ExtentionDev已存在"
elif [ -d "ExtentionDev" ]; then
    move_to_dir "ExtentionDev" "02_development_guides/ExtentionDev" "扩展开发文档"
fi
echo ""

# 步骤2: 处理Ptrade_coding目录
echo "步骤2: 处理Ptrade_coding目录"
if [ -d "Ptrade_coding" ] && [ -d "04_platform_integration/Ptrade_coding" ]; then
    echo "  发现重复的Ptrade_coding目录，移动到tmp"
    move_to_tmp "Ptrade_coding" "04_platform_integration/Ptrade_coding已存在"
elif [ -d "Ptrade_coding" ]; then
    move_to_dir "Ptrade_coding" "04_platform_integration/Ptrade_coding" "PTrade编码文档"
fi
echo ""

# 步骤3: 整理根目录的Markdown文件
echo "步骤3: 整理根目录文件（移动到相应分类目录）"
echo "这需要根据文件名模式分类..."
echo ""

# 架构相关文件
echo "  整理架构相关文件..."
for file in ARCHITECTURE*.md DATA_ANALYSIS_ARCHITECTURE.md DESIGN.md GUI_ARCHITECTURE.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "01_architecture" "架构文档"
    fi
done

# 开发指南相关文件
echo "  整理开发指南相关文件..."
for file in INSTALLATION.md DEVELOPMENT*.md PROJECT*.md CURSOR*.md mcp_setup_guide.md CONFIG_VERIFICATION.md REVIEW_CHECKLIST.md DEV_DEBUG*.md COMPLETE_DEVELOPMENT*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "02_development_guides" "开发指南"
    fi
done

# 模块相关文件
echo "  整理模块相关文件..."
for file in CANDIDATE_POOL*.md FACTOR*.md MARKET_TREND*.md DATA_SOURCE*.md STOCK_SELECTION*.md TIME_DIMENSION*.md FIVE_DIMENSION*.md HEATMAP*.md MAINLINE*.md FUNDS_DIMENSION*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "03_modules" "模块文档"
    fi
done

# 平台集成相关文件
echo "  整理平台集成相关文件..."
for file in PTRADE*.md QMT*.md QUANTCONNECT*.md ALLTICK*.md AKSHARE*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "04_platform_integration" "平台集成"
    fi
done

# JQData相关文件 - 创建专门目录或放在根目录
echo "  整理JQData相关文件..."
JQDATA_DIR="jqdata_docs"
mkdir -p "$JQDATA_DIR"
for file in JQDATA*.md JOINQUANT*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "$JQDATA_DIR" "JQData文档"
    fi
done

# 工作流程相关文件
echo "  整理工作流程相关文件..."
for file in WORKFLOW*.md MCP_WORKFLOW*.md STANDARD*.md ENGINEERING_WORKFLOW*.md INVESTMENT_WORKFLOW*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "07_workflow" "工作流程"
    fi
done

# AI工具相关文件
echo "  整理AI工具相关文件..."
for file in AI_MODEL*.md AI_TOOL*.md AUTO_COMMIT_GUIDE.md chat_history_backup.md finance-glossary*.md glossary-api*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "08_ai_tools" "AI工具"
    fi
done

# Git相关文件
echo "  整理Git相关文件..."
GIT_DIR="02_development_guides/git"
mkdir -p "$GIT_DIR"
for file in GIT_*.md GIT_SETUP*.md GIT_SAFETY*.md GIT_WORKDIRECTORY*.md GIT_RESET*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "$GIT_DIR" "Git文档"
    fi
done

# 代码嵌入相关文件（很多版本，移动到tmp）
echo "  整理代码嵌入相关文件（多个版本，移动到tmp）..."
for file in CODE_EMBEDDING*.md; do
    if [ -f "$file" ]; then
        # 检查是否在相应目录中已有
        if [ -f "02_development_guides/$file" ] || [ -f "08_ai_tools/$file" ]; then
            move_to_tmp "$file" "已存在于分类目录中"
        else
            move_to_dir "$file" "08_ai_tools" "代码嵌入（保留一个版本）"
        fi
    fi
done

# 知识库相关文件
echo "  整理知识库相关文件..."
KB_DIR="knowledge_base_docs"
mkdir -p "$KB_DIR"
for file in KB_*.md DATABASE_ARCHITECTURE*.md KB_RAG*.md KB_SEARCH*.md KB_GROUNDING*.md; do
    if [ -f "$file" ]; then
        move_to_dir "$file" "$KB_DIR" "知识库文档"
    fi
done

echo ""
echo "步骤4: 处理其他文件"
echo "  移动PDF文件到05_reference_books（如果不在那里）..."
for file in *.pdf; do
    if [ -f "$file" ] && [ ! -f "05_reference_books/$file" ]; then
        move_to_dir "$file" "05_reference_books" "参考书籍"
    fi
done

echo ""
echo "✅ 整理完成！"
echo ""
echo "统计:"
echo "  tmp_old_files/ 目录大小: $(du -sh $TMP_DIR 2>/dev/null | cut -f1 || echo '0')"
echo "  剩余根目录文件数: $(find . -maxdepth 1 -type f | wc -l)"
echo ""
echo "下一步:"
echo "1. 检查 tmp_old_files/ 目录确认重复/过时文件"
echo "2. 审查后可以删除tmp目录或保留备份"
echo "3. 运行 git status 查看更改"





