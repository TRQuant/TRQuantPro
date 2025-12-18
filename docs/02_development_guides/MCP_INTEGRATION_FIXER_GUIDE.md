# MCP服务器集成常见错误修复规范

> **创建时间**: 2025-12-14  
> **目的**: 规范化MCP服务器集成过程，防止常见错误

## 📋 常见错误类型

### 1. 转义字符问题
**错误示例**:
```python
raise NotImplementedError(\"mcp_integration_helper未安装\")
```

**正确写法**:
```python
raise NotImplementedError("mcp_integration_helper未安装")
```

**修复方法**: 使用 `lint.fix_mcp_integration` 工具自动修复

### 2. 缩进错误（try-except结构）
**错误示例**:
```python
try:
from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call
```

**正确写法**:
```python
try:
    from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call
```

**修复方法**: 使用 `lint.fix_mcp_integration` 工具自动修复

### 3. 多余的括号/符号
**错误示例**:
```python
else:
    raise ValueError(f"未知工具: {name}")
]
except ValueError as e:
```

**正确写法**:
```python
else:
    raise ValueError(f"未知工具: {name}")

except ValueError as e:
```

**修复方法**: 使用 `lint.fix_mcp_integration` 工具自动修复

### 4. 导入语句缩进错误
**错误示例**:
```python
try:
    from mcp.server import Server
from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call
```

**正确写法**:
```python
try:
    from mcp.server import Server
    from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call
```

**修复方法**: 使用 `lint.fix_mcp_integration` 工具自动修复

### 5. 适配函数缺失
**问题**: 使用 `process_mcp_tool_call` 但缺少 `_adapt_mcp_result_to_text_content` 适配函数

**修复方法**: 使用 `lint.fix_mcp_integration` 工具自动添加

## 🛠️ 使用方法

### 通过MCP工具调用
```python
# 调用lint.fix_mcp_integration工具
result = await lint_server.call_tool("lint.fix_mcp_integration", {
    "file_path": "mcp_servers/your_server.py"
})
```

### 直接使用脚本
```bash
python mcp_servers/utils/mcp_integration_fixer.py mcp_servers/your_server.py
```

## 📝 集成规范

### 1. 导入规范
- 所有导入应该在try块内，有正确的缩进
- 使用绝对导入：`from mcp_servers.utils.xxx import yyy`
- 如果导入失败，提供fallback机制

### 2. 缩进规范
- try-except块内的代码应该有4个空格缩进
- 嵌套的try-except应该有正确的相对缩进
- 使用空格，不使用制表符

### 3. 适配函数规范
- 如果使用官方SDK模式（返回List[TextContent]），必须提供适配函数
- 适配函数应该在 `@server.call_tool()` 之前定义
- 适配函数应该处理所有可能的返回格式

### 4. 错误处理规范
- 使用统一的错误处理机制
- 使用 `process_mcp_tool_call` 统一处理
- 错误信息应该清晰明确

## ✅ 检查清单

在集成MCP服务器后，检查以下项目：

- [ ] 语法检查通过（`python -m py_compile`）
- [ ] 导入语句缩进正确
- [ ] try-except结构缩进正确
- [ ] 没有转义字符问题
- [ ] 没有多余的括号/符号
- [ ] 适配函数已添加（如需要）
- [ ] 使用 `lint.fix_mcp_integration` 工具验证

## 🔄 自动化流程

1. **集成前**: 使用 `lint.fix_mcp_integration` 检查现有问题
2. **集成中**: 遵循规范，避免常见错误
3. **集成后**: 使用 `lint.fix_mcp_integration` 自动修复
4. **验证**: 使用 `python -m py_compile` 验证语法

## 📚 相关工具

- `mcp_servers/utils/mcp_integration_fixer.py` - 修复工具实现
- `mcp_servers/lint_server.py` - MCP工具接口
- `lint.fix_mcp_integration` - MCP工具调用
