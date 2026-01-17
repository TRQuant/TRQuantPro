# Windows 端 Git 同步和应用指南

> **目的**: 帮助 Windows 端用户同步 Linux 端的更新，包括代码、配置文件和知识库  
> **适用版本**: Windows 10/11  
> **更新时间**: 2026-01-16

---

## 📋 目录

1. [准备工作](#准备工作)
2. [Git 同步步骤](#git-同步步骤)
3. [知识库同步](#知识库同步)
4. [配置文件应用](#配置文件应用)
5. [验证和测试](#验证和测试)
6. [常见问题](#常见问题)

---

## 🚀 准备工作

### 1. 确认 Git 已安装

```powershell
# 检查 Git 版本
git --version

# 如果未安装，请下载安装
# https://git-scm.com/download/win
```

### 2. 确认项目目录

```powershell
# 切换到项目目录（根据实际路径调整）
cd C:\path\to\TRQuant\ope

# 或者克隆项目（如果是首次同步）
git clone https://github.com/TRQuant/TRQuantPro.git TRQuant
cd TRQuant\ope
```

### 3. 配置 Git 用户信息（如未配置）

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 📥 Git 同步步骤

### 步骤 1: 查看当前状态

```powershell
# 查看当前分支
git branch

# 查看当前状态
git status

# 查看未提交的更改
git status --short
```

### 步骤 2: 拉取远程更新

```powershell
# 方法1: 使用 git pull（推荐）
git pull origin ope

# 方法2: 先 fetch 再 merge（更安全）
git fetch origin ope
git merge origin/ope

# 方法3: 使用 rebase（保持提交历史线性）
git fetch origin ope
git rebase origin/ope
```

### 步骤 3: 处理冲突（如有）

如果出现合并冲突：

```powershell
# 查看冲突文件
git status

# 手动解决冲突后
git add <冲突文件>
git commit -m "解决合并冲突"
```

### 步骤 4: 验证更新

```powershell
# 查看最近的提交
git log --oneline -5

# 查看文件更新
git diff HEAD~1 HEAD --name-only

# 确认已同步到最新版本
git log origin/ope --oneline -1
```

---

## 📚 知识库同步

### 方法 1: 自动同步（推荐）

知识库文件 `.trquant/dev/knowledge/knowledge_base.json` 会随 Git 同步自动更新。

```powershell
# 拉取更新后，知识库文件会自动同步
git pull origin ope

# 验证知识库文件已更新
Test-Path .trquant\dev\knowledge\knowledge_base.json
Get-Item .trquant\dev\knowledge\knowledge_base.json | Select-Object Length, LastWriteTime
```

### 方法 2: 手动同步（如需要）

如果知识库文件很大（2.5GB+），可能需要使用 Git LFS：

```powershell
# 检查是否安装了 Git LFS
git lfs version

# 如果未安装，下载安装
# https://git-lfs.github.com/

# 启用 Git LFS
git lfs install

# 拉取大文件
git lfs pull
```

### 方法 3: 跳过知识库同步（仅同步代码和配置）

如果不需要同步知识库（文件太大），可以：

```powershell
# 在 .gitignore 中添加知识库文件（不推荐）
echo ".trquant/dev/knowledge/knowledge_base.json" >> .gitignore

# 或者使用 sparse-checkout（推荐）
git sparse-checkout init --cone
git sparse-checkout set "!/.trquant/dev/knowledge/knowledge_base.json"
```

---

## ⚙️ 配置文件应用

### 1. CLAUDE.md 配置文件

**位置**: `CLAUDE.md`（项目根目录）

**应用步骤**:

```powershell
# 确认文件已同步
Test-Path CLAUDE.md

# 查看文件大小（应该约 30KB）
Get-Item CLAUDE.md | Select-Object Length

# 在 Cursor 中打开文件验证
# File > Open File > CLAUDE.md
```

**在 Cursor 中应用**:

1. 打开 Cursor
2. 打开项目文件夹: `File > Open Folder` > 选择 `TRQuant/ope`
3. 打开 `CLAUDE.md` 文件，确认内容正确
4. Cursor 会自动识别并使用配置文件

### 2. 规则文件（.cursor/rules/）

**位置**: `.cursor/rules/` 目录

**应用步骤**:

```powershell
# 确认规则文件目录存在
Test-Path .cursor\rules\

# 列出所有规则文件（应该有4个）
Get-ChildItem .cursor\rules\*.md

# 验证文件内容
Get-ChildItem .cursor\rules\*.md | ForEach-Object {
    Write-Host "$($_.Name): $((Get-Content $_.FullName | Measure-Object -Line).Lines) 行"
}
```

**规则文件列表**:
- `architecture.md` - 架构规范
- `coding-standards.md` - 编码标准
- `market-trend-analysis.md` - 市场分析规则
- `notebook-development.md` - Notebook 规范

**在 Cursor 中应用**:

1. 确保 Cursor 已打开项目文件夹
2. Cursor 会自动读取 `.cursor/rules/` 目录下的规则文件
3. 在 Cursor Chat 中测试，AI 助手应该能识别规则

---

## ✅ 验证和测试

### 验证步骤 1: 检查文件存在

创建验证脚本 `verify_sync.ps1`:

```powershell
$files_to_check = @(
    "CLAUDE.md",
    ".cursor\rules\architecture.md",
    ".cursor\rules\coding-standards.md",
    ".cursor\rules\market-trend-analysis.md",
    ".cursor\rules\notebook-development.md",
    ".trquant\dev\knowledge\knowledge_base.json"
)

Write-Host "=== 同步验证 ===" -ForegroundColor Cyan
$all_ok = $true

foreach ($file in $files_to_check) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "✅ $file ($([math]::Round($size/1KB, 2)) KB)" -ForegroundColor Green
    } else {
        Write-Host "❌ $file (不存在)" -ForegroundColor Red
        $all_ok = $false
    }
}

if ($all_ok) {
    Write-Host "`n✅ 所有文件已同步" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  部分文件缺失" -ForegroundColor Yellow
}
```

**运行验证**:

```powershell
.\verify_sync.ps1
```

### 验证步骤 2: 测试 Cursor 配置

1. **打开 Cursor**
2. **打开项目文件夹**: `File > Open Folder` > 选择 `TRQuant/ope`
3. **测试 CLAUDE.md**:
   - 打开 `CLAUDE.md` 文件
   - 确认内容包含项目概览、系统架构等
4. **测试规则文件**:
   - 打开 `.cursor/rules/` 目录
   - 确认 4 个规则文件存在
5. **测试 AI 助手**:
   - 在 Cursor Chat 中输入：`请参考架构规范，说明项目的三层架构`
   - AI 助手应该能够引用 `architecture.md` 中的内容

### 验证步骤 3: 测试 Git 同步

```powershell
# 检查本地和远程是否同步
git fetch origin ope
git status

# 如果显示 "Your branch is up to date"，说明已同步
# 如果显示 "Your branch is behind"，需要再次执行 git pull
```

---

## 🔄 定期同步流程

### 日常同步（推荐）

创建同步脚本 `sync_windows.ps1`:

```powershell
Write-Host "=== Windows 端 Git 同步 ===" -ForegroundColor Cyan

# 切换到项目目录
Set-Location "C:\path\to\TRQuant\ope"

# 查看当前状态
Write-Host "`n1. 查看当前状态..." -ForegroundColor Yellow
git status --short

# 拉取更新
Write-Host "`n2. 拉取远程更新..." -ForegroundColor Yellow
git pull origin ope

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 同步成功" -ForegroundColor Green
    
    # 验证文件
    Write-Host "`n3. 验证文件..." -ForegroundColor Yellow
    .\verify_sync.ps1
    
    # 提示重启 Cursor
    Write-Host "`n💡 提示: 如果 Cursor 已打开，建议重启以加载新配置" -ForegroundColor Cyan
} else {
    Write-Host "❌ 同步失败，请检查错误信息" -ForegroundColor Red
}
```

**设置定时任务**（可选）:

```powershell
# 使用 Windows 任务计划程序设置定时同步
# 1. 打开"任务计划程序"（Task Scheduler）
# 2. 创建基本任务
# 3. 触发器: 每天特定时间
# 4. 操作: 启动程序 powershell.exe
# 5. 参数: -File "C:\path\to\sync_windows.ps1"
```

---

## 🛠️ 常见问题

### 问题 1: 拉取失败，提示 "Your local changes would be overwritten"

**原因**: 本地有未提交的更改

**解决方案**:

```powershell
# 方法1: 提交本地更改
git add .
git commit -m "本地更改"
git pull origin ope

# 方法2: 暂存本地更改
git stash
git pull origin ope
git stash pop

# 方法3: 放弃本地更改（谨慎使用）
git reset --hard HEAD
git pull origin ope
```

### 问题 2: 知识库文件太大，同步很慢

**原因**: `knowledge_base.json` 文件约 2.5GB

**解决方案**:

```powershell
# 方法1: 使用 Git LFS（推荐）
git lfs install
git lfs pull

# 方法2: 跳过知识库同步（仅同步代码）
git sparse-checkout init
git sparse-checkout set "!/.trquant/dev/knowledge/knowledge_base.json"

# 方法3: 配置 .gitignore（不推荐，会永久排除）
echo ".trquant/dev/knowledge/knowledge_base.json" >> .gitignore
```

### 问题 3: Cursor 未识别配置文件和规则

**原因**: Cursor 需要重启或配置文件路径不正确

**解决方案**:

1. **完全关闭 Cursor**（确保所有窗口都关闭）
2. **重新打开 Cursor**
3. **重新打开项目文件夹**: `File > Open Folder` > 选择 `TRQuant/ope`
4. **验证配置文件**:
   - 打开 `CLAUDE.md` 文件
   - 检查 `.cursor/rules/` 目录
   - 在 Cursor Chat 中测试

### 问题 4: Git 拉取时出现权限错误

**原因**: Windows 文件权限或防病毒软件阻止

**解决方案**:

```powershell
# 检查文件权限
icacls .cursor\rules\*.md

# 如果需要，重置权限
icacls .cursor\rules\*.md /reset

# 将项目目录添加到防病毒软件白名单
# Windows Defender: 设置 > 更新和安全 > Windows 安全 > 病毒和威胁防护 > 管理设置 > 排除项
```

### 问题 5: 中文文件名乱码

**原因**: Git 编码设置问题

**解决方案**:

```powershell
# 配置 Git 编码
git config --global core.quotepath false
git config --global gui.encoding utf-8
git config --global i18n.commitencoding utf-8
git config --global i18n.logoutputencoding utf-8

# 设置 PowerShell 编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 📝 同步检查清单

每次同步后，请确认：

- [ ] `git pull origin ope` 执行成功
- [ ] `CLAUDE.md` 文件存在且内容完整（约 30KB）
- [ ] `.cursor/rules/` 目录存在
- [ ] 4 个规则文件都已同步
- [ ] `.trquant/dev/knowledge/knowledge_base.json` 已更新（如果同步）
- [ ] Cursor 能够识别配置文件
- [ ] AI 助手能够引用规则内容
- [ ] 没有 Git 冲突或错误

---

## 📚 相关文档

- [Windows 安装配置指南](./WINDOWS_INSTALLATION_GUIDE.md)
- [Windows CLAUDE 设置指南](./WINDOWS_CLAUDE_SETUP_GUIDE.md)
- [Git 同步完整指南](./CROSS_PLATFORM_SYNC_GUIDE.md)
- [CLAUDE.md 导出步骤](./EXPORT_CLAUDE_FILES_STEPS.md)

---

## 🔄 下一步

完成同步后：

1. **重启 Cursor**（如需要）
2. **验证配置**: 在 Cursor Chat 中测试 AI 助手
3. **开始工作**: 使用同步的配置文件和知识库进行开发

---

**最后更新**: 2026-01-16  
**维护者**: TRQuant Team
