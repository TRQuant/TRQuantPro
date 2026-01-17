# Git同步快速开始指南

> **版本**: v1.0  
> **更新**: 2026-01-15  
> **目的**: 快速设置Ubuntu和Windows双平台Git同步

---

## 🚀 Ubuntu端快速开始（3步）

### 步骤1: 运行设置脚本

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./scripts/setup_git_sync.sh
```

脚本会自动：
- ✅ 初始化Git仓库（如果还没有）
- ✅ 创建或切换到 `ope` 分支
- ✅ 创建 `.gitignore`
- ✅ 创建所有同步脚本

### 步骤2: 配置远程仓库

```bash
# 如果使用GitHub/GitLab
git remote add origin https://github.com/your-username/TRQuant_ope.git

# 或使用SSH
git remote add origin git@github.com:your-username/TRQuant_ope.git
```

### 步骤3: 首次提交并推送

```bash
# 添加所有文件
git add .

# 提交
git commit -m "feat: Ubuntu系统初始提交"

# 推送到远程
git push -u origin ope
```

---

## 🚀 Windows端快速开始（3步）

### 步骤1: 初始化Git仓库

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 初始化Git
git init

# 配置用户信息
git config user.name "TRQuant"
git config user.email "zhutechllc@gmail.com"
```

### 步骤2: 配置远程仓库并创建分支

```powershell
# 配置远程仓库（使用Token）
git remote set-url origin https://[TOKEN]@github.com/TRQuant/TRQuantPro.git

# 创建Windows分支
git checkout -b windows

# 首次推送
git push -u origin windows
```

### 步骤3: 验证同步脚本

同步脚本已包含在打包中，位于 `scripts\sync\` 目录。

---

## 📚 日常使用

### Ubuntu端

#### 同步知识库

```bash
# 方法1: 使用脚本（推荐）
./scripts/sync/sync_knowledge_base.sh

# 方法2: 手动
git add .trquant/dev/knowledge/knowledge_base.json
git commit -m "sync: 知识库更新"
git push origin ope
```

#### 同步共用模块

```bash
# 使用脚本
./scripts/sync/sync_common_modules.sh
```

#### 拉取更新

```bash
# 使用脚本
./scripts/sync/pull_common_modules.sh
```

### Windows端

#### 同步知识库

```powershell
# 使用脚本
.\scripts\sync\sync_knowledge_base.ps1
```

#### 同步共用模块

```powershell
# 使用脚本
.\scripts\sync\sync_common_modules.ps1
```

#### 拉取更新

```powershell
# 使用脚本
.\scripts\sync\pull_common_modules.ps1
```

---

## 🤖 自动同步设置（可选）

### Ubuntu端 - 每日自动同步知识库

```bash
# 编辑crontab
crontab -e

# 添加以下行（每天9点同步）
0 9 * * * /home/taotao/.cursor/worktrees/TRQuant/ope/scripts/sync/sync_kb_daily.sh
```

### Windows端 - 每日自动同步知识库

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器: 每天9:00
4. 操作: 启动程序
   - 程序: `powershell.exe`
   - 参数: `-File "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\scripts\sync\sync_kb_daily.ps1"`

---

## ⚠️ 重要提示

### 共用模块（必须同步）

以下模块在两个分支都同步：
- `core/` - 核心功能
- `mcp_servers/` - MCP工具接口
- `notebooks/` - Jupyter Notebook
- `scripts/` - 脚本文件
- `strategies/` - 策略文件
- `data_sources/` - 数据源模块
- `utils/` - 工具函数
- `docs/` - 文档
- `.trquant/dev/knowledge/` - **知识库（最重要）**

### 平台特定模块（隔离）

- `platform/linux/` - 只在 `ope` 分支
- `platform/windows/` - 只在 `windows` 分支
- `config/*.json` - 平台特定配置（不同步）

---

## 🔧 故障排除

### 问题1: 推送失败

```bash
# 检查远程仓库配置
git remote -v

# 更新远程URL
git remote set-url origin <新的URL>
```

### 问题2: 合并冲突

```bash
# 查看冲突
git status

# 手动解决冲突后
git add <冲突文件>
git commit
```

### 问题3: 知识库冲突

```bash
# 运行冲突解决工具
python scripts/kb/resolve_kb_conflict.py
```

---

## 📝 相关文档

- **完整指南**: `docs/GIT_SYNC_COMPLETE_GUIDE.md`
- **跨平台同步**: `docs/CROSS_PLATFORM_SYNC_GUIDE.md`

---

**最后更新**: 2026-01-15
