# 完整开发工作流方案

## 🎯 核心目标

1. ✅ **安全同步**：不丢失任何文件
2. ✅ **主项目开发**：在Cursor中开发，能看到实际效果
3. ✅ **快捷方式**：保持Dock快捷方式可用
4. ✅ **Docker部署**：跨平台安装和运行

---

## 📋 方案总览

### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    开发环境（主项目）                          │
│  /home/taotao/dev/QuantTest/TRQuant                         │
│  - Git仓库                                                    │
│  - Cursor管理                                                  │
│  - 源代码开发                                                  │
└─────────────────────────────────────────────────────────────┘
                        ↕ 双向同步
┌─────────────────────────────────────────────────────────────┐
│                    运行环境（安装目录）                        │
│  ~/.local/share/jqquant                                     │
│  - 桌面应用安装                                               │
│  - 快捷方式指向                                               │
│  - Docker挂载                                                 │
└─────────────────────────────────────────────────────────────┘
                        ↕ Docker挂载
┌─────────────────────────────────────────────────────────────┐
│                    Docker容器                                 │
│  - 跨平台运行                                                 │
│  - 数据持久化                                                 │
│  - 配置独立                                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔒 第一部分：安全同步（不丢失文件）

### 1.1 同步策略

**原则**：
- ✅ 只复制文件，不删除目标文件
- ✅ 如果目标文件较新，跳过（不覆盖）
- ✅ 支持备份
- ✅ 支持干运行（预览）

### 1.2 使用安全同步脚本

```bash
# 1. 预览模式（不实际复制）
cd ~/.local/share/jqquant
python scripts/sync_to_main_project_safe.py --dry-run

# 2. 实际同步（带备份）
python scripts/sync_to_main_project_safe.py --backup

# 3. 仅同步（不备份）
python scripts/sync_to_main_project_safe.py
```

### 1.3 同步内容

**会同步**：
- 代码文件（`gui/`, `markets/`, `core/`等）
- 文档文件（`docs/`）
- 配置文件（`config/`，不含敏感信息）
- 脚本文件（`scripts/`）

**不会同步**（避免覆盖）：
- Git目录（`.git/`）
- 缓存文件（`__pycache__/`, `*.pyc`）
- 数据文件（`data/`, `cache/`, `logs/`）
- 虚拟环境（`venv/`）

### 1.4 安全保证

1. **备份机制**：
   ```bash
   # 自动备份到主目录的父目录
   /home/taotao/dev/QuantTest/TRQuant_backup_20241129_120000
   ```

2. **文件保护**：
   - 不删除目标文件
   - 不覆盖较新的文件
   - 保留Git历史

3. **日志记录**：
   - 详细记录每个操作
   - 显示跳过的文件及原因

---

## 💻 第二部分：主项目开发（看到实际效果）

### 2.1 开发环境配置

#### 步骤1：修改配置支持开发模式

**修改 `config/settings.py`**：

```python
import os
from pathlib import Path

# 检测运行模式
def get_project_root():
    """获取项目根目录"""
    # 优先使用环境变量
    if os.getenv('JQQUANT_DEV_MODE') == '1':
        return Path('/home/taotao/dev/QuantTest/TRQuant')
    
    # 检测当前文件位置
    current_file = Path(__file__).resolve()
    current_path = str(current_file)
    
    # 如果在dev目录，使用主项目
    if 'dev/QuantTest/TRQuant' in current_path:
        return Path('/home/taotao/dev/QuantTest/TRQuant')
    
    # 默认使用安装目录
    return Path(__file__).parent.parent

PROJECT_ROOT = get_project_root()

# 数据目录（可以独立配置）
if os.getenv('JQQUANT_DEV_MODE') == '1':
    # 开发模式：数据目录也在主项目
    DATA_DIR = PROJECT_ROOT / "data"
    CACHE_DIR = PROJECT_ROOT / "cache"
    LOGS_DIR = PROJECT_ROOT / "logs"
    REPORTS_DIR = PROJECT_ROOT / "reports"
else:
    # 生产模式：使用用户目录
    user_data_dir = Path.home() / '.local/share/jqquant'
    DATA_DIR = user_data_dir / "data"
    CACHE_DIR = user_data_dir / "cache"
    LOGS_DIR = user_data_dir / "logs"
    REPORTS_DIR = user_data_dir / "reports"
```

#### 步骤2：创建开发启动脚本

**创建 `scripts/dev_run.sh`**：

```bash
#!/usr/bin/env bash
# 开发模式启动脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 设置开发模式
export JQQUANT_DEV_MODE=1

# 激活虚拟环境（如果存在）
if [ -f "${PROJECT_ROOT}/venv/bin/activate" ]; then
    source "${PROJECT_ROOT}/venv/bin/activate"
fi

# 运行应用
cd "${PROJECT_ROOT}"
exec python3 JQQuant.py "$@"
```

**创建 `scripts/dev_run.py`**（Windows兼容）：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""开发模式启动脚本（跨平台）"""

import os
import sys
from pathlib import Path

# 设置开发模式
os.environ['JQQUANT_DEV_MODE'] = '1'

# 项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 切换到项目目录
os.chdir(project_root)

# 运行主程序
if __name__ == '__main__':
    from JQQuant import main
    main()
```

#### 步骤3：在Cursor中运行

**方法1：使用终端运行**
```bash
# 在Cursor终端中
cd /home/taotao/dev/QuantTest/TRQuant
JQQUANT_DEV_MODE=1 python JQQuant.py
```

**方法2：配置运行任务**

**创建 `.vscode/tasks.json`**：

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "运行JQQuant（开发模式）",
            "type": "shell",
            "command": "python3",
            "args": ["JQQuant.py"],
            "options": {
                "env": {
                    "JQQUANT_DEV_MODE": "1"
                },
                "cwd": "${workspaceFolder}"
            },
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        }
    ]
}
```

**创建 `.vscode/launch.json`**：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: JQQuant（开发模式）",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/JQQuant.py",
            "console": "integratedTerminal",
            "env": {
                "JQQUANT_DEV_MODE": "1"
            },
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### 2.2 开发工作流

1. **在Cursor中打开主项目**
   ```bash
   # File → Open Folder
   /home/taotao/dev/QuantTest/TRQuant
   ```

2. **编写代码**
   - 在Cursor中编辑
   - 实时看到代码

3. **运行测试**
   ```bash
   # 方式1：终端运行
   JQQUANT_DEV_MODE=1 python JQQuant.py
   
   # 方式2：使用运行任务（F5）
   ```

4. **查看效果**
   - GUI窗口正常打开
   - 功能正常使用
   - 数据保存在主项目的`data/`目录

---

## 🚀 第三部分：保持快捷方式可用

### 3.1 快捷方式配置

**修改 `scripts/sync_shortcuts.sh`**：

```bash
#!/usr/bin/env bash
# 同步快捷方式，支持开发模式

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 检测运行模式
if [ -n "${JQQUANT_DEV_MODE:-}" ] && [ "${JQQUANT_DEV_MODE}" = "1" ]; then
    # 开发模式：使用主项目目录
    APP_DIR="${PROJECT_ROOT}"
    INSTALL_DIR="${PROJECT_ROOT}"
else
    # 生产模式：使用安装目录
    INSTALL_DIR="${JQQUANT_INSTALL_DIR:-$HOME/.local/share/jqquant}"
    APP_DIR="${INSTALL_DIR}"
fi

LAUNCHER_PATH="$HOME/.local/bin/jqquant"
APPLICATIONS_DIR="$HOME/.local/share/applications"
ICON_TARGET="$HOME/.local/share/icons/hicolor/256x256/apps/jqquant.svg"
DESKTOP_ENTRY="$APPLICATIONS_DIR/jqquant.desktop"
USER_DESKTOP="${XDG_DESKTOP_DIR:-$HOME/Desktop}"
DESKTOP_SHORTCUT="$USER_DESKTOP/jqquant.desktop"
ICON_SOURCE="$APP_DIR/gui/resources/jqquant_icon.svg"

mkdir -p "$HOME/.local/bin" \
         "$APPLICATIONS_DIR" \
         "$HOME/.local/share/icons/hicolor/256x256/apps"

# 复制图标
if [ -f "$ICON_SOURCE" ]; then
    cp "$ICON_SOURCE" "$ICON_TARGET"
fi

# 创建启动脚本
cat > "$LAUNCHER_PATH" <<EOF_LAUNCHER
#!/usr/bin/env bash
set -euo pipefail

# 检测运行模式
if [ -f "${PROJECT_ROOT}/JQQuant.py" ] && [ -n "\${JQQUANT_USE_DEV:-}" ]; then
    # 开发模式
    APP_DIR="${PROJECT_ROOT}"
    export JQQUANT_DEV_MODE=1
else
    # 生产模式
    APP_DIR="${INSTALL_DIR}"
fi

if [ ! -f "\${APP_DIR}/JQQuant.py" ]; then
    echo "错误: 找不到JQQuant.py在 \${APP_DIR}"
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

# 创建桌面条目
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

# 复制到桌面
if [ -d "$USER_DESKTOP" ]; then
    cp "$DESKTOP_ENTRY" "$DESKTOP_SHORTCUT"
fi

update-desktop-database "$APPLICATIONS_DIR" >/dev/null 2>&1 || true

echo "✅ 快捷方式已更新"
echo "   启动脚本: $LAUNCHER_PATH"
echo "   桌面条目: $DESKTOP_ENTRY"
```

### 3.2 快捷方式使用

**默认行为**：
- 点击快捷方式 → 使用安装目录运行

**切换到开发模式**：
```bash
# 设置环境变量，下次启动使用开发模式
export JQQUANT_USE_DEV=1

# 或修改启动脚本，默认使用开发模式
```

---

## 🐳 第四部分：Docker跨平台部署

### 4.1 Docker配置优化

**修改 `docker-compose.yml`**：

```yaml
version: '3.8'

services:
  jqquant:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: jqquant
    volumes:
      # 挂载配置目录（从主项目或安装目录）
      - ${JQQUANT_CONFIG_DIR:-./config}:/app/config:ro
      # 挂载数据目录（持久化）
      - ${JQQUANT_DATA_DIR:-./data}:/app/data
      # 挂载日志目录
      - ${JQQUANT_LOGS_DIR:-./logs}:/app/logs
      # 挂载结果目录
      - ${JQQUANT_RESULTS_DIR:-./results}:/app/results
      # 如果需要GUI，挂载X11
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
      - ${XAUTHORITY:-$HOME/.Xauthority}:/root/.Xauthority:ro
    environment:
      - PYTHONUNBUFFERED=1
      - DISPLAY=${DISPLAY:-:0}
      - JQQUANT_DEV_MODE=${JQQUANT_DEV_MODE:-0}
    network_mode: host  # 如果需要访问本地服务
    # 如果需要GUI
    privileged: true
```

### 4.2 跨平台Docker脚本

**创建 `docker/run_cross_platform.sh`**：

```bash
#!/usr/bin/env bash
# 跨平台Docker运行脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux";;
        Darwin*)    echo "macos";;
        MINGW*)     echo "windows";;
        CYGWIN*)   echo "windows";;
        *)          echo "unknown";;
    esac
}

OS=$(detect_os)

# 配置目录（优先使用主项目，否则使用安装目录）
if [ -f "${PROJECT_ROOT}/JQQuant.py" ]; then
    CONFIG_DIR="${PROJECT_ROOT}/config"
    DATA_DIR="${PROJECT_ROOT}/data"
    LOGS_DIR="${PROJECT_ROOT}/logs"
    RESULTS_DIR="${PROJECT_ROOT}/results"
else
    INSTALL_DIR="${HOME}/.local/share/jqquant"
    CONFIG_DIR="${INSTALL_DIR}/config"
    DATA_DIR="${INSTALL_DIR}/data"
    LOGS_DIR="${INSTALL_DIR}/logs"
    RESULTS_DIR="${INSTALL_DIR}/results"
fi

# 创建目录
mkdir -p "${CONFIG_DIR}" "${DATA_DIR}" "${LOGS_DIR}" "${RESULTS_DIR}"

# Docker镜像名称
IMAGE_NAME="jqquant:latest"

# 构建镜像（如果需要）
if [ "${1:-}" = "--build" ] || ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "构建Docker镜像..."
    docker build -t "${IMAGE_NAME}" -f "${PROJECT_ROOT}/Dockerfile" "${PROJECT_ROOT}"
fi

# 运行容器
echo "启动Docker容器..."
docker run -it --rm \
    --name jqquant-container \
    -v "${CONFIG_DIR}:/app/config:ro" \
    -v "${DATA_DIR}:/app/data" \
    -v "${LOGS_DIR}:/app/logs" \
    -v "${RESULTS_DIR}:/app/results" \
    -e PYTHONUNBUFFERED=1 \
    "${IMAGE_NAME}" \
    python3 JQQuant.py "${@:2}"
```

### 4.3 跨平台安装脚本

**创建 `scripts/install_cross_platform.sh`**：

```bash
#!/usr/bin/env bash
# 跨平台安装脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 检测操作系统
OS=$(uname -s)

# 安装目录
case "$OS" in
    Linux*)
        INSTALL_DIR="${HOME}/.local/share/jqquant"
        BIN_DIR="${HOME}/.local/bin"
        ;;
    Darwin*)
        INSTALL_DIR="${HOME}/Library/Application Support/jqquant"
        BIN_DIR="${HOME}/.local/bin"
        ;;
    MINGW*|CYGWIN*)
        INSTALL_DIR="${APPDATA}/jqquant"
        BIN_DIR="${HOME}/.local/bin"
        ;;
    *)
        echo "不支持的操作系统: $OS"
        exit 1
        ;;
esac

echo "安装目录: ${INSTALL_DIR}"
echo "二进制目录: ${BIN_DIR}"

# 创建目录
mkdir -p "${INSTALL_DIR}" "${BIN_DIR}"

# 复制文件
echo "复制文件..."
rsync -a \
    --exclude ".git/" \
    --exclude "__pycache__/" \
    --exclude "venv/" \
    --exclude "*.pyc" \
    "${PROJECT_ROOT}/" "${INSTALL_DIR}/"

# 创建启动脚本
cat > "${BIN_DIR}/jqquant" <<EOF
#!/usr/bin/env bash
cd "${INSTALL_DIR}"
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi
exec python3 JQQuant.py "\$@"
EOF

chmod +x "${BIN_DIR}/jqquant"

echo "✅ 安装完成！"
echo "   运行: ${BIN_DIR}/jqquant"
```

### 4.4 Docker多阶段构建（优化）

**修改 `Dockerfile`**：

```dockerfile
# 阶段1：构建
FROM python:3.12-slim as builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make wget \
    && rm -rf /var/lib/apt/lists/*

# 安装TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# 阶段2：运行
FROM python:3.12-slim

WORKDIR /app

# 从构建阶段复制依赖
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/lib/libta_lib.so* /usr/lib/

# 复制项目文件
COPY . .

# 创建必要目录
RUN mkdir -p data logs results

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

# 暴露端口
EXPOSE 8000

# 默认命令
CMD ["python3", "JQQuant.py"]
```

---

## 📋 完整工作流总结

### 日常开发流程

1. **在Cursor中打开主项目**
   ```bash
   /home/taotao/dev/QuantTest/TRQuant
   ```

2. **编写代码**
   - 在Cursor中编辑
   - 使用Git管理版本

3. **运行测试**
   ```bash
   JQQUANT_DEV_MODE=1 python JQQuant.py
   ```

4. **同步到安装目录**（可选）
   ```bash
   cd ~/.local/share/jqquant
   python scripts/sync_to_main_project_safe.py
   ```

5. **提交Git**
   ```bash
   cd /home/taotao/dev/QuantTest/TRQuant
   git add .
   git commit -m "功能描述"
   git push
   ```

### 部署流程

1. **构建Docker镜像**
   ```bash
   cd /home/taotao/dev/QuantTest/TRQuant
   docker build -t jqquant:latest .
   ```

2. **运行容器**
   ```bash
   ./docker/run_cross_platform.sh
   ```

3. **跨平台安装**
   ```bash
   ./scripts/install_cross_platform.sh
   ```

---

## ✅ 检查清单

### 开发环境
- [ ] 主项目目录可正常打开
- [ ] Cursor可以运行代码
- [ ] 开发模式环境变量生效
- [ ] GUI可以正常显示

### 快捷方式
- [ ] Dock快捷方式可用
- [ ] 桌面快捷方式可用
- [ ] 启动脚本正确

### Docker
- [ ] Docker镜像可以构建
- [ ] 容器可以运行
- [ ] 数据持久化正常
- [ ] 跨平台脚本可用

---

*完整方案文档 - 最后更新：2024-11-29*

