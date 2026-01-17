# TRQuant 标准开发流程 V2

> 更新日期: 2025-12-18  
> **工作目录**: `/home/taotao/dev/QuantTest/TRQuant` (必须确认)

---

## 一、开发前检查（必须）

### 1.1 确认工作目录
```bash
cd /home/taotao/dev/QuantTest/TRQuant
pwd  # 必须显示正确路径
source venv/bin/activate
```

### 1.2 查询当前任务状态
```python
await call_tool("task.list", {"project": "trquant", "status": "in_progress"})
await call_tool("milestone.list", {"project": "trquant"})
```

---

## 二、开发流程（4阶段）

### 阶段1: 规划

| 步骤 | MCP工具 | 参数 |
|------|---------|------|
| 创建任务 | `task.create` | title, description, status="pending" |
| 记录规划 | `devlog.add` | content, tags=["planning"] |
| 创建里程碑 | `milestone.create` | name, description, due_date |

**示例**:
```python
await call_tool("task.create", {
    "title": "Phase4: JQData数据源接入",
    "description": "接入JQData真实数据源",
    "status": "in_progress",
    "project": "trquant"
})
await call_tool("devlog.add", {
    "content": "【规划】Phase4开发目标...",
    "tags": ["planning", "phase4"],
    "project": "trquant"
})
```

### 阶段2: 开发

| 步骤 | MCP工具 | 参数 |
|------|---------|------|
| 更新任务状态 | `task.update` | task_id, status="in_progress" |
| 记录开发过程 | `devlog.add` | content, tags=["development"] |
| 遇到问题时 | `issue.create` | title, description, priority |

**示例**:
```python
await call_tool("devlog.add", {
    "content": "【开发】创建jqdata_enhanced.py...",
    "tags": ["development", "phase4"],
    "project": "trquant"
})
```

### 阶段3: 测试

| 步骤 | MCP工具 | 参数 |
|------|---------|------|
| 记录测试结果 | `devlog.add` | content, tags=["testing"] |
| 问题解决时 | `issue.resolve` | issue_id, solution |
| 记录经验 | `experience.add` | content, category |

**示例**:
```python
await call_tool("devlog.add", {
    "content": "【测试】JQData连接测试通过...",
    "tags": ["testing", "phase4"],
    "project": "trquant"
})
```

### 阶段4: 记录

| 步骤 | MCP工具 | 参数 |
|------|---------|------|
| 完成任务 | `task.complete` | task_id |
| 更新里程碑 | `milestone.progress` | milestone_id, progress |
| 最终日志 | `devlog.add` | content, tags=["completed"] |
| 系统注册 | `registry.register` | module_id, name, tools |

**示例**:
```python
await call_tool("task.complete", {
    "task_id": "task_xxx",
    "project": "trquant"
})
await call_tool("devlog.add", {
    "content": "【完成】Phase4开发完成...",
    "tags": ["completed", "phase4"],
    "project": "trquant"
})
```

---

## 三、MCP工具清单（开发相关）

### 3.1 任务管理 (task.*)
| 工具 | 说明 | 服务器 |
|------|------|--------|
| `task.create` | 创建任务 | dev_task_server |
| `task.list` | 列出任务 | dev_task_server |
| `task.get` | 获取任务详情 | dev_task_server |
| `task.update` | 更新任务 | dev_task_server |
| `task.complete` | 完成任务 | dev_task_server |
| `task.add_note` | 添加备注 | project_manager_server |
| `task.analyze` | 分析任务复杂度 | dev_task_server |
| `task.recommend_mode` | 推荐执行模式 | dev_task_server |
| `task.cache_context` | 缓存上下文 | dev_task_server |

### 3.2 开发日志 (devlog.*)
| 工具 | 说明 | 服务器 |
|------|------|--------|
| `devlog.add` | 添加开发日志 | dev_task_server |
| `devlog.list` | 列出开发日志 | dev_task_server |

### 3.3 里程碑 (milestone.*)
| 工具 | 说明 | 服务器 |
|------|------|--------|
| `milestone.create` | 创建里程碑 | project_manager_server |
| `milestone.list` | 列出里程碑 | dev_task_server |
| `milestone.progress` | 更新进度 | project_manager_server |

### 3.4 问题追踪 (issue.*)
| 工具 | 说明 | 服务器 |
|------|------|--------|
| `issue.create` | 创建问题 | project_manager_server |
| `issue.list` | 列出问题 | project_manager_server |
| `issue.resolve` | 解决问题 | project_manager_server |

### 3.5 经验管理 (experience.*)
| 工具 | 说明 | 服务器 |
|------|------|--------|
| `experience.add` | 添加经验 | project_manager_server |
| `experience.search` | 搜索经验 | project_manager_server |
| `experience.mark_useful` | 标记有用 | project_manager_server |

### 3.6 风险管理 (risk.*)
| 工具 | 说明 | 服务器 |
|------|------|--------|
| `risk.add` | 添加风险 | project_manager_server |
| `risk.assess` | 评估风险 | project_manager_server |

### 3.7 进度报告 (progress.*)
| 工具 | 说明 | 服务器 |
|------|------|--------|
| `progress.summary` | 进度摘要 | project_manager_server |
| `progress.daily_report` | 日报 | project_manager_server |

### 3.8 工作流 (workflow.*)
| 工具 | 说明 | 服务器 |
|------|------|--------|
| `workflow.batch` | 批量执行工具 | dev_task_server |
| `workflow.auto` | 自动执行流程 | dev_task_server |

---

## 四、批量调用（Max模式优化）

### 4.1 规划阶段批量
```python
await call_tool("workflow.batch", {
    "tools": [
        {"name": "task.create", "args": {...}},
        {"name": "devlog.add", "args": {...}},
        {"name": "milestone.create", "args": {...}}
    ]
})
```

### 4.2 记录阶段批量
```python
await call_tool("workflow.batch", {
    "tools": [
        {"name": "task.complete", "args": {...}},
        {"name": "devlog.add", "args": {...}},
        {"name": "milestone.progress", "args": {...}}
    ]
})
```

---

## 五、防止遗忘/漂移

### 5.1 每次开发开始前
1. ✅ 确认工作目录: `cd /home/taotao/dev/QuantTest/TRQuant`
2. ✅ 查询当前任务: `task.list`
3. ✅ 查询开发日志: `devlog.list`

### 5.2 每次开发结束后
1. ✅ 更新任务状态: `task.update` 或 `task.complete`
2. ✅ 记录开发日志: `devlog.add`
3. ✅ Git提交: `git commit -m "..."`

### 5.3 遇到问题时
1. ✅ 搜索经验: `experience.search`
2. ✅ 创建问题: `issue.create`
3. ✅ 解决后记录: `issue.resolve` + `experience.add`

---

## 六、工具总数统计

| 服务器 | 工具数 |
|--------|--------|
| trquant_core_server | 132 |
| dev_task_server | 15 |
| project_manager_server | 18 |
| **总计** | **158** |

---

*文档版本: 2.0 | 生成时间: 2025-12-18*
