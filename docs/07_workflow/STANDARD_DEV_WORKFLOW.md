# TRQuant 标准开发流程

> **重要**: 所有开发环节必须通过MCP工具进行管理，确保一致性和可追溯性

## 🔄 开发周期

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   1. 规划       │ -> │   2. 开发       │ -> │   3. 测试       │ -> │   4. 记录       │
│   MCP: task.*   │    │   MCP: module.* │    │   MCP: 功能测试  │    │   MCP: devlog.* │
│   milestone.*   │    │   编码实现      │    │   pytest        │    │   experience.*  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         ^                                                                    │
         └────────────────────────────────────────────────────────────────────┘
                                    持续迭代
```

---

## 📝 步骤详解

### 1. 规划阶段 (MCP工具必须使用)

```python
# 1.1 检查里程碑进度
milestone.list()
milestone.progress(milestone_id="M3")

# 1.2 创建/更新任务
task.create(
    title="M3.1: RawDoc + Event抽取",
    description="公告/年报/互动易 → RawDoc → Event",
    priority="critical",
    milestone="M3"
)
task.update(task_id="M3_step1", status="in_progress")

# 1.3 检查系统状态
module.list()  # 查看已注册模块
system.snapshot()  # 获取系统快照
```

### 2. 开发阶段 (MCP工具辅助)

```python
# 2.1 注册新模块
module.register(
    name="tenbagger_rawdoc",
    version="0.1.0",
    status="developing",
    dependencies=["mongodb"]
)

# 2.2 记录变更
change.log(
    module="tenbagger_rawdoc",
    change_type="feature",
    description="添加RawDoc存储功能"
)

# 2.3 遇到问题时查询
issue_tracker.quick_debug(error_message="MongoDB连接失败")

# 2.4 记录经验
experience.add(
    title="pymongo Collection检查",
    content="使用 'collection is None' 而不是 'not collection'"
)
```

### 3. 测试阶段 (MCP工具验证)

```bash
# 3.1 运行pytest
pytest tests/ -v

# 3.2 通过MCP工具测试功能
# 测试M3.1
call_m31_tool("doc.stats")
call_m31_tool("event.types")

# 测试M3.2
call_m32_tool("stage.stats")
call_m32_tool("scorecard.dimensions")

# 3.3 端到端测试
# 通过GUI执行9步工作流
```

### 4. 记录阶段 (MCP工具必须使用)

```python
# 4.1 记录开发日志
devlog.add(
    content="完成M3.1: RawDoc + Event抽取...",
    tags=["milestone", "m31", "completed"]
)

# 4.2 更新任务状态
task.update(task_id="M3_step1", status="completed")

# 4.3 更新里程碑进度
milestone.update(milestone_id="M3", progress=25)

# 4.4 更新模块状态
module.update(name="tenbagger_rawdoc", status="active")

# 4.5 Git提交
git commit -m "feat(M3.1): 完成RawDoc + Event抽取"
git push trquantpro main
```

---

## 🔧 MCP工具清单

### 项目管理工具 (trquant-project)

| 工具 | 功能 | 使用时机 |
|------|------|----------|
| `task.create` | 创建任务 | 规划阶段 |
| `task.update` | 更新任务 | 开发/记录阶段 |
| `task.list` | 列出任务 | 任意时机 |
| `milestone.list` | 列出里程碑 | 规划阶段 |
| `milestone.progress` | 查看进度 | 规划阶段 |
| `devlog.add` | 添加开发日志 | 记录阶段 |
| `experience.add` | 记录经验 | 开发/记录阶段 |
| `module.register` | 注册模块 | 开发阶段 |
| `module.list` | 列出模块 | 任意时机 |
| `system.snapshot` | 系统快照 | 规划阶段 |
| `change.log` | 记录变更 | 开发阶段 |

### M1工具 (trquant-core)

| 工具 | 功能 |
|------|------|
| `context.set_output` | 设置步骤输出 |
| `context.get_input` | 获取步骤输入 |
| `snapshot.create` | 创建数据快照 |
| `experiment.create` | 创建实验 |
| `experiment.complete` | 完成实验 |

### M3.1工具 (trquant-core)

| 工具 | 功能 |
|------|------|
| `doc.ingest` | 入库文档 |
| `doc.search` | 搜索文档 |
| `doc.stats` | 文档统计 |
| `event.extract` | 事件抽取 |
| `event.list` | 列出事件 |
| `event.validate` | 验证事件 |

### M3.2工具 (trquant-core)

| 工具 | 功能 |
|------|------|
| `stage.compute` | 更新状态 |
| `stage.get` | 获取阶段 |
| `stage.history` | 状态历史 |
| `scorecard.compute` | 计算评分 |
| `scorecard.explain` | 评分解释 |

---

## 🔍 Debug流程

```
遇到错误 
    ↓
issue_tracker.quick_debug(error) 
    ↓
有记录? ──→ 应用解决方案
    ↓ 无
研究问题 
    ↓
解决问题
    ↓
issue_tracker.record_solution(issue_id, description, code_snippet)
    ↓
experience.add(title, content)  # 记录经验
```

---

## 📊 数据存储

| 类型 | 文件/集合 | 说明 |
|------|----------|------|
| 任务 | `.trquant/project_data/trquant/tasks.json` | 开发任务 |
| 日志 | `.trquant/project_data/trquant/devlog.json` | 开发记录 |
| 经验 | `.trquant/project_data/trquant/experience.json` | 学习经验 |
| 里程碑 | `.trquant/project_data/trquant/milestones.json` | 里程碑 |
| 问题 | `data/issues/known_issues.json` | 已知问题 |
| 方案 | `data/issues/solutions.json` | 解决方案 |
| 文档 | `trquant.raw_docs` (MongoDB) | 原始文档 |
| 事件 | `trquant.events` (MongoDB) | 抽取事件 |
| 阶段 | `trquant.stages` (MongoDB) | 股票阶段 |
| 评分 | `trquant.scorecards` (MongoDB) | 评分卡 |

---

## ⚠️ 注意事项

1. **规划阶段必须**：检查里程碑、创建/更新任务
2. **开发阶段必须**：注册模块、记录变更
3. **测试阶段必须**：通过MCP工具验证功能
4. **记录阶段必须**：更新任务状态、添加开发日志、Git提交
5. **遇到问题必须**：查询issue_tracker，记录解决方案和经验

---

**版本**: 2.0 | **更新**: 2025-12-18 | **强调MCP工具使用**
