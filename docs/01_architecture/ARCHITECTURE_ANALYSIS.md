# 9步工作流架构分析与问题诊断

> 创建时间: 2025-12-22  
> 目标: 分析当前架构，找出问题根源，提出解决方案

---

## 📊 当前架构分析

### 调用链路

```
┌─────────────────────────────────────────────────────────────┐
│                   当前调用链路                               │
└─────────────────────────────────────────────────────────────┘

TypeScript扩展 (unifiedDashboard.ts)
    ↓ spawn(bridge.py)
Python Bridge (extension/python/bridge.py)
    ↓ call_workflow9_tool()
    ↓ 直接导入 workflow_9steps_server._handle_tool
    ↓ asyncio.run_until_complete()
workflow_9steps_server.py
    ↓ _handle_tool()
    ↓ execute_step_data_source()
    ↓ 直接调用 data_source_server_v2._handle_health_check
数据源检查完成
```

### 架构特点

1. **直接函数调用**：不通过MCP协议，直接导入Python模块
2. **异步函数处理**：使用 `asyncio.run_until_complete()` 在同步上下文中运行异步函数
3. **subprocess通信**：TypeScript通过spawn启动Python进程，通过stdin/stdout通信

---

## 🔍 潜在问题分析

### 问题1: 事件循环管理

**代码位置**: `extension/python/bridge.py:262-274`

```python
try:
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

result = loop.run_until_complete(_handle_tool(tool_name, arguments))
```

**潜在问题**：
- 在subprocess中，可能没有事件循环
- `get_event_loop()` 在Python 3.10+中已弃用
- 多个调用可能共享同一个事件循环，导致冲突

**参考方案**（FastMCP）：
```python
# FastMCP使用asyncio.run()，自动管理事件循环
if __name__ == "__main__":
    mcp.run()  # 内部使用asyncio.run()
```

### 问题2: 错误传播

**代码位置**: `extension/python/bridge.py:284-293`

```python
except Exception as e:
    error_msg = f'Workflow9工具调用失败: {str(e)}'
    logger.error(f'{error_msg}\n{traceback.format_exc()}')
    return {
        'ok': False, 
        'error': error_msg,
        'traceback': traceback.format_exc(),
        'hint': '请检查：1) workflow_9steps_server 模块是否可用 2) 依赖是否安装完整'
    }
```

**潜在问题**：
- 错误信息可能没有正确传递到TypeScript
- traceback可能包含敏感信息
- 错误格式不统一

### 问题3: 超时处理

**代码位置**: `extension/src/views/unifiedDashboard.ts:152-160`

```typescript
const timeout = setTimeout(() => {
    proc.kill();
    resolve({ 
        ok: false, 
        data: null, 
        error: '调用超时(30秒)',
        details: `stdout: ${stdout.substring(0, 500)}\nstderr: ${stderr.substring(0, 500)}`
    });
}, 30000);
```

**潜在问题**：
- 30秒可能不够（数据源检查可能需要更长时间）
- 强制kill可能导致资源泄漏
- 没有区分不同类型的超时

### 问题4: 环境变量和路径

**代码位置**: `extension/src/views/unifiedDashboard.ts:126-142`

```typescript
const pythonPaths = [
    projectRoot,
    path.join(projectRoot, 'mcp_servers'),
    path.join(projectRoot, 'extension', 'python')
].filter(p => fs.existsSync(p));

const proc = spawn(pythonPath, [bridgePath], {
    cwd: projectRoot,
    env: {
        ...process.env,
        PYTHONPATH: pythonPathStr,
        TRQUANT_ROOT: projectRoot,
        PYTHONIOENCODING: 'utf-8'
    },
    stdio: ['pipe', 'pipe', 'pipe']
});
```

**潜在问题**：
- PYTHONPATH可能不正确
- 没有使用venv的Python（可能使用系统Python）
- 环境变量可能被覆盖

---

## 🎯 参考架构（FastMCP）

### FastMCP的架构

```python
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")

@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()  # 自动处理stdio通信和事件循环
```

**优点**：
- ✅ 自动管理事件循环
- ✅ 标准化MCP协议
- ✅ 错误处理完善
- ✅ 支持类型验证

### 标准MCP服务器模式

```python
from mcp.server import Server
import mcp.server.stdio

server = Server("my-server")

@server.call_tool()
async def call_tool(name: str, arguments: Dict) -> List[TextContent]:
    # 处理工具调用
    return [TextContent(type="text", text=json.dumps(result))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, ...)

if __name__ == "__main__":
    asyncio.run(main())
```

**优点**：
- ✅ 标准化协议
- ✅ 进程隔离
- ✅ 自动重连
- ✅ 错误处理完善

---

## 🔧 问题诊断清单

### 1. 检查事件循环

```bash
# 测试事件循环管理
cd /home/taotao/dev/QuantTest/TRQuant
./venv/bin/python -c "
import sys
import asyncio
sys.path.insert(0, 'mcp_servers')
from workflow_9steps_server import _handle_tool

# 测试不同的事件循环创建方式
try:
    # 方式1: 使用asyncio.run()（推荐）
    result = asyncio.run(_handle_tool('workflow9.get_steps', {}))
    print('✅ asyncio.run() 成功')
except Exception as e:
    print(f'❌ asyncio.run() 失败: {e}')

try:
    # 方式2: 手动管理事件循环（当前方式）
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(_handle_tool('workflow9.get_steps', {}))
    loop.close()
    print('✅ 手动管理事件循环成功')
except Exception as e:
    print(f'❌ 手动管理事件循环失败: {e}')
"
```

### 2. 检查错误传播

```bash
# 测试错误处理
cd /home/taotao/dev/QuantTest/TRQuant
./venv/bin/python extension/python/bridge.py <<EOF
{"action": "call_mcp_tool", "params": {"tool_name": "workflow9.run_step", "arguments": {"workflow_id": "test", "step_id": "data_source", "args": {}}}}
EOF
```

### 3. 检查环境变量

```bash
# 检查Python路径和环境
cd /home/taotao/dev/QuantTest/TRQuant
./venv/bin/python -c "
import sys
import os
print(f'Python路径: {sys.executable}')
print(f'PYTHONPATH: {os.environ.get(\"PYTHONPATH\", \"未设置\")}')
print(f'TRQUANT_ROOT: {os.environ.get(\"TRQUANT_ROOT\", \"未设置\")}')
print(f'sys.path: {sys.path[:5]}')
"
```

---

## 💡 解决方案建议

### 方案1: 改进事件循环管理（推荐）

**修改 `bridge.py`**：

```python
def call_workflow9_tool(tool_name: str, arguments: dict) -> dict:
    """调用9步工作流工具（改进版）"""
    import traceback
    import asyncio
    
    try:
        # 添加路径
        mcp_servers_path = os.path.join(TRQUANT_ROOT, 'mcp_servers')
        if mcp_servers_path not in sys.path:
            sys.path.insert(0, mcp_servers_path)
        if TRQUANT_ROOT not in sys.path:
            sys.path.insert(0, TRQUANT_ROOT)
        
        # 导入
        from workflow_9steps_server import _handle_tool
        
        # 使用asyncio.run()（Python 3.7+推荐方式）
        # 自动创建和管理事件循环
        result = asyncio.run(_handle_tool(tool_name, arguments))
        
        # 格式化返回
        if isinstance(result, dict):
            if 'success' not in result:
                result['success'] = True
            return {
                'ok': result.get('success', True), 
                'data': result, 
                'error': result.get('error')
            }
        else:
            return {'ok': True, 'data': result}
            
    except Exception as e:
        import traceback
        error_msg = f'Workflow9工具调用失败: {str(e)}'
        logger.error(f'{error_msg}\n{traceback.format_exc()}')
        return {
            'ok': False, 
            'error': error_msg,
            'traceback': traceback.format_exc(),
            'hint': '请检查：1) workflow_9steps_server 模块是否可用 2) 依赖是否安装完整'
        }
```

**优点**：
- ✅ 使用标准 `asyncio.run()`，自动管理事件循环
- ✅ 避免事件循环冲突
- ✅ 代码更简洁

### 方案2: 增加超时和重试机制

**修改 `unifiedDashboard.ts`**：

```typescript
private async _callMCP(
    toolName: string, 
    args: Record<string, any> = {},
    timeout: number = 60000  // 增加到60秒
): Promise<MCPResult> {
    // ... 现有代码 ...
    
    // 增加重试机制
    let retries = 3;
    let lastError: any = null;
    
    for (let i = 0; i < retries; i++) {
        try {
            const result = await this._callMCPOnce(toolName, args, timeout);
            if (result.ok) {
                return result;
            }
            lastError = result;
        } catch (error) {
            lastError = error;
        }
        
        if (i < retries - 1) {
            // 等待后重试
            await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        }
    }
    
    return {
        ok: false,
        data: null,
        error: `调用失败（重试${retries}次）: ${lastError?.error || '未知错误'}`,
        details: lastError?.details
    };
}
```

### 方案3: 改进错误处理

**统一错误格式**：

```python
def format_error_response(error: Exception, context: str = "") -> dict:
    """格式化错误响应"""
    import traceback
    return {
        'ok': False,
        'error': str(error),
        'error_type': type(error).__name__,
        'context': context,
        'traceback': traceback.format_exc(),
        'timestamp': datetime.now().isoformat()
    }
```

---

## 📝 下一步行动

1. **运行诊断脚本**：检查事件循环、环境变量、错误传播
2. **实施方案1**：改进事件循环管理
3. **增加日志**：在关键位置添加详细日志
4. **测试验证**：运行完整的工作流测试

---

*创建时间: 2025-12-22*




























































