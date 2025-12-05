#!/bin/bash
# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"






# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"




# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"

# 创建 AppImage 可执行文件
# AppImage 是一个单文件可执行程序，双击即可运行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build/AppDir"
OUTPUT_DIR="$PROJECT_DIR/dist"

echo "========================================"
echo "  JQQuant AppImage 打包工具"
echo "========================================"
echo ""

# 清理旧构建
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

echo "1. 创建AppDir结构..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/jqquant"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

echo "2. 复制项目文件..."
# 复制主要代码
cp -r "$PROJECT_DIR/gui" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/core" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/strategies" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/jqdata" "$BUILD_DIR/usr/lib/jqquant/"
cp -r "$PROJECT_DIR/config" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/usr/lib/jqquant/"
cp "$PROJECT_DIR/JQQuant.py" "$BUILD_DIR/usr/lib/jqquant/"

echo "3. 创建启动脚本..."
cat > "$BUILD_DIR/usr/bin/jqquant" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/jqquant"

echo "4. 创建桌面文件..."
cat > "$BUILD_DIR/usr/share/applications/jqquant.desktop" << EOF
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
EOF

# 复制桌面文件到AppDir根目录
cp "$BUILD_DIR/usr/share/applications/jqquant.desktop" "$BUILD_DIR/"

echo "5. 复制图标..."
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/jqquant.svg"
cp "$PROJECT_DIR/gui/resources/jqquant_icon.svg" "$BUILD_DIR/jqquant.svg"

echo "6. 创建AppRun..."
cat > "$BUILD_DIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$APPDIR/usr/lib/jqquant:$PYTHONPATH"
cd "$APPDIR/usr/lib/jqquant"
exec python3 JQQuant.py "$@"
EOF
chmod +x "$BUILD_DIR/AppRun"

echo ""
echo "========================================"
echo "  AppDir 结构创建完成！"
echo "========================================"
echo ""
echo "AppDir位置: $BUILD_DIR"
echo ""
echo "要创建AppImage，需要下载appimagetool:"
echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
echo "  chmod +x appimagetool-x86_64.AppImage"
echo "  ./appimagetool-x86_64.AppImage $BUILD_DIR $OUTPUT_DIR/JQQuant.AppImage"
echo ""
echo "或者直接运行AppDir中的AppRun测试:"
echo "  $BUILD_DIR/AppRun"














