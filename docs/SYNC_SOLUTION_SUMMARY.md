# TRQuant 跨平台同步方案总结

> **版本**: v1.0  
> **更新**: 2026-01-15  
> **状态**: ✅ 全部完成

---

## 📋 方案概述

### 目标

实现Ubuntu和Windows双平台开发，保持共用模块（特别是知识库）的一致性。

### 核心策略

1. **Git分支管理**: 使用 `ope` (Ubuntu) 和 `windows` (Windows) 两个分支
2. **共用模块同步**: 核心代码、文档、知识库在两个分支都同步
3. **平台特定隔离**: Linux/Windows特定代码只在对应分支
4. **知识库优先**: 知识库同步优先级最高，支持自动同步

---

## ✅ 已完成的工作

### 1. Git同步脚本

#### Ubuntu端
- ✅ `scripts/setup_git_sync.sh` - Git仓库设置脚本
- ✅ `scripts/sync/sync_common_modules.sh` - 同步共用模块
- ✅ `scripts/sync/sync_knowledge_base.sh` - 同步知识库
- ✅ `scripts/sync/pull_common_modules.sh` - 拉取更新
- ✅ `scripts/sync/sync_kb_daily.sh` - 每日自动同步

#### Windows端
- ✅ `scripts/sync/sync_common_modules.ps1` - 同步共用模块
- ✅ `scripts/sync/sync_knowledge_base.ps1` - 同步知识库
- ✅ `scripts/sync/pull_common_modules.ps1` - 拉取更新
- ✅ `scripts/sync/sync_kb_daily.ps1` - 每日自动同步

### 2. 文档

- ✅ `docs/GIT_SYNC_COMPLETE_GUIDE.md` - Git同步完整指南
- ✅ `docs/GIT_SYNC_QUICK_START.md` - Git同步快速开始
- ✅ `docs/CROSS_PLATFORM_SYNC_GUIDE.md` - 跨平台同步指南
- ✅ `docs/SYNC_SOLUTION_SUMMARY.md` - 本总结文档

---

## 🎯 同步策略详解

### 分支结构

```
main (主分支，可选)
├── ope (Ubuntu开发分支)
│   ├── 共用模块 ✅
│   └── platform/linux/ (Linux特定)
└── windows (Windows开发分支)
    ├── 共用模块 ✅
    └── platform/windows/ (Windows特定)
```

### 共用模块列表（必须同步）

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

3. **知识库（最重要）**
   - `.trquant/dev/knowledge/knowledge_base.json` ✅
   - `.trquant/dev/knowledge/strategy_knowledge/` ✅
   - `.trquant/dev/knowledge/vector_index/` ⚠️ (可选，可重建)

### 平台特定模块（隔离）

- `platform/linux/` - 只在 `ope` 分支
- `platform/windows/` - 只在 `windows` 分支
- `config/*.json` - 平台特定配置（不同步）

---

## 🚀 使用流程

### Ubuntu端

#### 初始化（一次性）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./scripts/setup_git_sync.sh
git remote add origin <远程仓库URL>
git push -u origin ope
```

#### 日常使用

```bash
# 同步知识库
./scripts/sync/sync_knowledge_base.sh

# 同步共用模块
./scripts/sync/sync_common_modules.sh

# 拉取更新
./scripts/sync/pull_common_modules.sh
```

### Windows端

#### 初始化（一次性）

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
git init
git config user.name "TRQuant"
git config user.email "zhutechllc@gmail.com"
git remote add origin <远程仓库URL>
git checkout -b windows
git push -u origin windows
```

#### 日常使用

```powershell
# 同步知识库
.\scripts\sync\sync_knowledge_base.ps1

# 同步共用模块
.\scripts\sync\sync_common_modules.ps1

# 拉取更新
.\scripts\sync\pull_common_modules.ps1
```

---

## 🤖 自动同步设置

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

## ⚠️ 注意事项

### 知识库同步

1. **优先级最高**: 知识库同步优先级最高
2. **及时同步**: 每次更新知识库后立即同步
3. **每日同步**: 每天开始工作前拉取最新知识库
4. **向量索引**: 向量索引可重建，优先同步JSON文件

### 共用模块同步

1. **双向同步**: 共用模块的修改在两个分支都同步
2. **定期同步**: 定期同步，减少冲突
3. **提交规范**: 使用规范的提交信息

### 冲突处理

1. **知识库冲突**: 使用自动合并工具
2. **代码冲突**: 按常规Git流程处理
3. **及时解决**: 发现冲突及时解决

---

## 📊 方案优势

1. **自动化**: 提供自动化脚本，减少手动操作
2. **安全性**: 使用Git版本控制，可追溯历史
3. **灵活性**: 支持手动和自动同步
4. **可扩展**: 易于添加新的同步模块
5. **文档完善**: 提供完整的文档和指南

---

## 📝 相关文档

1. **快速开始**: `docs/GIT_SYNC_QUICK_START.md`
2. **完整指南**: `docs/GIT_SYNC_COMPLETE_GUIDE.md`
3. **跨平台同步**: `docs/CROSS_PLATFORM_SYNC_GUIDE.md`
4. **Windows迁移**: `docs/WINDOWS_MIGRATION_COMPLETE_GUIDE.md`

---

## ✅ 验证清单

### Ubuntu端

- [ ] Git仓库已初始化
- [ ] `ope` 分支已创建
- [ ] 远程仓库已配置
- [ ] 同步脚本已创建并可执行
- [ ] 首次提交并推送成功
- [ ] 自动同步已设置（可选）

### Windows端

- [ ] Git仓库已初始化
- [ ] `windows` 分支已创建
- [ ] 远程仓库已配置
- [ ] 同步脚本已创建
- [ ] 首次提交并推送成功
- [ ] 自动同步已设置（可选）

---

**最后更新**: 2026-01-15  
**状态**: ✅ 全部完成，可以使用
