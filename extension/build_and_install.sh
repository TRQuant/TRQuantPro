#!/bin/bash
# TRQuant Extension 一键构建和安装脚本

set -e  # 遇到错误立即退出

echo "================================================"
echo "  TRQuant Cursor Extension 构建脚本"
echo "================================================"
echo ""

# 进入扩展目录
cd "$(dirname "$0")"
EXTENSION_DIR=$(pwd)
echo "📁 工作目录: $EXTENSION_DIR"
echo ""

# 步骤1：检查环境
echo "🔍 步骤1：检查环境..."
echo "   Node.js: $(node --version 2>/dev/null || echo '未安装')"
echo "   npm: $(npm --version 2>/dev/null || echo '未安装')"
echo "   Python: $(python --version 2>/dev/null || python3 --version 2>/dev/null || echo '未安装')"
echo ""

# 步骤2：安装依赖
echo "📦 步骤2：安装依赖..."
npm install --silent
echo "   ✅ npm依赖安装完成"
echo ""

# 步骤3：编译TypeScript
echo "🔨 步骤3：编译TypeScript..."
npm run compile
echo "   ✅ 编译完成"
echo ""

# 检查dist目录
if [ -f "dist/extension.js" ]; then
    echo "   📄 dist/extension.js 已生成"
else
    echo "   ❌ 编译失败，未找到extension.js"
    exit 1
fi
echo ""

# 步骤4：打包VSIX
echo "📦 步骤4：打包VSIX..."
npx @vscode/vsce package --allow-missing-repository --no-dependencies
echo "   ✅ 打包完成"
echo ""

# 查找生成的vsix文件
VSIX_FILE=$(ls -t *.vsix 2>/dev/null | head -1)
if [ -n "$VSIX_FILE" ]; then
    echo "   📄 生成文件: $VSIX_FILE"
else
    echo "   ❌ 打包失败，未找到vsix文件"
    exit 1
fi
echo ""

# 步骤5：安装到Cursor
echo "🚀 步骤5：安装到Cursor..."
if command -v cursor &> /dev/null; then
    cursor --install-extension "$VSIX_FILE"
    echo "   ✅ 安装完成"
else
    echo "   ⚠️ 未找到cursor命令，请手动安装:"
    echo "      cursor --install-extension $EXTENSION_DIR/$VSIX_FILE"
fi
echo ""

echo "================================================"
echo "  🎉 构建完成！"
echo "================================================"
echo ""
echo "下一步操作："
echo "  1. 重启Cursor"
echo "  2. 按 Ctrl+Shift+P 输入 'TRQuant' 查看命令"
echo "  3. 或点击左侧边栏的TRQuant图标"
echo ""
echo "调试模式："
echo "  在Cursor中打开 $EXTENSION_DIR 后按F5"
echo ""







