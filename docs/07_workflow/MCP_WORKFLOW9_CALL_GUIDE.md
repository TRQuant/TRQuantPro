# 9步工作流MCP服务器调用指南

> 创建时间: 2025-12-22  
> 说明: workflow_9steps_server的正确调用方式

---

## 📋 当前状态

### ✅ 已配置的MCP服务器

在 `~/.cursor/mcp.json` 中已配置：

```json
{
  "mcpServers": {
    "trquant-workflow": {
      "command": "/home/taotao/dev/QuantTest/TRQuant/venv/bin/python",
      "args": [
        "/home/taotao/dev/QuantTest/TRQuant/mcp_servers/workflow_9steps_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant"
      },
      "description": "📊 9步投资工作流"
    }
  }
}
```

### 🔧 可用的工具

服务器提供以下9个工具：

1. `workflow9.get_steps` - 获取9步工作流的所有步骤定义
2. `workflow9.create` - 创建新的9步工作流会话
3. `workflow9.status` - 获取工作流状态
4. `workflow9.run_step` - 执行指定步骤
5. `workflow9.run_all` - 一键执行所有9个步骤
6. `workflow9.get_context` - 获取工作流上下文
7. `workflow9.list` - 列出所有保存的工作流
8. `workflow9.restore` - 从存储恢复工作流
9. `workflow9.delete` - 删除保存的工作流

---

## 🎯 调用方式

### 方式1: 通过Cursor MCP直接调用（推荐）

**在Cursor中直接使用MCP工具**：

```
请调用 workflow9.get_steps 获取工作流步骤
请调用 workflow9.create 创建新工作流
请调用 workflow9.run_step 执行步骤1
```

**优点**：
- ✅ 标准化MCP协议
- ✅ 进程隔离
- ✅ 自动重连
- ✅ 错误处理完善

### 方式2: 通过bridge.py调用（当前实现）

**在TypeScript扩展中**：

```typescript
// extension/src/views/unifiedDashboard.ts
const result = await this._callMCP('workflow9.run_step', {
  workflow_id: this._workflowId,
  step_id: 'data_source',
  args: {}
});
```

**在Python中**：

```python
# extension/python/bridge.py
from bridge import call_mcp_tool

result = call_mcp_tool({
    'tool_name': 'workflow9.run_step',
    'arguments': {
        'workflow_id': 'wf_123',
        'step_id': 'data_source',
        'args': {}
    }
})
```

**调用链**：
```
TypeScript → bridge.py → call_workflow9_tool() → workflow_9steps_server._handle_tool()
```

**优点**：
- ✅ 直接函数调用，速度快
- ✅ 错误处理简单
- ✅ 适合工作流内部调用

### 方式3: 通过MCPClient调用

**在Python代码中**：

```python
from core.mcp.client import MCPClient
from pathlib import Path

client = MCPClient(project_root=Path('/home/taotao/dev/QuantTest/TRQuant'))
result = client.call('workflow9.run_step', {
    'workflow_id': 'wf_123',
    'step_id': 'data_source',
    'args': {}
})
```

**注意**：`MCPClient._call_mcp_server` 会检测到 `workflow9.*` 工具，使用 `_call_workflow9_direct` 直接调用，而不是通过subprocess。

---

## 🔍 为什么"看不到"？

### 问题1: Cursor MCP工具列表中没有显示

**原因**：
- Cursor需要重启才能加载新的MCP服务器
- MCP服务器启动失败
- 工具名称格式问题

**解决**：
1. 完全关闭Cursor
2. 重新打开Cursor
3. 检查MCP服务器状态（Cursor设置 → MCP Servers）
4. 查看Cursor日志

### 问题2: 不知道如何调用

**在Cursor中**：
- 直接说："请调用 workflow9.get_steps"
- 或者："请使用9步工作流工具创建新工作流"

**在代码中**：
- 使用 `bridge.py` 的 `call_workflow9_tool`（当前实现）
- 或使用 `MCPClient.call`（标准化调用）

---

## 📊 调用流程图

```
┌─────────────────────────────────────────────────────────┐
│                   调用方式对比                           │
└─────────────────────────────────────────────────────────┘

方式1: Cursor MCP直接调用
  Cursor AI → MCP协议 → workflow_9steps_server.py (stdio)
  ✅ 标准化，进程隔离
  ❌ 需要Cursor重启

方式2: bridge.py调用（当前）
  TypeScript → bridge.py → call_workflow9_tool() → _handle_tool()
  ✅ 快速，直接调用
  ✅ 当前实现方式

方式3: MCPClient调用
  Python代码 → MCPClient.call() → _call_workflow9_direct() → _handle_tool()
  ✅ 标准化接口
  ✅ 自动回退到直接调用
```

---

## 🛠️ 验证配置

### 1. 检查MCP服务器是否运行

```bash
cd /home/taotao/dev/QuantTest/TRQuant
./venv/bin/python mcp_servers/workflow_9steps_server.py
```

应该看到服务器启动，等待stdio输入。

### 2. 测试工具列表

```bash
cd /home/taotao/dev/QuantTest/TRQuant
./venv/bin/python -c "
import sys
sys.path.insert(0, 'mcp_servers')
from workflow_9steps_server import TOOLS
print(f'工具数量: {len(TOOLS)}')
for tool in TOOLS:
    print(f'  - {tool.name}: {tool.description}')
"
```

### 3. 测试直接调用

```bash
cd /home/taotao/dev/QuantTest/TRQuant
./venv/bin/python -c "
import sys
import asyncio
sys.path.insert(0, 'mcp_servers')
from workflow_9steps_server import _handle_tool

async def test():
    result = await _handle_tool('workflow9.get_steps', {})
    print(result)

asyncio.run(test())
"
```

---

## ⚠️ 常见问题

### Q1: 为什么bridge.py中直接调用而不是通过MCP？

**A**: 
- 工作流服务器内部调用，直接函数调用更快
- 避免subprocess开销
- 错误处理更简单
- 这是"混合方案"的设计

### Q2: 如何让Cursor看到workflow9工具？

**A**:
1. 确保 `~/.cursor/mcp.json` 中有 `trquant-workflow` 配置
2. 完全重启Cursor
3. 在Cursor中尝试："请列出所有MCP工具"
4. 检查Cursor日志

### Q3: 两种调用方式有什么区别？

**A**:
- **bridge.py调用**: 直接函数调用，快速，适合内部使用
- **MCP协议调用**: 标准化，进程隔离，适合外部调用

---

## 📝 总结

1. **workflow_9steps_server已配置**在Cursor MCP中（`trquant-workflow`）
2. **当前实现**：通过 `bridge.py` 的 `call_workflow9_tool` 直接调用
3. **也可以**：通过Cursor MCP直接调用（需要重启Cursor）
4. **推荐**：保持当前实现（bridge.py调用），快速可靠

---

*创建时间: 2025-12-22*




























































