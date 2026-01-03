#!/bin/bash
# MCP配置验证脚本

echo "🔍 验证MCP配置..."

# 检查配置文件
if [ -f ".cursor/mcp.json" ]; then
    echo "✅ .cursor/mcp.json 存在"
    
    # 验证JSON格式
    if python3 -m json.tool .cursor/mcp.json > /dev/null 2>&1; then
        echo "✅ JSON格式正确"
    else
        echo "❌ JSON格式错误"
        exit 1
    fi
else
    echo "⚠️  .cursor/mcp.json 不存在"
    echo "   请从 .cursor/mcp.json.template 创建"
    exit 1
fi

# 检查依赖
echo ""
echo "📦 检查依赖..."

# Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
else
    echo "❌ Node.js 未安装"
fi

# npm
if command -v npm &> /dev/null; then
    echo "✅ npm: $(npm --version)"
else
    echo "❌ npm 未安装"
fi

# Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
else
    echo "❌ Python 未安装"
fi

# uvx (可选)
if command -v uvx &> /dev/null; then
    echo "✅ uvx 已安装"
else
    echo "⚠️  uvx 未安装（Git服务器需要）"
    echo "   安装: pip install uv 或 curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

echo ""
echo "✅ 配置验证完成"
