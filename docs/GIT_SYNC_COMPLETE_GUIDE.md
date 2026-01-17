# TRQuant Git同步完整指南

> **版本**: v1.1  
> **更新**: 2026-01-15  
> **目的**: Ubuntu和Windows双平台Git同步方案  
> **Token配置**: 参见 `docs/GIT_TOKEN_CONFIG.md`

---

## 🎯 同步策略

### 分支结构

```
main (主分支，可选)
├── ope (Ubuntu开发分支)
│   └── 包含Linux特定模块
└── windows (Windows开发分支)
    └── 包含Windows特定模块
```

### 共用模块（必须同步）

以下模块在两个分支都同步：
- `core/` - 核心功能实现
- `mcp_servers/` - MCP工具接口
- `notebooks/` - Jupyter Notebook
- `scripts/` - 脚本文件
- `strategies/` - 策略文件
- `data_sources/` - 数据源模块
- `utils/` - 工具函数
- `docs/` - 文档
- `.trquant/dev/knowledge/` - 知识库（**最重要**）

### 平台特定模块（隔离）

- `platform/linux/` - 只在 `ope` 分支
- `platform/windows/` - 只在 `windows` 分支
- `config/*.json` - 平台特定配置（不同步）

---

## 📋 Ubuntu端设置

### 步骤1: 运行设置脚本

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
chmod +x scripts/setup_git_sync.sh
./scripts/setup_git_sync.sh
```

脚本会：
- 初始化Git仓库（如果还没有）
- 配置远程仓库
- 创建或切换到 `ope` 分支
- 创建 `.gitignore`
- 创建同步脚本

### 步骤2: 配置远程仓库

如果还没有远程仓库，可以：

#### 选项1: 使用GitHub/GitLab

```bash
# 配置远程仓库（使用Token）
git remote set-url origin https://[TOKEN]@github.com/TRQuant/TRQuantPro.git
git push -u origin ope
```

#### 选项2: 使用本地Git服务器

```bash
# 如果有本地Git服务器
git remote add origin git@your-server:TRQuant_ope.git
git push -u origin ope
```

### 步骤3: 首次提交

```bash
# 添加所有文件
git add .

# 提交
git commit -m "feat: Ubuntu系统初始提交"

# 推送到远程
git push -u origin ope
```

---

## 📋 Windows端设置

### 步骤1: 初始化Git仓库

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 初始化Git（如果还没有）
git init

# 配置用户信息
git config user.name "TRQuant"
git config user.email "zhutechllc@gmail.com"
```

### 步骤2: 配置远程仓库

```powershell
# 配置远程仓库（使用Token）
git remote set-url origin https://[TOKEN]@github.com/TRQuant/TRQuantPro.git

# 创建Windows分支
git checkout -b windows

# 首次推送
git push -u origin windows
```

### 步骤3: 创建同步脚本

创建 `scripts\sync\sync_common_modules.ps1`:

```powershell
# 同步共用模块到Git（Windows端）
$PROJECT_ROOT = "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
Set-Location $PROJECT_ROOT

# 共用模块列表
$COMMON_MODULES = @(
    "core",
    "mcp_servers",
    "notebooks",
    "scripts",
    "strategies",
    "data_sources",
    "utils",
    "docs",
    ".trquant\dev\knowledge"
)

Write-Host "=========================================="
Write-Host "同步共用模块到Git"
Write-Host "=========================================="

# 添加共用模块
foreach ($module in $COMMON_MODULES) {
    if (Test-Path $module) {
        Write-Host "添加 $module..."
        git add $module
    }
}

# 提交
$COMMIT_MSG = Read-Host "请输入提交信息"
if ([string]::IsNullOrEmpty($COMMIT_MSG)) {
    $COMMIT_MSG = "sync: 同步共用模块"
}

git commit -m $COMMIT_MSG

# 推送到远程
$remotes = git remote
if ($remotes -match "origin") {
    $confirm = Read-Host "是否推送到远程仓库? (y/n)"
    if ($confirm -eq "y") {
        git push origin windows
        Write-Host "✅ 已推送到远程仓库"
    }
}

Write-Host "✅ 共用模块同步完成"
```

创建 `scripts\sync\sync_knowledge_base.ps1`:

```powershell
# 知识库同步脚本（Windows端）
$PROJECT_ROOT = "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
Set-Location $PROJECT_ROOT

Write-Host "=========================================="
Write-Host "同步知识库到Git"
Write-Host "=========================================="

# 检查知识库文件
$KB_JSON = ".trquant\dev\knowledge\knowledge_base.json"

if (-not (Test-Path $KB_JSON)) {
    Write-Host "❌ 知识库JSON文件不存在: $KB_JSON"
    exit 1
}

# 添加知识库文件
Write-Host "添加知识库文件..."
git add $KB_JSON
git add .trquant\dev\knowledge\strategy_knowledge\

# 检查是否有更改
$staged = git diff --cached --name-only
if ([string]::IsNullOrEmpty($staged)) {
    Write-Host "✅ 知识库没有更改"
    exit 0
}

# 提交
$COMMIT_MSG = Read-Host "请输入提交信息 (默认: sync: 知识库更新)"
if ([string]::IsNullOrEmpty($COMMIT_MSG)) {
    $COMMIT_MSG = "sync: 知识库更新"
}

git commit -m $COMMIT_MSG

# 推送到远程
$remotes = git remote
if ($remotes -match "origin") {
    $confirm = Read-Host "是否推送到远程仓库? (y/n)"
    if ($confirm -eq "y") {
        git push origin windows
        Write-Host "✅ 知识库已推送到远程仓库"
    }
}

Write-Host "✅ 知识库同步完成"
```

创建 `scripts\sync\pull_common_modules.ps1`:

```powershell
# 从Git拉取共用模块更新（Windows端）
$PROJECT_ROOT = "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
Set-Location $PROJECT_ROOT

Write-Host "=========================================="
Write-Host "从Git拉取共用模块更新"
Write-Host "=========================================="

# 检查远程仓库
$remotes = git remote
if ($remotes -notmatch "origin") {
    Write-Host "❌ 未配置远程仓库"
    exit 1
}

# 拉取更新
Write-Host "拉取远程更新..."
git fetch origin windows

# 检查是否有冲突
$status = git status --porcelain
if (-not [string]::IsNullOrEmpty($status)) {
    Write-Host "⚠️  有未提交的本地更改，请先提交或暂存"
    git status
    $confirm = Read-Host "是否继续合并? (y/n)"
    if ($confirm -ne "y") {
        exit 1
    }
}

# 合并
git merge origin/windows

# 如果知识库有更新，重建向量索引
$kbChanged = git diff HEAD@{1} HEAD --name-only | Select-String "knowledge_base.json"
if ($kbChanged) {
    Write-Host "知识库已更新，重建向量索引..."
    python scripts\kb\kb_manager.py build-index
}

Write-Host "✅ 共用模块更新完成"
```

---

## 🔄 日常同步流程

### Ubuntu端

#### 同步共用模块

```bash
# 方法1: 使用同步脚本
./scripts/sync/sync_common_modules.sh

# 方法2: 手动同步
git add core/ mcp_servers/ notebooks/ scripts/ strategies/ data_sources/ utils/ docs/
git commit -m "sync: 同步共用模块"
git push origin ope
```

#### 同步知识库

```bash
# 方法1: 使用同步脚本
./scripts/sync/sync_knowledge_base.sh

# 方法2: 手动同步
git add .trquant/dev/knowledge/knowledge_base.json
git add .trquant/dev/knowledge/strategy_knowledge/
git commit -m "sync: 知识库更新"
git push origin ope
```

#### 拉取更新

```bash
# 方法1: 使用拉取脚本
./scripts/sync/pull_common_modules.sh

# 方法2: 手动拉取
git fetch origin ope
git merge origin/ope
```

### Windows端

#### 同步共用模块

```powershell
# 使用同步脚本
.\scripts\sync\sync_common_modules.ps1
```

#### 同步知识库

```powershell
# 使用同步脚本
.\scripts\sync\sync_knowledge_base.ps1
```

#### 拉取更新

```powershell
# 使用拉取脚本
.\scripts\sync\pull_common_modules.ps1
```

---

## ⚠️ 冲突解决

### 知识库冲突

当Git合并时出现知识库冲突：

#### Ubuntu端

```bash
# 运行冲突解决工具
python scripts/kb/resolve_kb_conflict.py

# 验证合并结果
python scripts/kb/sync_knowledge_base.py stats

# 提交合并结果
git add .trquant/dev/knowledge/knowledge_base.json
git commit -m "merge: 解决知识库冲突"
```

#### Windows端

```powershell
# 运行冲突解决工具
python scripts\kb\resolve_kb_conflict.py

# 验证合并结果
python scripts\kb\sync_knowledge_base.py stats

# 提交合并结果
git add .trquant\dev\knowledge\knowledge_base.json
git commit -m "merge: 解决知识库冲突"
```

### 代码冲突

按常规Git流程处理：

```bash
# 查看冲突
git status

# 手动解决冲突
# 编辑冲突文件

# 标记已解决
git add <冲突文件>

# 完成合并
git commit
```

---

## 🤖 自动同步设置

### Ubuntu端（每日同步）

添加到crontab：

```bash
# 编辑crontab
crontab -e

# 添加以下行（每天9点同步知识库）
0 9 * * * /home/taotao/.cursor/worktrees/TRQuant/ope/scripts/sync/sync_kb_daily.sh
```

### Windows端（每日同步）

使用任务计划程序：

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器: 每天9:00
4. 操作: 启动程序
   - 程序: `powershell.exe`
   - 参数: `-File "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\scripts\sync\sync_kb_daily.ps1"`
5. 完成

---

## 📋 最佳实践

1. **知识库优先**
   - 每次更新知识库后立即同步
   - 每天开始工作前拉取最新知识库
   - 向量索引可重建，优先同步JSON文件

2. **共用模块同步**
   - 共用模块的修改在两个分支都同步
   - 平台特定模块只在对应分支
   - 定期同步，减少冲突

3. **提交规范**
   - 知识库更新: `sync: 知识库更新`
   - 共用模块: `sync: 同步共用模块`
   - 功能开发: `feat: 功能描述`
   - 修复bug: `fix: 问题描述`

4. **冲突处理**
   - 知识库冲突使用自动合并工具
   - 代码冲突按常规Git流程处理
   - 定期同步，减少冲突

---

## 🚀 快速开始

### Ubuntu端

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./scripts/setup_git_sync.sh
```

### Windows端

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
# 手动初始化Git（参考上面的步骤）
```

---

## 📝 相关文档

- **跨平台同步指南**: `docs/CROSS_PLATFORM_SYNC_GUIDE.md`
- **Windows迁移指南**: `docs/WINDOWS_MIGRATION_COMPLETE_GUIDE.md`

---

**最后更新**: 2026-01-15
