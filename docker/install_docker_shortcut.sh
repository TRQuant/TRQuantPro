#!/usr/bin/env bash

# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"







# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"





# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"


# Install a desktop shortcut that launches TaoRui Quant (Docker) from the Ubuntu dock.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

LAUNCHER_SRC="${PROJECT_ROOT}/docker/run_gui_container.sh"
LAUNCHER_BIN="${BIN_DIR}/jqquant-docker"
DESKTOP_FILE="${DESKTOP_DIR}/jqquant-docker.desktop"
ICON_SRC="${PROJECT_ROOT}/gui/resources/jqquant_icon.svg"
ICON_DST="${ICON_DIR}/jqquant-docker.svg"

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

cp "${LAUNCHER_SRC}" "${LAUNCHER_BIN}"
chmod +x "${LAUNCHER_BIN}"

if [[ -f "${ICON_SRC}" ]]; then
    cp "${ICON_SRC}" "${ICON_DST}"
fi

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=韬睿量化 (Docker)
Comment=Launch TaoRui Quant Professional via Docker container
Exec=${LAUNCHER_BIN}
Icon=${ICON_DST}
Terminal=false
Type=Application
Categories=Finance;Office;
StartupNotify=true
EOF

update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

echo "✅ Desktop shortcut installed:"
echo "   - Binary launcher : ${LAUNCHER_BIN}"
echo "   - Desktop entry   : ${DESKTOP_FILE}"
echo ""
echo "在 GNOME Show Applications 中搜索 “韬睿量化 (Docker)” 即可添加到 Dock。"














