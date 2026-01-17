# 计划文件管理

## 📁 目录结构

```
.cursor/
├── plans/                       # 进行中的计划文件（Cursor会读取）
│   ├── README.md               # 本说明文件
│   ├── xxx.plan.md             # 进行中的计划文件
│   └── ...
└── archived_plans/             # 已归档的计划（Cursor不会读取）
    └── 2026-01/                # 2026年1月归档
        ├── xxx.plan.md
        └── ...
```

## 🔄 自动归档机制

### 归档规则

已完成的计划文件会自动归档到 `archived_plans/YYYY-MM/` 目录下，归档条件：

1. **所有任务都已完成**: 计划文件中所有 `todos` 的 `status` 都是 `completed`、`done` 或 `finished`
2. **至少有一个任务**: 计划文件必须包含至少一个任务项

### 如何归档

运行归档脚本：

```bash
# 试运行（查看哪些计划将被归档）
python scripts/archive_completed_plans.py --dry-run

# 实际归档
python scripts/archive_completed_plans.py
```

### 归档位置

- **归档目录**: `.cursor/archived_plans/YYYY-MM/`（在plans目录外，Cursor不会读取）
- **按月份组织**: 自动按归档月份创建子目录
- **保留原文件名**: 归档后文件名不变，便于查找

## 📋 当前状态

### 进行中的计划

当前 `.cursor/plans/` 目录下只显示**进行中的计划**，包括：

- 有未完成任务（`status` 不是 `completed`）的计划
- 没有任务列表的计划（视为进行中）

### 已归档的计划

已完成的计划已移动到 `archived_plans/` 目录，可按月份查找：

```bash
# 查看2026年1月归档的计划
ls .cursor/archived_plans/2026-01/
```

## 🔍 查找已归档计划

如果需要查看已归档的计划：

```bash
# 查找特定计划
find .cursor/archived_plans -name "*关键词*"

# 查看所有归档计划
find .cursor/archived_plans -name "*.plan.md"
```

## 📝 计划文件格式

计划文件使用 YAML frontmatter + Markdown 格式：

```yaml
---
name: 计划名称
overview: 计划概述
todos:
  - id: task-1
    content: "任务描述"
    status: completed  # pending | in_progress | completed | cancelled
  - id: task-2
    content: "另一个任务"
    status: in_progress
    dependencies:
      - task-1
---

# 计划详细内容

...
```

## ⚙️ 手动管理

如果需要手动归档或恢复计划：

```bash
# 手动归档（移动到归档目录）
mv .cursor/plans/xxx.plan.md .cursor/archived_plans/2026-01/

# 恢复归档的计划（移回主目录）
mv .cursor/archived_plans/2026-01/xxx.plan.md .cursor/plans/
```

## 🗑️ 清理旧归档

如果需要清理很久以前的归档（例如6个月以上）：

```bash
# 手动删除（谨慎操作）
rm -rf .cursor/archived_plans/2025-*
```

---

**最后更新**: 2026-01-12  
**维护**: TRQuant Team
