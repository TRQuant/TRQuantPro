# 快速开始 - 上下文恢复指南

> **用途**：在新工作环境中快速了解当前状态和关键信息

## 🚀 快速检查清单

### 1. 当前工作目录
```bash
pwd
# 应该是: /home/taotao/.cursor/worktrees/TRQuant
```

### 2. Git状态
```bash
git status
git branch
git remote -v
```

### 3. 关键文件检查
```bash
ls -la core/market_env_identifier_v3.py
ls -la notebooks/research/03_market_env_concise_v3.ipynb
ls -la docs/CONTEXT_HISTORY.md
```

---

## 📋 当前状态摘要

### 工作环境
- **工作目录**: `~/.cursor/worktrees/TRQuant/`
- **Git分支**: main
- **Remote**: trquantpro/main (主要), origin, upstream
- **文件数量**: 173,950个文件
- **目录大小**: 20GB

### 最近完成的工作
1. ✅ 清理worktrees目录（删除ope, abd, tde）
2. ✅ 市场环境识别模块（14种状态定义）
3. ✅ Notebook修复（MarketGauge API, 数据源等）

### 关键模块位置
- 市场环境识别: `core/market_env_identifier_v3.py`
- 扩展参数: `core/market_env_params_extended.py`
- Notebook: `notebooks/research/03_market_env_concise_v3.ipynb`
- 图表引擎: `core/visualization/chart_engine.py`
- 仪表盘: `core/visualization/dashboard.py`

---

## 🔧 开发规则

### 文件操作
- ✅ **必须使用绝对路径**
- ❌ 禁止使用相对路径
- 主项目路径: `/home/taotao/dev/QuantTest/TRQuant`

### 数据源
- ✅ 优先使用JQData
- ✅ akshare作为补充（当JQData无数据时）

### Git工作流
- ✅ 使用commit/push/pull
- ❌ 不要文件复制
- 主分支: main
- 主要remote: trquantpro

---

## 📚 相关文档

1. **上下文历史**: `docs/CONTEXT_HISTORY.md` - 详细的开发历史
2. **工作流指南**: `docs/WORKTREE_ROOT_WORKFLOW.md` - worktree工作流
3. **目录机制**: `docs/WORKTREE_FOLDER_EXPLANATION.md` - worktree机制说明

---

## 💡 快速命令

```bash
# 检查工作目录
cd ~/.cursor/worktrees/TRQuant && pwd

# Git状态
git status

# 查看最近的提交
git log --oneline -5

# 检查关键文件
ls -la core/market_env_identifier_v3.py
ls -la notebooks/research/03_market_env_concise_v3.ipynb
```

---

*最后更新: 2025-01-03*










