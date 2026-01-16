# TRQuant 韬睿量化系统 - Windows工作站安装配置指南

> **版本**: v2.0  
> **更新**: 2026-01-16  
> **目的**: Windows工作站完整安装和配置指南  
> **Windows安装路径**: `C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope`

---

## 📋 目录

1. [系统要求](#系统要求)
2. [环境准备](#环境准备)
3. [安装步骤](#安装步骤)
4. [配置设置](#配置设置)
5. [Git同步配置](#git同步配置)
6. [知识库设置](#知识库设置)
7. [验证安装](#验证安装)
8. [日常使用](#日常使用)
9. [故障排除](#故障排除)

---

## 💻 系统要求

### Windows系统要求

- **操作系统**: Windows 10/11 (64位)
- **内存**: 至少 8GB RAM（推荐16GB）
- **磁盘空间**: 至少 20GB 可用空间
- **权限**: 管理员权限（用于安装Python和依赖）

### 必需软件

- **Python**: 3.9+ (推荐 3.11，QMT需要3.12以下)
- **Git**: Git for Windows
- **MongoDB**: 可选，如果需要本地数据库
- **Node.js**: 18+ (如果使用Cursor扩展)

---

## 🔧 环境准备

### 步骤1: 安装Python

1. 下载Python 3.11
   - 访问: https://www.python.org/downloads/
   - 选择: Python 3.11.x (64-bit)
   - ⚠️ **重要**: 安装时勾选 "Add Python to PATH"

2. 验证安装
   ```powershell
   python --version
   # 应该显示: Python 3.11.x
   
   pip --version
   # 应该显示: pip 23.x.x
   ```

### 步骤2: 安装Git

1. 下载Git for Windows
   - 访问: https://git-scm.com/download/win
   - 下载并安装

2. 验证安装
   ```powershell
   git --version
   # 应该显示: git version 2.x.x
   ```

### 步骤3: 创建项目目录

```powershell
# 创建项目目录
New-Item -ItemType Directory -Force -Path "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"

# 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
```

---

## 📦 安装步骤

### 方法1: 从Git仓库克隆（推荐）

```powershell
# 1. 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro

# 2. 克隆仓库
git clone https://[TOKEN]@github.com/TRQuant/TRQuantPro.git ope

# 3. 进入项目目录
cd ope

# 4. 切换到windows分支
git checkout windows
```

### 方法2: 从压缩包安装

如果已有打包文件：

```powershell
# 1. 解压文件到临时目录
# 例如: C:\Temp\TRQuant

# 2. 复制文件到项目目录
Copy-Item -Path "C:\Temp\TRQuant\*" -Destination "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope" -Recurse -Force

# 3. 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
```

### 步骤: 创建Python虚拟环境

```powershell
# 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 如果遇到执行策略错误，运行:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 升级pip
python -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

---

## ⚙️ 配置设置

### 步骤1: 配置JQData

编辑配置文件:

```powershell
# 使用文本编辑器打开配置文件
notepad config\jqdata_config.json
```

配置内容:

```json
{
  "username": "你的JQData账号",
  "password": "你的JQData密码"
}
```

### 步骤2: 配置系统路径

编辑 `config/settings.py`（如果存在），确保路径正确:

```python
# Windows路径配置
PROJECT_ROOT = r"C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
```

### 步骤3: 配置环境变量（可选）

如果需要全局访问，可以添加到系统环境变量:

```powershell
# 添加到PATH环境变量
[Environment]::SetEnvironmentVariable(
    "TRQUANT_HOME",
    "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope",
    "User"
)
```

---

## 🔄 Git同步配置

### 步骤1: 配置Git用户信息

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 配置Git用户信息
git config user.name "TRQuant"
git config user.email "zhutechllc@gmail.com"

# 验证配置
git config user.name
git config user.email
```

### 步骤2: 配置远程仓库

```powershell
# 配置远程仓库（请替换[TOKEN]为实际Token）
git remote set-url origin https://[TOKEN]@github.com/TRQuant/TRQuantPro.git

# 验证配置
git remote -v
```

### 步骤3: 创建并切换到windows分支

```powershell
# 创建windows分支
git checkout -b windows

# 首次推送
git push -u origin windows
```

### 步骤4: 验证Git配置

```powershell
# 测试连接
git ls-remote origin

# 拉取最新代码
git pull origin windows
```

---

## 📚 知识库设置

### 步骤1: 检查知识库文件

```powershell
# 检查知识库JSON文件
Test-Path .trquant\dev\knowledge\knowledge_base.json

# 应该返回: True
```

### 步骤2: 重建向量索引（如果需要）

```powershell
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 重建向量索引
python scripts\kb\kb_manager.py build-index
```

### 步骤3: 验证知识库

```powershell
# 查看知识库统计
python scripts\kb\kb_manager.py stats
```

---

## ✅ 验证安装

### 步骤1: 测试Python环境

```powershell
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 测试导入核心模块
python -c "from core.market_trend_analyzer import MarketTrendAnalyzer; print('✅ 核心模块导入成功')"
```

### 步骤2: 测试JQData连接

```powershell
# 测试JQData连接
python -c "import jqdatasdk as jq; from config.config_manager import get_config_manager; cm = get_config_manager(); jq_config = cm.get_config('jqdata'); jq.auth(jq_config['username'], jq_config['password']); print('✅ JQData连接成功')"
```

### 步骤3: 测试Git同步

```powershell
# 测试Git同步脚本
.\scripts\sync\pull_common_modules.ps1
```

### 步骤4: 测试知识库

```powershell
# 测试知识库搜索
python scripts\kb\kb_manager.py search "市场趋势分析" --limit 5
```

---

## 📋 日常使用

### 每天开始工作前

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 1. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 2. 拉取最新代码
.\scripts\sync\pull_common_modules.ps1

# 3. 检查知识库更新
python scripts\kb\kb_manager.py stats
```

### 更新知识库后

```powershell
# 同步知识库到Git
.\scripts\sync\sync_knowledge_base.ps1
```

### 修改共用模块后

```powershell
# 同步共用模块到Git
.\scripts\sync\sync_common_modules.ps1
```

### 运行Jupyter Notebook

```powershell
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 启动Jupyter Notebook
jupyter notebook notebooks\research\
```

---

## 🔧 故障排除

### 问题1: Python虚拟环境激活失败

**错误**: `无法加载文件，因为在此系统上禁止运行脚本`

**解决方案**:
```powershell
# 设置执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 重新激活虚拟环境
.\venv\Scripts\Activate.ps1
```

### 问题2: pip安装失败

**错误**: `pip install` 失败或超时

**解决方案**:
```powershell
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3: TA-Lib安装失败

**错误**: `TA-Lib` 安装失败

**解决方案**:
1. 下载预编译版本: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
2. 选择对应Python版本的.whl文件
3. 安装: `pip install TA_Lib-0.4.xx-cp311-cp311-win_amd64.whl`

### 问题4: Git推送失败（403错误）

**错误**: `Permission denied`

**解决方案**:
1. 检查Token权限（需要 `repo` 权限）
2. 验证Token是否过期
3. 确认账号有仓库访问权限

### 问题5: 知识库向量索引重建失败

**错误**: 向量索引重建失败

**解决方案**:
```powershell
# 检查依赖
pip install chromadb sentence-transformers

# 手动重建
python scripts\kb\kb_manager.py build-index
```

---

## 📝 相关文档

- `docs/WORKSTATION_SYNC_MANAGEMENT_GUIDE.md` - 工作站同步与日常管理指南
- `docs/GIT_TOKEN_CONFIG.md` - Git Token配置说明
- `docs/GIT_SYNC_COMPLETE_GUIDE.md` - Git同步完整指南
- `docs/CROSS_PLATFORM_SYNC_GUIDE.md` - 跨平台同步指南

---

## 🎯 快速参考

### 常用命令

```powershell
# 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 拉取最新代码
.\scripts\sync\pull_common_modules.ps1

# 同步知识库
.\scripts\sync\sync_knowledge_base.ps1

# 同步共用模块
.\scripts\sync\sync_common_modules.ps1

# 启动Jupyter Notebook
jupyter notebook notebooks\research\
```

### 目录结构

```
C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\
├── core/                          # 核心功能模块
├── mcp_servers/                   # MCP服务器
├── notebooks/                     # Jupyter Notebook
├── scripts/                       # 脚本文件
│   └── sync/                      # 同步脚本
├── config/                        # 配置文件
├── .trquant/                      # 知识库目录
│   └── dev/
│       └── knowledge/
├── venv/                          # Python虚拟环境
└── docs/                          # 文档
```

---

**最后更新**: 2026-01-16  
**维护者**: TRQuant Team
