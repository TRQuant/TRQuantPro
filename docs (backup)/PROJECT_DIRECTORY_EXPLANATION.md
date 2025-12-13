# 项目目录完整说明

## 📋 目录全情

### 两个目录的由来

#### 1. 主项目目录（开发目录）
**路径**：`/home/taotao/dev/QuantTest/TRQuant`
- **性质**：Git仓库，源代码管理
- **用途**：版本控制、代码开发、Git提交
- **特点**：
  - ✅ 可以在Cursor中打开和管理
  - ✅ 有完整的Git历史
  - ✅ 适合团队协作
  - ⚠️ 代码可能不是最新的（如果没同步）

#### 2. 用户数据目录（运行目录）
**路径**：`/home/taotao/.local/share/jqquant`
- **性质**：安装后的应用目录（符合Linux XDG标准）
- **用途**：实际运行、数据存储、用户配置
- **特点**：
  - ✅ 包含所有最新代码
  - ✅ 包含运行时数据（缓存、日志、报告）
  - ✅ 符合Linux桌面应用标准
  - ❌ 不是Git仓库
  - ❌ 不能直接在Cursor中管理

## 🔍 什么时候开始在.local里面工作的？

### 历史原因

根据代码分析，这个变化发生在**安装脚本（install.sh）**被创建时：

1. **安装脚本的设计**（`install.sh`）：
   ```bash
   INSTALL_DIR="${HOME}/.local/share/jqquant"
   ```
   - 将项目安装到用户数据目录
   - 符合Linux XDG Base Directory规范
   - 创建桌面快捷方式和应用图标

2. **Docker脚本的设计**（`docker/run_gui_container.sh`）：
   ```bash
   DATA_ROOT="${HOME}/.local/share/jqquant"
   ```
   - Docker容器挂载用户数据目录
   - 保持配置和数据持久化

3. **启动脚本的设计**（`scripts/sync_shortcuts.sh`）：
   ```bash
   DEFAULT_APP_DIR="$INSTALL_DIR"  # ~/.local/share/jqquant
   FALLBACK_APP_DIR="$PROJECT_ROOT"  # /home/taotao/dev/QuantTest/TRQuant
   ```
   - 优先使用安装目录
   - 如果不存在，回退到项目目录

### 设计意图

这个设计是为了：
1. **桌面应用化**：将项目作为标准的Linux桌面应用安装
2. **数据分离**：代码和数据分离，符合应用管理规范
3. **多用户支持**：每个用户有独立的数据目录
4. **Docker集成**：容器化部署时使用统一的数据目录

## 🎯 使用.local目录的意义

### 优势

1. **符合Linux标准**
   - 遵循XDG Base Directory规范
   - 用户数据存储在 `~/.local/share/`
   - 配置文件存储在 `~/.config/`

2. **数据持久化**
   - 运行时数据（缓存、日志、报告）独立存储
   - 不会污染源代码目录
   - 便于备份和迁移

3. **Docker友好**
   - 容器挂载用户数据目录
   - 配置和数据在容器外持久化
   - 容器重建不影响数据

4. **多环境支持**
   - 开发环境：主项目目录
   - 生产环境：用户数据目录
   - 可以同时存在

### 劣势

1. **版本控制困难**
   - 不是Git仓库
   - 代码更改无法直接提交
   - 需要手动同步

2. **Cursor管理不便**
   - 不能直接在Cursor中打开
   - 需要手动同步代码

3. **双目录维护**
   - 需要保持两个目录同步
   - 容易产生不一致

## 🐳 与Docker的关系

### Docker配置

查看 `docker/run_gui_container.sh`：

```bash
DATA_ROOT="${HOME}/.local/share/jqquant"
CONFIG_DIR="${DATA_ROOT}/config"
LOGS_DIR="${DATA_ROOT}/logs"
RESULTS_DIR="${DATA_ROOT}/results"
```

**设计逻辑**：
1. Docker容器挂载用户数据目录
2. 配置、日志、结果都存储在用户目录
3. 容器重建时数据不丢失

### Docker运行流程

```
1. 构建Docker镜像（从主项目目录）
   ↓
2. 运行容器时挂载 ~/.local/share/jqquant
   ↓
3. 容器内使用挂载的目录
   ↓
4. 数据持久化在用户目录
```

## 🔄 如果换回主项目，需要做什么调整？

### 方案1：完全切换回主项目（推荐用于开发）

#### 步骤1：同步代码
```bash
# 使用同步脚本
cd /home/taotao/.local/share/jqquant
python scripts/sync_to_main_project.py
```

#### 步骤2：修改路径配置

**修改 `config/settings.py`**：
```python
# 原代码（使用相对路径）
PROJECT_ROOT = Path(__file__).parent.parent

# 如果需要，可以改为绝对路径
# PROJECT_ROOT = Path('/home/taotao/dev/QuantTest/TRQuant')
```

#### 步骤3：修改启动脚本

**修改 `scripts/sync_shortcuts.sh`**：
```bash
# 改为优先使用项目目录
DEFAULT_APP_DIR="$PROJECT_ROOT"
FALLBACK_APP_DIR="$INSTALL_DIR"
```

#### 步骤4：修改Docker配置（可选）

**修改 `docker/run_gui_container.sh`**：
```bash
# 改为使用项目目录
DATA_ROOT="${PROJECT_ROOT}"
# 或保持原样，但挂载项目目录
```

#### 步骤5：在Cursor中打开主项目
```bash
# 在Cursor中打开
/home/taotao/dev/QuantTest/TRQuant
```

### 方案2：保持双目录，但主目录作为开发目录（推荐）

#### 工作流程

1. **开发时**：
   - 在Cursor中打开主项目目录
   - 在主目录中编写代码
   - 使用Git管理版本

2. **运行时**：
   - 使用安装目录运行
   - 或定期同步到安装目录

3. **同步策略**：
   - 开发完成后同步到安装目录
   - 使用同步脚本自动化

#### 配置调整

**创建环境变量配置**（`config/settings.py`）：
```python
import os
from pathlib import Path

# 检测运行模式
if os.getenv('JQQUANT_DEV_MODE') == '1':
    # 开发模式：使用主项目目录
    PROJECT_ROOT = Path('/home/taotao/dev/QuantTest/TRQuant')
else:
    # 生产模式：使用安装目录
    PROJECT_ROOT = Path(__file__).parent.parent
```

**启动时设置环境变量**：
```bash
# 开发模式运行
JQQUANT_DEV_MODE=1 python JQQuant.py

# 生产模式运行（默认）
python JQQuant.py
```

### 方案3：使用符号链接（不推荐）

```bash
# 创建符号链接（可能导致Git混乱）
ln -s /home/taotao/dev/QuantTest/TRQuant /home/taotao/.local/share/jqquant
```

**问题**：
- Git可能无法正确处理
- 可能导致循环引用
- 不推荐使用

## 📝 推荐方案

### 当前阶段：双目录模式

1. **开发**：在主项目目录（`/home/taotao/dev/QuantTest/TRQuant`）
   - 在Cursor中打开
   - 使用Git管理
   - 编写和测试代码

2. **运行**：在安装目录（`~/.local/share/jqquant`）
   - 使用桌面快捷方式启动
   - 或Docker容器运行
   - 数据持久化

3. **同步**：定期同步
   - 开发完成后运行同步脚本
   - 提交到Git

### 未来优化：统一到主项目

1. **修改配置**：支持环境变量切换
2. **修改启动脚本**：优先使用主项目目录
3. **修改Docker**：挂载主项目目录
4. **统一工作流**：所有开发在主项目进行

## 🔧 具体调整步骤

### 立即可以做的

1. **创建同步脚本**（已完成）
   - `scripts/sync_to_main_project.py`

2. **修改settings.py支持环境变量**：
```python
import os
from pathlib import Path

# 支持环境变量切换
if os.getenv('JQQUANT_DEV_MODE') == '1':
    PROJECT_ROOT = Path('/home/taotao/dev/QuantTest/TRQuant')
else:
    # 尝试检测当前目录
    current_file = Path(__file__).resolve()
    if 'dev/QuantTest' in str(current_file):
        PROJECT_ROOT = Path('/home/taotao/dev/QuantTest/TRQuant')
    else:
        PROJECT_ROOT = Path(__file__).parent.parent
```

3. **在Cursor中打开主项目**：
   - File → Open Folder
   - 选择 `/home/taotao/dev/QuantTest/TRQuant`

4. **定期同步**：
   ```bash
   cd ~/.local/share/jqquant
   python scripts/sync_to_main_project.py
   cd /home/taotao/dev/QuantTest/TRQuant
   git add .
   git commit -m "同步最新代码"
   ```

## ⚠️ 注意事项

1. **路径硬编码**
   - 检查代码中是否有硬编码路径
   - 使用 `PROJECT_ROOT` 或环境变量

2. **数据目录**
   - 数据目录（cache、logs、reports）可以保持独立
   - 或使用符号链接指向统一位置

3. **Git忽略**
   - 确保 `.gitignore` 正确配置
   - 排除缓存、日志等文件

4. **Docker挂载**
   - 如果使用Docker，需要调整挂载路径
   - 或保持当前配置（挂载用户目录）

## 📋 检查清单

切换前：
- [ ] 备份两个目录
- [ ] 检查Git状态
- [ ] 确认要同步的文件
- [ ] 检查路径引用

切换后：
- [ ] 验证代码运行
- [ ] 检查数据目录
- [ ] 测试Docker（如果使用）
- [ ] 提交Git更改

---

*最后更新：2024-11-29*

