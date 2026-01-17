# 🐉 轩辕剑灵 - MCP标准开发流程完全指南

> **版本**: 4.0  
> **日期**: 2025-12-20  
> **状态**: 生产就绪
> **重要更新**: 新增知识构建阶段，先构建知识库再开发

---

## 一、核心问题与解决方案

### 1.1 Cursor的限制

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 记忆丢失 | 上下文窗口限制，每次对话独立 | MCP工具持久化 + .cursorrules |
| 流程漂移 | 长对话中偏离原计划 | 强制检查点 + 状态查询 |
| 规则遗忘 | 新对话不知道之前的规则 | 项目级规则文件 + 系统Prompt |
| worktrees问题 | Cursor创建隔离工作区 | 绝对路径 + 环境变量 |
| **知识缺失** | knowledge.search无结果 | **先网络搜索+爬虫构建知识库** |

### 1.2 多层保障机制

```
┌─────────────────────────────────────────────────────────────┐
│                    保障层级                                 │
├─────────────────────────────────────────────────────────────┤
│ L0: 知识库构建           - 网络搜索+爬虫+knowledge.add       │
│ L1: .cursorrules           - 项目级强制规则（自动加载）      │
│ L2: .cursor/rules/         - 模块化规则文件                  │
│ L3: MCP持久化存储           - 任务/日志/问题持久化           │
│ L4: 系统Prompt模板          - 标准化开发入口                 │
│ L5: 自动检查工具            - 流程合规性验证                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、标准开发流程 (6步法) 🆕

### 🔴 步骤0: 会话初始化 (必须)

**每次新对话开始时，Cursor必须执行**:

```python
# 0.1 确认工作目录
cd /home/taotao/dev/QuantTest/TRQuant && pwd

# 0.2 检查当前状态
result = await call_mcp("workflow.check", {})
tasks = await call_mcp("task.list", {"status": "in_progress"})
logs = await call_mcp("devlog.list", {"limit": 5})

# 0.3 显示状态摘要
print("当前进行中任务:", tasks)
print("最近开发日志:", logs)
```

### 🆕 步骤0.5: 知识构建 (Knowledge Building) ⭐关键步骤

**在开发任何新功能前，必须先构建相关知识库！**

```python
# 0.5.1 搜索已有知识
existing = await call_mcp("knowledge.search", {"query": "技术关键词"})

# 0.5.2 如果知识不足，进行网络搜索
# 使用Cursor内置的web_search工具
web_search("技术关键词 best practices 2024")
web_search("技术关键词 example github")

# 0.5.3 爬取官方文档
docs = await call_mcp("crawler.fetch", {
    "url": "https://official-docs.com/guide",
    "extract_text": True
})

# 0.5.4 提取代码示例
code = await call_mcp("crawler.extract_code", {
    "url": "https://github.com/example/repo",
    "language": "typescript"
})

# 0.5.5 添加到知识库
await call_mcp("knowledge.add", {
    "title": "技术名称开发指南",
    "content": "整理的知识内容...",
    "type": "technical",  # technical/lesson/architecture
    "tags": ["技术标签"]
})
```

### 🟡 步骤1: 规划 (Planning)

**启动新任务时执行**:

```python
# 1.1 搜索相关知识和经验
await call_mcp("knowledge.search", {"query": "相关关键词"})
await call_mcp("experience.search", {"query": "类似问题"})

# 1.2 创建任务
task = await call_mcp("quick.start_task", {
    "title": "任务标题",
    "description": "详细描述",
    "tags": ["gui", "react"]  # 新增tags参数支持
})

# 1.3 可选：创建里程碑
await call_mcp("milestone.create", {
    "name": "Phase1: GUI基础框架",
    "due_date": "2025-12-20"
})
```

### 🟢 步骤2: 开发 (Development)

**开发过程中执行**:

```python
# 2.1 记录开发进度（每个重要节点）
await call_mcp("devlog.add", {
    "content": "【开发】完成xxx功能...",
    "tags": ["development"]
})

# 2.2 遇到问题时
await call_mcp("issue.create", {
    "title": "问题标题",
    "description": "问题描述",
    "priority": "high"
})

# 2.3 调试日志
await call_mcp("debug.log", {
    "message": "调试信息",
    "level": "info",
    "context": {"file": "xxx.ts", "line": 100}
})
```

### 🔵 步骤3: 测试 (Testing)

**测试完成后执行**:

```python
# 3.1 记录测试结果
await call_mcp("devlog.add", {
    "content": "【测试】测试通过/失败，结果：...",
    "tags": ["testing"]
})

# 3.2 运行测试
await call_mcp("eng.test", {"pattern": "tests/test_xxx.py"})
```

### ⚪ 步骤4: 记录 (Documentation)

**任务完成后执行**:

```python
# 4.1 完成任务
await call_mcp("quick.finish_task", {
    "task_id": "task_xxx",
    "summary": "完成总结"
})

# 4.2 记录经验到知识库
await call_mcp("knowledge.add", {
    "title": "开发经验：XXX",
    "content": "经验内容...",
    "type": "lesson",
    "tags": ["经验标签"]
})

# 4.3 更新里程碑进度
await call_mcp("milestone.progress", {
    "milestone_id": "ms_xxx",
    "progress": 50
})
```

### 🟣 步骤5: 问题解决 (Issue Resolution)

**解决问题后执行**:

```python
# 5.1 解决问题（自动触发learn.from_issue）
await call_mcp("issue.resolve", {
    "issue_id": "issue_xxx",
    "solution": "解决方案描述"
})

# 5.2 记录经验到知识库
await call_mcp("knowledge.add", {
    "title": "问题解决：XXX",
    "content": "问题原因和解决方案",
    "type": "lesson",
    "tags": ["troubleshooting"]
})
```

---

## 三、MCP工具完整列表 (103个)

### 3.1 🆕 知识构建工具 (16个) ⭐新增

| 类别 | 工具 | 说明 |
|------|------|------|
| **crawler.*** | fetch, search_docs, download, extract_code, api_docs | 网络爬虫 |
| **knowledge.*** | add, search, get, update, mark_useful, stats | 知识管理 |
| **learn.*** | from_issue, from_experience, suggest, auto_extract | 自学习 |
| **research.*** | note, list, search | 研究笔记 |

### 3.2 快捷工具 (4个) ⭐推荐

| 工具 | 用途 | 示例 |
|------|------|------|
| `quick.start_task` | 一键启动任务 | 创建任务+日志 |
| `quick.finish_task` | 一键完成任务 | 完成任务+学习 |
| `quick.log` | 快速日志 | 自动标签 |
| `quick.issue` | 快速问题 | 简化创建 |

### 3.3 核心开发工具 (33个)

| 类别 | 工具 | 说明 |
|------|------|------|
| **task.*** | create, list, get, update, complete, add_note, analyze, recommend_mode, cache_context | 任务管理 |
| **devlog.*** | add, list | 开发日志 |
| **milestone.*** | create, list, progress | 里程碑 |
| **issue.*** | create, list, resolve | 问题追踪 |
| **experience.*** | add, search, mark_useful | 经验管理 |
| **progress.*** | summary, daily_report | 进度报告 |
| **risk.*** | add, assess | 风险管理 |
| **registry.*** | register, list, status, snapshot | 系统注册 |
| **debug.*** | log, trace, status | 调试工具 |
| **workflow.*** | batch, check | 工作流 |

### 3.4 策略知识库工具 (8个)

| 类别 | 工具 | 说明 |
|------|------|------|
| **kb.*** | search, get_strategy, get_api, best_practices, add | 策略知识 |
| **evidence.*** | add, list, search | 证据追踪 |

### 3.5 代码质量工具 (18个)

| 类别 | 工具 | 说明 |
|------|------|------|
| **code.*** | analyze, lint, convert | 代码分析 |
| **lint.*** | check, fix, rules | 代码检查 |
| **eng.*** | test, build, deploy | 工程工具 |
| **docs.*** | list, get, search | 文档工具 |
| **schema.*** | list, get | 数据模型 |
| **practice.*** | add, list, search | 最佳实践 |

### 3.6 GUI开发工具 (10个)

| 类别 | 工具 | 说明 |
|------|------|------|
| **gui.*** | status, validate, generate_html, check_csp | GUI状态 |
| **panel.*** | list, get_config, validate | 面板管理 |

---

## 四、知识库构建指南 🆕

### 4.1 何时需要构建知识库

| 场景 | 需要构建 | 工具 |
|------|---------|------|
| 使用新技术 | ✅ | web_search + crawler.fetch |
| 首次开发某功能 | ✅ | knowledge.search → 如无则构建 |
| 遇到未知错误 | ✅ | web_search + knowledge.add |
| 日常开发 | ❌ | knowledge.search 即可 |

### 4.2 知识构建流程

```
┌─────────────────────────────────────────────────────────────┐
│                    知识构建流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. knowledge.search("关键词")                               │
│           │                                                  │
│           ├── 有结果 → 使用已有知识                          │
│           │                                                  │
│           └── 无结果 → 进入构建流程                          │
│                   │                                          │
│                   ▼                                          │
│  2. web_search("关键词 best practices 2024")                │
│           │                                                  │
│           ▼                                                  │
│  3. crawler.fetch(url="官方文档")                           │
│           │                                                  │
│           ▼                                                  │
│  4. crawler.extract_code(url="代码示例")                    │
│           │                                                  │
│           ▼                                                  │
│  5. knowledge.add(title="xxx", content="...", type="...")   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 知识类型

| type | 用途 | 示例 |
|------|------|------|
| `technical` | 技术文档 | API指南、框架使用 |
| `lesson` | 经验教训 | 问题解决、踩坑记录 |
| `architecture` | 架构设计 | 系统设计、技术选型 |

### 4.4 已构建的知识库索引

| 知识ID | 标题 | 类型 |
|--------|------|------|
| kb_20251219_192338 | GUI架构研究与规划报告 | architecture |
| kb_20251219_193502 | VS Code Webview API开发指南 | technical |
| kb_20251219_193506 | Vite构建工具指南 | technical |
| kb_20251219_193512 | Ant Design 5.x组件库 | technical |

---

## 五、Cursor规则配置

### 5.1 .cursorrules 文件（项目根目录）

```markdown
# TRQuant 开发规则 v5.1

## 强制规则（每次对话开始必须执行）

### 1. 会话初始化检查
每次新对话开始，必须先执行:
- `workflow.check` - 检查开发流程状态
- `task.list` - 查询进行中任务
- `devlog.list` - 查询最近日志

### 2. 知识库构建（新功能开发前）
- `knowledge.search` - 先搜索已有知识
- `web_search` - 如无结果，网络搜索
- `crawler.fetch` - 爬取官方文档
- `knowledge.add` - 添加到知识库

### 3. 工作目录
- 工作目录: `/home/taotao/dev/QuantTest/TRQuant`
- 所有文件操作必须使用绝对路径
- 禁止使用worktrees路径

### 4. 开发流程
- 新任务: quick.start_task → devlog.add(planning)
- 开发中: devlog.add(development) → issue.create(如有问题)
- 测试: eng.test → devlog.add(testing)
- 完成: quick.finish_task → knowledge.add(lesson)

### 5. 日志格式
devlog内容必须以标签开头:
- 【规划】- 任务规划
- 【开发】- 开发进度
- 【测试】- 测试结果
- 【完成】- 任务完成
- 【问题】- 遇到问题
```

---

## 六、最佳实践

### 6.1 知识库优先原则 🆕

| 做法 | 说明 |
|------|------|
| ✅ 先搜索后开发 | `knowledge.search` 确认已有知识 |
| ✅ 无知识则构建 | `web_search` + `crawler` + `knowledge.add` |
| ✅ 开发后沉淀 | 完成后用 `knowledge.add` 记录经验 |
| ✅ 问题即知识 | 解决问题后添加到知识库 |

### 6.2 防止记忆丢失

| 做法 | 说明 |
|------|------|
| ✅ 每次开始先查询状态 | `task.list` + `devlog.list` |
| ✅ 使用MCP工具持久化 | 任务、日志、问题都存储到文件 |
| ✅ 记录经验到知识库 | `knowledge.add` 而非 `experience.add` |
| ✅ 使用标准化格式 | 日志内容以【】标签开头 |

### 6.3 快捷工具优先

| 场景 | 推荐工具 | 原因 |
|------|---------|------|
| 启动任务 | `quick.start_task` | 一键创建任务+日志 |
| 完成任务 | `quick.finish_task` | 自动触发学习 |
| 快速记录 | `quick.log` | 自动标签 |
| 快速问题 | `quick.issue` | 简化创建 |

---

## 七、故障排除

### 7.1 常见问题

| 问题 | 解决方案 |
|------|----------|
| MCP调用失败 | 检查统一服务器是否运行: `python3 mcp_servers/unified_dev_server.py` |
| knowledge.search无结果 | **先用web_search+crawler构建知识库** |
| quick.start_task报错 | 检查参数，tags参数已支持 |
| 任务状态不同步 | 手动调用 `task.list` 查看 |
| 日志丢失 | 检查 `.trquant/dev/devlog/trquant.json` |

### 7.2 数据位置

```
.trquant/dev/
├── tasks/trquant.json        # 任务数据
├── devlog/trquant.json       # 开发日志
├── issues/trquant.json       # 问题数据
├── experience/trquant.json   # 经验数据
├── knowledge/trquant.json    # 知识库数据 🆕
├── milestones/trquant.json   # 里程碑
└── registry/modules.json     # 模块注册
```

---

## 八、推荐技术栈（React迁移）

### 8.1 前端技术栈

| 类别 | 推荐 | 说明 |
|------|------|------|
| 框架 | React 18.x + TypeScript | 组件化开发 |
| 构建 | Vite | 比webpack快10倍 |
| 状态 | Zustand | 轻量，API简洁 |
| UI库 | Ant Design 5.x | 组件丰富 |
| 图表 | ECharts | 金融图表支持好 |

### 8.2 后端技术栈

| 类别 | 推荐 | 说明 |
|------|------|------|
| API | FastAPI | WebSocket支持 |
| 缓存 | Redis | 高性能 |
| 队列 | Celery | 任务调度 |

### 8.3 通信架构

| 方案 | 延迟 | 推荐阶段 |
|------|------|---------|
| 进程池优化 | 30-50ms | 短期 |
| WebSocket | 10-30ms | 中期 |
| TypeScript直接MCP | 5-15ms | 长期 |

---

*文档版本: 4.0 | 更新时间: 2025-12-20*
