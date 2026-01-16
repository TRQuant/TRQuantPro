# TRQuant 跨平台开发与同步指南

> **版本**: v1.1  
> **更新**: 2026-01-15  
> **目的**: Ubuntu和Windows双平台开发，保持共用模块一致  
> **Token配置**: 参见 `docs/GIT_TOKEN_CONFIG.md`

---

## 🎯 架构设计

### 目录分类

```
TRQuant/
├── core/                    # ✅ 共用模块（跨平台）
├── mcp_servers/             # ✅ 共用模块（跨平台）
├── notebooks/               # ✅ 共用模块（跨平台）
├── .trquant/dev/knowledge/  # ✅ 共用模块（必须同步）
├── platform/                # 🆕 平台特定模块（隔离）
│   ├── linux/              # Linux特定代码
│   └── windows/            # Windows特定代码
├── config/                  # ⚠️ 平台特定配置（不同步）
└── workspace/               # ⚠️ 工作空间（不同步）
```

---

## 🔄 Git工作流

### 分支策略

```
main (主分支)
├── ope (Ubuntu开发分支)
│   └── 包含Linux特定模块
└── windows (Windows开发分支)
    └── 包含Windows特定模块
```

### 共用模块同步

共用模块在两个分支都同步：
- `core/`
- `mcp_servers/`
- `notebooks/`
- `.trquant/dev/knowledge/` (知识库)

### 平台特定模块隔离

平台特定模块只在对应分支：
- `platform/linux/` - 只在 `ope` 分支
- `platform/windows/` - 只在 `windows` 分支

---

## 📚 知识库同步机制

### 方案1: Git自动同步（推荐）

知识库文件 `.trquant/dev/knowledge/knowledge_base.json` 已包含在打包中。

#### Ubuntu端操作

```bash
# 1. 更新知识库后，同步到Git
cd /home/taotao/.cursor/worktrees/TRQuant/ope
python scripts/kb/sync_knowledge_base.py push
git add .trquant/dev/knowledge/knowledge_base.json
git commit -m "sync: 知识库更新"
git push origin ope

# 2. 从Git拉取最新知识库
git pull origin ope
python scripts/kb/sync_knowledge_base.py pull
```

#### Windows端操作

```powershell
# 1. 从Git拉取最新知识库
cd C:\TRQuantPro\ope
git pull origin windows
python scripts\kb\sync_knowledge_base.py pull

# 2. 更新知识库后，同步到Git
python scripts\kb\sync_knowledge_base.py push
git add .trquant\dev\knowledge\knowledge_base.json
git commit -m "sync: 知识库更新"
git push origin windows
```

### 方案2: 定期同步脚本

#### Ubuntu端（每日同步）

```bash
# 添加到crontab
0 9 * * * /home/taotao/.cursor/worktrees/TRQuant/ope/scripts/kb/sync_kb_daily.sh
```

#### Windows端（每日同步）

使用任务计划程序，每天9点运行：
```powershell
C:\TRQuantPro\ope\scripts\kb\sync_kb_daily.ps1
```

---

## 🔧 平台特定模块开发

### Ubuntu端开发Linux特定模块

```bash
# 在 platform/linux/ 目录下开发
cd /home/taotao/.cursor/worktrees/TRQuant/ope
mkdir -p platform/linux/scripts
# 开发Linux特定功能
git add platform/linux/
git commit -m "feat: Linux特定功能"
git push origin ope
```

### Windows端开发Windows特定模块

```powershell
# 在 platform\windows\ 目录下开发
cd C:\TRQuantPro\ope
mkdir -p platform\windows\scripts
# 开发Windows特定功能
git add platform\windows\
git commit -m "feat: Windows特定功能"
git push origin windows
```

---

## ⚠️ 冲突解决

### 知识库冲突处理

当Git合并时出现知识库冲突：

```bash
# 运行冲突解决工具
python scripts/kb/resolve_kb_conflict.py

# 验证合并结果
python scripts/kb/sync_knowledge_base.py stats

# 提交合并结果
git add .trquant/dev/knowledge/knowledge_base.json
git commit -m "merge: 解决知识库冲突"
```

---

## 📋 最佳实践

1. **知识库同步**
   - 每次更新知识库后立即同步到Git
   - 每天开始工作前拉取最新知识库
   - 向量索引可重建，优先同步JSON文件

2. **代码组织**
   - 共用模块放在 `core/`, `mcp_servers/` 等根目录
   - 平台特定模块放在 `platform/{platform}/` 目录
   - 使用平台检测工具动态加载

3. **Git工作流**
   - 共用模块的修改在两个分支都同步
   - 平台特定模块只在对应分支
   - 知识库变更优先合并

4. **冲突处理**
   - 知识库冲突使用自动合并工具
   - 代码冲突按常规Git流程处理
   - 定期同步，减少冲突

---

## 🚀 快速开始

### Ubuntu端初始化

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
git checkout ope
python scripts/kb/sync_knowledge_base.py pull
```

### Windows端初始化

```powershell
cd C:\TRQuantPro\ope
git checkout windows
python scripts\kb\sync_knowledge_base.py pull
```

---

**最后更新**: 2026-01-15
