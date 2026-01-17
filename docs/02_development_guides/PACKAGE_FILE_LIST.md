# TRQuant Windows打包文件清单

> **版本**: v1.0  
> **更新**: 2026-01-11  
> **目的**: 明确列出需要打包的文件，优化打包大小

---

## 📋 打包策略

### 核心原则
1. **只打包源代码和配置文件** - 不包含可重建内容
2. **排除运行时生成文件** - 缓存、日志、数据等
3. **排除Python库** - 通过requirements.txt重建
4. **知识库JSON必需，向量索引可选** - 向量索引可以重建

---

## ✅ 必须打包的文件

### 1. 核心代码（必需）

```
core/                          # 核心功能模块
├── *.py                       # 所有Python源文件
├── market_regime/             # 市场环境识别
├── rotation/                  # 行业轮动
├── selection/                 # 标的筛选
├── backtest/                  # 回测模块
├── factors/                   # 因子库
├── strategy/                  # 策略开发
└── ...

mcp_servers/                   # MCP工具接口
├── *.py                       # 所有MCP服务器
├── utils/                     # 工具函数
└── ...

notebooks/                     # Jupyter Notebook研究前端
├── research/                  # 研究Notebook
├── lib/                       # Notebook工具库
└── ...

scripts/                       # 脚本文件
├── *.py                       # Python脚本
├── *.sh                       # Shell脚本
└── ...

strategies/                    # 策略文件
├── qmt/                       # QMT策略
├── ptrade/                    # PTrade策略
└── ...

data_sources/                  # 数据源模块
├── *.py                       # 数据源实现
└── ...
```

### 2. 配置文件（必需，使用模板）

```
config/
├── jqdata_config.json.example # 配置模板（不含密码）
├── config_manager.py          # 配置管理器
├── settings.py                # 系统设置
└── ...
```

### 3. 知识库（必需JSON，向量索引可选）

```
.trquant/dev/knowledge/
├── knowledge_base.json        # ✅ 必需 - 知识库JSON
└── vector_index/             # ⚠️ 可选 - 可以重建（约63MB）
    └── ...
```

**说明**:
- `knowledge_base.json` 是必需的，包含所有知识条目
- `vector_index/` 可以重建，如果包含会增加约63MB
- 重建命令: `python scripts/kb/kb_manager.py build-index`

### 4. 依赖列表（必需）

```
requirements.txt               # Python依赖列表
requirements-dev.txt           # 开发依赖（可选）
```

### 5. 文档（精简版）

```
docs/
├── MUST_READ/                 # 必读文档
├── 02_development_guides/
│   ├── WINDOWS_MIGRATION_GUIDE.md  # Windows迁移指南
│   └── ABD_MERGE_COMPLETE.md       # 合并报告
├── 01_architecture/           # 架构文档
└── 04_platform_integration/
    └── QMT_BRIDGE_GUIDE.md    # QMT桥接指南
```

### 6. 根目录文件（必需）

```
README.md                      # 项目说明
CLAUDE.md                      # AI助手上下文文档
README_WINDOWS_MIGRATION.md    # Windows迁移快速指南
*.py                           # Python入口文件（如果有）
```

---

## ❌ 不需要打包的文件

### 1. Python环境（可重建）

```
venv/                          # ❌ Python虚拟环境（9.5GB）
.venv/                         # ❌ 虚拟环境
.venv_playwright/              # ❌ Playwright虚拟环境
```

**重建方式**: 
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 缓存和临时文件（运行时生成）

```
__pycache__/                   # ❌ Python缓存（4,224个目录）
*.pyc                          # ❌ 编译文件（32,702个文件）
*.pyo                          # ❌ 优化文件
*.egg-info/                    # ❌ 包信息
.pytest_cache/                 # ❌ 测试缓存
```

### 3. 数据文件（可重新下载）

```
data/                          # ❌ 数据文件（565MB）
cache/                         # ❌ 缓存文件
```

**说明**: 数据可以通过JQData重新下载

### 4. 运行时生成文件（可重建）

```
logs/                          # ❌ 日志文件（9.9MB）
reports/                       # ❌ 报告文件（12MB）
results/                       # ❌ 结果文件（5.5MB）
backtest_results/              # ❌ 回测结果（14MB）
output/                        # ❌ 输出文件（75MB）
```

### 5. 第三方库（如果存在）

```
third_party/                   # ❌ 第三方库（7.6GB）
node_modules/                  # ❌ Node.js依赖（23MB）
```

### 6. 可选模块（根据需要）

```
extension/                     # ⚠️ 可选 - Cursor扩展（538MB）
frontend/                      # ⚠️ 可选 - 前端代码
gui/                           # ⚠️ 可选 - GUI界面
```

### 7. 其他不需要的文件

```
.git/                          # ❌ Git目录
.vscode/                       # ❌ VS Code配置
.cursor/                       # ❌ Cursor配置
*.vsix                         # ❌ VS Code扩展包（多个，共约250MB）
```

---

## 📊 文件大小对比

### 完整打包（包含所有文件）
- **总大小**: ~20GB
- **主要占用**:
  - venv: 9.5GB
  - third_party: 7.6GB
  - data: 565MB
  - extension: 538MB
  - docs: 342MB

### 最小化打包（只包含必需文件）
- **预计大小**: ~500MB - 1GB
- **主要包含**:
  - core: 17MB
  - mcp_servers: 33MB
  - notebooks: 35MB
  - scripts: 14MB
  - docs: ~100MB（精简版）
  - 其他: ~300MB

### 压缩后大小
- **预计**: ~200-400MB（取决于是否包含向量索引）

---

## 🔧 打包脚本

### 最小化打包脚本

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./scripts/package_for_windows_minimal.sh
```

### 脚本功能

1. **自动排除**:
   - `__pycache__/`, `*.pyc`, `*.pyo`
   - `venv/`, `.venv/`
   - `data/`, `cache/`, `logs/`, `reports/`, `results/`
   - `.git/`, `node_modules/`

2. **交互式选择**:
   - 是否包含向量索引（可重建）
   - 是否包含GUI模块（可选）
   - 是否包含Extension（可选）

3. **自动创建**:
   - Windows安装脚本
   - 配置文件模板
   - 启动脚本

---

## 📝 重建清单

在Windows上安装后，以下内容会自动重建：

### 自动重建（通过安装脚本）

1. **Python虚拟环境**
   ```powershell
   python -m venv venv
   ```

2. **Python依赖库**
   ```powershell
   pip install -r requirements.txt
   ```

3. **知识库向量索引**（如果未包含）
   ```powershell
   python scripts\kb\kb_manager.py build-index
   ```

### 运行时生成

1. **数据文件** - 首次运行时自动下载
2. **缓存文件** - 运行时自动生成
3. **日志文件** - 运行时自动创建
4. **报告文件** - 生成报告时创建

---

## ✅ 验证清单

打包后验证：

- [ ] 核心代码完整（core/, mcp_servers/, notebooks/）
- [ ] 配置文件存在（config/）
- [ ] 知识库JSON存在（.trquant/dev/knowledge/knowledge_base.json）
- [ ] 依赖列表存在（requirements.txt）
- [ ] 文档存在（docs/，精简版）
- [ ] 安装脚本存在（install_windows.ps1）
- [ ] 无Python缓存文件（__pycache__/, *.pyc）
- [ ] 无虚拟环境（venv/）
- [ ] 无数据文件（data/）
- [ ] 无日志文件（logs/）

---

## 🎯 推荐打包方式

### 方式1: 最小化打包（推荐）

```bash
./scripts/package_for_windows_minimal.sh
```

**优点**:
- 文件小（~200-400MB压缩后）
- 传输快
- 安装快

**缺点**:
- 需要重建向量索引（约5-10分钟）

### 方式2: 包含向量索引

在最小化打包时选择包含向量索引

**优点**:
- 无需重建向量索引
- 安装后立即可用

**缺点**:
- 文件稍大（~300-500MB压缩后）

---

**最后更新**: 2026-01-11  
**维护者**: TRQuant Team
