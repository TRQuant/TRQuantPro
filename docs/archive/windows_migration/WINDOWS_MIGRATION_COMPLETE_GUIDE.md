# TRQuant Windows迁移完整指南

> **版本**: v1.0  
> **更新**: 2026-01-15  
> **目的**: 从Ubuntu系统迁移到Windows系统的完整流程

---

## 📋 迁移流程概览

```
Ubuntu端 (已完成)
  ↓
1. 打包所有必需文件 ✅
  ↓
2. 上传到云存储 📤
  ↓
3. Windows端下载 📥
  ↓
4. 解压和安装 🔧
  ↓
5. 配置Git同步 🔄
  ↓
6. 验证和测试 ✅
```

---

## ✅ 步骤1: Ubuntu端打包（已完成）

### 打包结果

- **压缩包位置**: `/mnt/data/TRQuant_backup/TRQuant_Windows_Transfer_20260115_155034.tar.gz`
- **压缩包大小**: 约70M
- **打包大小**: 约328M（解压后）

### 包含内容

✅ **核心代码**
- `core/` - 核心功能实现
- `mcp_servers/` - MCP工具接口
- `notebooks/` - Jupyter Notebook
- `scripts/` - 脚本文件（已分类）
- `strategies/` - 策略文件
- `data_sources/` - 数据源模块

✅ **知识库（必须同步）**
- `.trquant/dev/knowledge/knowledge_base.json` ✅
- `.trquant/dev/knowledge/strategy_knowledge/` ✅
- `.trquant/dev/knowledge/vector_index/` ✅ (可选，可重建)

✅ **文档**
- `docs/` - 完整文档（分门别类）
- `CLAUDE.md`, `QUICK_START.txt`

✅ **配置文件**
- `requirements.txt` - Python依赖
- `pyproject.toml` - 项目配置
- `config/` - 配置文件（模板）

✅ **安装指南**
- `WINDOWS_INSTALL_GUIDE.md` - Windows安装指南
- `CROSS_PLATFORM_SYNC_GUIDE.md` - 跨平台同步指南
- `PACKAGE_MANIFEST.txt` - 打包清单

---

## 📤 步骤2: 上传到云存储

### 推荐云存储

1. **百度网盘** - 国内速度快，免费2TB
2. **阿里云盘** - 不限速，免费1TB
3. **OneDrive** - 微软官方，与Windows集成好
4. **腾讯微云** - 国内速度快

### 上传步骤

1. 打开云存储客户端或网页版
2. 找到压缩包：`TRQuant_Windows_Transfer_20260115_155034.tar.gz`
3. 上传到云存储（约70M，上传时间取决于网速）
4. 记录分享链接（如果需要）

---

## 📥 步骤3: Windows端下载

### 下载步骤

1. 在Windows电脑上打开云存储
2. 下载压缩包到临时目录（如 `C:\Users\YourName\Downloads\`）
3. 等待下载完成

---

## 📦 步骤4: 解压和安装

### 4.1 解压文件

1. 使用7-Zip或WinRAR解压压缩包
2. 解压到目标目录：`C:\TRQuantPro\ope\`
3. 确保目录结构正确

### 4.2 创建Python虚拟环境

```powershell
# 打开PowerShell（管理员权限）
cd C:\TRQuantPro\ope

# 创建虚拟环境（Python 3.11）
py -3.11 -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1
```

⚠️ **重要**: 如果遇到执行策略错误，运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4.3 安装Python依赖

```powershell
# 升级pip
python -m pip install --upgrade pip setuptools wheel

# 安装核心依赖
pip install -r requirements.txt

# 安装知识库依赖（RAG）
pip install sentence-transformers chromadb

# 如果使用QMT，需要TA-Lib（可能需要预编译版本）
# 下载: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# 安装: pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl
```

### 4.4 配置JQData

编辑 `config\jqdata_config.json`:
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

⚠️ **安全提示**: 不要将包含密码的配置文件提交到Git！

### 4.5 重建向量索引（可选）

如果向量索引缺失或需要重建：

```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1
python scripts\kb\kb_manager.py build-index
```

### 4.6 验证安装

```powershell
# 验证Python环境
python --version
# 应显示: Python 3.11.x

# 验证核心模块
python -c "from core.market_trend_analyzer import MarketTrendAnalyzer; print('✅ 核心模块正常')"

# 验证知识库
python scripts\kb\kb_manager.py stats
```

---

## 🔄 步骤5: 配置Git同步

### 5.1 初始化Git仓库

```powershell
cd C:\TRQuantPro\ope

# 初始化Git（如果还没有）
git init

# 添加远程仓库
git remote add origin https://github.com/TRQuant/TRQuant_ope.git

# 创建Windows分支
git checkout -b windows

# 或从远程拉取
git fetch origin
git checkout -b windows origin/windows
```

### 5.2 配置Git用户信息

```powershell
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 5.3 首次提交

```powershell
# 添加所有文件
git add .

# 提交
git commit -m "feat: Windows系统初始迁移"

# 推送到远程（如果已设置）
git push -u origin windows
```

---

## 📚 步骤6: 知识库同步设置

### 6.1 验证知识库

```powershell
# 检查知识库文件
python scripts\kb\kb_manager.py stats

# 应该显示知识库统计信息
```

### 6.2 设置自动同步

#### 方案1: 手动同步（推荐）

每次更新知识库后：

```powershell
# 更新知识库后
python scripts\kb\sync_knowledge_base.py push

# 提交到Git
git add .trquant\dev\knowledge\knowledge_base.json
git commit -m "sync: 知识库更新"
git push origin windows
```

#### 方案2: 定时同步

使用Windows任务计划程序，每天9点运行：
```powershell
C:\TRQuantPro\ope\scripts\kb\sync_kb_daily.ps1
```

---

## 🚀 步骤7: 启动系统

### 启动Jupyter Notebook

```powershell
cd C:\TRQuantPro\ope
.\venv\Scripts\Activate.ps1
jupyter notebook notebooks\research\
```

### 启动GUI（如果已安装）

```powershell
python gui\main.py
```

---

## ⚠️ 注意事项

### Python版本

- **必须是3.11或3.10**（QMT需要3.12以下）
- 不要使用3.12+，会导致QMT不兼容

### 路径分隔符

- Windows使用 `\`，但Python的`pathlib`会自动处理
- 在代码中使用 `Path` 对象，不要硬编码路径

### 文件权限

- Windows没有Linux的`chmod`，大部分文件不需要特殊权限
- 如果遇到权限问题，以管理员身份运行

### 知识库同步

- **定期同步**: 每天开始工作前拉取最新知识库
- **及时推送**: 更新知识库后立即推送到Git
- **冲突处理**: 使用自动合并工具解决冲突

---

## 🔧 常见问题

### Q1: Python虚拟环境激活失败

**解决方案**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q2: TA-Lib安装失败

**解决方案**: 使用预编译版本
1. 下载: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
2. 安装: `pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl`

### Q3: 知识库向量索引缺失

**解决方案**: 重建索引
```powershell
python scripts\kb\kb_manager.py build-index
```

### Q4: Git推送失败

**解决方案**: 检查远程仓库配置
```powershell
git remote -v
git push -u origin windows
```

---

## 📝 相关文档

1. **Windows安装指南**: `WINDOWS_INSTALL_GUIDE.md` (在打包中)
2. **跨平台同步指南**: `CROSS_PLATFORM_SYNC_GUIDE.md` (在打包中)
3. **打包清单**: `PACKAGE_MANIFEST.txt` (在打包中)
4. **文件系统结构**: `docs/FILESYSTEM_STRUCTURE.md`

---

## ✅ 验证清单

迁移完成后，请验证以下项目：

- [ ] Python虚拟环境已创建并激活
- [ ] 所有依赖已安装（`pip list`）
- [ ] 核心模块可以导入（`python -c "from core.market_trend_analyzer import MarketTrendAnalyzer"`）
- [ ] JQData配置已设置
- [ ] 知识库文件存在（`.trquant/dev/knowledge/knowledge_base.json`）
- [ ] Git仓库已初始化
- [ ] 可以启动Jupyter Notebook
- [ ] 可以运行测试脚本

---

**最后更新**: 2026-01-15  
**状态**: ✅ Ubuntu端打包完成，等待Windows端安装
