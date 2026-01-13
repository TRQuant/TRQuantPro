#!/bin/bash
# 合并abd目录到ope目录的脚本
# 用途: 将abd中的文件合并到ope，然后删除abd目录
# 日期: 2026-01-11

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 合并abd目录到ope目录${NC}"
echo "=========================================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ABD_DIR="$PROJECT_ROOT/../abd"
OPE_DIR="$PROJECT_ROOT"

# 检查目录
if [ ! -d "$OPE_DIR" ]; then
    echo -e "${RED}❌ ope目录不存在: $OPE_DIR${NC}"
    exit 1
fi

if [ ! -d "$ABD_DIR" ]; then
    echo -e "${YELLOW}⚠️  abd目录不存在，可能已经合并或删除${NC}"
    exit 0
fi

echo -e "${YELLOW}📦 ope目录: $OPE_DIR${NC}"
echo -e "${YELLOW}📦 abd目录: $ABD_DIR${NC}"
echo ""

# 合并文件
echo "📋 合并文件..."
rsync -av --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' --exclude='.venv' "$ABD_DIR/" "$OPE_DIR/"

echo ""
echo -e "${GREEN}✅ 文件合并完成${NC}"

# 询问是否删除abd目录
echo ""
read -p "是否删除abd目录? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  删除abd目录..."
    rm -rf "$ABD_DIR"
    echo -e "${GREEN}✅ abd目录已删除${NC}"
else
    echo -e "${YELLOW}⚠️  保留abd目录（可以手动删除）${NC}"
fi

echo ""
echo -e "${GREEN}✨ 合并完成！${NC}"
echo -e "${YELLOW}下一步: 从ope目录运行打包脚本${NC}"
echo -e "${YELLOW}  cd $OPE_DIR${NC}"
echo -e "${YELLOW}  ./scripts/package_for_windows.sh${NC}"
