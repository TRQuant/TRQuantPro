# TRQuant MCP 服务器规范

> **版本**: 2.0.0  
> **更新日期**: 2025-12-15  
> **适用范围**: 所有 MCP 服务器

---

## 1. 命名规范

### 1.1 服务器命名

格式: `{module}-server`

```
✅ 正确示例:
- data-source-server
- market-server
- backtest-server
- report-server

❌ 错误示例:
- DataServer
- marketServer
- backtest_server
```

### 1.2 工具命名

格式: `{module}.{action}` 或 `{module}.{sub_module}`

```
✅ 正确示例:
- data_source.check
- market.status
- backtest.run
- report.generate

❌ 错误示例:
- dataSourceCheck
- getMarketStatus
- runBacktest
```

### 1.3 参数命名

使用 snake_case:

```
✅ 正确示例:
- start_date
- end_date
- strategy_type
- max_drawdown

❌ 错误示例:
- startDate
- EndDate
- StrategyType
```

---

## 2. 参数验证

### 2.1 JSON Schema 要求

每个工具必须定义完整的 inputSchema:

```python
Tool(
    name="backtest.run",
    description="执行回测",
    inputSchema={
        "type": "object",
        "properties": {
            "strategy_type": {
                "type": "string",
                "enum": ["momentum", "mean_reversion"],
                "description": "策略类型"
            },
            "start_date": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                "description": "开始日期 (YYYY-MM-DD)"
            },
            "securities": {
                "type": "array",
                "items": {"type": "string"},
                "description": "股票代码列表"
            },
            "initial_capital": {
                "type": "number",
                "minimum": 10000,
                "default": 1000000,
                "description": "初始资金"
            }
        },
        "required": ["strategy_type", "start_date", "end_date"]
    }
)
```

### 2.2 使用验证器

```python
from mcp_servers.utils.mcp_standard import ParamValidator

schema = tool.inputSchema
valid, validated_args, errors = ParamValidator.validate(schema, arguments)

if not valid:
    return wrap_error(
        ErrorCode.PARAM_VALIDATION,
        f"参数验证失败: {', '.join(errors)}"
    )
```

---

## 3. trace_id 追踪机制

### 3.1 trace_id 格式

- 12位 UUID 短格式
- 示例: `a1b2c3d4e5f6`

### 3.2 使用方式

```python
from mcp_servers.utils.mcp_standard import TraceManager, TraceContext

# 方式1: 获取或创建
trace_id = TraceManager.get_or_create(arguments)

# 方式2: 上下文管理器
with TraceContext(trace_id, "my-server", "my.tool"):
    # 执行逻辑
    result = await do_something()

# 方式3: 手动管理
TraceManager.set(trace_id)
TraceManager.add_span(trace_id, "database_query", {"sql": "..."})
```

### 3.3 trace_id 传递

- 请求参数中可选传入 `trace_id`
- 如果没有，自动生成
- 响应中必须返回 `trace_id`

```json
// 请求（可选）
{
    "trace_id": "a1b2c3d4e5f6",
    "strategy_type": "momentum"
}

// 响应（必须）
{
    "success": true,
    "trace_id": "a1b2c3d4e5f6",
    "data": {...}
}
```

---

## 4. 错误码规范

### 4.1 错误码格式

格式: `{MODULE}_{NUMBER}`

| 模块 | 范围 | 说明 |
|------|------|------|
| PARAM | 1xx | 参数错误 |
| DATA | 2xx | 数据错误 |
| BIZ | 3xx | 业务错误 |
| SYS | 5xx | 系统错误 |

### 4.2 错误码列表

```python
class ErrorCode(Enum):
    # 参数错误 (1xx)
    PARAM_MISSING = "PARAM_101"           # 缺少必填参数
    PARAM_TYPE_ERROR = "PARAM_102"        # 参数类型错误
    PARAM_FORMAT_ERROR = "PARAM_103"      # 参数格式错误
    PARAM_RANGE_ERROR = "PARAM_104"       # 参数范围错误
    PARAM_VALIDATION = "PARAM_105"        # 参数验证失败
    
    # 数据错误 (2xx)
    DATA_NOT_FOUND = "DATA_201"           # 数据不存在
    DATA_FORMAT_ERROR = "DATA_202"        # 数据格式错误
    DATA_ACCESS_ERROR = "DATA_203"        # 数据访问失败
    DATA_SOURCE_ERROR = "DATA_204"        # 数据源错误
    
    # 业务错误 (3xx)
    BUSINESS_NOT_FOUND = "BIZ_301"        # 资源不存在
    BUSINESS_FORBIDDEN = "BIZ_302"        # 操作被禁止
    BUSINESS_CONFLICT = "BIZ_303"         # 操作冲突
    BUSINESS_RULE_VIOLATION = "BIZ_304"   # 违反业务规则
    
    # 系统错误 (5xx)
    SYSTEM_INTERNAL = "SYS_501"           # 内部错误
    SYSTEM_UNAVAILABLE = "SYS_502"        # 服务不可用
    SYSTEM_TIMEOUT = "SYS_503"            # 超时
    SYSTEM_DEPENDENCY = "SYS_505"         # 依赖错误
```

### 4.3 错误响应格式

```json
{
    "success": false,
    "trace_id": "a1b2c3d4e5f6",
    "error": {
        "code": "PARAM_101",
        "message": "缺少必填参数: start_date",
        "details": {
            "validation_errors": ["start_date is required"]
        }
    },
    "server": "backtest-server",
    "tool": "backtest.run"
}
```

---

## 5. 响应格式

### 5.1 成功响应

```json
{
    "success": true,
    "trace_id": "a1b2c3d4e5f6",
    "timestamp": "2025-12-15T10:30:00.000Z",
    "data": {
        // 工具返回的数据
    },
    "server": "backtest-server",
    "tool": "backtest.run",
    "duration_ms": 123.45
}
```

### 5.2 错误响应

```json
{
    "success": false,
    "trace_id": "a1b2c3d4e5f6",
    "timestamp": "2025-12-15T10:30:00.000Z",
    "error": {
        "code": "SYS_501",
        "message": "回测执行失败",
        "details": {
            "exception_type": "RuntimeError"
        }
    },
    "server": "backtest-server",
    "tool": "backtest.run"
}
```

---

## 6. 服务器实现模板

### 6.1 使用 MCPStandard 基类

```python
from mcp_servers.utils.mcp_standard import (
    MCPStandard, 
    wrap_success, 
    wrap_error, 
    ErrorCode
)

class MyServer(MCPStandard):
    SERVER_NAME = "my-server"
    SERVER_VERSION = "1.0.0"
    
    TOOLS = [
        Tool(
            name="my.action",
            description="执行操作",
            inputSchema={...}
        )
    ]
    
    async def handle_my_action(self, args: Dict) -> Dict:
        """处理 my.action 工具调用"""
        # 业务逻辑
        result = do_something(args)
        return {"result": result}
```

### 6.2 使用装饰器

```python
from mcp_servers.utils.mcp_standard import mcp_tool

SCHEMA = {
    "type": "object",
    "properties": {...},
    "required": [...]
}

@mcp_tool(schema=SCHEMA, server_name="my-server")
async def handle_my_action(args: Dict) -> Dict:
    # 自动处理参数验证、trace_id、错误处理
    return {"result": "ok"}
```

---

## 7. 监控和日志

### 7.1 结构化日志

```python
import logging
logger = logging.getLogger(__name__)

# 使用结构化日志
logger.info("工具调用", extra={
    "trace_id": trace_id,
    "server": SERVER_NAME,
    "tool": tool_name,
    "duration_ms": duration,
})
```

### 7.2 性能监控

- 所有响应包含 `duration_ms`
- 超过 500ms 记录警告日志
- 超过 2000ms 记录错误日志

---

## 8. 检查清单

开发新 MCP 服务器时，确保：

- [ ] 服务器名称符合 `xxx-server` 格式
- [ ] 工具名称符合 `module.action` 格式
- [ ] 所有工具定义了完整的 inputSchema
- [ ] 使用 ParamValidator 验证参数
- [ ] 所有响应包含 trace_id
- [ ] 错误使用标准错误码
- [ ] 响应符合标准格式
- [ ] 添加了结构化日志
- [ ] 记录了响应耗时

---

## 9. 更新记录

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0.0 | 2025-12-15 | 统一错误码，增强 trace_id，添加 MCPStandard 基类 |
| 1.0.0 | 2025-11-01 | 初始版本 |

