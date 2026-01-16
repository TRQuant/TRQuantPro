# TRQuant 工作站同步与日常管理完整指南

> **版本**: v1.0  
> **更新**: 2026-01-15  
> **目的**: US-China双工作站同步和日常管理完整指南  
> **状态**: ✅ 已配置并测试通过

---

## 📋 目录

1. [系统配置信息](#系统配置信息)
2. [初始化设置](#初始化设置)
3. [日常同步流程](#日常同步流程)
4. [知识库管理](#知识库管理)
5. [共用模块管理](#共用模块管理)
6. [冲突处理](#冲突处理)
7. [自动同步设置](#自动同步设置)
8. [故障排除](#故障排除)

---

## 🔧 系统配置信息

### Ubuntu端（美国Linux系统）

| 配置项 | 值 |
|--------|-----|
| **工作路径** | `/home/taotao/.cursor/worktrees/TRQuant/ope` |
| **Git用户** | `TRQuant` |
| **Git邮箱** | `zhutechllc@gmail.com` |
| **远程仓库** | `TRQuant/TRQuantPro` |
| **分支** | `ope` |
| **Token** | `[请使用Personal Access Token]` |

### Windows端（中国Windows系统）

| 配置项 | 值 |
|--------|-----|
| **工作路径** | `C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope` |
| **Git用户** | `TRQuant` |
| **Git邮箱** | `zhutechllc@gmail.com` |
| **远程仓库** | `TRQuant/TRQuantPro` |
| **分支** | `windows` |
| **Token** | `[请使用Personal Access Token]` |

---

## 🚀 初始化设置

### Ubuntu端初始化（一次性设置）

```bash
# 1. 进入工作目录
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 2. 配置Git用户信息
git config user.name "TRQuant"
git config user.email "zhutechllc@gmail.com"

# 3. 配置远程仓库
git remote set-url origin https://[TOKEN]@github.com/TRQuant/TRQuantPro.git

# 4. 验证配置
git remote -v
git config user.name
git config user.email

# 5. 确保在ope分支
git checkout ope

# 6. 首次推送（如果还没有）
git push -u origin ope
```

### Windows端初始化（一次性设置）

```powershell
# 1. 进入工作目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 2. 配置Git用户信息
git config user.name "TRQuant"
git config user.email "zhutechllc@gmail.com"

# 3. 配置远程仓库
git remote set-url origin https://[TOKEN]@github.com/TRQuant/TRQuantPro.git

# 4. 验证配置
git remote -v
git config user.name
git config user.email

# 5. 创建并切换到windows分支
git checkout -b windows

# 6. 首次推送
git push -u origin windows
```

---

## 🔄 日常同步流程

### 场景1: 每天开始工作前（拉取最新代码）

#### Ubuntu端

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 方法1: 使用拉取脚本（推荐）
./scripts/sync/pull_common_modules.sh

# 方法2: 手动拉取
git fetch origin ope
git merge origin/ope

# 如果知识库有更新，重建向量索引
python scripts/kb/kb_manager.py build-index
```

#### Windows端

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 方法1: 使用拉取脚本（推荐）
.\scripts\sync\pull_common_modules.ps1

# 方法2: 手动拉取
git fetch origin windows
git merge origin/windows

# 如果知识库有更新，重建向量索引
python scripts\kb\kb_manager.py build-index
```

### 场景2: 更新知识库后（同步知识库）

#### Ubuntu端

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 方法1: 使用同步脚本（推荐）
./scripts/sync/sync_knowledge_base.sh

# 方法2: 手动同步
git add .trquant/dev/knowledge/knowledge_base.json
git add .trquant/dev/knowledge/strategy_knowledge/
git commit -m "sync: 知识库更新"
git push origin ope
```

#### Windows端

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 方法1: 使用同步脚本（推荐）
.\scripts\sync\sync_knowledge_base.ps1

# 方法2: 手动同步
git add .trquant\dev\knowledge\knowledge_base.json
git add .trquant\dev\knowledge\strategy_knowledge\
git commit -m "sync: 知识库更新"
git push origin windows
```

### 场景3: 修改共用模块后（同步共用模块）

#### Ubuntu端

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 方法1: 使用同步脚本（推荐）
./scripts/sync/sync_common_modules.sh

# 方法2: 手动同步
git add core/ mcp_servers/ notebooks/ scripts/ strategies/ data_sources/ utils/ docs/
git commit -m "sync: 同步共用模块"
git push origin ope
```

#### Windows端

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 方法1: 使用同步脚本（推荐）
.\scripts\sync\sync_common_modules.ps1

# 方法2: 手动同步
git add core\ mcp_servers\ notebooks\ scripts\ strategies\ data_sources\ utils\ docs\
git commit -m "sync: 同步共用模块"
git push origin windows
```

### 场景4: 开发平台特定功能

#### Ubuntu端（开发Linux特定功能）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 在platform/linux/目录下开发
mkdir -p platform/linux/scripts
# 开发Linux特定功能...

# 提交到ope分支
git add platform/linux/
git commit -m "feat: Linux特定功能"
git push origin ope
```

#### Windows端（开发Windows特定功能）

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 在platform\windows\目录下开发
mkdir -p platform\windows\scripts
# 开发Windows特定功能...

# 提交到windows分支
git add platform\windows\
git commit -m "feat: Windows特定功能"
git push origin windows
```

---

## 📚 知识库管理

### 知识库同步优先级

**知识库同步优先级最高**，因为：
- 知识库是策略开发的核心资源
- 需要保持两端一致
- 向量索引可以重建，优先同步JSON文件

### 知识库同步最佳实践

1. **更新后立即同步**
   - 每次添加或修改知识库内容后，立即同步到Git
   - 不要积累多个更新再同步

2. **每天开始工作前拉取**
   - 每天开始工作前，先拉取最新知识库
   - 确保使用最新的知识库内容

3. **向量索引重建**
   - 如果知识库JSON文件有更新，需要重建向量索引
   - 使用命令: `python scripts/kb/kb_manager.py build-index`

### 知识库同步检查清单

#### 同步前检查

- [ ] 确认知识库JSON文件存在
- [ ] 检查是否有未提交的更改
- [ ] 确认当前分支正确（Ubuntu: ope, Windows: windows）

#### 同步后检查

- [ ] 确认推送成功
- [ ] 验证远程仓库有最新提交
- [ ] 如果知识库更新，重建向量索引

---

## 🔧 共用模块管理

### 共用模块列表

以下模块在两个分支都同步：

1. **核心代码**
   - `core/` - 核心功能实现
   - `mcp_servers/` - MCP工具接口
   - `notebooks/` - Jupyter Notebook
   - `scripts/` - 脚本文件
   - `strategies/` - 策略文件
   - `data_sources/` - 数据源模块
   - `utils/` - 工具函数

2. **文档**
   - `docs/` - 完整文档

3. **知识库**
   - `.trquant/dev/knowledge/knowledge_base.json`
   - `.trquant/dev/knowledge/strategy_knowledge/`

### 共用模块同步规则

1. **双向同步**
   - 共用模块的修改在两个分支都同步
   - 确保两端代码一致

2. **提交规范**
   - 知识库更新: `sync: 知识库更新`
   - 共用模块: `sync: 同步共用模块`
   - 功能开发: `feat: 功能描述`
   - 修复bug: `fix: 问题描述`

3. **定期同步**
   - 建议每天至少同步一次
   - 重要更新后立即同步

---

## ⚠️ 冲突处理

### 知识库冲突处理

当Git合并时出现知识库冲突：

#### Ubuntu端

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 1. 查看冲突
git status

# 2. 运行冲突解决工具（如果有）
python scripts/kb/resolve_kb_conflict.py

# 3. 手动解决冲突（如果需要）
# 编辑 .trquant/dev/knowledge/knowledge_base.json
# 合并两端的更改

# 4. 验证合并结果
python scripts/kb/kb_manager.py stats

# 5. 提交合并结果
git add .trquant/dev/knowledge/knowledge_base.json
git commit -m "merge: 解决知识库冲突"
git push origin ope
```

#### Windows端

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 1. 查看冲突
git status

# 2. 运行冲突解决工具（如果有）
python scripts\kb\resolve_kb_conflict.py

# 3. 手动解决冲突（如果需要）
# 编辑 .trquant\dev\knowledge\knowledge_base.json
# 合并两端的更改

# 4. 验证合并结果
python scripts\kb\kb_manager.py stats

# 5. 提交合并结果
git add .trquant\dev\knowledge\knowledge_base.json
git commit -m "merge: 解决知识库冲突"
git push origin windows
```

### 代码冲突处理

按常规Git流程处理：

```bash
# 1. 查看冲突
git status

# 2. 查看冲突文件
git diff

# 3. 手动解决冲突
# 编辑冲突文件，保留需要的更改

# 4. 标记已解决
git add <冲突文件>

# 5. 完成合并
git commit -m "merge: 解决代码冲突"
```

---

## 🤖 自动同步设置

### Ubuntu端（每日自动同步知识库）

#### 设置方法

```bash
# 编辑crontab
crontab -e

# 添加以下行（每天9点同步知识库）
0 9 * * * /home/taotao/.cursor/worktrees/TRQuant/ope/scripts/sync/sync_kb_daily.sh
```

#### 验证设置

```bash
# 查看crontab
crontab -l

# 查看cron日志（如果需要）
grep CRON /var/log/syslog
```

### Windows端（每日自动同步知识库）

#### 设置方法

1. 打开"任务计划程序"（Task Scheduler）
2. 创建基本任务
3. 触发器: 每天9:00
4. 操作: 启动程序
   - 程序: `powershell.exe`
   - 参数: `-ExecutionPolicy Bypass -File "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\scripts\sync\sync_kb_daily.ps1"`
5. 完成

#### 验证设置

- 在任务计划程序中查看任务状态
- 检查任务历史记录

---

## 🔍 故障排除

### 问题1: 403 Permission Denied

**症状**: `git push` 时出现403错误

**可能原因**:
1. Token权限不足
2. Token过期或被撤销
3. 账号没有仓库访问权限

**解决方案**:
1. 检查Token权限（需要 `repo` 权限）
2. 验证Token是否过期
3. 确认账号有仓库访问权限

### 问题2: 合并冲突

**症状**: `git pull` 或 `git merge` 时出现冲突

**解决方案**:
1. 查看冲突文件: `git status`
2. 手动解决冲突
3. 提交合并结果: `git add <文件>` 然后 `git commit`

### 问题3: 知识库不同步

**症状**: 两端知识库内容不一致

**解决方案**:
1. 检查是否有未提交的更改: `git status`
2. 拉取最新知识库: `git pull origin <分支>`
3. 如果知识库更新，重建向量索引: `python scripts/kb/kb_manager.py build-index`

### 问题4: 分支不同步

**症状**: 本地分支和远程分支不一致

**解决方案**:
1. 查看分支状态: `git status`
2. 拉取最新更改: `git fetch origin <分支>`
3. 合并远程更改: `git merge origin/<分支>`

### 问题5: Token泄露

**症状**: Token出现在提交历史中

**解决方案**:
1. 立即在GitHub上撤销Token
2. 生成新Token
3. 更新远程仓库URL
4. 从提交历史中移除Token（使用 `git rebase` 或 `git filter-branch`）

---

## 📋 日常管理检查清单

### 每天开始工作前

#### Ubuntu端

- [ ] 拉取最新代码: `./scripts/sync/pull_common_modules.sh`
- [ ] 检查知识库更新: `python scripts/kb/kb_manager.py stats`
- [ ] 如果知识库更新，重建向量索引: `python scripts/kb/kb_manager.py build-index`

#### Windows端

- [ ] 拉取最新代码: `.\scripts\sync\pull_common_modules.ps1`
- [ ] 检查知识库更新: `python scripts\kb\kb_manager.py stats`
- [ ] 如果知识库更新，重建向量索引: `python scripts\kb\kb_manager.py build-index`

### 每次更新知识库后

#### Ubuntu端

- [ ] 同步知识库: `./scripts/sync/sync_knowledge_base.sh`
- [ ] 验证推送成功: `git log -1`

#### Windows端

- [ ] 同步知识库: `.\scripts\sync\sync_knowledge_base.ps1`
- [ ] 验证推送成功: `git log -1`

### 每次修改共用模块后

#### Ubuntu端

- [ ] 同步共用模块: `./scripts/sync/sync_common_modules.sh`
- [ ] 验证推送成功: `git log -1`

#### Windows端

- [ ] 同步共用模块: `.\scripts\sync\sync_common_modules.ps1`
- [ ] 验证推送成功: `git log -1`

### 每周检查

- [ ] 检查Git状态: `git status`
- [ ] 检查远程分支: `git branch -r`
- [ ] 检查提交历史: `git log --oneline -10`
- [ ] 验证Token有效性: `git ls-remote origin`

---

## 📝 相关文档

- `docs/GIT_TOKEN_CONFIG.md` - Git Token配置说明
- `docs/GIT_SYNC_COMPLETE_GUIDE.md` - Git同步完整指南
- `docs/CROSS_PLATFORM_SYNC_GUIDE.md` - 跨平台同步指南
- `docs/SYNC_SOLUTION_SUMMARY.md` - 同步方案总结

---

## 🎯 快速参考

### Ubuntu端常用命令

```bash
# 进入工作目录
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 拉取最新代码
./scripts/sync/pull_common_modules.sh

# 同步知识库
./scripts/sync/sync_knowledge_base.sh

# 同步共用模块
./scripts/sync/sync_common_modules.sh

# 查看Git状态
git status

# 查看提交历史
git log --oneline -10
```

### Windows端常用命令

```powershell
# 进入工作目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 拉取最新代码
.\scripts\sync\pull_common_modules.ps1

# 同步知识库
.\scripts\sync\sync_knowledge_base.ps1

# 同步共用模块
.\scripts\sync\sync_common_modules.ps1

# 查看Git状态
git status

# 查看提交历史
git log --oneline -10
```

---

**最后更新**: 2026-01-15  
**维护者**: TRQuant Team
