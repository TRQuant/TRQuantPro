#!/bin/bash
# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"






# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"




# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"

# 创建 .deb 安装包
# 适用于 Ubuntu/Debian 系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="2.0.0"
PACKAGE_NAME="jqquant"
BUILD_DIR="$PROJECT_DIR/build/deb"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant DEB 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建DEB包结构..."
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"
mkdir -p "$DEB_ROOT/DEBIAN"
mkdir -p "$DEB_ROOT/opt/jqquant"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps"

echo "2. 创建控制文件..."
cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: finance
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-numpy, python3-pandas
Maintainer: JQQuant Team <jqquant@example.com>
Description: JQQuant Quantitative Trading Platform
 A quantitative trading platform based on JQData API.
 Features include strategy development, backtesting,
 and live trading support.
Homepage: https://github.com/ZhuTechLLC/JQQuant
EOF

echo "3. 创建安装后脚本..."
cat > "$DEB_ROOT/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# 更新图标缓存
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "JQQuant 安装完成！"
echo "您可以通过以下方式启动："
echo "  1. 在应用菜单中搜索 'JQQuant'"
echo "  2. 在终端中运行 'jqquant'"
EOF
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

echo "4. 创建卸载前脚本..."
cat > "$DEB_ROOT/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "正在卸载 JQQuant..."
EOF
chmod 755 "$DEB_ROOT/DEBIAN/prerm"

echo "5. 复制项目文件..."
cp -r "$PROJECT_DIR/gui" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/core" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/utils" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$DEB_ROOT/opt/jqquant/"
cp -r "$PROJECT_DIR/config" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/main.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$DEB_ROOT/opt/jqquant/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_ROOT/opt/jqquant/"

echo "6. 创建启动脚本..."
cat > "$DEB_ROOT/usr/bin/jqquant" << 'EOF'
#!/bin/bash
export PYTHONPATH="/opt/jqquant:$PYTHONPATH"
cd /opt/jqquant
exec python3 JQQuant.py "$@"
EOF
chmod 755 "$DEB_ROOT/usr/bin/jqquant"

echo "7. 创建桌面文件..."
cat > "$DEB_ROOT/usr/share/applications/jqquant.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=JQQuant
Name[zh_CN]=JQQuant量化交易
Comment=Quantitative Trading Platform
Comment[zh_CN]=量化交易平台
Exec=jqquant
Icon=jqquant
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
Keywords=quant;trading;stock;finance;backtest;
EOF

echo "8. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/jqquant.svg"

echo "9. 构建DEB包..."
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OUTPUT_DIR/"

echo ""
echo "========================================"
echo "  DEB包创建完成！"
echo "========================================"
echo ""
echo "安装包位置: $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo ""
echo "安装命令:"
echo "  sudo dpkg -i $OUTPUT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
echo "  sudo apt-get install -f  # 安装依赖"
echo ""
echo "卸载命令:"
echo "  sudo apt remove jqquant"














