#!/bin/bash
# TRQuant Windows 打包脚本
# 排除可重建的目录，保留核心文件和重建说明

set -e

PROJECT_ROOT="/home/taotao/dev/QuantTest/TRQuant"
OUTPUT_DIR="/home/taotao/dev/QuantTest/TRQuant_backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ZIP_NAME="TRQuant_for_windows_${TIMESTAMP}.zip"

cd "$PROJECT_ROOT"

echo "=========================================="
echo "TRQuant Windows 打包脚本"
echo "=========================================="
echo ""

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo "临时目录: $TEMP_DIR"

# 复制项目到临时目录（排除不需要的文件）
echo "复制项目文件..."
rsync -av \
  --exclude='.backups' \
  --exclude='.git' \
  --exclude='venv' \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.pyo' \
  --exclude='*.pyd' \
  --exclude='.Python' \
  --exclude='*.so' \
  --exclude='*.egg' \
  --exclude='*.egg-info' \
  --exclude='dist' \
  --exclude='build' \
  --exclude='.astro' \
  --exclude='.next' \
  --exclude='.turbo' \
  --exclude='.vercel' \
  --exclude='*.vsix' \
  --exclude='*.tgz' \
  --exclude='*.tar.gz' \
  --exclude='*.log' \
  --exclude='*.tmp' \
  --exclude='*.temp' \
  --exclude='*.backup' \
  --exclude='*.bak' \
  --exclude='.DS_Store' \
  --exclude='Thumbs.db' \
  --exclude='*.swp' \
  --exclude='*.swo' \
  --exclude='.idea' \
  --exclude='.vscode' \
  --exclude='*.env' \
  --exclude='data/' \
  --exclude='logs/' \
  --exclude='output/' \
  --exclude='reports/' \
  --exclude='results/' \
  --exclude='.pytest_cache' \
  --exclude='.mypy_cache' \
  --exclude='.ruff_cache' \
  --exclude='.tox' \
  --exclude='.hypothesis' \
  --exclude='.coverage' \
  --exclude='htmlcov' \
  --exclude='.eggs' \
  --exclude='.ipynb_checkpoints' \
  --exclude='.jupyter' \
  "$PROJECT_ROOT/" "$TEMP_DIR/TRQuant/"

# 确保保留venv目录结构（空目录）
echo "创建venv目录结构..."
mkdir -p "$TEMP_DIR/TRQuant/venv"
touch "$TEMP_DIR/TRQuant/venv/.gitkeep"

# 确保保留node_modules目录结构
echo "创建node_modules目录结构..."
mkdir -p "$TEMP_DIR/TRQuant/extension/node_modules"
mkdir -p "$TEMP_DIR/TRQuant/extension/AShare-manual/node_modules"
touch "$TEMP_DIR/TRQuant/extension/node_modules/.gitkeep"
touch "$TEMP_DIR/TRQuant/extension/AShare-manual/node_modules/.gitkeep"

# 验证requirements.txt存在
if [ ! -f "$TEMP_DIR/TRQuant/requirements.txt" ]; then
  echo "警告: requirements.txt 不存在！"
fi

if [ ! -f "$TEMP_DIR/TRQuant/extension/requirements.txt" ]; then
  echo "警告: extension/requirements.txt 不存在！"
fi

# 验证重建说明存在
if [ ! -f "$TEMP_DIR/TRQuant/NODEJS_REBUILD_GUIDE.md" ]; then
  echo "警告: NODEJS_REBUILD_GUIDE.md 不存在！"
fi

# 创建快速开始说明
cat > "$TEMP_DIR/TRQuant/QUICK_START_WINDOWS.md" << 'EOF'
# TRQuant Windows 快速开始指南

## 📋 前置要求

1. **Python 3.11+** (64-bit)
   - 下载: https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **Node.js 18 LTS+**
   - 下载: https://nodejs.org/
   - 验证: `node --version` 和 `npm --version`

3. **Git** (可选，用于版本控制)
   - 下载: https://git-scm.com/download/win

## 🚀 安装步骤

### 1. 解压项目

将 `TRQuant_for_windows_*.zip` 解压到目标目录，例如：
```
C:\trquant
```

**注意**: 路径不要包含空格，尽量简短。

### 2. 重建 Python 环境

打开 PowerShell（以管理员身份运行）：

```powershell
cd C:\trquant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

如果遇到 TA-Lib 安装问题，参考 `docs/project_guides/WINDOWS_INSTALL_AND_TEST.md`

### 3. 重建 Node.js 依赖

#### 3.1 VS Code 扩展依赖

```powershell
cd C:\trquant\extension
npm install
npm run compile
```

#### 3.2 AShare Manual 文档系统依赖

```powershell
cd C:\trquant\extension\AShare-manual
npm install
```

详细说明请参考 `NODEJS_REBUILD_GUIDE.md`

### 4. 配置项目

复制配置文件模板：

```powershell
cd C:\trquant\config
copy broker_config.json.example broker_config.json
copy jqdata_config.json.example jqdata_config.json
copy emquant_config.json.example emquant_config.json
```

编辑配置文件，填入你的 API 密钥等信息。

### 5. 验证安装

```powershell
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 测试导入
python -c "import numpy; import pandas; print('Python依赖正常')"

# 测试扩展编译
cd extension
npm run compile
```

## 📚 更多文档

- **Windows安装详细指南**: `docs/project_guides/WINDOWS_INSTALL_AND_TEST.md`
- **Node.js重建指南**: `NODEJS_REBUILD_GUIDE.md`
- **项目使用教程**: `docs/project_guides/USAGE_TUTORIAL.md`
- **快速开始**: `QUICK_START.md`

## ⚠️ 常见问题

### Python 环境问题

- **问题**: `python` 命令未找到
- **解决**: 确保 Python 已添加到 PATH，或使用完整路径

### TA-Lib 安装失败

- **问题**: `pip install ta-lib` 失败
- **解决**: 使用 conda 安装或下载预编译 wheel，详见安装指南

### Node.js 编译错误

- **问题**: `npm run compile` 失败
- **解决**: 检查 Node.js 版本，清除缓存后重试

## 🎯 下一步

安装完成后，可以：
1. 阅读 `README.md` 了解项目结构
2. 查看 `docs/` 目录下的文档
3. 运行示例项目：`Projects/`
4. 使用 VS Code 扩展（需先编译）

---

**最后更新**: 2025-12-06
EOF

# 创建打包信息文件
cat > "$TEMP_DIR/TRQuant/PACKAGE_INFO.txt" << EOF
TRQuant Windows 打包信息
========================

打包时间: $(date '+%Y-%m-%d %H:%M:%S')
打包版本: $(git describe --tags 2>/dev/null || echo "未知")
Python版本要求: 3.11+
Node.js版本要求: 18 LTS+

包含内容:
- 核心源代码
- 配置文件模板
- 文档和指南
- 重建说明

排除内容:
- venv/ (Python虚拟环境，需重建)
- node_modules/ (Node.js依赖，需重建)
- .backups/ (备份文件)
- 缓存和临时文件

重建步骤:
1. 解压到目标目录
2. 按照 QUICK_START_WINDOWS.md 执行
3. 参考 NODEJS_REBUILD_GUIDE.md 重建Node.js依赖

更多信息请查看:
- QUICK_START_WINDOWS.md
- NODEJS_REBUILD_GUIDE.md
- docs/project_guides/WINDOWS_INSTALL_AND_TEST.md
EOF

# 打包为zip
echo ""
echo "创建压缩包..."
cd "$TEMP_DIR"
zip -r "$OUTPUT_DIR/$ZIP_NAME" TRQuant/ -q

# 计算大小
ZIP_SIZE=$(du -h "$OUTPUT_DIR/$ZIP_NAME" | cut -f1)

echo ""
echo "=========================================="
echo "打包完成！"
echo "=========================================="
echo "文件: $OUTPUT_DIR/$ZIP_NAME"
echo "大小: $ZIP_SIZE"
echo ""
echo "包含内容:"
echo "  ✓ 核心源代码"
echo "  ✓ 配置文件"
echo "  ✓ 文档和指南"
echo "  ✓ 重建说明"
echo ""
echo "排除内容:"
echo "  ✗ venv/ (需重建)"
echo "  ✗ node_modules/ (需重建)"
echo "  ✗ 缓存和临时文件"
echo ""
echo "下一步:"
echo "  1. 将zip文件传输到Windows系统"
echo "  2. 解压到目标目录"
echo "  3. 按照 QUICK_START_WINDOWS.md 执行安装"
echo ""

# 清理临时目录
rm -rf "$TEMP_DIR"

echo "临时文件已清理"
echo "完成！"


