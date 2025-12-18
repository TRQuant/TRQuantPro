# trace_id追踪机制设计

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: 所有TRQuant MCP服务器和工具调用

---

## 📋 概述

本文档定义了TRQuant系统中trace_id追踪机制的设计，用于关联和追踪整个调用链，便于问题排查、性能分析和日志关联。

## 🎯 设计目标

1. **可追溯性**: 能够追踪完整的调用链
2. **可关联性**: 日志、错误、结果可以通过trace_id关联
3. **可分析性**: 支持性能分析和调用链分析
4. **低侵入性**: 对现有代码的侵入性最小

---

## 🔑 trace_id生成规则

### 格式

使用UUID v4格式：

```
xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
```

其中：
- `x` 是十六进制数字（0-9, a-f）
- `4` 是版本号（固定）
- `y` 是8, 9, a, 或 b之一

### 示例

```
550e8400-e29b-41d4-a716-446655440000
```

### 生成规则

1. **根trace_id**: 由调用方（Cursor扩展、GUI、CLI）生成
2. **子trace_id**: 如果需要在调用链中创建新的分支，可以生成子trace_id
3. **传递规则**: trace_id在调用链中自动传递

---

## 📝 trace_id传递机制

### 传递方式

1. **参数传递**: 作为工具参数传递
2. **上下文传递**: 通过上下文对象传递
3. **日志关联**: 所有日志自动包含trace_id

### 传递流程

```
调用方（生成trace_id）
    ↓
MCP工具调用（接收并传递trace_id）
    ↓
内部函数调用（传递trace_id）
    ↓
日志记录（包含trace_id）
    ↓
结果返回（包含trace_id）
```

---

## 🔧 实现方案

### 1. trace_id生成器

```python
import uuid
from typing import Optional

def generate_trace_id() -> str:
    """生成新的trace_id"""
    return str(uuid.uuid4())
```

### 2. trace_id管理器

```python
class TraceManager:
    """trace_id管理器"""
    
    def __init__(self):
        self.current_trace_id: Optional[str] = None
    
    def set_trace_id(self, trace_id: str):
        """设置当前trace_id"""
        self.current_trace_id = trace_id
    
    def get_trace_id(self) -> Optional[str]:
        """获取当前trace_id"""
        return self.current_trace_id
    
    def generate_and_set(self) -> str:
        """生成并设置新的trace_id"""
        trace_id = generate_trace_id()
        self.set_trace_id(trace_id)
        return trace_id
```

### 3. 参数Schema扩展

所有工具的参数Schema应包含可选的trace_id字段：

```python
{
    "type": "object",
    "properties": {
        "trace_id": {
            "type": "string",
            "description": "追踪ID，用于关联调用链",
            "pattern": "^[a-f0-9-]{36}$"
        },
        # ... 其他参数
    }
}
```

---

## 📊 使用场景

### 场景1: MCP工具调用

```python
# 调用方生成trace_id
trace_id = generate_trace_id()

# 调用MCP工具时传递
result = await mcp_tool.call(
    name="kb.query",
    arguments={
        "query": "test",
        "trace_id": trace_id
    }
)
```

### 场景2: 日志记录

```python
import logging

logger = logging.getLogger(__name__)

# 日志自动包含trace_id
logger.info(f"[trace_id={trace_id}] 开始查询知识库")
```

### 场景3: 错误追踪

```python
try:
    result = some_operation()
except Exception as e:
    logger.error(f"[trace_id={trace_id}] 操作失败: {e}")
    raise
```

### 场景4: 结果返回

```python
return {
    "trace_id": trace_id,
    "result": result_data,
    "status": "success"
}
```

---

## 🔍 日志关联

### 日志格式

所有日志应包含trace_id：

```
[2025-12-14 10:30:45] [INFO] [trace_id=550e8400-...] 开始处理请求
[2025-12-14 10:30:45] [DEBUG] [trace_id=550e8400-...] 调用MCP工具: kb.query
[2025-12-14 10:30:46] [INFO] [trace_id=550e8400-...] 查询完成，返回10条结果
```

### 日志检索

可以通过trace_id检索所有相关日志：

```bash
grep "trace_id=550e8400-.*" logs/app.log
```

---

## 📖 相关文档

- [MCP工具命名规范](./MCP_NAMING_CONVENTIONS.md)
- [MCP参数结构规范](./MCP_PARAMETER_SCHEMA.md)
- [MCP错误码体系](./ERROR_CODE_SYSTEM.md)

---

**最后更新**: 2025-12-14
