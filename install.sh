#!/usr/bin/env bash
# JQQuant 安装脚本
# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"


# 将当前源码完整部署为桌面应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/share/trquant"
LAUNCHER_PATH="${HOME}/.local/bin/jqquant"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
ICON_SOURCE="${SCRIPT_DIR}/gui/resources/jqquant_icon.svg"
ICON_TARGET="${ICON_DIR}/jqquant.svg"

echo "========================================"
echo "  JQQuant 安装程序"
echo "========================================"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""

AUTO_YES="${JQQUANT_AUTO_YES:-false}"

if [[ "${AUTO_YES}" == "true" ]]; then
    echo "已自动确认安装（JQQUANT_AUTO_YES=true）"
else
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
fi

if [[ -d "${INSTALL_DIR}" ]]; then
    echo ""
    echo "检测到已有安装: ${INSTALL_DIR}"
    if [[ "${AUTO_YES}" == "true" ]]; then
        echo "已自动确认覆盖现有安装"
    else
        read -p "是否覆盖并安装最新版? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    rm -rf "${INSTALL_DIR}"
fi

echo ""
echo "1. 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${HOME}/.local/bin"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

echo "2. 复制程序文件..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a \
        --exclude ".git/" \
        --exclude ".cursor/" \
        --exclude "__pycache__/" \
        --exclude ".mypy_cache/" \
        --exclude ".pytest_cache/" \
        --exclude "venv/" \
        --exclude "terminals/" \
        --exclude "*.pyc" \
        --exclude "*.pyo" \
        "${SCRIPT_DIR}/" "${INSTALL_DIR}/"
else
    echo "⚠️ 未检测到 rsync，将使用 cp -r 拷贝（包含全部文件）"
    cp -r "${SCRIPT_DIR}/." "${INSTALL_DIR}/"
fi

echo "3. 创建虚拟环境..."
python3 -m venv "${INSTALL_DIR}/venv"

echo "4. 安装依赖..."
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "${INSTALL_DIR}/requirements.txt" -q
deactivate

echo "5. 创建启动脚本..."
cat > "${LAUNCHER_PATH}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DEFAULT_APP_DIR="${HOME}/.local/share/trquant"
FALLBACK_APP_DIR="${HOME}/dev/QuantTest/TRQuant"
APP_DIR="${JQQUANT_APP_DIR:-${DEFAULT_APP_DIR}}"

if [[ ! -f "${APP_DIR}/JQQuant.py" ]]; then
  APP_DIR="${FALLBACK_APP_DIR}"
fi

cd "${APP_DIR}" || exit 1
if [[ -f "venv/bin/activate" ]]; then
  source "venv/bin/activate"
fi
export PYTHONPATH="${APP_DIR}:${PYTHONPATH:-}"
exec python3 JQQuant.py "$@"
EOF
chmod +x "${LAUNCHER_PATH}"

echo "6. 创建桌面快捷方式..."
cat > "${DESKTOP_DIR}/jqquant.desktop" <<EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=韬睿量化
Comment=机构级量化投研平台
Exec=${LAUNCHER_PATH}
Icon=${ICON_TARGET}
Terminal=false
Categories=Finance;Office;Development;
StartupNotify=true
StartupWMClass=JQQuant
EOF

echo "7. 安装图标..."
cp "${ICON_SOURCE}" "${ICON_TARGET}"

echo "8. 更新桌面数据库..."
update-desktop-database "${DESKTOP_DIR}" 2>/dev/null || true
gtk-update-icon-cache -f "${HOME}/.local/share/icons/hicolor/" 2>/dev/null || true

echo ""
echo "========================================"
echo "  ✅ 安装完成！"
echo "========================================"
echo ""
echo "启动方式："
echo "  1. 在应用菜单中搜索 “韬睿量化” 或 “JQQuant”"
echo "  2. 在终端中运行: jqquant"
echo ""
echo "如果应用菜单中未立即刷新，请注销后重新登录。"
echo ""
echo "卸载命令: rm -rf ${INSTALL_DIR} ${LAUNCHER_PATH} ${DESKTOP_DIR}/jqquant.desktop"

