# 🔧 TRQuant 增强版标准开发流程指南

> **版本**: 5.0  
> **更新日期**: 2026-01-11  
> **状态**: 生产就绪

---

## 📋 概述

增强版标准开发流程在原有MCP标准开发流程基础上，增加了5个关键改进：

| # | 改进项 | 说明 | 工具 |
|---|--------|------|------|
| 1 | **开发前调研** | 充分调研背景，与专业标准对照 | `research.*` |
| 2 | **代码复用检查** | 查询是否有相关功能可复用 | `dev.check_existing` |
| 3 | **增量测试验证** | 每一步测试通过后再继续 | `workflow.incremental_test` |
| 4 | **知识库记录** | 开发过程记录到RAG知识库 | `dev.record_to_kb` |
| 5 | **MongoDB测试管理** | 测试结果由数据库管理 | `test.*` |

---

## ⚠️ 严格错误处理原则（必须遵守）

### 核心原则

**如果某一步出现错误，必须立即停止运行，修复后再运行。**

### 原则说明

1. **错误即停止**：任何步骤出现错误（如初始化失败、回测失败、数据加载失败等），程序必须立即停止，不允许忽略错误继续执行。

2. **修复后重运行**：错误必须修复后再重新运行，不允许在未修复的情况下继续执行后续步骤。

3. **错误处理机制**：
   - 使用 `FatalError` 异常表示致命错误
   - 使用 `check_and_raise()` 函数检查关键条件
   - 所有关键步骤必须进行错误检查和验证

### 实现示例

```python
# 定义致命错误类
class FatalError(Exception):
    """致命错误 - 必须停止运行"""
    pass

# 检查函数
def check_and_raise(error_message: str, condition: bool = True):
    """检查条件，如果失败则抛出致命错误"""
    if not condition:
        logger.error(f"❌ 致命错误: {error_message}")
        logger.error("⚠️ 根据标准开发流程：遇到错误必须停止运行，修复后再运行")
        raise FatalError(error_message)

# 使用示例
try:
    # 初始化（严格检查）
    preloader = DataPreloader(...)
    check_and_raise("DataPreloader初始化失败", preloader is not None)
    
    # 数据预加载（严格检查）
    result = preloader.preload_market_data(...)
    check_and_raise("数据预加载返回None", result is not None)
    
    # 回测执行（严格检查）
    bt_result = backtest.run_backtest(...)
    check_and_raise("回测返回None", bt_result is not None)
    
except FatalError as e:
    logger.error(f"❌ 致命错误：程序已停止")
    logger.error(f"错误信息: {e}")
    logger.error("⚠️ 请修复错误后重新运行")
    sys.exit(1)
```

### 错误处理最佳实践

1. **关键步骤必须检查**：
   - 模块初始化
   - 数据加载
   - 回测执行
   - 结果验证

2. **错误信息要详细**：
   - 明确指出错误位置
   - 提供错误原因
   - 给出修复建议

3. **日志输出要清晰**：
   - 使用 `❌` 标记致命错误
   - 使用 `⚠️` 标记警告信息
   - 错误后输出修复指导

---

## 🛡️ 防止重复开发机制（必须遵守）

### 核心问题

**即使我们已经开发过某个功能，如果没有正确的机制，还是可能会重复踩坑。**

例如：BulletTrade引擎需要设置JQData环境变量，但这个知识如果没有存入知识库，下次使用时还是可能忘记。

### 必须执行的步骤

**在开发任何涉及第三方库或已开发模块的功能前，必须：**

1. **查询RAG知识库**：
```python
# 使用MCP工具查询
await call_mcp("knowledge.search", {"query": "BulletTrade", "limit": 5})
await call_mcp("error_pattern.search", {"error_msg": "账号权限"})
await call_mcp("practice.search", {"query": "回测环境变量"})
```

2. **查询错误模式库**：
```python
# 搜索相关错误模式
await call_mcp("error_pattern.search", {"error_msg": "相关错误关键词"})
```

3. **查询最佳实践库**：
```python
# 搜索最佳实践
await call_mcp("practice.search", {"query": "相关功能关键词"})
```

### 开发后必须执行的步骤

**解决问题或完成功能后，必须将经验存入知识库：**

1. **存储错误模式**（如果遇到了错误）：
```python
await call_mcp("error_pattern.add", {
    "error_type": "错误类型",
    "pattern": "错误模式描述",
    "solution": "解决方案",
    "prevention": "预防措施",
    "tags": ["相关标签"]
})
```

2. **存储最佳实践**（如果发现了最佳实践）：
```python
await call_mcp("practice.add", {
    "title": "实践标题",
    "description": "实践描述",
    "code_example": "示例代码",
    "category": "分类",
    "tags": ["相关标签"]
})
```

3. **存储通用知识**：
```python
await call_mcp("knowledge.add", {
    "title": "知识标题",
    "content": "详细内容",
    "type": "lesson",  # lesson/error/practice
    "tags": ["相关标签"],
    "source": "来源"
})
```

### 已知的关键知识点

| 模块/库 | 关键知识 | 知识库ID |
|--------|----------|----------|
| BulletTrade | 必须设置JQDATA_USERNAME和JQDATA_PASSWORD环境变量 | kb_20260111_174532 |
| JQData | 正式账号无数据限制，试用账号只有1年数据 | - |
| DataPreloader | 最大3个并发线程下载JQData数据 | - |

### 机制保障

1. **开发前自动检查**：在开发脚本中集成知识库查询
2. **开发后自动提醒**：提示将经验存入知识库
3. **定期知识库审计**：检查知识库覆盖率

---

## 🚀 快速开始

### 1. 新功能开发流程

```python
# 步骤1: 开发前调研
await call_mcp("research.background", {
    "topic": "功能描述",
    "module_name": "模块名",
    "search_kb": True,
    "search_web": True
})

# 步骤2: 检查代码复用
await call_mcp("dev.check_existing", {
    "module_name": "模块名",
    "functionality": "功能描述",
    "search_scope": "all"
})

# 步骤3: 与专业标准对照
await call_mcp("research.compare_standards", {
    "module_name": "模块名",
    "implementation_plan": "实现方案描述",
    "standard_type": "best_practice"
})

# 步骤4: 创建任务并开发
await call_mcp("task.create", {"title": "任务标题"})

# 步骤5: 每个步骤完成后测试
await call_mcp("workflow.incremental_test", {
    "task_id": "task_xxx",
    "step_name": "步骤名",
    "test_function": "测试命令"
})

# 步骤6: 记录测试结果
await call_mcp("test.record", {
    "module_name": "模块名",
    "test_name": "测试名",
    "status": "passed"
})

# 步骤7: 验证步骤可继续
await call_mcp("workflow.validate_step", {
    "task_id": "task_xxx",
    "step_name": "步骤名"
})

# 步骤8: 完成后记录到知识库
await call_mcp("dev.record_to_kb", {
    "task_id": "task_xxx",
    "module_name": "模块名",
    "title": "开发经验: XXX",
    "summary": "开发总结",
    "lessons_learned": ["经验1", "经验2"]
})
```

---

## 📚 工具详解

### 1. 调研工具 (research.*)

#### research.background - 开发前背景调研

在开发任何模块前，充分调研背景、最佳实践和已有知识。

```python
result = await call_mcp("research.background", {
    "topic": "MongoDB测试结果存储",      # 调研主题
    "module_name": "test_storage",       # 模块名称
    "objectives": ["了解MongoDB最佳实践", "确认数据结构"],  # 调研目标
    "search_kb": True,                   # 搜索知识库
    "search_web": True                   # 需要网络搜索建议
})

# 返回结果
{
    "success": True,
    "research": {
        "research_id": "research_20260111_xxx",
        "findings": {
            "kb_coverage": "充分/需要补充",
            "kb_results": [...],
            "web_search_needed": True/False
        },
        "recommendations": [...],
        "next_steps": [...]
    },
    "web_search_suggestions": ["搜索建议1", "搜索建议2"]
}
```

#### research.compare_standards - 与专业标准对照

```python
result = await call_mcp("research.compare_standards", {
    "module_name": "test_storage",
    "implementation_plan": "使用MongoDB存储测试结果，支持查询和统计",
    "standard_type": "best_practice"  # best_practice/api_design/testing/security
})
```

### 2. 代码复用检查 (dev.*)

#### dev.check_existing - 检查已有实现

在开发新功能前，检查是否有可复用的代码。

```python
result = await call_mcp("dev.check_existing", {
    "module_name": "test_storage",
    "functionality": "MongoDB存储测试结果",
    "search_scope": "all"  # all/core/mcp_servers/scripts
})

# 返回结果
{
    "success": True,
    "check_result": {
        "existing_modules": [
            {"path": "core/market_trend_storage.py", "match_score": 0.8, "description": "..."}
        ],
        "kb_references": [
            {"id": "kb_xxx", "title": "MongoDB最佳实践", "type": "lesson"}
        ],
        "recommendations": [
            "强烈建议：发现高度相似的模块 xxx，建议直接复用或继承"
        ]
    }
}
```

#### dev.record_progress - 记录开发进度

```python
await call_mcp("dev.record_progress", {
    "task_id": "task_xxx",
    "module_name": "test_storage",
    "step_name": "实现存储类",
    "status": "completed",  # started/in_progress/completed/blocked
    "details": "已完成MongoDB存储类",
    "code_changes": ["core/dev_workflow/test_result_storage.py"]
})
```

#### dev.record_to_kb - 记录到知识库

```python
await call_mcp("dev.record_to_kb", {
    "task_id": "task_xxx",
    "module_name": "test_storage",
    "title": "开发经验: MongoDB测试结果存储",
    "summary": "实现了测试结果的MongoDB存储，支持查询、统计和趋势分析",
    "lessons_learned": [
        "使用pymongo时需要处理连接超时",
        "索引创建要在初始化时完成"
    ],
    "code_examples": [
        {
            "name": "记录测试结果",
            "language": "python",
            "code": "storage.record_test(module_name='xxx', test_name='xxx', status='passed')"
        }
    ],
    "tags": ["mongodb", "testing", "storage"]
})
```

### 3. 测试管理 (test.*)

#### test.record - 记录测试结果

```python
await call_mcp("test.record", {
    "module_name": "core.dev_workflow",
    "test_name": "test_storage_connection",
    "status": "passed",  # passed/failed/skipped/error
    "duration_ms": 150.5,
    "message": "MongoDB连接测试通过",
    "test_type": "unit",  # unit/integration/e2e
    "tags": ["mongodb", "connection"]
})
```

#### test.query - 查询测试结果

```python
result = await call_mcp("test.query", {
    "module_name": "core.dev_workflow",
    "status": "failed",
    "test_type": "unit",
    "limit": 50
})
```

#### test.start_session - 开始测试会话

```python
result = await call_mcp("test.start_session", {
    "task_id": "task_xxx",
    "module_name": "test_storage",
    "test_plan": ["test_connection", "test_record", "test_query"]
})
# 返回 session_id
```

#### test.complete_session - 完成测试会话

```python
await call_mcp("test.complete_session", {
    "session_id": "session_xxx",
    "summary": {
        "total": 10,
        "passed": 9,
        "failed": 1,
        "duration_ms": 5000,
        "coverage_pct": 85.0
    }
})
```

#### test.get_stats - 获取模块测试统计

```python
result = await call_mcp("test.get_stats", {
    "module_name": "core.dev_workflow"
})
# 返回 pass_rate, total, passed, failed 等统计
```

### 4. 工作流增强 (workflow.*)

#### workflow.incremental_test - 增量测试验证

**核心工具！** 确保每个步骤测试通过后才能继续。

```python
result = await call_mcp("workflow.incremental_test", {
    "task_id": "task_xxx",
    "step_name": "实现存储类",
    "test_function": "./venv/bin/python -c 'from core.dev_workflow import get_test_storage; print(get_test_storage())'",
    "expected_result": "passed"
})

# 返回
{
    "success": True,
    "verification": {...},
    "instructions": [
        "1. 执行测试: ...",
        "2. 期望结果: passed",
        "3. 测试通过后调用: test.record(...)",
        "4. 测试失败则记录问题: issue.create(...)"
    ],
    "next_step_blocked": True,  # 下一步被阻塞，直到测试通过
    "message": "请完成测试验证后再继续开发"
}
```

#### workflow.validate_step - 验证步骤可继续

```python
result = await call_mcp("workflow.validate_step", {
    "task_id": "task_xxx",
    "step_name": "实现存储类"
})

# 返回
{
    "success": True,
    "validation": {
        "can_proceed": True,  # 是否可以继续
        "has_passed_tests": True,
        "message": "✅ 步骤已通过测试，可以继续下一步"
    }
}
```

#### workflow.enhanced_check - 增强版流程检查

检查整体开发流程状态。

```python
result = await call_mcp("workflow.enhanced_check", {
    "task_id": "task_xxx"
})

# 返回
{
    "success": True,
    "status": {
        "research": {"has_recent_research": True, "status": "✅"},
        "testing": {"total_tests": 10, "pass_rate": 90.0, "status": "✅"},
        "development": {"records_count": 5, "status": "✅"}
    },
    "recommendations": ["✅ 开发流程状态良好，继续保持！"]
}
```

---

## 🔄 完整开发流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                   增强版标准开发流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Phase 0: 调研阶段]                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ research.background() → 知识库搜索 + 网络搜索建议        │   │
│  │ research.compare_standards() → 与专业标准对照            │   │
│  │ dev.check_existing() → 检查可复用代码                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  [Phase 1: 规划阶段]                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ task.create() → 创建任务                                 │   │
│  │ dev.record_progress(status='started') → 记录开始         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  [Phase 2: 开发循环] ◄─────────────────────────────────┐       │
│  ┌─────────────────────────────────────────────────────│───┐   │
│  │ for each step:                                      │   │   │
│  │   1. 编写代码                                       │   │   │
│  │   2. workflow.incremental_test() → 增量测试验证     │   │   │
│  │   3. test.record() → 记录测试结果到MongoDB          │   │   │
│  │   4. workflow.validate_step() → 验证是否可继续      │   │   │
│  │      ├── 通过 → 继续下一步 ─────────────────────────┘   │   │
│  │      └── 失败 → issue.create() → 修复 → 返回步骤2       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│  [Phase 3: 完成阶段]                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ test.complete_session() → 完成测试会话                   │   │
│  │ task.complete() → 完成任务                               │   │
│  │ dev.record_to_kb() → 记录经验到知识库                    │   │
│  │ workflow.enhanced_check() → 流程完整性检查               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 数据存储

### MongoDB 集合

| 集合名 | 用途 | 存储位置 |
|--------|------|----------|
| `test_results` | 测试结果 | MongoDB: trquant_dev |
| `test_sessions` | 测试会话 | MongoDB: trquant_dev |
| `test_coverage` | 测试覆盖率 | MongoDB: trquant_dev |

### 文件存储（备份）

```
~/.local/share/trquant/test_results/
├── results/          # 测试结果JSON文件
└── sessions/         # 测试会话JSON文件

~/.trquant/dev/
├── research/         # 调研记录
├── dev_records/      # 开发进度记录
└── test_sessions/    # 测试会话（文件模式）
```

---

## 🔧 MCP服务器配置

服务器已添加到 `~/.cursor/mcp.json`:

```json
{
  "enhanced-dev-workflow": {
    "command": "/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python",
    "args": [
      "/home/taotao/.cursor/worktrees/TRQuant/ope/mcp_servers/enhanced_dev_workflow_server.py"
    ],
    "env": {
      "PYTHONIOENCODING": "utf-8",
      "TRQUANT_ROOT": "/home/taotao/.cursor/worktrees/TRQuant/ope"
    },
    "description": "🔧 增强版开发工作流 - 调研/代码复用/增量测试/知识库记录/MongoDB测试管理 (15个工具)"
  }
}
```

---

## ⚠️ 重要原则

### 1. 调研先行

> 开发任何新功能前，必须先调研背景和检查代码复用

```python
# ❌ 错误：直接开始开发
await call_mcp("task.create", {"title": "实现新功能"})

# ✅ 正确：先调研
await call_mcp("research.background", {...})
await call_mcp("dev.check_existing", {...})
await call_mcp("task.create", {"title": "实现新功能"})
```

### 2. 增量测试

> 每个步骤必须测试通过后才能继续下一步

```python
# ❌ 错误：堆积代码后统一测试
# 开发步骤1
# 开发步骤2
# 开发步骤3
# 最后一起测试

# ✅ 正确：每步都测试
# 开发步骤1 → workflow.incremental_test() → test.record() → validate_step()
# 开发步骤2 → workflow.incremental_test() → test.record() → validate_step()
# 开发步骤3 → workflow.incremental_test() → test.record() → validate_step()
```

### 3. 知识沉淀

> 开发完成后必须记录到知识库

```python
# ✅ 每次完成任务后
await call_mcp("dev.record_to_kb", {
    "title": "开发经验: XXX",
    "summary": "...",
    "lessons_learned": [...]
})
```

---

## 📊 工具统计

| 类别 | 工具数量 | 工具列表 |
|------|---------|----------|
| 调研工具 | 4 | research.background, research.compare_standards, research.query_history, research.add_finding |
| 代码复用 | 3 | dev.check_existing, dev.record_progress, dev.record_to_kb |
| 测试管理 | 5 | test.record, test.query, test.start_session, test.complete_session, test.get_stats |
| 工作流增强 | 3 | workflow.incremental_test, workflow.validate_step, workflow.enhanced_check |
| **总计** | **15** | |

---

*文档版本: 5.0 | 更新时间: 2026-01-11*
