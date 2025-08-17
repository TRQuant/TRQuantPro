#!/bin/bash
# QuantConnect Research 工作区自动化设置脚本
# 用法: ./setup_workspace.sh [workspace_name]

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查依赖
check_dependencies() {
    print_info "检查依赖..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        exit 1
    fi
    
    # 检查 Lean CLI
    if ! command -v lean &> /dev/null; then
        print_warning "Lean CLI 未安装，请先安装: pipx install lean"
        exit 1
    fi
    
    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装"
        exit 1
    fi
    
    print_success "依赖检查完成"
}

# 初始化工作区
init_workspace() {
    local workspace_name=${1:-"QuantTest"}
    
    print_info "初始化工作区: $workspace_name"
    
    # 创建目录
    mkdir -p "$workspace_name"
    cd "$workspace_name"
    
    # 初始化 Lean 环境
    if [ ! -f "lean.json" ]; then
        print_info "初始化 Lean 环境..."
        lean init
        print_success "Lean 环境初始化完成"
    else
        print_info "Lean 环境已存在"
    fi
    
    # 创建 Scripts 目录
    if [ ! -d "Scripts" ]; then
        mkdir -p Scripts
        print_info "创建 Scripts 目录"
    fi
    
    print_success "工作区初始化完成"
}

# 下载基础数据
download_basic_data() {
    print_info "下载基础数据..."
    
    # 下载主要指数
    print_info "下载主要指数数据..."
    python3 Scripts/data_downloader.py --indices || print_warning "指数数据下载失败"
    
    # 下载行业ETF
    print_info "下载行业ETF数据..."
    python3 Scripts/data_downloader.py --sectors || print_warning "行业ETF数据下载失败"
    
    # 下载商品
    print_info "下载商品数据..."
    python3 Scripts/data_downloader.py --commodities || print_warning "商品数据下载失败"
    
    print_success "基础数据下载完成"
}

# 创建常用笔记本
create_common_notebooks() {
    print_info "创建常用笔记本..."
    
    # 市场分析笔记本
    python3 Scripts/create_research_notebook.py market_analysis --template data_analysis || print_warning "市场分析笔记本创建失败"
    
    # 策略开发笔记本
    python3 Scripts/create_research_notebook.py strategy_development --template strategy || print_warning "策略开发笔记本创建失败"
    
    # 回测分析笔记本
    python3 Scripts/create_research_notebook.py backtest_analysis --template backtest || print_warning "回测分析笔记本创建失败"
    
    # 基础研究笔记本
    python3 Scripts/create_research_notebook.py basic_research --template basic || print_warning "基础研究笔记本创建失败"
    
    print_success "常用笔记本创建完成"
}

# 配置笔记本
configure_notebooks() {
    print_info "配置笔记本..."
    
    # 添加标准配置
    python3 Scripts/notebook_manager.py batch-add-config || print_warning "笔记本配置失败"
    
    # 生成索引
    python3 Scripts/notebook_manager.py index || print_warning "索引生成失败"
    
    print_success "笔记本配置完成"
}

# 启动 Research 环境
start_research() {
    print_info "启动 Research 环境..."
    
    # 检查是否已有容器运行
    if docker ps --filter "ancestor=quantconnect/research" -q | grep -q .; then
        print_info "Research 容器已在运行"
    else
        print_info "启动 Research 容器..."
        lean research . --port 8888 &
        sleep 5  # 等待容器启动
        
        if docker ps --filter "ancestor=quantconnect/research" -q | grep -q .; then
            print_success "Research 环境启动成功"
            print_info "Jupyter 服务器地址: http://127.0.0.1:8888"
        else
            print_warning "Research 环境启动失败"
        fi
    fi
}

# 显示使用说明
show_usage() {
    print_info "工作区设置完成！"
    echo
    echo "📋 使用说明:"
    echo "1. 启动 Research 环境: lean research . --port 8888"
    echo "2. 在 VS Code/Cursor 中连接 Jupyter 服务器: http://127.0.0.1:8888"
    echo "3. 开始使用笔记本进行研究"
    echo
    echo "🛠️  可用工具:"
    echo "- 创建笔记本: python3 Scripts/create_research_notebook.py <name> --template <template>"
    echo "- 下载数据: python3 Scripts/data_downloader.py <symbol>"
    echo "- 分析回测: python3 Scripts/backtest_analyzer.py <backtest_id>"
    echo "- 管理笔记本: python3 Scripts/notebook_manager.py <command>"
    echo
    echo "📚 文档:"
    echo "- 环境设置: QuantConnect_Research_Start.md"
    echo "- 脚本使用: Scripts/README.md"
}

# 主函数
main() {
    local workspace_name=${1:-"QuantTest"}
    
    echo "🚀 QuantConnect Research 工作区自动化设置"
    echo "=========================================="
    
    # 检查依赖
    check_dependencies
    
    # 初始化工作区
    init_workspace "$workspace_name"
    
    # 下载基础数据
    download_basic_data
    
    # 创建常用笔记本
    create_common_notebooks
    
    # 配置笔记本
    configure_notebooks
    
    # 启动 Research 环境
    start_research
    
    # 显示使用说明
    show_usage
    
    print_success "工作区设置完成！"
}

# 脚本入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi 