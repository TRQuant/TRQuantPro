#!/bin/bash
# TRQuant Cursor Extension - Linux/macOS 安装脚本
# 用法: ./scripts/setup.sh

set -e

echo "=========================================="
echo "  TRQuant Cursor Extension 安装脚本"
echo "  平台: Linux/macOS"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 未安装${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1 已安装: $($1 --version 2>/dev/null | head -1)${NC}"
        return 0
    fi
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTENSION_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$EXTENSION_DIR")"

echo ""
echo "📁 项目路径: $PROJECT_ROOT"
echo "📁 Extension路径: $EXTENSION_DIR"
echo ""

# 1. 检查依赖
echo "🔍 检查系统依赖..."
echo "-------------------"

DEPS_OK=true

if ! check_command node; then
    echo -e "${YELLOW}   请安装Node.js: https://nodejs.org/${NC}"
    DEPS_OK=false
fi

if ! check_command npm; then
    DEPS_OK=false
fi

if ! check_command python3; then
    if ! check_command python; then
        echo -e "${YELLOW}   请安装Python: https://www.python.org/${NC}"
        DEPS_OK=false
    fi
fi

if [ "$DEPS_OK" = false ]; then
    echo ""
    echo -e "${RED}请先安装缺失的依赖后重新运行此脚本${NC}"
    exit 1
fi

echo ""

# 2. 安装Node依赖
echo "📦 安装Node依赖..."
echo "-------------------"
cd "$EXTENSION_DIR"
npm install
echo -e "${GREEN}✓ Node依赖安装完成${NC}"
echo ""

# 3. 创建Python虚拟环境（如果不存在）
echo "🐍 配置Python环境..."
echo "-------------------"
cd "$PROJECT_ROOT"

if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv || python -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装Python依赖
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo -e "${GREEN}✓ Python环境配置完成${NC}"
echo ""

# 4. 构建Extension
echo "🔨 构建Extension..."
echo "-------------------"
cd "$EXTENSION_DIR"
npm run compile
echo -e "${GREEN}✓ Extension构建完成${NC}"
echo ""

# 5. 创建配置文件
echo "⚙️  创建配置文件..."
echo "-------------------"

PYTHON_PATH="$PROJECT_ROOT/venv/bin/python"

# 创建.vscode/settings.json（用于开发）
mkdir -p "$EXTENSION_DIR/.vscode"
cat > "$EXTENSION_DIR/.vscode/settings.json" << EOF
{
  "trquant.pythonPath": "$PYTHON_PATH",
  "trquant.serverHost": "127.0.0.1",
  "trquant.serverPort": 5000,
  "trquant.mcpEnabled": true
}
EOF

echo -e "${GREEN}✓ 配置文件已创建${NC}"
echo ""

# 6. 验证安装
echo "🧪 验证安装..."
echo "-------------------"

# 测试bridge.py
TEST_RESULT=$(echo '{"action": "get_market_status", "params": {}}' | "$PYTHON_PATH" "$EXTENSION_DIR/python/bridge.py" 2>/dev/null)
if echo "$TEST_RESULT" | grep -q '"ok": true'; then
    echo -e "${GREEN}✓ bridge.py 工作正常${NC}"
else
    echo -e "${YELLOW}⚠ bridge.py 返回: $TEST_RESULT${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ 安装完成！${NC}"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 在Cursor中按F5启动调试模式"
echo "2. 或运行 'npm run package' 打包VSIX"
echo "3. 在新窗口中测试 'TRQuant: 获取市场状态' 命令"
echo ""
echo "配置文件位置："
echo "  $EXTENSION_DIR/.vscode/settings.json"
echo ""

