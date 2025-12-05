# 项目目录同步指南

## 📁 目录结构说明

### 1. 项目主目录（Git仓库）
**路径**：`/home/taotao/dev/QuantTest/TRQuant`
- ✅ Git仓库，可以版本控制
- ✅ 可以在Cursor中打开和管理
- ⚠️ 代码可能不是最新的

### 2. 实际工作目录（用户数据目录）
**路径**：`/home/taotao/.local/share/jqquant`
- ✅ 包含所有最新的代码和文档
- ✅ 实际运行时的目录
- ❌ 不是Git仓库，不能版本控制
- ❌ 不能直接在Cursor中管理（不在工作区）

## 🔍 两个目录的区别

### 相同点
- 都包含项目代码（`gui/`, `core/`, `markets/`等）
- 都包含文档（`docs/`）
- 都包含配置文件（`config/`）

### 不同点

| 项目 | 主目录 | 工作目录 |
|------|--------|----------|
| Git管理 | ✅ 是Git仓库 | ❌ 不是Git仓库 |
| Cursor管理 | ✅ 可以打开 | ❌ 不能直接打开 |
| 代码更新 | ⚠️ 可能滞后 | ✅ 最新代码 |
| 数据文件 | 较少 | 较多（缓存、报告等） |
| 大小 | ~2.3GB | ~2.2GB |

## 🎯 需要同步的内容

### ✅ 需要同步（代码和文档）

1. **代码文件**
   - `gui/` - GUI界面代码
   - `markets/` - 市场数据模块
   - `core/` - 核心功能
   - `utils/` - 工具函数
   - `jqdata/` - JQData集成
   - `ptrade_bridge/` - PTrade桥接
   - `qmt_bridge/` - QMT桥接
   - `quantconnect_bridge/` - QuantConnect桥接

2. **文档文件**
   - `docs/` - 所有Markdown文档
   - `README.md` - 项目说明
   - 其他`.md`文件

3. **配置文件**
   - `config/` - 配置文件（不含敏感信息）
   - `requirements.txt` - 依赖列表
   - `JQQuant.py` - 主入口文件

4. **脚本文件**
   - `scripts/` - 脚本文件
   - `*.py` - Python脚本（不含缓存）

### ❌ 不需要同步（数据和缓存）

1. **缓存文件**
   - `cache/` - 数据缓存
   - `__pycache__/` - Python缓存
   - `*.pyc` - 编译文件

2. **数据文件**
   - `data/` - 数据文件（MongoDB数据）
   - `logs/` - 日志文件
   - `reports/` - 生成的报告（可选）

3. **虚拟环境**
   - `venv/` - Python虚拟环境
   - `jqdata_env/` - JQData环境

4. **其他**
   - `node_modules/` - Node.js依赖
   - `.git/` - Git目录（主目录已有）

## 🔄 同步方案

### 方案1：手动同步（推荐用于重要更新）

使用提供的同步脚本：

```bash
# 从工作目录同步到主目录
cd /home/taotao/.local/share/jqquant
python scripts/sync_to_main_project.py
```

### 方案2：符号链接（不推荐）

创建符号链接可能导致Git混乱，不推荐。

### 方案3：直接在主目录工作（推荐长期方案）

**步骤**：
1. 将主目录设置为工作目录
2. 修改代码中的路径引用
3. 在Cursor中打开主目录

## 📝 同步脚本使用

### 创建同步脚本

脚本位置：`/home/taotao/.local/share/jqquant/scripts/sync_to_main_project.py`

**功能**：
- 同步代码文件到主目录
- 排除缓存和数据文件
- 保留Git历史
- 显示同步进度

**使用方法**：
```bash
cd /home/taotao/.local/share/jqquant
python scripts/sync_to_main_project.py
```

## ⚠️ 注意事项

1. **备份重要数据**
   - 同步前建议备份主目录
   - 特别是未提交的更改

2. **检查差异**
   - 同步前检查两个目录的差异
   - 确认要同步的文件

3. **Git提交**
   - 同步后记得在主目录提交更改
   - 使用有意义的提交信息

4. **路径引用**
   - 检查代码中的硬编码路径
   - 使用相对路径或环境变量

## 🎯 最佳实践

### 短期方案（当前）

1. 在`.local/share/jqquant`中开发
2. 定期同步到主目录
3. 在主目录提交Git

### 长期方案（推荐）

1. **切换到主目录工作**
   - 在Cursor中打开`/home/taotao/dev/QuantTest/TRQuant`
   - 修改代码中的路径引用
   - 使用环境变量或配置文件管理路径

2. **统一工作目录**
   - 所有开发在主目录进行
   - `.local/share/jqquant`仅用于运行时数据

3. **路径配置**
   - 使用配置文件管理路径
   - 支持多环境（开发/生产）

## 🔧 路径配置示例

在`config/settings.py`中：

```python
import os
from pathlib import Path

# 项目根目录
if os.getenv('JQQUANT_DEV_MODE'):
    # 开发模式：使用主目录
    PROJECT_ROOT = Path('/home/taotao/dev/QuantTest/TRQuant')
else:
    # 生产模式：使用用户目录
    PROJECT_ROOT = Path.home() / '.local/share/jqquant'

# 数据目录
DATA_DIR = PROJECT_ROOT / 'data'
CACHE_DIR = PROJECT_ROOT / 'cache'
REPORTS_DIR = PROJECT_ROOT / 'reports'
```

## 📋 同步检查清单

同步前检查：
- [ ] 备份主目录
- [ ] 检查Git状态
- [ ] 确认要同步的文件
- [ ] 检查路径引用

同步后检查：
- [ ] 验证文件同步成功
- [ ] 检查Git状态
- [ ] 测试代码运行
- [ ] 提交Git更改

---

*最后更新：2024-11-29*

