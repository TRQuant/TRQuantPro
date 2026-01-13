# TRQuant 韬睿量化系统 - Windows迁移安装指南

> **版本**: v1.1  
> **更新**: 2026-01-11  
> **目的**: 将TRQuant系统从Linux迁移到Windows的完整方案  
> **项目目录**: `/home/taotao/.cursor/worktrees/TRQuant/ope`  
> **Windows安装路径**: `C:\TRQuantPro\ope`

---

## 📋 目录

1. [迁移前准备](#迁移前准备)
2. [需要打包的文件清单](#需要打包的文件清单)
3. [Windows环境准备](#windows环境准备)
4. [安装步骤](#安装步骤)
5. [配置调整](#配置调整)
6. [验证安装](#验证安装)
7. [常见问题](#常见问题)

---

## 📦 迁移前准备

### 1. 系统要求检查

**Windows系统要求**:
- Windows 10/11 (64位)
- 至少 8GB RAM（推荐16GB）
- 至少 20GB 可用磁盘空间
- 管理员权限（用于安装Python和依赖）

**必需软件**:
- Python 3.9+ (推荐 3.11)
- Git for Windows
- MongoDB (可选，如果需要本地数据库)
- Node.js 18+ (如果使用Cursor扩展)

---

## 📁 需要打包的文件清单

### ✅ 核心代码文件（必须）

```
TRQuant/
├── core/                          # 核心功能模块（必须）
│   ├── market_trend_analyzer.py
│   ├── trend_analyzer.py
│   ├── candidate_pool_builder.py
│   ├── signal_backtest.py
│   ├── market_regime/             # 市场环境识别
│   ├── rotation/                  # 行业轮动
│   ├── selection/                 # 标的筛选
│   ├── backtest/                  # 回测模块
│   ├── factors/                   # 因子库
│   ├── strategy/                  # 策略开发
│   └── ...
├── mcp_servers/                   # MCP服务器（必须）
│   ├── trquant_core_server.py
│   ├── workflow_9steps_server.py
│   ├── unified_dev_server.py
│   └── ...
├── notebooks/                     # Jupyter Notebook（必须）
│   ├── research/
│   └── lib/
├── config/                        # 配置文件（必须）
│   ├── jqdata_config.json         # ⚠️ 需要手动配置
│   ├── config_manager.py
│   └── settings.py
├── scripts/                       # 脚本文件（必须）
├── strategies/                    # 策略文件（必须）
├── data_sources/                  # 数据源模块（必须）
├── gui/                           # GUI界面（可选）
├── extension/                     # Cursor扩展（可选）
├── .trquant/                      # 知识库目录（必须）
│   └── dev/
│       └── knowledge/
│           ├── knowledge_base.json    # 知识库JSON
│           └── vector_index/         # 向量索引（如果存在）
├── requirements.txt               # Python依赖（必须）
├── requirements-dev.txt           # 开发依赖（可选）
└── README.md                      # 项目说明（必须）
```

### ✅ 配置文件（需要手动调整）

```
config/
├── jqdata_config.json             # JQData账号配置（需要填写）
│   {
│     "username": "你的账号",
│     "password": "你的密码"
│   }
└── settings.py                    # 系统设置（路径需要调整）
```

### ✅ 文档文件（推荐）

```
docs/                              # 完整文档（推荐）
├── MUST_READ/                     # 必读文档
├── 01_architecture/               # 架构文档
├── 02_development_guides/          # 开发指南
└── ...
```

### ❌ 不需要打包的文件

```
# 缓存和临时文件
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg-info/
dist/
build/

# 虚拟环境
venv/
env/
.venv/

# IDE配置
.vscode/
.idea/
*.swp
*.swo

# 数据文件（太大，可重新生成）
data/
cache/
logs/
reports/
results/
backtest_results/

# Git相关
.git/
.gitignore

# 系统文件
.DS_Store
Thumbs.db

# 注意: .trquant/dev/knowledge/vector_index/ 如果很大可以排除
# 但建议包含，因为重建需要时间
```

---

## 🖥️ Windows环境准备

### 步骤1: 安装Python

⚠️ **重要**: QMT需要Python 3.12以下版本，推荐使用 **Python 3.11** 或 **3.10**

1. **下载Python**
   - 访问 https://www.python.org/downloads/
   - 下载 **Python 3.11.x** (64位) - 推荐
   - 或 **Python 3.10.x** (64位) - 备选
   - ⚠️ **重要**: 安装时勾选 "Add Python to PATH"
   - ❌ **不要安装**: Python 3.12+ (QMT不兼容)

2. **验证安装**
   ```powershell
   # 检查Python 3.11
   python3.11 --version
   # 或使用py启动器
   py -3.11 --version
   # 应显示: Python 3.11.x
   
   # 检查pip
   py -3.11 -m pip --version
   # 应显示: pip 23.x.x
   ```

### 步骤2: 安装Git for Windows

1. **下载Git**
   - 访问 https://git-scm.com/download/win
   - 下载并安装（使用默认选项）

2. **验证安装**
   ```powershell
   git --version
   # 应显示: git version 2.x.x
   ```

### 步骤3: 安装MongoDB（可选）

如果需要本地MongoDB数据库：

1. **下载MongoDB Community Server**
   - 访问 https://www.mongodb.com/try/download/community
   - 下载Windows版本
   - 安装到默认路径: `C:\Program Files\MongoDB\Server\7.0\`

2. **配置MongoDB服务**
   ```powershell
   # MongoDB会自动安装为Windows服务
   # 验证服务状态
   Get-Service MongoDB
   ```

### 步骤4: 安装Node.js（如果使用Cursor扩展）

1. **下载Node.js**
   - 访问 https://nodejs.org/
   - 下载 LTS 版本（18.x 或更高）

2. **验证安装**
   ```powershell
   node --version
   npm --version
   ```

---

## 📥 安装步骤

### 步骤1: 传输文件到Windows

**方式1: 使用压缩包（推荐）**

在Linux系统上（从ope目录）：
```bash
# ⚠️ 重要: 从ope目录运行打包脚本
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 运行打包脚本
./scripts/package_for_windows.sh

# 或手动打包（如果脚本不存在）
cat > package_for_windows.sh << 'EOF'
#!/bin/bash
# 打包TRQuant系统用于Windows迁移

PACKAGE_NAME="TRQuant_Windows_$(date +%Y%m%d).tar.gz"
EXCLUDE_PATTERNS=(
    "--exclude=__pycache__"
    "--exclude=*.pyc"
    "--exclude=*.pyo"
    "--exclude=venv"
    "--exclude=.venv"
    "--exclude=env"
    "--exclude=.git"
    "--exclude=data"
    "--exclude=cache"
    "--exclude=logs"
    "--exclude=reports"
    "--exclude=results"
    "--exclude=backtest_results"
    "--exclude=.vscode"
    "--exclude=.idea"
    "--exclude=*.swp"
    "--exclude=.DS_Store"
    "--exclude=Thumbs.db"
)

tar -czf "$PACKAGE_NAME" \
    "${EXCLUDE_PATTERNS[@]}" \
    core/ \
    mcp_servers/ \
    notebooks/ \
    config/ \
    scripts/ \
    strategies/ \
    data_sources/ \
    gui/ \
    extension/ \
    docs/ \
    requirements.txt \
    requirements-dev.txt \
    README.md \
    CLAUDE.md \
    *.py 2>/dev/null

echo "✅ 打包完成: $PACKAGE_NAME"
echo "📦 文件大小: $(du -h "$PACKAGE_NAME" | cut -f1)"
EOF

chmod +x package_for_windows.sh
./package_for_windows.sh
```

**方式2: 使用Git（如果Windows有Git访问权限）**

在Windows上：
```powershell
# 克隆仓库（如果有Git访问）
git clone <repository-url> C:\TRQuant
cd C:\TRQuant
```

### 步骤2: 解压到Windows目录

```powershell
# ⚠️ 重要: 安装路径为 C:\TRQuantPro\ope (与Ubuntu结构一致)
# 解压文件到临时目录，安装脚本会自动安装到正确位置

# 解压文件（如果使用压缩包）
# 使用7-Zip或WinRAR解压 TRQuant_Windows_*.tar.gz 到临时目录
# 然后运行解压后的 install_windows.ps1 脚本
```

### 步骤3: 运行安装脚本

```powershell
# ⚠️ 重要: 安装路径为 C:\TRQuantPro\ope
# 解压文件后，进入解压目录运行安装脚本

# 进入解压后的TRQuant目录
cd <解压目录>\TRQuant

# 以管理员身份运行PowerShell，然后执行：
.\install_windows.ps1

# 安装脚本会自动：
# 1. 创建 C:\TRQuantPro\ope 目录
# 2. 复制所有文件到安装目录
# 3. 创建Python虚拟环境
# 4. 安装所有依赖
# 5. 配置知识库

# 如果PowerShell执行策略限制，先运行：
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 步骤4: 安装Python依赖（如果手动安装）

如果使用 `install_windows.ps1` 脚本，依赖会自动安装。如果需要手动安装：

```powershell
# 进入安装目录
cd C:\TRQuantPro\ope

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 升级pip
python -m pip install --upgrade pip setuptools wheel

# 安装核心依赖
pip install -r requirements.txt

# 安装知识库依赖（RAG）
pip install sentence-transformers chromadb

# 如果遇到TA-Lib安装问题（Windows常见），使用预编译版本：
# 1. 下载: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# 2. 安装: pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl
```

**Windows特殊依赖处理**:

```powershell
# TA-Lib (技术指标库) - Windows需要预编译版本
# 下载地址: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# 选择对应Python版本的.whl文件，然后：
pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl

# 如果PyQt6安装失败，尝试：
pip install PyQt6 --no-cache-dir

# 如果vectorbt安装失败，可能需要Visual C++ Build Tools
# 下载: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### 步骤5: 配置系统路径

**安装路径**: `C:\TRQuantPro\ope` (与Ubuntu结构一致)

系统会自动使用以下路径：
- **项目根目录**: `C:\TRQuantPro\ope`
- **知识库目录**: `C:\TRQuantPro\ope\.trquant\dev\knowledge`
- **用户数据目录**: `%LOCALAPPDATA%\TRQuant` (Windows标准位置)
  - 数据: `%LOCALAPPDATA%\TRQuant\data`
  - 缓存: `%LOCALAPPDATA%\TRQuant\cache`
  - 日志: `%LOCALAPPDATA%\TRQuant\logs`
  - 报告: `%LOCALAPPDATA%\TRQuant\reports`

**知识库路径**: 系统会自动检测并使用 `C:\TRQuantPro\ope\.trquant\dev\knowledge\`

### 步骤6: 配置JQData账号

编辑 `C:\TRQuantPro\ope\config\jqdata_config.json`:

```json
{
  "username": "你的JQData账号",
  "password": "你的JQData密码",
  "data_range": {
    "start_date": "2022-01-01",
    "end_date": "2024-12-31"
  }
}
```

⚠️ **安全提示**: 不要将包含密码的配置文件提交到Git仓库！

### 步骤7: 配置知识库（RAG）

知识库文件已包含在打包中，位于 `C:\TRQuantPro\ope\.trquant\dev\knowledge\`

**如果向量索引不存在**，需要构建：

```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1
python scripts\kb\kb_manager.py build-index
```

**验证知识库**:
```powershell
python scripts\kb\kb_manager.py stats
```

### 步骤8: 配置QMT（如果使用）

1. **确认Python版本**: 必须是3.11或3.10（QMT需要3.12以下）
   ```powershell
   python --version
   # 应显示: Python 3.11.x 或 3.10.x
   ```

2. **配置QMT SDK路径**: 在策略文件中设置QMT SDK路径
   - 参考: `docs\04_platform_integration\QMT_BRIDGE_GUIDE.md`

3. **测试QMT连接**: 
   ```powershell
   python -c "from core.qmt import QMTBridge; bridge = QMTBridge(); print('✅ QMT连接成功')"
   ```

---

## ⚙️ 配置调整

### 1. 路径分隔符调整

**问题**: Linux使用 `/`，Windows使用 `\`

**解决方案**: Python的 `pathlib.Path` 会自动处理，但需要检查硬编码路径：

```python
# ❌ 错误（硬编码Linux路径）
config_path = "/home/taotao/.local/share/trquant/config.json"

# ✅ 正确（跨平台）
from pathlib import Path
config_path = Path.home() / ".local" / "share" / "trquant" / "config.json"
# 或Windows特定：
config_path = Path.home() / "AppData" / "Local" / "TRQuant" / "config.json"
```

### 2. 文件权限调整

**问题**: Windows没有Linux的chmod权限系统

**解决方案**: 
- 大部分Python文件不需要执行权限
- 脚本文件使用 `.bat` 或 `.ps1` 替代 `.sh`

### 3. 环境变量设置

**创建Windows环境变量脚本** `setup_env.bat`:

```batch
@echo off
REM TRQuant Windows环境变量设置

set TRQUANT_HOME=C:\TRQuant
set TRQUANT_DATA=%LOCALAPPDATA%\TRQuant
set PYTHONPATH=%TRQUANT_HOME%;%PYTHONPATH%

echo ✅ TRQuant环境变量已设置
echo TRQUANT_HOME=%TRQUANT_HOME%
echo TRQUANT_DATA=%TRQUANT_DATA%
```

### 4. MongoDB连接配置（如果使用）

**Windows MongoDB默认配置**:
- 连接字符串: `mongodb://localhost:27017/`
- 数据目录: `C:\Program Files\MongoDB\Server\7.0\data\`

**修改连接配置**（如果MongoDB不在本地）:
```python
# config/mongodb_config.json
{
  "host": "localhost",
  "port": 27017,
  "database": "trquant",
  "username": "",  # 如果设置了认证
  "password": ""   # 如果设置了认证
}
```

---

## ✅ 验证安装

### 1. 验证Python环境

```powershell
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 检查Python版本
python --version

# 检查关键依赖
python -c "import pandas; import numpy; import jqdatasdk; print('✅ 核心依赖正常')"
```

### 2. 验证JQData连接

```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1

python -c "
from config.config_manager import get_config_manager
import jqdatasdk as jq

cm = get_config_manager()
jq_config = cm.get_config('jqdata')
jq.auth(jq_config['username'], jq_config['password'])
print('✅ JQData连接成功' if jq.is_auth() else '❌ JQData连接失败')
"
```

### 3. 验证知识库

```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1

# 检查知识库文件
python -c "
from pathlib import Path
kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
if kb_file.exists():
    import json
    kb = json.loads(kb_file.read_text(encoding='utf-8'))
    print(f'✅ 知识库文件存在，包含 {len(kb.get(\"items\", []))} 个条目')
else:
    print('⚠️  知识库文件不存在')
"

# 检查向量索引
python -c "
from pathlib import Path
idx_dir = Path('.trquant/dev/knowledge/vector_index')
if idx_dir.exists() and any(idx_dir.iterdir()):
    print('✅ 向量索引存在')
else:
    print('⚠️  向量索引不存在，需要构建')
"
```

### 4. 验证核心模块

```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1

python -c "
import sys
sys.path.insert(0, r'C:\TRQuantPro\ope')

from core.market_trend_analyzer import MarketTrendAnalyzer
from core.trend_analyzer import TrendAnalyzer
print('✅ 核心模块导入成功')
"
```

### 5. 验证QMT兼容性

```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1

python -c "
import sys
version = sys.version_info
if version.major == 3 and version.minor < 12:
    print(f'✅ Python版本兼容: {version.major}.{version.minor}.{version.micro} (QMT要求3.12以下)')
else:
    print(f'❌ Python版本不兼容: {version.major}.{version.minor}.{version.micro} (QMT需要3.12以下)')
"
```

### 4. 运行测试脚本

```powershell
# 运行依赖检查
python check_dependencies.py

# 运行配置验证
python verify_config.py
```

---

## 🚀 启动系统

### 方式1: 启动GUI（如果已安装）

```powershell
# 进入安装目录
cd C:\TRQuantPro\ope

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 启动GUI
python gui/main.py
```

### 方式2: 启动Jupyter Notebook

```powershell
# 进入安装目录
cd C:\TRQuantPro\ope

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 启动Jupyter
jupyter notebook notebooks\research\

# 或使用批处理脚本
.\start_jupyter.bat
```

### 方式3: 使用命令行工具

```powershell
# 进入安装目录
cd C:\TRQuantPro\ope

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 运行工作流
python scripts\workflow_9steps.py
```

---

## 🔧 常见问题

### Q1: Python模块导入失败

**问题**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
```powershell
# 确保虚拟环境已激活
.\venv\Scripts\Activate.ps1

# 重新安装依赖
pip install -r requirements.txt

# 检查PYTHONPATH
python -c "import sys; print('\n'.join(sys.path))"
```

### Q2: TA-Lib安装失败

**问题**: `error: Microsoft Visual C++ 14.0 is required`

**解决方案**:
1. 下载预编译的.whl文件: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
2. 选择对应Python版本的.whl文件
3. 安装: `pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl`

### Q3: PyQt6安装失败

**问题**: PyQt6在Windows上编译失败

**解决方案**:
```powershell
# 使用预编译版本
pip install PyQt6 --no-cache-dir

# 或使用conda（如果安装了Anaconda）
conda install pyqt
```

### Q4: 路径问题

**问题**: `FileNotFoundError` 或路径分隔符错误

**解决方案**:
- 使用 `pathlib.Path` 而不是字符串拼接
- 检查硬编码的Linux路径
- 使用相对路径或环境变量

### Q5: MongoDB连接失败

**问题**: `pymongo.errors.ServerSelectionTimeoutError`

**解决方案**:
```powershell
# 检查MongoDB服务是否运行
Get-Service MongoDB

# 如果未运行，启动服务
Start-Service MongoDB

# 或使用远程MongoDB
# 修改连接字符串为远程地址
```

### Q6: 权限问题

**问题**: `PermissionError` 或无法写入文件

**解决方案**:
- 以管理员身份运行PowerShell
- 检查文件夹权限
- 使用用户目录而不是系统目录

### Q7: Python版本问题（QMT）

**问题**: QMT连接失败，提示Python版本不兼容

**解决方案**:
- QMT需要Python 3.12以下版本
- 推荐使用Python 3.11
- 如果安装了多个Python版本，使用py启动器指定版本：
  ```powershell
  py -3.11 -m venv venv
  py -3.11 -m pip install -r requirements.txt
  ```

### Q8: 知识库向量索引构建失败

**问题**: `ModuleNotFoundError: No module named 'sentence_transformers'`

**解决方案**:
```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1
pip install sentence-transformers chromadb
python scripts\kb\kb_manager.py build-index
```

---

## 📝 迁移检查清单

### 迁移前
- [ ] 备份Linux系统上的配置文件（特别是 `config/jqdata_config.json`）
- [ ] 确认需要迁移的数据文件（如果有）
- [ ] 记录当前系统版本和依赖版本

### 打包时
- [ ] 排除缓存文件（`__pycache__`, `*.pyc`）
- [ ] 排除虚拟环境（`venv/`, `.venv/`）
- [ ] 排除数据文件（`data/`, `cache/`, `logs/`）
- [ ] 包含所有核心代码（`core/`, `mcp_servers/`, `notebooks/`）
- [ ] 包含配置文件模板（`config/`）
- [ ] 包含依赖列表（`requirements.txt`）
- [ ] **包含知识库文件**（`.trquant/dev/knowledge/`）
  - [ ] `knowledge_base.json`
  - [ ] `vector_index/` (如果存在)

### 安装后
- [ ] Python环境正常（`python --version`，必须是3.11或3.10）
- [ ] 虚拟环境创建成功（在 `C:\TRQuantPro\ope\venv`）
- [ ] 所有依赖安装成功（`pip list`）
- [ ] 知识库依赖已安装（`sentence-transformers`, `chromadb`）
- [ ] JQData连接正常
- [ ] 核心模块可以导入
- [ ] 配置文件已正确设置（`config\jqdata_config.json`）
- [ ] 路径配置已调整（安装路径: `C:\TRQuantPro\ope`）
- [ ] 知识库文件存在（`.trquant\dev\knowledge\knowledge_base.json`）
- [ ] 向量索引已构建或可以构建
- [ ] QMT兼容性验证通过（Python版本 < 3.12）
- [ ] 测试脚本运行正常

---

## 📚 相关文档

- **系统架构**: `docs/01_architecture/SYSTEM_REVIEW_AND_PLAN.md`
- **开发指南**: `docs/02_development_guides/`
- **配置说明**: `docs/JQDATA_CONFIGURATION_GUIDE.md`
- **CLAUDE.md**: 项目上下文文档

---

## 🆘 获取帮助

如果遇到问题：

1. **查看日志**: `%LOCALAPPDATA%\TRQuant\logs\`
2. **检查配置**: `config/jqdata_config.json`
3. **运行诊断**: `python check_dependencies.py`
4. **查看文档**: `docs/` 目录

---

**最后更新**: 2026-01-11  
**维护者**: TRQuant Team
