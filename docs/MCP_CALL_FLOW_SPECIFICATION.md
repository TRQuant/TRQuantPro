# TRQuant MCP调用流程规范

> **创建时间**: 2025-12-14  
> **版本**: 1.0.0  
> **状态**: 正式发布

---

## 📋 概述

本文档定义了TRQuant项目中MCP（Model Context Protocol）的调用流程规范，确保：
1. 统一的调用接口和响应格式
2. 完善的错误处理和日志记录
3. 高效的上下文管理和缓存策略
4. 清晰的工具分类和命名规范

---

## 🏗️ 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                      Cursor AI Agent                         │
├─────────────────────────────────────────────────────────────┤
│                        MCP Protocol                          │
├─────────────────────────────────────────────────────────────┤
│                    MCP Server Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ trquant      │  │ trquant-spec │  │ trquant-task │       │
│  │ (business)   │  │ (规范)       │  │ (任务管理)   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ trquant-kb   │  │ trquant-     │  │ trquant-     │       │
│  │ (知识库)     │  │ evidence     │  │ backtest     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
├─────────────────────────────────────────────────────────────┤
│                    Integration Layer                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  process_mcp_tool_call() + envelope wrapper           │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                     Core Services                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ DataCenter   │  │ Backtest     │  │ Strategy     │       │
│  │              │  │ Engine       │  │ Generator    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 调用流程规范

### 1. 标准调用流程

```python
# 1. AI Agent发起调用
request = {
    "tool": "trquant.market_status",
    "arguments": {
        "universe": "CN_EQ",
        "trace_id": "tr-xxxx-xxxx",  # 可选，用于追踪
        "mode": "read",              # read/dry_run/execute
        "artifact_policy": "inline"  # inline/pointer
    }
}

# 2. MCP Server接收并处理
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    # 2.1 提取参数
    trace_id = extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    
    # 2.2 定义handler
    def handler(args):
        # 业务逻辑
        return result
    
    # 2.3 使用统一处理函数
    result = process_mcp_tool_call(
        tool_name=name,
        arguments=arguments,
        tools_list=tools_list,
        tool_handler_func=handler,
        server_name="trquant",
        version="1.0.0"
    )
    
    # 2.4 返回统一格式
    return _adapt_mcp_result_to_text_content(result)

# 3. 响应格式（envelope）
response = {
    "success": True,
    "data": {...},
    "metadata": {
        "server_name": "trquant",
        "tool_name": "trquant.market_status",
        "version": "1.0.0",
        "trace_id": "tr-xxxx-xxxx",
        "timestamp": "2025-12-14T10:00:00Z"
    }
}
```

### 2. 工具命名规范

| 类别 | 前缀 | 示例 |
|------|------|------|
| 业务工具 | `trquant.` | `trquant.market_status`, `trquant.generate_strategy` |
| 规范工具 | `spec.` | `spec.list`, `spec.validate` |
| 知识库 | `kb.` | `kb.search`, `kb.add` |
| 任务管理 | `task.` | `task.analyze_complexity`, `task.cache_context` |
| 数据质量 | `quality.` | `quality.check`, `quality.validate` |
| 回测相关 | `backtest.` | `backtest.run`, `backtest.analyze` |
| 策略模板 | `template.` | `template.list`, `template.generate` |
| 配置管理 | `config.` | `config.get`, `config.set` |

### 3. 参数规范

#### 3.1 基础参数（所有工具都支持）

```json
{
    "trace_id": "string",       // 追踪ID，用于日志关联
    "mode": "read|dry_run|execute",  // 操作模式
    "artifact_policy": "inline|pointer"  // 大数据处理策略
}
```

#### 3.2 模式说明

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `read` | 只读操作 | 查询、获取数据 |
| `dry_run` | 模拟执行 | 预览变更、验证参数 |
| `execute` | 实际执行 | 创建、修改、删除 |

#### 3.3 artifact_policy说明

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| `inline` | 数据内嵌在响应中 | 小数据（<10KB） |
| `pointer` | 返回artifact指针 | 大数据（>10KB），如策略代码 |

---

## 🔧 统一封装层

### 1. process_mcp_tool_call 函数

```python
def process_mcp_tool_call(
    tool_name: str,
    arguments: Dict[str, Any],
    tools_list: List[Tool],
    tool_handler_func: Callable,
    server_name: str = "trquant",
    version: str = "1.0.0",
    trace_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    统一处理MCP工具调用
    
    功能：
    1. 参数校验（基于工具Schema）
    2. 调用业务逻辑
    3. 错误处理和日志记录
    4. 响应包装（envelope格式）
    
    参数：
        tool_name: 工具名称
        arguments: 调用参数
        tools_list: 工具列表（用于Schema校验）
        tool_handler_func: 业务逻辑处理函数
        server_name: 服务器名称
        version: 版本号
        trace_id: 追踪ID（可选）
    
    返回：
        统一格式的响应envelope
    """
```

### 2. envelope响应格式

#### 2.1 成功响应

```json
{
    "success": true,
    "data": {
        // 业务数据
    },
    "metadata": {
        "server_name": "trquant",
        "tool_name": "trquant.market_status",
        "version": "1.0.0",
        "trace_id": "tr-xxxx-xxxx",
        "timestamp": "2025-12-14T10:00:00Z",
        "duration_ms": 150
    }
}
```

#### 2.2 错误响应

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "缺少必需参数: universe",
        "hint": "请提供universe参数，可选值：CN_EQ, US_EQ",
        "details": {
            "missing_params": ["universe"]
        }
    },
    "metadata": {
        "server_name": "trquant",
        "tool_name": "trquant.market_status",
        "version": "1.0.0",
        "trace_id": "tr-xxxx-xxxx",
        "timestamp": "2025-12-14T10:00:00Z"
    }
}
```

### 3. 错误码规范

| 错误码 | 说明 | HTTP等效 |
|--------|------|----------|
| `VALIDATION_ERROR` | 参数验证失败 | 400 |
| `NOT_FOUND` | 资源不存在 | 404 |
| `PERMISSION_DENIED` | 权限不足 | 403 |
| `DEPENDENCY_ERROR` | 依赖服务不可用 | 503 |
| `INTERNAL_ERROR` | 内部错误 | 500 |
| `TIMEOUT` | 操作超时 | 504 |
| `RATE_LIMITED` | 请求过于频繁 | 429 |

---

## 📊 上下文管理

### 1. 上下文缓存策略

```python
# 使用task_optimizer_server管理上下文缓存

# 1. 检查缓存
context = task.get_context(file_path="docs/PROJECT_TASK_LIST.md")

if context["cached"]:
    # 使用缓存，节省token
    use_cached_context(context["context"])
else:
    # 读取文件
    content = read_file("docs/PROJECT_TASK_LIST.md")
    
    # 缓存上下文
    task.cache_context(
        file_path="docs/PROJECT_TASK_LIST.md",
        context={
            "summary": "项目任务列表，包含15个主要阶段",
            "key_tasks": [...],
            "last_updated": "2025-12-14"
        }
    )
```

### 2. 工作流优化

```python
# 任务开始前优化工作流
workflow = task.optimize_workflow(
    task_title="修复MCP服务器",
    file_paths=[
        "mcp_servers/schema_server.py",
        "mcp_servers/factor_server.py",
        "docs/MCP_INTEGRATION_BEST_PRACTICES.md"
    ]
)

# 结果包含：
# - cached_files: 可以复用的文件列表
# - need_read_files: 需要读取的文件列表
# - token_savings: 预计节省的tokens
```

---

## 🔄 调用示例

### 1. 获取市场状态

```python
# AI调用
result = trquant.market_status(universe="CN_EQ")

# 响应
{
    "success": true,
    "data": {
        "regime": "neutral",
        "index_trend": {...},
        "style_rotation": [...],
        "summary": "市场处于震荡格局，价值风格相对占优"
    },
    "metadata": {...}
}
```

### 2. 生成策略代码

```python
# AI调用
result = trquant.generate_strategy(
    factors=["ROE_ttm", "PE_ttm", "momentum_20d"],
    style="multi_factor",
    platform="ptrade",
    max_position=0.1,
    stop_loss=0.08,
    take_profit=0.2
)

# 响应（使用artifact_policy=pointer）
{
    "success": true,
    "data": {
        "artifact_pointer": "artifacts/strategy_20251214_100000.json",
        "summary": {
            "name": "multi_factor_ptrade_20251214",
            "platform": "ptrade",
            "factors": ["ROE_ttm", "PE_ttm", "momentum_20d"],
            "code_lines": 150
        },
        "preview": "# -*- coding: utf-8 -*-\n..."
    },
    "metadata": {...}
}
```

### 3. 分析任务复杂度

```python
# AI调用
result = task.analyze_complexity(
    task_title="修复MCP服务器集成",
    file_count=6,
    code_complexity="medium"
)

# 响应
{
    "success": true,
    "data": {
        "complexity": "complex",
        "complexity_score": 5,
        "recommended_mode": "max",
        "reason": "任务涉及多个文件或复杂业务逻辑，需要Max mode的深度理解能力"
    },
    "metadata": {...}
}
```

---

## 📝 最佳实践

### 1. 工具开发

1. **使用process_mcp_tool_call**：所有工具都应使用统一的处理函数
2. **完善参数Schema**：提供清晰的参数描述和验证规则
3. **提供错误提示**：在错误响应中包含有用的hint
4. **支持trace_id**：便于调试和日志追踪

### 2. 上下文管理

1. **优先使用缓存**：检查缓存再读取文件
2. **及时更新缓存**：读取新文件后立即缓存
3. **定期清理**：清理过期缓存避免占用空间

### 3. 错误处理

1. **分类处理**：区分验证错误、业务错误、系统错误
2. **提供上下文**：在错误信息中包含足够的上下文
3. **记录日志**：所有错误都应记录日志

---

## 📚 相关文档

- [MCP集成最佳实践](./MCP_INTEGRATION_BEST_PRACTICES.md)
- [任务优化指南](./TASK_OPTIMIZATION_GUIDE.md)
- [错误码设计](./TRACE_ID_AND_ERROR_CODE_DESIGN.md)

---

**文档维护**: TRQuant Team  
**最后更新**: 2025-12-14
