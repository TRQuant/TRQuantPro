#!/bin/bash
# TRQuant Windows迁移打包脚本
# 用途: 打包TRQuant系统用于Windows迁移
# 作者: TRQuant Team
# 日期: 2026-01-11

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 TRQuant Windows迁移打包工具${NC}"
echo "=========================================="
echo -e "${YELLOW}⚠️  重要: 此脚本从ope目录打包，将安装到Windows的 C:\\TRQuantPro\\ope${NC}"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ⚠️ 重要: 项目根目录必须是ope目录
if [[ "$PROJECT_ROOT" != *"/ope" ]]; then
    echo -e "${RED}❌ 错误: 项目根目录必须是ope目录${NC}"
    echo -e "${YELLOW}当前目录: $PROJECT_ROOT${NC}"
    echo -e "${YELLOW}请从ope目录运行此脚本${NC}"
    echo -e "${YELLOW}正确路径: /home/taotao/.cursor/worktrees/TRQuant/ope${NC}"
    exit 1
fi

# 进入项目根目录
cd "$PROJECT_ROOT"

# 生成包名
PACKAGE_NAME="TRQuant_Windows_$(date +%Y%m%d_%H%M%S).tar.gz"
PACKAGE_DIR="TRQuant_Windows_Package_$(date +%Y%m%d_%H%M%S)"

echo -e "${YELLOW}📦 项目根目录: $PROJECT_ROOT${NC}"
echo -e "${YELLOW}📦 打包目录: $PACKAGE_DIR${NC}"
echo -e "${GREEN}✅ 确认: 从ope目录打包，将安装到Windows的 C:\\TRQuantPro\\ope${NC}"
echo ""

# 创建临时打包目录
mkdir -p "$PACKAGE_DIR"
cd "$PACKAGE_DIR"

# 创建目录结构
echo "📁 创建目录结构..."
mkdir -p TRQuant/{core,mcp_servers,notebooks,config,scripts,strategies,data_sources,.trquant/dev/knowledge}

# 复制核心代码（排除缓存）
echo "📋 复制核心代码（排除缓存）..."
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='*.pyo' \
    "$PROJECT_ROOT/core/" TRQuant/core/ > /dev/null 2>&1 || true
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='*.pyo' \
    "$PROJECT_ROOT/mcp_servers/" TRQuant/mcp_servers/ > /dev/null 2>&1 || true
rsync -av --exclude='__pycache__' --exclude='*.pyc' \
    "$PROJECT_ROOT/notebooks/" TRQuant/notebooks/ > /dev/null 2>&1 || true
rsync -av --exclude='__pycache__' --exclude='*.pyc' \
    "$PROJECT_ROOT/scripts/" TRQuant/scripts/ > /dev/null 2>&1 || true
rsync -av --exclude='__pycache__' --exclude='*.pyc' \
    "$PROJECT_ROOT/strategies/" TRQuant/strategies/ > /dev/null 2>&1 || true
rsync -av --exclude='__pycache__' --exclude='*.pyc' \
    "$PROJECT_ROOT/data_sources/" TRQuant/data_sources/ > /dev/null 2>&1 || true

# GUI和Extension（可选，默认不包含以减小包大小）
if [ -d "$PROJECT_ROOT/gui" ]; then
    read -p "是否包含GUI模块? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  ✅ gui/ - GUI界面"
        mkdir -p TRQuant/gui
        rsync -av --exclude='__pycache__' --exclude='*.pyc' \
            "$PROJECT_ROOT/gui/" TRQuant/gui/ > /dev/null 2>&1 || true
    fi
fi

if [ -d "$PROJECT_ROOT/extension" ]; then
    read -p "是否包含Cursor扩展? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  ✅ extension/ - Cursor扩展"
        mkdir -p TRQuant/extension
        rsync -av --exclude='node_modules' --exclude='__pycache__' \
            "$PROJECT_ROOT/extension/" TRQuant/extension/ > /dev/null 2>&1 || true
    fi
fi

# 复制配置文件（模板）
echo "⚙️  复制配置文件..."
if [ -d "$PROJECT_ROOT/config" ]; then
    cp -r "$PROJECT_ROOT/config"/* TRQuant/config/ 2>/dev/null || true
    # 创建配置模板
    if [ -f "TRQuant/config/jqdata_config.json" ]; then
        cat > TRQuant/config/jqdata_config.json.example << 'EOF'
{
  "username": "请填写你的JQData账号",
  "password": "请填写你的JQData密码",
  "data_range": {
    "start_date": "2022-01-01",
    "end_date": "2024-12-31"
  }
}
EOF
        echo "  ✅ 创建了 jqdata_config.json.example 模板"
    fi
fi

# 复制文档（精简版，只包含必需文档）
echo "📚 复制文档（精简版）..."
if [ -d "$PROJECT_ROOT/docs" ]; then
    mkdir -p TRQuant/docs
    
    # 必需文档目录
    ESSENTIAL_DOCS=(
        "MUST_READ"
        "02_development_guides/WINDOWS_MIGRATION_GUIDE.md"
        "02_development_guides/ABD_MERGE_COMPLETE.md"
        "02_development_guides/PACKAGE_FILE_LIST.md"
        "01_architecture"
        "04_platform_integration/QMT_BRIDGE_GUIDE.md"
    )
    
    for doc_path in "${ESSENTIAL_DOCS[@]}"; do
        src_path="$PROJECT_ROOT/docs/$doc_path"
        if [ -e "$src_path" ]; then
            if [ -d "$src_path" ]; then
                rsync -av "$src_path/" "TRQuant/docs/$doc_path/" > /dev/null 2>&1 || true
            else
                mkdir -p "TRQuant/docs/$(dirname "$doc_path")"
                cp "$src_path" "TRQuant/docs/$doc_path" 2>/dev/null || true
            fi
        fi
    done
    echo "  ✅ 文档已复制（精简版）"
fi

# 复制知识库文件（RAG知识库）
echo "🧠 复制知识库文件..."
if [ -f "$PROJECT_ROOT/.trquant/dev/knowledge/knowledge_base.json" ]; then
    echo "  ✅ knowledge_base.json - 知识库JSON（必需）"
    mkdir -p TRQuant/.trquant/dev/knowledge
    cp "$PROJECT_ROOT/.trquant/dev/knowledge/knowledge_base.json" \
       TRQuant/.trquant/dev/knowledge/ 2>/dev/null || true
else
    echo "  ⚠️  knowledge_base.json 不存在，将在Windows上重新构建"
fi

# 向量索引（可选，可以重建，约63MB）
if [ -d "$PROJECT_ROOT/.trquant/dev/knowledge/vector_index" ]; then
    VECTOR_INDEX_SIZE=$(du -sh "$PROJECT_ROOT/.trquant/dev/knowledge/vector_index" 2>/dev/null | cut -f1)
    echo "  ⚠️  vector_index/ 存在 (${VECTOR_INDEX_SIZE})，但可以重建"
    read -p "  是否包含向量索引? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  ✅ 包含向量索引"
        rsync -av "$PROJECT_ROOT/.trquant/dev/knowledge/vector_index/" \
            TRQuant/.trquant/dev/knowledge/vector_index/ > /dev/null 2>&1 || true
    else
        echo "  ⏭️  跳过向量索引（将在Windows上重建，运行: python scripts\\kb\\kb_manager.py build-index）"
    fi
fi

# 复制根目录文件
echo "📄 复制根目录文件..."
cp "$PROJECT_ROOT/requirements.txt" TRQuant/ 2>/dev/null || true
cp "$PROJECT_ROOT/requirements-dev.txt" TRQuant/ 2>/dev/null || true
cp "$PROJECT_ROOT/README.md" TRQuant/ 2>/dev/null || true
cp "$PROJECT_ROOT/CLAUDE.md" TRQuant/ 2>/dev/null || true
cp "$PROJECT_ROOT/VERSION" TRQuant/ 2>/dev/null || true

# 复制Python入口文件
find "$PROJECT_ROOT" -maxdepth 1 -name "*.py" -type f -exec cp {} TRQuant/ \; 2>/dev/null || true

# 创建Windows安装脚本
echo "🔧 创建Windows安装脚本..."
cat > TRQuant/install_windows.ps1 << 'EOF'
# TRQuant Windows安装脚本
# PowerShell脚本，用于在Windows上安装TRQuant系统
# 安装路径: C:\TRQuantPro\ope
# Python版本要求: 3.11 或 3.10 (QMT需要3.12以下)

$InstallPath = "C:\TRQuantPro\ope"
$PythonVersion = "3.11"  # 推荐3.11，QMT兼容

Write-Host "🚀 TRQuant Windows安装程序" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "安装路径: $InstallPath" -ForegroundColor Yellow
Write-Host "Python版本要求: $PythonVersion (QMT需要3.12以下)" -ForegroundColor Yellow
Write-Host ""

# 检查Python版本（优先检查3.11，然后是3.10）
Write-Host "📋 检查Python环境..." -ForegroundColor Yellow
$pythonCmd = $null
$pythonVersion = $null

# 尝试Python 3.11
try {
    $result = & python3.11 --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = "python3.11"
        $pythonVersion = $result
    }
} catch {}

# 尝试Python 3.10
if ($null -eq $pythonCmd) {
    try {
        $result = & python3.10 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "python3.10"
            $pythonVersion = $result
        }
    } catch {}
}

# 尝试py启动器
if ($null -eq $pythonCmd) {
    try {
        $result = & py -3.11 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "py -3.11"
            $pythonVersion = $result
        }
    } catch {}
}

if ($null -eq $pythonCmd) {
    try {
        $result = & py -3.10 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "py -3.10"
            $pythonVersion = $result
        }
    } catch {}
}

# 最后尝试默认python
if ($null -eq $pythonCmd) {
    try {
        $result = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $versionNum = ($result -replace "Python ", "").Split(".")[0..1] -join "."
            if ([version]"$versionNum" -lt [version]"3.12") {
                $pythonCmd = "python"
                $pythonVersion = $result
            }
        }
    } catch {}
}

if ($null -eq $pythonCmd) {
    Write-Host "❌ 未找到Python 3.11或3.10" -ForegroundColor Red
    Write-Host "请安装Python 3.11或3.10（QMT需要3.12以下）" -ForegroundColor Red
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "⚠️  安装时请勾选 'Add Python to PATH'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ 找到Python: $pythonVersion" -ForegroundColor Green
Write-Host "   使用命令: $pythonCmd" -ForegroundColor Green

# 检查pip
Write-Host "📋 检查pip..." -ForegroundColor Yellow
$pipResult = & $pythonCmd -m pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ pip未安装" -ForegroundColor Red
    exit 1
}
Write-Host "✅ $pipResult" -ForegroundColor Green

# 创建安装目录
Write-Host ""
Write-Host "📁 创建安装目录..." -ForegroundColor Yellow
if (-not (Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    Write-Host "✅ 已创建: $InstallPath" -ForegroundColor Green
} else {
    Write-Host "✅ 目录已存在: $InstallPath" -ForegroundColor Green
}

# 复制文件到安装目录
Write-Host ""
Write-Host "📋 复制文件到安装目录..." -ForegroundColor Yellow
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -Path "$SourceDir\*" -Destination $InstallPath -Recurse -Force -Exclude "install_windows.ps1"
Write-Host "✅ 文件复制完成" -ForegroundColor Green

# 切换到安装目录
Set-Location $InstallPath

# 创建虚拟环境
Write-Host ""
Write-Host "📦 创建Python虚拟环境..." -ForegroundColor Yellow
& $pythonCmd -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 虚拟环境创建失败" -ForegroundColor Red
    exit 1
}
Write-Host "✅ 虚拟环境创建成功" -ForegroundColor Green

# 激活虚拟环境
Write-Host ""
Write-Host "🔄 激活虚拟环境..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# 升级pip
Write-Host ""
Write-Host "⬆️  升级pip..." -ForegroundColor Yellow
& $pythonCmd -m pip install --upgrade pip setuptools wheel

# 安装依赖
Write-Host ""
Write-Host "📦 安装Python依赖..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟时间..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  部分依赖安装失败，请检查错误信息" -ForegroundColor Yellow
    Write-Host "常见问题:" -ForegroundColor Yellow
    Write-Host "  - TA-Lib: 需要下载预编译版本" -ForegroundColor Yellow
    Write-Host "  - PyQt6: 可能需要Visual C++ Build Tools" -ForegroundColor Yellow
}

# 配置JQData
Write-Host ""
Write-Host "⚙️  配置JQData..." -ForegroundColor Yellow
if (Test-Path "config\jqdata_config.json.example") {
    if (-not (Test-Path "config\jqdata_config.json")) {
        Copy-Item "config\jqdata_config.json.example" "config\jqdata_config.json"
        Write-Host "✅ 已创建配置文件模板" -ForegroundColor Green
        Write-Host "⚠️  请编辑 config\jqdata_config.json 填写你的JQData账号信息" -ForegroundColor Yellow
    } else {
        Write-Host "✅ 配置文件已存在" -ForegroundColor Green
    }
}

# 安装知识库依赖（RAG）
Write-Host ""
Write-Host "🧠 安装知识库依赖（RAG）..." -ForegroundColor Yellow
pip install sentence-transformers chromadb
Write-Host "✅ 知识库依赖安装完成" -ForegroundColor Green

# 检查知识库文件
Write-Host ""
Write-Host "📚 检查知识库文件..." -ForegroundColor Yellow
if (Test-Path ".trquant\dev\knowledge\knowledge_base.json") {
    Write-Host "✅ 知识库JSON文件已存在" -ForegroundColor Green
    if (Test-Path ".trquant\dev\knowledge\vector_index") {
        Write-Host "✅ 向量索引已存在" -ForegroundColor Green
    } else {
        Write-Host "⚠️  向量索引不存在，将自动构建" -ForegroundColor Yellow
        Write-Host "   运行: python scripts\kb\kb_manager.py build-index" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  知识库文件不存在，需要重新构建" -ForegroundColor Yellow
}

# QMT相关说明
Write-Host ""
Write-Host "📋 QMT配置说明..." -ForegroundColor Yellow
Write-Host "   QMT需要Python 3.12以下版本（当前使用: $pythonVersion）" -ForegroundColor Green
Write-Host "   QMT SDK路径需要配置在策略中" -ForegroundColor Yellow
Write-Host "   参考文档: docs\04_platform_integration\QMT_BRIDGE_GUIDE.md" -ForegroundColor Yellow

# 创建启动脚本
Write-Host ""
Write-Host "📝 创建启动脚本..." -ForegroundColor Yellow
@"
@echo off
REM TRQuant启动脚本
cd /d %~dp0
call venv\Scripts\activate.bat
python -c "from config.config_manager import get_config_manager; import jqdatasdk as jq; cm = get_config_manager(); cfg = cm.get_config('jqdata'); jq.auth(cfg['username'], cfg['password']); print('✅ JQData连接成功' if jq.is_auth() else '❌ JQData连接失败')"
pause
"@ | Out-File -FilePath "test_connection.bat" -Encoding ASCII

Write-Host ""
Write-Host "✅ 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "安装路径: $InstallPath" -ForegroundColor Cyan
Write-Host "Python版本: $pythonVersion" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "  1. 编辑 config\jqdata_config.json 填写JQData账号" -ForegroundColor Yellow
Write-Host "  2. 运行 test_connection.bat 测试连接" -ForegroundColor Yellow
Write-Host "  3. 运行 python check_dependencies.py 检查依赖" -ForegroundColor Yellow
Write-Host "  4. 如果知识库向量索引不存在，运行构建脚本" -ForegroundColor Yellow
Write-Host ""
Write-Host "启动Jupyter Notebook:" -ForegroundColor Yellow
Write-Host "  cd $InstallPath" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  jupyter notebook notebooks\research\" -ForegroundColor Yellow
Write-Host ""
Write-Host "QMT配置:" -ForegroundColor Yellow
Write-Host "  QMT需要Python 3.12以下版本（当前: $pythonVersion）" -ForegroundColor Green
Write-Host "  请确保QMT SDK路径正确配置" -ForegroundColor Yellow
EOF

# 创建Windows批处理启动脚本
cat > TRQuant/start_jupyter.bat << 'EOF'
@echo off
REM TRQuant Jupyter Notebook启动脚本
REM 安装路径: C:\TRQuantPro\ope
cd /d C:\TRQuantPro\ope
call venv\Scripts\activate.bat
jupyter notebook notebooks\research\
pause
EOF

# 创建测试连接脚本
cat > TRQuant/test_connection.bat << 'EOF'
@echo off
REM TRQuant连接测试脚本
REM 安装路径: C:\TRQuantPro\ope
cd /d C:\TRQuantPro\ope
call venv\Scripts\activate.bat
python -c "from config.config_manager import get_config_manager; import jqdatasdk as jq; cm = get_config_manager(); cfg = cm.get_config('jqdata'); jq.auth(cfg['username'], cfg['password']); print('✅ JQData连接成功' if jq.is_auth() else '❌ JQData连接失败')"
pause
EOF

# 创建README
cat > TRQuant/README_WINDOWS.md << 'EOF'
# TRQuant Windows安装说明

## ⚠️ 重要提示

- **安装路径**: `C:\TRQuantPro\ope` (与Ubuntu结构一致)
- **Python版本**: 3.11 或 3.10 (QMT需要3.12以下)
- **知识库**: 已包含RAG知识库文件，首次运行会自动构建向量索引

## 快速安装

1. **解压文件**
   - 将 `TRQuant_Windows_*.tar.gz` 解压到临时目录
   - 运行安装脚本会自动安装到 `C:\TRQuantPro\ope`

2. **运行安装脚本**
   ```powershell
   # 以管理员身份运行PowerShell
   cd <解压目录>\TRQuant
   .\install_windows.ps1
   ```

3. **配置JQData**
   - 编辑 `C:\TRQuantPro\ope\config\jqdata_config.json`
   - 填写你的JQData账号和密码

4. **测试连接**
   ```powershell
   cd C:\TRQuantPro\ope
   .\test_connection.bat
   ```

## Python版本要求

**QMT兼容性**: 国金QMT需要Python 3.12以下版本

- ✅ **推荐**: Python 3.11
- ✅ **备选**: Python 3.10
- ❌ **不支持**: Python 3.12+

安装Python时请勾选 "Add Python to PATH"

## 知识库（RAG）

知识库文件已包含在打包中：
- `knowledge_base.json` - 知识库JSON文件
- `vector_index/` - ChromaDB向量索引（如果存在）

如果向量索引不存在，首次运行时会自动构建：
```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1
python scripts\kb\kb_manager.py build-index
```

## QMT配置

1. **确保Python版本正确** (3.11或3.10)
2. **配置QMT SDK路径** (在策略文件中)
3. **参考文档**: `docs\04_platform_integration\QMT_BRIDGE_GUIDE.md`

## 详细说明

请查看 `docs\02_development_guides\WINDOWS_MIGRATION_GUIDE.md`

## 常见问题

### TA-Lib安装失败
下载预编译版本: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
选择对应Python版本的.whl文件安装

### PyQt6安装失败
可能需要安装 Visual C++ Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### MongoDB连接失败
MongoDB是可选的，如果不需要可以忽略连接错误

### 知识库向量索引构建失败
确保已安装: `pip install sentence-transformers chromadb`
EOF

# 清理不需要的文件
echo ""
echo "🧹 清理不需要的文件..."
find TRQuant -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find TRQuant -type f -name "*.pyc" -delete 2>/dev/null || true
find TRQuant -type f -name "*.pyo" -delete 2>/dev/null || true
find TRQuant -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find TRQuant -type d -name ".git" -exec rm -rf {} + 2>/dev/null || true
find TRQuant -type f -name ".DS_Store" -delete 2>/dev/null || true
find TRQuant -type f -name "Thumbs.db" -delete 2>/dev/null || true

# 排除其他不需要的目录（如果误复制）
rm -rf TRQuant/venv TRQuant/.venv TRQuant/data TRQuant/cache \
       TRQuant/logs TRQuant/reports TRQuant/results \
       TRQuant/backtest_results TRQuant/output \
       TRQuant/third_party TRQuant/node_modules 2>/dev/null || true

# 计算大小
PACKAGE_SIZE=$(du -sh "$PACKAGE_DIR" | cut -f1)
echo ""
echo -e "${GREEN}✅ 打包完成！${NC}"
echo -e "${GREEN}📦 打包目录: $PACKAGE_DIR${NC}"
echo -e "${GREEN}📊 目录大小: $PACKAGE_SIZE${NC}"
echo ""
echo -e "${BLUE}📋 打包内容总结:${NC}"
echo "  ✅ 核心代码 (core, mcp_servers, notebooks, scripts, strategies, data_sources)"
echo "  ✅ 配置文件 (config/)"
echo "  ✅ 知识库JSON (knowledge_base.json)"
echo "  ⚠️  向量索引 (可选，如果选择包含)"
echo "  ✅ 依赖列表 (requirements.txt)"
echo "  ✅ 文档 (精简版)"
echo "  ❌ Python虚拟环境 (venv/) - 将在Windows上重建"
echo "  ❌ 数据文件 (data/) - 可重新下载"
echo "  ❌ 缓存文件 (cache/, __pycache__/) - 运行时生成"
echo ""

# 创建压缩包
echo "🗜️  创建压缩包..."
cd "$PROJECT_ROOT"
tar -czf "$PACKAGE_NAME" "$PACKAGE_DIR" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  tar压缩失败，尝试使用zip...${NC}"
    zip -r "${PACKAGE_NAME%.tar.gz}.zip" "$PACKAGE_DIR" > /dev/null 2>&1 || {
        echo -e "${RED}❌ 压缩失败，请手动压缩 $PACKAGE_DIR 目录${NC}"
        exit 1
    }
    PACKAGE_NAME="${PACKAGE_NAME%.tar.gz}.zip"
}

COMPRESSED_SIZE=$(du -sh "$PACKAGE_NAME" | cut -f1)
echo ""
echo -e "${GREEN}✅ 压缩完成！${NC}"
echo -e "${GREEN}📦 压缩包: $PACKAGE_NAME${NC}"
echo -e "${GREEN}📊 压缩包大小: $COMPRESSED_SIZE${NC}"
echo ""
echo -e "${YELLOW}📋 下一步:${NC}"
echo "  1. 将 $PACKAGE_NAME 传输到Windows电脑"
echo "  2. 解压到 C:\\TRQuant"
echo "  3. 运行 install_windows.ps1"
echo ""
echo -e "${GREEN}✨ 打包完成！${NC}"
