#!/bin/bash
# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"






# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"




# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"

# JQQuant 卸载脚本

INSTALL_DIR="$HOME/.local/share/trquant"

echo "========================================"
echo "  JQQuant 卸载程序"
echo "========================================"
echo ""

# 确认卸载
read -p "确定要卸载 JQQuant 吗? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

echo ""
echo "正在卸载..."

# 删除程序文件
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ 已删除程序文件"
fi

# 删除启动脚本
if [ -f "$HOME/.local/bin/jqquant" ]; then
    rm -f "$HOME/.local/bin/jqquant"
    echo "✓ 已删除启动脚本"
fi

# 删除桌面文件
if [ -f "$HOME/.local/share/applications/jqquant.desktop" ]; then
    rm -f "$HOME/.local/share/applications/jqquant.desktop"
    echo "✓ 已删除桌面快捷方式"
fi

# 删除图标
if [ -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg" ]; then
    rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
    echo "✓ 已删除图标"
fi

# 更新桌面数据库
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 卸载完成！"
echo "========================================"














