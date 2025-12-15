---
title: "10.7 MCP服务器开发指南"
description: "深入解析TRQuant MCP服务器开发，包括MCP协议基础、服务器架构、工具开发、资源管理、提示模板等核心技术，为MCP工具开发提供完整的开发指导"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 🔧 10.7 MCP服务器开发指南

> **核心摘要：**
> 
> 本节系统介绍TRQuant MCP服务器开发，包括MCP协议基础、服务器架构、工具开发、资源管理、提示模板等核心技术。通过理解MCP Server开发的完整方法，帮助开发者掌握MCP工具的开发技巧，为构建专业级的AI工具链奠定基础。

MCP (Model Context Protocol) 是Anthropic开发的开放协议，用于AI助手与外部工具和数据源的安全交互。TRQuant系统通过MCP服务器将核心功能暴露给Cursor AI，实现智能化的开发辅助。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-10-7-1')">
    <h4>📚 10.7.1 MCP协议基础</h4>
    <p>协议概述、核心概念、通信协议、传输方式</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-7-2')">
    <h4>🏗️ 10.7.2 服务器架构</h4>
    <p>服务器分类、架构设计、通信流程、工具注册</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-7-3')">
    <h4>🛠️ 10.7.3 工具开发</h4>
    <p>工具定义、参数验证、错误处理、工具类型</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-7-4')">
    <h4>📦 10.7.4 资源管理</h4>
    <p>资源定义、资源访问、资源类型、资源缓存</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-7-5')">
    <h4>💬 10.7.5 提示模板</h4>
    <p>提示定义、模板变量、模板渲染、提示管理</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-7-6')">
    <h4>🔧 10.7.6 配置与部署</h4>
    <p>Cursor配置、环境变量、依赖管理、调试技巧</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解MCP协议**：掌握MCP协议的核心概念和通信机制
- **设计服务器架构**：理解MCP服务器的架构设计和实现方法
- **开发MCP工具**：掌握工具定义、参数验证、错误处理等开发技巧
- **管理资源**：理解资源定义、访问和管理方法
- **使用提示模板**：掌握提示模板的定义和使用方法
- **配置与部署**：掌握MCP服务器的配置和部署流程

## 📚 核心概念

### MCP协议

- **协议版本**：2024-11-05
- **通信方式**：JSON-RPC 2.0 over stdio/HTTP/SSE
- **核心组件**：Server、Tools、Resources、Prompts

### 服务器类型

- **业务服务器**：提供TRQuant核心功能（市场状态、主线识别、因子推荐等）
- **知识库服务器**：提供知识库检索和查询功能
- **数据收集服务器**：提供数据收集工具（网页爬虫、PDF下载等）

### 工具定义

- **工具名称**：遵循命名规范（如 `trquant_market_status`）
- **输入模式**：JSON Schema定义参数结构
- **返回值**：标准化的JSON格式

<h2 id="section-10-7-1">📚 10.7.1 MCP协议基础</h2>

MCP (Model Context Protocol) 是Anthropic开发的开放协议，用于AI助手与外部工具和数据源的安全交互。

### 协议概述

MCP协议的核心目标：

- **标准化交互**：为AI助手与外部工具提供统一的交互接口
- **安全控制**：通过权限管理确保数据安全
- **可扩展性**：支持自定义工具和资源
- **跨平台**：支持多种编程语言和平台

### 核心概念

#### 服务器（Server）

MCP服务器是一个独立的进程，提供工具和资源：

```python
# MCP服务器基本结构
class MCPServer:
    """MCP服务器基类"""
    
    def __init__(self):
        self.name = "my-server"
        self.version = "1.0.0"
        self.tools = []  # 工具列表
        self.resources = []  # 资源列表
    
    def list_tools(self) -> List[Dict]:
        """列出所有可用工具"""
        return self.tools
    
    async def call_tool(self, name: str, arguments: Dict) -> Dict:
        """调用工具"""
        pass
```

#### 工具（Tools）

工具是服务器提供的可调用功能：

```python
# 工具定义示例
tool = {
    "name": "trquant_market_status",
    "description": "获取A股市场当前状态，包括市场Regime、指数趋势和风格轮动",
    "inputSchema": {
        "type": "object",
        "properties": {
            "universe": {
                "type": "string",
                "description": "市场，默认CN_EQ表示A股",
                "default": "CN_EQ"
            }
        },
        "required": []
    }
}
```

#### 资源（Resources）

资源是服务器提供的可访问数据：

```python
# 资源定义示例
resource = {
    "uri": "file:///path/to/data",
    "name": "数据文件",
    "description": "数据文件资源",
    "mimeType": "text/plain"
}
```

### 通信协议

MCP使用JSON-RPC 2.0协议进行通信：

```json
// 请求格式
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "trquant_market_status",
        "arguments": {
            "universe": "CN_EQ"
        }
    }
}

// 响应格式
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "content": [
            {
                "type": "text",
                "text": "{\"regime\": \"neutral\", \"index_trend\": {...}}"
            }
        ]
    }
}
```

### 传输方式

MCP支持多种传输方式：

1. **stdio**：标准输入输出（最常用，TRQuant使用此方式）
2. **HTTP**：HTTP请求/响应
3. **SSE**：Server-Sent Events

<h2 id="section-10-7-2">🏗️ 10.7.2 服务器架构</h2>

TRQuant系统包含多个MCP服务器，每个服务器负责特定的功能领域。

### 服务器分类

```
mcp_servers/
├── kb_server.py              # 知识库服务器
├── data_collector_server.py  # 数据收集服务器
└── extension/python/
    └── mcp_server.py         # TRQuant业务服务器
```

### 业务服务器架构

```python
# extension/python/mcp_server.py
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class MCPTool:
    """MCP工具定义"""
    name: str
    description: str
    input_schema: dict

class MCPServer:
    """MCP Server实现"""
    
    def __init__(self):
        self.orchestrator = get_workflow_orchestrator() if TRQUANT_AVAILABLE else None
        logger.info(f"MCP Server初始化, TRQuant可用: {TRQUANT_AVAILABLE}")
    
    def list_tools(self) -> List[dict]:
        """列出所有可用工具"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in MCP_TOOLS
        ]
    
    async def call_tool(self, name: str, arguments: dict) -> dict:
        """调用工具"""
        logger.info(f"调用工具: {name}")
        
        handlers = {
            "trquant_market_status": self._get_market_status,
            "trquant_mainlines": self._get_mainlines,
            "trquant_recommend_factors": self._recommend_factors,
            "trquant_generate_strategy": self._generate_strategy,
            "trquant_analyze_backtest": self._analyze_backtest
        }
        
        handler = handlers.get(name)
        if not handler:
            return {"error": f"未知工具: {name}"}
        
        try:
            result = await handler(arguments)
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(result, ensure_ascii=False, indent=2)
                }]
            }
        except Exception as e:
            logger.error(f"工具执行失败: {e}")
            return {"error": str(e)}
```

### 知识库服务器架构

```python
# mcp_servers/kb_server.py
class KBMCPServer:
    """知识库MCP服务器"""
    
    def __init__(self):
        # 初始化知识库服务
        self.kb_server = KBServer()
        
        # 加载reranker（可选）
        try:
            self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        except:
            self.reranker = None
    
    async def call_tool(self, name: str, arguments: Dict) -> Dict:
        if name == "kb.query":
            # 1. 参数验证
            query = arguments.get("query")
            if not query:
                return {
                    "isError": True,
                    "content": [{"type": "text", "text": "查询文本不能为空"}]
                }
            
            # 2. 调用底层服务
            results = self.kb_server.query(
                query=query,
                scope=arguments.get("scope", "both"),
                top_k=arguments.get("top_k", 10),
                use_reranker=arguments.get("use_reranker", False)
            )
            
            # 3. 格式化返回
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(results, ensure_ascii=False, indent=2)
                }]
            }
```

### 通信流程

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Cursor    │────────▶│  MCP Server  │────────▶│   Backend   │
│   (Client)  │◀────────│   (stdio)    │◀────────│   Service   │
└─────────────┘         └──────────────┘         └─────────────┘
     │                        │                        │
     │  1. 发送工具调用请求    │                        │
     │───────────────────────▶│                        │
     │                        │  2. 调用后端服务        │
     │                        │───────────────────────▶│
     │                        │  3. 返回结果            │
     │                        │◀───────────────────────│
     │  4. 返回工具调用结果    │                        │
     │◀───────────────────────│                        │
```

<h2 id="section-10-7-3">🛠️ 10.7.3 工具开发</h2>

工具开发是MCP服务器的核心，需要遵循单一职责、参数验证、错误处理等原则。

### 工具定义

```python
# 定义MCP工具
MCP_TOOLS: List[MCPTool] = [
    MCPTool(
        name="trquant_market_status",
        description="获取A股市场当前状态，包括市场Regime（risk_on/risk_off/neutral）、指数趋势和风格轮动",
        input_schema={
            "type": "object",
            "properties": {
                "universe": {
                    "type": "string",
                    "description": "市场，默认CN_EQ表示A股",
                    "default": "CN_EQ"
                }
            },
            "required": []
        }
    ),
    MCPTool(
        name="trquant_mainlines",
        description="获取当前A股市场的投资主线，包括主线名称、评分、相关行业和投资逻辑",
        input_schema={
            "type": "object",
            "properties": {
                "top_n": {
                    "type": "integer",
                    "description": "返回前N条主线，默认10",
                    "default": 10
                },
                "time_horizon": {
                    "type": "string",
                    "enum": ["short", "medium", "long"],
                    "description": "投资周期：short(1-5天)、medium(1-4周)、long(1月+)",
                    "default": "short"
                }
            },
            "required": []
        }
    ),
    MCPTool(
        name="trquant_generate_strategy",
        description="生成PTrade或QMT量化策略代码，支持多因子、动量成长、价值、市场中性四种风格",
        input_schema={
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["ptrade", "qmt"],
                    "description": "目标平台",
                    "default": "ptrade"
                },
                "style": {
                    "type": "string",
                    "enum": ["multi_factor", "momentum_growth", "value", "market_neutral"],
                    "description": "策略风格",
                    "default": "multi_factor"
                },
                "factors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "使用的因子列表"
                },
                "max_position": {
                    "type": "number",
                    "description": "单票最大仓位(0-1)，默认0.1",
                    "default": 0.1
                }
            },
            "required": ["factors"]
        }
    )
]
```

### 工具实现

```python
async def _get_market_status(self, args: dict) -> dict:
    """获取市场状态"""
    if not TRQUANT_AVAILABLE:
        return self._mock_market_status()
    
    try:
        analyzer = TrendAnalyzer()
        result = analyzer.analyze_market()
        return {
            "regime": result.regime.value if hasattr(result.regime, 'value') else str(result.regime),
            "index_trend": result.index_zscore,
            "style_rotation": result.style_rotation,
            "summary": result.summary if hasattr(result, 'summary') else self._generate_summary(result)
        }
    except Exception as e:
        logger.error(f"获取市场状态失败: {e}")
        return self._mock_market_status()

async def _generate_strategy(self, args: dict) -> dict:
    """生成策略代码"""
    from tools.strategy_generator import StrategyGenerator
    
    generator = StrategyGenerator()
    result = generator.generate(
        platform=args.get('platform', 'ptrade'),
        style=args.get('style', 'multi_factor'),
        factors=args.get('factors', ['ROE_ttm', 'momentum_20d']),
        risk_params={
            'max_position': args.get('max_position', 0.1),
            'stop_loss': args.get('stop_loss', 0.08),
            'take_profit': args.get('take_profit', 0.2)
        }
    )
    
    return result
```

### 错误处理

```python
async def call_tool(self, name: str, arguments: dict) -> dict:
    """调用工具"""
    logger.info(f"调用工具: {name}")
    
    handlers = {
        "trquant_market_status": self._get_market_status,
        "trquant_mainlines": self._get_mainlines,
        "trquant_recommend_factors": self._recommend_factors,
        "trquant_generate_strategy": self._generate_strategy,
        "trquant_analyze_backtest": self._analyze_backtest
    }
    
    handler = handlers.get(name)
    if not handler:
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"未知工具: {name}"}]
        }
    
    try:
        # 参数验证
        if not self._validate_arguments(name, arguments):
            return {
                "isError": True,
                "content": [{"type": "text", "text": "参数验证失败"}]
            }
        
        result = await handler(arguments)
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False, indent=2)
            }]
        }
    except ValueError as e:
        logger.error(f"参数错误: {e}")
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"参数错误: {e}"}]
        }
    except Exception as e:
        logger.error(f"工具执行失败: {e}", exc_info=True)
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"执行失败: {e}"}]
        }
```

<h2 id="section-10-7-4">📦 10.7.4 资源管理</h2>

资源是MCP服务器提供的可访问数据，可以是文件、URL、数据库查询结果等。

### 资源定义

```python
# 资源定义示例
resources = [
    {
        "uri": "file:///path/to/data",
        "name": "数据文件",
        "description": "数据文件资源",
        "mimeType": "text/plain"
    },
    {
        "uri": "https://example.com/api/data",
        "name": "API数据",
        "description": "API数据资源",
        "mimeType": "application/json"
    }
]
```

### 资源访问

```python
async def get_resource(self, uri: str) -> dict:
    """获取资源"""
    if uri.startswith("file://"):
        # 文件资源
        file_path = uri.replace("file://", "")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            "content": [{
                "type": "text",
                "text": content
            }]
        }
    elif uri.startswith("https://"):
        # URL资源
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as response:
                content = await response.text()
        return {
            "content": [{
                "type": "text",
                "text": content
            }]
        }
    else:
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"不支持的资源类型: {uri}"}]
        }
```

<h2 id="section-10-7-5">💬 10.7.5 提示模板</h2>

提示模板（Prompts）是MCP服务器提供的预定义提示，用于指导AI助手执行特定任务。

### 提示定义

```python
# 提示定义示例
prompts = [
    {
        "name": "analyze_market",
        "description": "分析市场状态并给出投资建议",
        "arguments": [
            {
                "name": "universe",
                "description": "市场范围",
                "required": False
            }
        ]
    },
    {
        "name": "generate_strategy",
        "description": "生成量化策略代码",
        "arguments": [
            {
                "name": "factors",
                "description": "使用的因子列表",
                "required": True
            },
            {
                "name": "platform",
                "description": "目标平台（ptrade/qmt）",
                "required": False
            }
        ]
    }
]
```

### 提示渲染

```python
async def get_prompt(self, name: str, arguments: dict) -> dict:
    """获取提示"""
    prompt_templates = {
        "analyze_market": """
        请分析当前A股市场状态，包括：
        1. 市场Regime（risk_on/risk_off/neutral）
        2. 指数趋势
        3. 风格轮动
        4. 投资建议
        
        市场范围：{universe}
        """,
        "generate_strategy": """
        请生成量化策略代码，要求：
        1. 使用因子：{factors}
        2. 目标平台：{platform}
        3. 策略风格：{style}
        4. 风险参数：max_position={max_position}, stop_loss={stop_loss}
        """
    }
    
    template = prompt_templates.get(name)
    if not template:
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"未知提示: {name}"}]
        }
    
    # 渲染模板
    prompt = template.format(**arguments)
    
    return {
        "content": [{
            "type": "text",
            "text": prompt
        }]
    }
```

<h2 id="section-10-7-6">🔧 10.7.6 配置与部署</h2>

MCP服务器需要在Cursor中配置才能使用。

### Cursor配置

在 `.cursor/mcp.json` 中添加服务器配置：

```json
{
  "mcpServers": {
    "trquant-business": {
      "command": "python",
      "args": [
        "extension/python/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}/extension:${workspaceFolder}"
      },
      "cwd": "${workspaceFolder}"
    },
    "kb-server": {
      "command": "extension/venv/bin/python",
      "args": [
        "${workspaceFolder}/mcp_servers/kb_server.py"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}/extension:${workspaceFolder}"
      },
      "cwd": "${workspaceFolder}"
    },
    "data-collector": {
      "command": "extension/venv/bin/python",
      "args": [
        "${workspaceFolder}/mcp_servers/data_collector_server.py"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}/extension:${workspaceFolder}"
      },
      "cwd": "${workspaceFolder}"
    }
  }
}
```

### 环境变量

```bash
# .env 或环境变量
PYTHONPATH=/path/to/TRQuant/extension:/path/to/TRQuant
TRQUANT_DATA_DIR=/path/to/data
TRQUANT_KB_DIR=/path/to/kb
```

### 依赖管理

```bash
# 安装MCP相关依赖
pip install langchain langchain-community chromadb rank-bm25 sentence-transformers
```

### 调试技巧

```python
# 启用详细日志
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('MCP')

# 测试工具调用
async def test_tool():
    server = MCPServer()
    result = await server.call_tool(
        "trquant_market_status",
        {"universe": "CN_EQ"}
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 请求处理

```python
async def handle_request(request: dict, server: MCPServer) -> dict:
    """处理MCP请求"""
    method = request.get("method", "")
    params = request.get("params", {})
    req_id = request.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "trquant-mcp",
                    "version": "1.0.0"
                }
            }
        }
    
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": server.list_tools()
            }
        }
    
    elif method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        result = await server.call_tool(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result
        }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"未知方法: {method}"
            }
        }
```

### 主函数

```python
async def main():
    """主函数 - 运行MCP Server"""
    logger.info("TRQuant MCP Server 启动...")
    server = MCPServer()
    
    # 使用stdio通信
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
    
    writer_transport, writer_protocol = await asyncio.get_event_loop().connect_write_pipe(
        asyncio.streams.FlowControlMixin, sys.stdout
    )
    writer = asyncio.StreamWriter(writer_transport, writer_protocol, reader, asyncio.get_event_loop())
    
    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            
            request = json.loads(line.decode('utf-8'))
            response = await handle_request(request, server)
            
            if response:
                response_str = json.dumps(response, ensure_ascii=False) + '\n'
                writer.write(response_str.encode('utf-8'))
                await writer.drain()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
        except Exception as e:
            logger.error(f"处理请求错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔗 相关章节

- **10.9 MCP × Cursor × 工具链联用规范**：了解MCP与Cursor的集成方法
- **10.10 RAG知识库开发指南**：了解知识库服务器的实现细节
- **第7章：策略开发**：了解策略生成工具的使用场景

## 💡 关键要点

1. **协议基础**：MCP使用JSON-RPC 2.0协议，通过stdio进行通信
2. **服务器架构**：每个服务器负责特定功能领域，通过工具暴露功能
3. **工具开发**：遵循单一职责、参数验证、错误处理等原则
4. **资源管理**：支持文件、URL、数据库等多种资源类型
5. **提示模板**：提供预定义提示，指导AI助手执行任务
6. **配置部署**：在Cursor中配置MCP服务器，启用详细日志进行调试

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了MCP服务器开发，包括MCP协议基础、服务器架构、工具开发、资源管理、提示模板、配置与部署等核心技术。通过理解MCP Server开发的完整方法，帮助开发者掌握MCP工具的开发技巧。</p>
  
  <h3>下节预告</h3>
  <p>掌握了MCP服务器开发后，下一节将介绍版本与发布机制，包括版本管理、发布流程、变更日志、依赖管理等。通过理解版本与发布机制，帮助开发者掌握项目的版本管理和发布流程。</p>
  
  <a href="/ashare-book6/010_Chapter10_Development_Guide/10.8_Version_Release_Mechanism_CN" class="next-section">
    继续学习：10.8 版本与发布机制 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
