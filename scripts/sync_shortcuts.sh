#!/usr/bin/env bash
# Sync TaoRui Quant desktop + dock shortcuts so they open the same build
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
INSTALL_DIR="${JQQUANT_INSTALL_DIR:-$HOME/.local/share/trquant}"
LAUNCHER_PATH="$HOME/.local/bin/jqquant"
APPLICATIONS_DIR="$HOME/.local/share/applications"
ICON_TARGET="$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
DESKTOP_ENTRY="$APPLICATIONS_DIR/jqquant.desktop"
USER_DESKTOP="${XDG_DESKTOP_DIR:-$HOME/Desktop}"
DESKTOP_SHORTCUT="$USER_DESKTOP/jqquant.desktop"
ICON_SOURCE="$PROJECT_ROOT/gui/resources/jqquant_icon.svg"

mkdir -p "$HOME/.local/bin" \
         "$APPLICATIONS_DIR" \
         "$HOME/.local/share/icons/hicolor/256x256/apps"

if command -v xdg-user-dir >/dev/null 2>&1; then
    USER_DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || echo "$USER_DESKTOP")"
    DESKTOP_SHORTCUT="$USER_DESKTOP/jqquant.desktop"
fi

if [ ! -d "$INSTALL_DIR" ]; then
    echo "[sync-shortcuts] Warning: install dir $INSTALL_DIR not found, fallback to project root"
fi

cp "$ICON_SOURCE" "$ICON_TARGET"

cat > "$LAUNCHER_PATH" <<EOF_LAUNCHER
#!/usr/bin/env bash
set -euo pipefail

# 检测运行模式
if [ -f "${PROJECT_ROOT}/JQQuant.py" ] && [ -n "\${JQQUANT_USE_DEV:-}" ]; then
    # 开发模式：使用主项目目录
    APP_DIR="${PROJECT_ROOT}"
    export JQQUANT_DEV_MODE=1
else
    # 生产模式：使用安装目录
    APP_DIR="${INSTALL_DIR}"
fi

# 如果开发模式目录不存在，回退到安装目录
if [ ! -f "\${APP_DIR}/JQQuant.py" ]; then
    APP_DIR="${INSTALL_DIR}"
fi

if [ ! -f "\${APP_DIR}/JQQuant.py" ]; then
    echo "错误: 找不到JQQuant.py"
    echo "  尝试位置1: ${PROJECT_ROOT}/JQQuant.py"
    echo "  尝试位置2: ${INSTALL_DIR}/JQQuant.py"
    exit 1
fi

cd "\${APP_DIR}" || exit 1

# 激活虚拟环境（如果存在）
if [ -f "\${APP_DIR}/venv/bin/activate" ]; then
    source "\${APP_DIR}/venv/bin/activate"
fi

exec python3 JQQuant.py "\$@"
EOF_LAUNCHER
chmod +x "$LAUNCHER_PATH"

cat > "$DESKTOP_ENTRY" <<EOF_DESKTOP
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=$LAUNCHER_PATH
Icon=$ICON_TARGET
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF_DESKTOP

if [ -d "$USER_DESKTOP" ]; then
    cp "$DESKTOP_ENTRY" "$DESKTOP_SHORTCUT"
fi

update-desktop-database "$APPLICATIONS_DIR" >/dev/null 2>&1 || true
gtk-update-icon-cache -f "$HOME/.local/share/icons/hicolor" >/dev/null 2>&1 || true

echo "✅ dock 与桌面快捷方式已同步，均指向 $LAUNCHER_PATH"
