#!/usr/bin/env bash

# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py


# Launch TaoRui Quant Professional inside a Docker container with GUI forwarding.
# This script will build the image if it does not exist, then run the PyQt GUI
# while mounting user config/log directories for persistence.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${JQQUANT_DOCKER_IMAGE:-jqquant/gui:latest}"
CONTAINER_NAME="${JQQUANT_DOCKER_CONTAINER:-jqquant-gui}"

DATA_ROOT="${HOME}/.local/share/trquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
MANUAL_DIR="${DATA_ROOT}/investment-manual"

BUILD_IMAGE=0
EXTRA_ARGS=()

usage() {
    cat <<EOF
Usage: $(basename "$0") [options] [-- docker-run-args]

Options:
  -b, --build         Force rebuild the Docker image before running
  -r, --remove-image  Remove existing image and build from scratch
  -h, --help          Show this help message

Any arguments after "--" are passed directly to "docker run".
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--build)
            BUILD_IMAGE=1
            shift
            ;;
        -r|--remove-image)
            docker image rm -f "${IMAGE_NAME}" >/dev/null 2>&1 || true
            BUILD_IMAGE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS=("$@")
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ docker command not found. Please install Docker first."
    exit 1
fi

mkdir -p "${CONFIG_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}" "${MANUAL_DIR}"

# Sync the latest investment manual so it can be accessed read-only in the container
if [[ -d "${PROJECT_ROOT}/investment-manual" ]]; then
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${PROJECT_ROOT}/investment-manual/" "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    else
        rm -rf "${MANUAL_DIR}"
        mkdir -p "${MANUAL_DIR}"
        cp -R "${PROJECT_ROOT}/investment-manual/." "${MANUAL_DIR}/" >/dev/null 2>&1 || true
    fi
fi

if [[ "${BUILD_IMAGE}" -eq 1 ]] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "🔨 Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"
fi

if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    echo "⚠️ Container ${CONTAINER_NAME} is already running. Stopping it first..."
    docker stop "${CONTAINER_NAME}" >/dev/null
fi

# Allow Docker containers to access the X11 server
if [[ -n "${DISPLAY:-}" ]] && command -v xhost >/dev/null 2>&1; then
    xhost +local:docker >/dev/null 2>&1 || true
fi

DISPLAY_ENV="${DISPLAY:-:0}"
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_MOUNT=()
if [[ -f "${XAUTH_FILE}" ]]; then
    XAUTH_MOUNT=(-v "${XAUTH_FILE}:/root/.Xauthority:ro")
fi

echo "🚀 Starting TaoRui Quant (Docker) ..."
docker run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -e DISPLAY="${DISPLAY_ENV}" \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    "${XAUTH_MOUNT[@]}" \
    -v "${CONFIG_DIR}:/app/config" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -v "${MANUAL_DIR}:/app/investment-manual:ro" \
    --device /dev/dri:/dev/dri \
    --ipc=host \
    "${EXTRA_ARGS[@]}" \
    "${IMAGE_NAME}" \
    python3 JQQuant.py

