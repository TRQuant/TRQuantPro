# LLM集成架构分析

> **分析时间**: 2025-12-15
> **问题**: GUI如何调用Cursor的LLM？

## 🔍 当前架构分析

### 1. 桌面GUI (PyQt6)
- **位置**: `gui/main_window_v2.py`
- **环境**: 独立Python进程
- **能力**: ❌ 无法直接调用Cursor LLM
- **原因**: 不在Cursor环境中运行

### 2. MCP客户端 (core/mcp/client.py)
- **位置**: `core/mcp/client.py`
- **功能**: 调用MCP服务器工具
- **能力**: ⚠️ 可以调用MCP工具，但需要LLM MCP服务器
- **限制**: 当前只调用业务MCP服务器（backtest/factor等）

### 3. Cursor扩展件 (extension/)
- **位置**: `extension/src/`
- **环境**: Cursor/VSCode扩展环境
- **能力**: ✅ 可以直接调用Cursor LLM
- **原因**: 在Cursor环境中运行，可以访问Cursor的AI API

## 🎯 三种解决方案

### 方案1: MCP服务器桥接 ⭐ (推荐)

**原理**: 创建一个LLM MCP服务器，GUI通过MCP客户端调用

**架构**:
```
桌面GUI → MCP客户端 → LLM MCP服务器 → Cursor LLM API
```

**优点**:
- ✅ 统一接口（MCP协议）
- ✅ 与现有架构一致
- ✅ 可以独立运行（不依赖Cursor扩展）

**缺点**:
- ⚠️ 需要配置Cursor MCP连接
- ⚠️ 需要开发LLM MCP服务器

**实现**:
```python
# mcp_servers/llm_server.py
# 通过Cursor MCP协议调用LLM
```

---

### 方案2: Cursor扩展件桥接

**原理**: GUI通过扩展件间接调用LLM

**架构**:
```
桌面GUI → HTTP/WebSocket → Cursor扩展件 → Cursor LLM API
```

**优点**:
- ✅ 直接利用Cursor环境
- ✅ 无需额外配置

**缺点**:
- ❌ 必须运行Cursor
- ❌ 需要开发通信协议
- ❌ 架构复杂

---

### 方案3: 直接API集成

**原理**: GUI直接调用OpenAI/Anthropic API

**架构**:
```
桌面GUI → OpenAI/Anthropic API
```

**优点**:
- ✅ 完全独立
- ✅ 不依赖Cursor

**缺点**:
- ❌ 需要API密钥
- ❌ 产生费用
- ❌ 无法使用Cursor的免费额度

---

## 💡 推荐方案：MCP服务器桥接

### 实现步骤

1. **创建LLM MCP服务器**
   ```python
   # mcp_servers/llm_server.py
   # 提供工具：
   # - llm.chat: 对话
   # - llm.analyze: 分析
   # - llm.generate: 生成代码
   ```

2. **配置Cursor MCP**
   ```json
   // .cursor/mcp.json
   {
     "mcpServers": {
       "trquant-llm": {
         "command": "python",
         "args": ["-m", "mcp_servers.llm_server"]
       }
     }
   }
   ```

3. **GUI调用**
   ```python
   from core.mcp import get_mcp_client
   
   client = get_mcp_client()
   result = client.call("llm.chat", {
       "prompt": "分析这个策略...",
       "context": "..."
   })
   ```

---

## 📋 开发计划

### 阶段1: LLM MCP服务器 (1-2天)
- [ ] 创建 `mcp_servers/llm_server.py`
- [ ] 实现 `llm.chat` 工具
- [ ] 实现 `llm.analyze` 工具
- [ ] 实现 `llm.generate` 工具
- [ ] 配置Cursor MCP连接

### 阶段2: GUI集成 (1天)
- [ ] 在GUI中添加LLM调用入口
- [ ] 创建AI助手面板
- [ ] 集成到策略分析流程

### 阶段3: 功能增强 (可选)
- [ ] 对话历史管理
- [ ] 上下文缓存
- [ ] 多模型支持

---

## 🔧 技术细节

### LLM MCP服务器接口

```python
# mcp_servers/llm_server.py
tools = [
    {
        "name": "llm.chat",
        "description": "与LLM对话",
        "parameters": {
            "prompt": "用户提示",
            "context": "上下文信息",
            "model": "模型选择（可选）"
        }
    },
    {
        "name": "llm.analyze",
        "description": "分析策略/数据",
        "parameters": {
            "content": "要分析的内容",
            "analysis_type": "分析类型"
        }
    },
    {
        "name": "llm.generate",
        "description": "生成代码/策略",
        "parameters": {
            "task": "任务描述",
            "template": "模板类型"
        }
    }
]
```

### GUI调用示例

```python
# gui/widgets/ai_assistant_panel.py
class AIAssistantPanel(QWidget):
    def ask_ai(self, question: str):
        client = get_mcp_client()
        result = client.call("llm.chat", {
            "prompt": question,
            "context": self.get_context()
        })
        return result.data
```

---

## ✅ 结论

**推荐方案**: MCP服务器桥接

**理由**:
1. 架构统一，符合现有设计
2. 可以独立运行，不强制依赖Cursor
3. 易于扩展和维护
4. 可以复用Cursor的免费LLM额度

**下一步**: 开发LLM MCP服务器
