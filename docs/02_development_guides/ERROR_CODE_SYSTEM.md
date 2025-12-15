# MCP错误码体系

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: 所有TRQuant MCP服务器

---

## 📋 概述

本文档定义了TRQuant系统中统一的错误码体系，用于标准化错误处理和异常响应，便于问题定位和系统监控。

## 🎯 设计原则

1. **唯一性**: 每个错误码唯一标识一种错误类型
2. **可读性**: 错误码包含模块和错误类型信息
3. **可扩展性**: 支持新增错误码而不影响现有代码
4. **标准化**: 所有MCP工具使用统一的错误响应格式

---

## 📝 错误码格式

### 格式

```
{模块}_{错误类型}_{编号}
```

### 格式说明

- **模块**: 错误发生的模块（如 `kb`, `data`, `backtest`）
- **错误类型**: 错误类型（如 `param`, `system`, `business`）
- **编号**: 3位数字编号（001-999）

### 示例

```
KB_PARAM_001    # 知识库参数错误：缺少必填参数
DATA_SYSTEM_002 # 数据源系统错误：连接失败
BACKTEST_BUSINESS_001 # 回测业务错误：策略不存在
```

---

## 🏷️ 错误类型分类

### 1. 参数错误 (PARAM)

参数验证、格式、范围等错误。

| 错误码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| `*_PARAM_001` | 缺少必填参数 | 400 |
| `*_PARAM_002` | 参数类型错误 | 400 |
| `*_PARAM_003` | 参数格式错误 | 400 |
| `*_PARAM_004` | 参数值超出范围 | 400 |
| `*_PARAM_005` | 参数验证失败 | 400 |

### 2. 系统错误 (SYSTEM)

系统级错误，如连接失败、超时等。

| 错误码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| `*_SYSTEM_001` | 内部系统错误 | 500 |
| `*_SYSTEM_002` | 服务不可用 | 503 |
| `*_SYSTEM_003` | 连接超时 | 504 |
| `*_SYSTEM_004` | 资源不足 | 503 |
| `*_SYSTEM_005` | 配置错误 | 500 |

### 3. 业务错误 (BUSINESS)

业务逻辑错误。

| 错误码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| `*_BUSINESS_001` | 资源不存在 | 404 |
| `*_BUSINESS_002` | 操作不允许 | 403 |
| `*_BUSINESS_003` | 状态冲突 | 409 |
| `*_BUSINESS_004` | 业务规则违反 | 422 |
| `*_BUSINESS_005` | 操作失败 | 422 |

### 4. 数据错误 (DATA)

数据相关错误。

| 错误码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| `*_DATA_001` | 数据不存在 | 404 |
| `*_DATA_002` | 数据格式错误 | 400 |
| `*_DATA_003` | 数据验证失败 | 422 |
| `*_DATA_004` | 数据访问失败 | 500 |

---

## 📚 模块错误码定义

### 知识库模块 (KB)

| 错误码 | 说明 |
|--------|------|
| `KB_PARAM_001` | 缺少查询参数 |
| `KB_PARAM_002` | 查询参数格式错误 |
| `KB_SYSTEM_001` | 知识库连接失败 |
| `KB_SYSTEM_002` | 向量数据库错误 |
| `KB_BUSINESS_001` | 知识库不存在 |
| `KB_DATA_001` | 索引构建失败 |

### 数据源模块 (DATA)

| 错误码 | 说明 |
|--------|------|
| `DATA_PARAM_001` | 缺少数据源参数 |
| `DATA_PARAM_002` | 数据源类型不支持 |
| `DATA_SYSTEM_001` | 数据源连接失败 |
| `DATA_SYSTEM_002` | 数据源超时 |
| `DATA_BUSINESS_001` | 数据源不存在 |
| `DATA_DATA_001` | 数据查询失败 |

### 回测模块 (BACKTEST)

| 错误码 | 说明 |
|--------|------|
| `BACKTEST_PARAM_001` | 缺少策略参数 |
| `BACKTEST_PARAM_002` | 回测参数无效 |
| `BACKTEST_SYSTEM_001` | 回测引擎错误 |
| `BACKTEST_BUSINESS_001` | 策略不存在 |
| `BACKTEST_BUSINESS_002` | 回测任务已存在 |

---

## 🔧 错误响应格式

### 标准错误响应

```json
{
    "error": {
        "code": "KB_PARAM_001",
        "message": "缺少必填参数: query",
        "type": "PARAM",
        "module": "KB",
        "trace_id": "550e8400-e29b-41d4-a716-446655440000",
        "details": {
            "missing_params": ["query"]
        }
    }
}
```

### Python异常类

```python
class MCPError(Exception):
    """MCP工具基础异常类"""
    def __init__(self, code: str, message: str, details: Dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class MCPParameterError(MCPError):
    """参数错误"""
    pass

class MCPSystemError(MCPError):
    """系统错误"""
    pass

class MCPBusinessError(MCPError):
    """业务错误"""
    pass
```

---

## 📖 使用示例

### 示例1: 参数验证错误

```python
from mcp_servers.utils.error_handler import MCPParameterError

if "query" not in arguments:
    raise MCPParameterError(
        code="KB_PARAM_001",
        message="缺少必填参数: query",
        details={"missing_params": ["query"]}
    )
```

### 示例2: 系统错误

```python
from mcp_servers.utils.error_handler import MCPSystemError

try:
    result = connect_to_database()
except ConnectionError as e:
    raise MCPSystemError(
        code="KB_SYSTEM_001",
        message="知识库连接失败",
        details={"error": str(e)}
    )
```

### 示例3: 业务错误

```python
from mcp_servers.utils.error_handler import MCPBusinessError

if not kb_exists(kb_id):
    raise MCPBusinessError(
        code="KB_BUSINESS_001",
        message=f"知识库不存在: {kb_id}",
        details={"kb_id": kb_id}
    )
```

---

## 📖 相关文档

- [MCP工具命名规范](./MCP_NAMING_CONVENTIONS.md)
- [MCP参数结构规范](./MCP_PARAMETER_SCHEMA.md)
- [trace_id追踪机制](./TRACE_ID_DESIGN.md)

---

**最后更新**: 2025-12-14
