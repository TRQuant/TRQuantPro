# 开发上下文历史记录

> **目的**：保存重要的开发决策、操作和上下文，便于在新工作环境中快速恢复

## 📅 最后更新：2025-01-03

---

## 🔄 Worktrees目录整理 (2025-01-03)

### 背景
- Cursor默认在worktrees目录工作
- 已经将主目录文件复制到worktrees根目录
- 需要清理和整理工作环境

### 关键发现

1. **目录结构**：
   - 主项目目录：`/home/taotao/dev/QuantTest/TRQuant`（Git主仓库）
   - worktrees根目录：`~/.cursor/worktrees/TRQuant/`（20GB，完整Git仓库）
   - ope目录：`~/.cursor/worktrees/TRQuant/ope/`（1.2GB，Git worktree，已删除）

2. **worktrees根目录状态**：
   - ✅ 完整的Git仓库（有.git目录）
   - ✅ 173,950个文件（包含所有最新代码和数据）
   - ✅ Git配置完整（有remote: origin, trquantpro, upstream）
   - ✅ 在main分支，与主目录同步
   - ✅ 包含运行时环境（venv, data, logs等）

3. **差异分析**：
   - 根目录 vs ope目录：根目录文件多约148,000个
   - 212个文件内容不同（主要在core模块）
   - 根目录有更多回测结果和数据文件

### 决策

1. **最终工作目录**：`~/.cursor/worktrees/TRQuant/`（worktrees根目录）
   - 理由：Cursor默认在此工作，文件完整，Git配置好

2. **已删除**：
   - `ope/`目录（不再需要）
   - `abd/`目录（重复的worktree）
   - `tde/`目录（不完整的worktree）

3. **保留**：
   - worktrees根目录的所有文件
   - Git仓库和配置
   - 运行时环境（venv, data等）

### 工作流程

```bash
# 工作目录
cd ~/.cursor/worktrees/TRQuant

# 开发代码
# ...

# Git提交
git add .
git commit -m "描述"
git push trquantpro main

# 主目录同步（如果需要）
cd /home/taotao/dev/QuantTest/TRQuant
git pull trquantpro main
```

---

## 📊 市场环境识别模块 (2025-01-03)

### 已完成

1. **14种市场状态定义表**
   - 位置：`notebooks/research/03_market_env_concise_v3.ipynb`
   - 包含完整14种状态定义（牛市4种、熊市4种、震荡4种、转折2种）
   - 已清理所有12种状态的说明（统一使用14种）

2. **核心模块**：
   - `core/market_env_identifier_v3.py` - 市场环境识别（12种状态）
   - `core/market_env_params_extended.py` - 扩展参数定义
   - `core/visualization/chart_engine.py` - 图表引擎
   - `core/visualization/dashboard.py` - 仪表盘（MarketGauge）

3. **Notebook修复**：
   - MarketGauge API参数名：`score`, `risk_score`, `position`（不是`value`）
   - position参数范围：0-1（不是百分比）
   - 数据传入：`identifier.identify(df)`需要DataFrame，不是symbol字符串

### 关键经验

- MarketGauge API参数名要使用正确的参数名
- 数据源优先使用JQData，akshare作为补充
- Notebook图表要专业美观，参考专业金融机构

---

## 🔧 开发规则和配置

### 工作目录

- **主工作目录**：`/home/taotao/.cursor/worktrees/TRQuant/`
- **Git主仓库**：`/home/taotao/dev/QuantTest/TRQuant`
- **同步方式**：通过Git remote（trquantpro/main）

### Cursor配置

- worktrees已禁用自动创建（settings.json中配置）
- 文件操作必须使用绝对路径
- 主项目路径：`/home/taotao/dev/QuantTest/TRQuant`

### Git配置

- Remote: origin (TRQuantExt), trquantpro (TRQuantPro), upstream
- 主分支：main
- 工作目录在main分支，与主目录同步

---

## 📝 待办事项

1. ✅ 清理worktrees目录（ope, abd, tde已删除）
2. ⏳ 测试worktrees根目录工作环境
3. ⏳ 验证Git工作流
4. ⏳ 确认文件路径和配置

---

## 🔗 相关文档

- `docs/WORKTREE_FOLDER_EXPLANATION.md` - worktree文件夹机制说明
- `docs/WORKTREE_ROOT_WORKFLOW.md` - worktree根目录工作流
- `docs/CURSOR_DEFAULT_WORKDIRECTORY.md` - Cursor默认工作目录机制
- `docs/DISABLE_CURSOR_WORKTREES.md` - 禁用worktrees指南

---

## 💡 重要提示

1. **文件操作**：始终使用绝对路径
2. **Git工作流**：使用commit/push/pull，不要文件复制
3. **数据源**：优先JQData，akshare作为补充
4. **工作目录**：在worktrees根目录工作，通过Git同步到主目录

---

*本文档应该在新工作环境中首先查看，以快速了解当前状态和关键决策*










