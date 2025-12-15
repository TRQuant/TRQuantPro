# MCP参数结构规范

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: 所有TRQuant MCP服务器

---

## 📋 概述

本文档定义了TRQuant系统中所有MCP工具的参数结构规范，包括JSON Schema定义模板、参数类型规范、参数验证规则等。

## 🎯 规范原则

1. **统一性**: 所有工具使用统一的参数结构
2. **完整性**: 参数定义完整，包含类型、描述、验证规则
3. **可验证性**: 所有参数可进行自动验证
4. **可扩展性**: 支持参数扩展和版本管理

---

## 📝 JSON Schema定义模板

### 基本模板

```json
{
  "type": "object",
  "properties": {
    "param_name": {
      "type": "string|number|boolean|object|array",
      "description": "参数描述",
      "default": "默认值（可选）",
      "enum": ["可选值1", "可选值2"],
      "minimum": 最小值（数字类型）,
      "maximum": 最大值（数字类型）,
      "minLength": 最小长度（字符串类型）,
      "maxLength": 最大长度（字符串类型）,
      "pattern": "正则表达式（字符串类型）",
      "items": { "type": "..." }（数组类型）,
      "properties": { ... }（对象类型）
    }
  },
  "required": ["param_name1", "param_name2"]
}
```

### Python实现模板

```python
{
    "type": "object",
    "properties": {
        "param_name": {
            "type": "string",
            "description": "参数描述",
            "default": "默认值"
        }
    },
    "required": ["param_name"]
}
```

---

## 🔤 参数类型规范

### 1. 字符串类型 (string)

```python
{
    "type": "string",
    "description": "参数描述",
    "default": "默认值",
    "minLength": 1,
    "maxLength": 100,
    "pattern": "^[a-z0-9_]+$"  # 可选：正则表达式
}
```

**使用场景**:
- 文本输入
- ID标识符
- 文件路径
- 查询字符串

### 2. 数字类型 (number/integer)

```python
{
    "type": "integer",  # 或 "number"
    "description": "参数描述",
    "default": 10,
    "minimum": 0,
    "maximum": 100
}
```

**使用场景**:
- 数量、计数
- 索引、偏移量
- 阈值、限制值

### 3. 布尔类型 (boolean)

```python
{
    "type": "boolean",
    "description": "参数描述",
    "default": False
}
```

**使用场景**:
- 开关标志
- 选项启用/禁用

### 4. 对象类型 (object)

```python
{
    "type": "object",
    "description": "参数描述",
    "properties": {
        "nested_param": {
            "type": "string",
            "description": "嵌套参数描述"
        }
    },
    "required": ["nested_param"]
}
```

**使用场景**:
- 复杂配置对象
- 嵌套参数结构

### 5. 数组类型 (array)

```python
{
    "type": "array",
    "description": "参数描述",
    "items": {
        "type": "string"  # 数组元素类型
    },
    "minItems": 1,
    "maxItems": 100
}
```

**使用场景**:
- 列表、集合
- 多选值

### 6. 枚举类型 (enum)

```python
{
    "type": "string",
    "enum": ["value1", "value2", "value3"],
    "description": "参数描述",
    "default": "value1"
}
```

**使用场景**:
- 固定选项列表
- 状态值
- 类型标识

---

## ✅ 参数验证规则

### 必填参数 (required)

```python
{
    "type": "object",
    "properties": {
        "required_param": {
            "type": "string",
            "description": "必填参数"
        },
        "optional_param": {
            "type": "string",
            "description": "可选参数"
        }
    },
    "required": ["required_param"]  # 必填参数列表
}
```

### 默认值 (default)

```python
{
    "type": "string",
    "description": "参数描述",
    "default": "默认值"  # 未提供时使用默认值
}
```

### 取值范围 (minimum/maximum)

```python
{
    "type": "integer",
    "description": "参数描述",
    "minimum": 0,      # 最小值
    "maximum": 100,     # 最大值
    "default": 10
}
```

### 字符串长度限制 (minLength/maxLength)

```python
{
    "type": "string",
    "description": "参数描述",
    "minLength": 1,     # 最小长度
    "maxLength": 100,   # 最大长度
    "default": ""
}
```

### 正则表达式验证 (pattern)

```python
{
    "type": "string",
    "description": "参数描述",
    "pattern": "^[a-z0-9_]+$",  # 正则表达式
    "default": ""
}
```

---

## 📚 标准参数定义

### 通用参数

#### trace_id

```python
{
    "type": "string",
    "description": "追踪ID，用于关联调用链",
    "pattern": "^[a-f0-9-]{36}$"  # UUID格式
}
```

#### limit / offset

```python
{
    "type": "integer",
    "description": "返回结果数量限制",
    "minimum": 1,
    "maximum": 1000,
    "default": 100
}

{
    "type": "integer",
    "description": "结果偏移量，用于分页",
    "minimum": 0,
    "default": 0
}
```

#### scope

```python
{
    "type": "string",
    "enum": ["manual", "engineering", "both"],
    "description": "查询范围",
    "default": "both"
}
```

---

## 📖 完整示例

### 示例1: 知识库查询工具

```python
{
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "查询文本",
            "minLength": 1,
            "maxLength": 500
        },
        "scope": {
            "type": "string",
            "enum": ["manual", "engineering", "both"],
            "default": "both",
            "description": "查询范围"
        },
        "top_k": {
            "type": "integer",
            "description": "返回结果数量",
            "minimum": 1,
            "maximum": 100,
            "default": 10
        },
        "use_reranker": {
            "type": "boolean",
            "description": "是否使用reranker重新排序",
            "default": False
        },
        "trace_id": {
            "type": "string",
            "description": "追踪ID",
            "pattern": "^[a-f0-9-]{36}$"
        }
    },
    "required": ["query"]
}
```

### 示例2: 数据查询工具

```python
{
    "type": "object",
    "properties": {
        "data_source": {
            "type": "string",
            "enum": ["jqdata", "akshare", "tushare"],
            "description": "数据源名称"
        },
        "data_type": {
            "type": "string",
            "enum": ["stock_data", "factor_data", "financial_data", "macro_data"],
            "description": "数据类型"
        },
        "params": {
            "type": "object",
            "description": "查询参数（根据数据源和数据类型而定）"
        },
        "trace_id": {
            "type": "string",
            "description": "追踪ID",
            "pattern": "^[a-f0-9-]{36}$"
        }
    },
    "required": ["data_source", "data_type"]
}
```

---

## 🔧 参数验证实现

### Python验证函数

```python
import jsonschema
from typing import Dict, Any

def validate_parameters(schema: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证参数是否符合Schema定义
    
    Args:
        schema: JSON Schema定义
        params: 待验证的参数
    
    Returns:
        {"valid": True/False, "errors": [...]}
    """
    try:
        jsonschema.validate(instance=params, schema=schema)
        return {"valid": True, "errors": []}
    except jsonschema.ValidationError as e:
        return {"valid": False, "errors": [str(e)]}
```

---

## 📖 相关文档

- [MCP工具命名规范](./MCP_NAMING_CONVENTIONS.md)
- [MCP工具调用流程规范](./CURSOR_MCP_CALL_FLOW.md)
- [MCP错误码体系](./ERROR_CODE_SYSTEM.md)

---

**最后更新**: 2025-12-14
