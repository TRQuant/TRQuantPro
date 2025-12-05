#!/bin/bash
# TRQuant 扩展一键部署脚本
# 使用方法: ./deploy_extension.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "📦 开始部署 TRQuant 扩展..."

# 1. 编译 TypeScript
echo "🔨 编译 TypeScript..."
npm run compile

# 2. 打包为 .vsix 文件
echo "📦 打包扩展..."
npx @vscode/vsce package --allow-missing-repository --no-dependencies

# 3. 安装到 Cursor
echo "🚀 安装到 Cursor..."
VSIX_FILE=$(ls -t *.vsix | head -1)
cursor --install-extension "$VSIX_FILE" --force

echo ""
echo "✅ 部署完成！"
echo ""
echo "⚠️  请执行以下操作使更改生效："
echo "   1. 在 Cursor 中按 Ctrl+Shift+P"
echo "   2. 输入 'Developer: Reload Window'"
echo "   3. 按 Enter"







