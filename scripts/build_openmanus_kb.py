#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus代码知识库构建脚本
==========================
将OpenManus的核心代码和架构知识添加到RAG知识库

功能:
1. 分析OpenManus代码结构
2. 提取核心概念和API
3. 构建知识库条目
4. 添加到RAG知识库

作者: TRQuant Team
日期: 2026-01-11
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
OPENMANUS_DIR = PROJECT_ROOT / "third_party" / "OpenManus"
sys.path.insert(0, str(PROJECT_ROOT))


def create_openmanus_kb_items() -> List[Dict[str, Any]]:
    """
    创建OpenManus知识库条目
    
    Returns:
        List[Dict]: 知识库条目列表
    """
    kb_items = []
    
    # 1. OpenManus概述
    kb_items.append({
        "title": "OpenManus - 开源AI Agent框架概述",
        "content": """# OpenManus - 开源AI Agent框架

## 项目概述

OpenManus是一个开源的AI Agent框架，支持多Agent协作、任务分解、执行和验证。

**核心特性**:
- 多Agent协作框架
- 工具调用系统（Tool Calling）
- MCP（Model Context Protocol）支持
- 浏览器自动化
- 代码执行环境
- 文件操作

**项目来源**: MetaGPT团队
**开源协议**: MIT License

## 架构设计

OpenManus采用模块化设计：

1. **Agent层** (`app/agent/`)
   - Manus: 通用Agent
   - BrowserAgent: 浏览器专用Agent
   - MCPAgent: MCP服务器Agent
   - SandboxManus: 沙箱环境Agent
   - DataAnalysisAgent: 数据分析Agent
   - SWEAgent: 软件工程Agent

2. **工具层** (`app/tool/`)
   - BrowserUseTool: 浏览器自动化
   - PythonExecute: Python代码执行
   - StrReplaceEditor: 代码编辑器
   - Bash: Shell命令执行
   - MCP工具: MCP客户端工具
   - Search工具: 网络搜索

3. **MCP层** (`app/mcp/`)
   - MCPServer: MCP服务器实现
   - 工具注册和管理
   - stdio/SSE传输支持

4. **流程层** (`app/flow/`)
   - FlowFactory: 工作流工厂
   - PlanningFlow: 规划流程
   - 多Agent协作流程

## 在TRQuant中的应用

OpenManus已集成到TRQuant系统，用于：
- 浏览器自动化（财经网站数据抓取）
- 数据收集（新闻、公告）
- 工作流增强（R0数据源检测、R1市场趋势分析）

**集成位置**:
- Core模块: `core/automation/`, `core/data_collection/`
- 工作流集成: `core/workflow/openmanus_integration.py`
- MCP服务器: `~/.cursor/mcp.json` (openmanus配置)
""",
        "type": "lesson",
        "tags": ["OpenManus", "AI Agent", "框架", "架构", "TRQuant集成"],
        "source": "third_party/OpenManus/README.md"
    })
    
    # 2. Manus Agent
    kb_items.append({
        "title": "OpenManus - Manus Agent核心类",
        "content": """# Manus Agent - 通用AI Agent

## 类定义

```python
from app.agent.manus import Manus
from app.agent.toolcall import ToolCallAgent

class Manus(ToolCallAgent):
    \"\"\"通用AI Agent，支持本地和MCP工具\"\"\"
    
    name: str = "Manus"
    description: str = "支持多种工具的通用Agent"
    
    # MCP客户端
    mcp_clients: MCPClients = Field(default_factory=MCPClients)
    
    # 可用工具
    available_tools: ToolCollection = Field(
        default_factory=lambda: ToolCollection(
            PythonExecute(),
            BrowserUseTool(),
            StrReplaceEditor(),
            AskHuman(),
            Terminate(),
        )
    )
```

## 核心功能

1. **工具调用**
   - 支持本地工具（PythonExecute, BrowserUseTool等）
   - 支持MCP工具（通过MCPClients）

2. **MCP服务器管理**
   - `connect_mcp_server()`: 连接MCP服务器
   - `disconnect_mcp_server()`: 断开MCP服务器
   - `initialize_mcp_servers()`: 初始化配置的MCP服务器

3. **浏览器上下文管理**
   - BrowserContextHelper: 浏览器上下文助手
   - 自动管理浏览器生命周期

## 使用示例

```python
from app.agent.manus import Manus

# 创建Agent
agent = await Manus.create()

# 执行任务
result = await agent.run("访问网站并提取内容")

# 清理资源
await agent.cleanup()
```

## 在TRQuant中的使用

TRQuant封装了Manus Agent为 `core.automation.OpenManusAgent`，提供统一的API接口。
""",
        "type": "reference",
        "tags": ["OpenManus", "Manus", "Agent", "ToolCallAgent", "API"],
        "source": "third_party/OpenManus/app/agent/manus.py"
    })
    
    # 3. BrowserUseTool
    kb_items.append({
        "title": "OpenManus - BrowserUseTool浏览器自动化工具",
        "content": """# BrowserUseTool - 浏览器自动化工具

## 类定义

```python
from app.tool.browser_use_tool import BrowserUseTool
from app.tool.base import BaseTool

class BrowserUseTool(BaseTool):
    \"\"\"浏览器自动化工具，基于Playwright\"\"\"
    
    name: str = "browser"
    description: str = "浏览器自动化工具"
```

## 支持的操作

1. **go_to_url** - 访问网页
   - 参数: `url` (str)
   - 功能: 导航到指定URL

2. **click_element** - 点击元素
   - 参数: `index` (int)
   - 功能: 点击指定索引的元素

3. **input_text** - 输入文本
   - 参数: `index` (int), `text` (str), `submit` (bool)
   - 功能: 在指定元素输入文本

4. **extract_content** - 提取内容
   - 参数: `goal` (str)
   - 功能: 使用LLM提取页面内容（需要LLM API）

5. **screenshot** - 截图
   - 参数: `filename` (str)
   - 功能: 截取页面截图

6. **scroll_down/scroll_up** - 滚动
7. **wait** - 等待
8. **go_back** - 返回
9. **refresh** - 刷新
10. **switch_tab/open_tab/close_tab** - 标签管理

## 使用示例

```python
from app.tool.browser_use_tool import BrowserUseTool

tool = BrowserUseTool()

# 访问网页
result = await tool.execute(
    action="go_to_url",
    url="https://www.eastmoney.com"
)

# 提取内容（需要LLM API）
result = await tool.execute(
    action="extract_content",
    goal="获取页面标题和主要内容"
)
```

## 在TRQuant中的使用

TRQuant封装为 `core.automation.BrowserAgent`，提供统一的浏览器操作API。
""",
        "type": "reference",
        "tags": ["OpenManus", "BrowserUseTool", "浏览器", "Playwright", "自动化"],
        "source": "third_party/OpenManus/app/tool/browser_use_tool.py"
    })
    
    # 4. MCP Server
    kb_items.append({
        "title": "OpenManus - MCP服务器实现",
        "content": """# OpenManus MCP服务器实现

## MCPServer类

```python
from app.mcp.server import MCPServer
from mcp.server.fastmcp import FastMCP

class MCPServer:
    \"\"\"MCP服务器实现，工具注册和管理\"\"\"
    
    def __init__(self, name: str = "openmanus"):
        self.server = FastMCP(name)
        self.tools: Dict[str, BaseTool] = {}
        
        # 初始化标准工具
        self.tools["bash"] = Bash()
        self.tools["browser"] = BrowserUseTool()
        self.tools["editor"] = StrReplaceEditor()
        self.tools["terminate"] = Terminate()
```

## 注册的工具

1. **bash** - Bash命令执行
2. **browser** - 浏览器自动化
3. **editor** - 代码编辑器
4. **terminate** - 终止工具

## 工具注册方法

```python
def register_tool(self, tool: BaseTool, method_name: Optional[str] = None):
    \"\"\"注册工具到MCP服务器\"\"\"
    tool_name = method_name or tool.name
    tool_param = tool.to_param()
    tool_function = tool_param["function"]
    
    # 定义异步函数
    async def tool_method(**kwargs):
        result = await tool.execute(**kwargs)
        # 处理结果...
        return result
    
    # 注册到服务器
    self.server.tool()(tool_method)
```

## MCP配置

在Cursor的 `~/.cursor/mcp.json` 中配置：

```json
{
  "mcpServers": {
    "openmanus": {
      "command": "/path/to/.venv/bin/python",
      "args": ["-m", "app.mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/OpenManus"
      }
    }
  }
}
```

## 在TRQuant中的应用

OpenManus MCP服务器已配置到Cursor，可以通过Cursor Chat直接调用browser、bash、editor工具。
""",
        "type": "reference",
        "tags": ["OpenManus", "MCP", "服务器", "FastMCP", "工具注册"],
        "source": "third_party/OpenManus/app/mcp/server.py"
    })
    
    # 5. Tool Base
    kb_items.append({
        "title": "OpenManus - BaseTool工具基类",
        "content": """# BaseTool - 工具基类

## 类定义

```python
from app.tool.base import BaseTool
from app.schema import ToolResult

class BaseTool:
    \"\"\"所有工具的基类\"\"\"
    
    name: str
    description: str
    
    def to_param(self) -> Dict:
        \"\"\"转换为工具参数格式\"\"\"
        pass
    
    async def execute(self, **kwargs) -> ToolResult:
        \"\"\"执行工具\"\"\"
        pass
```

## 工具实现要求

1. **name属性** - 工具名称
2. **description属性** - 工具描述
3. **to_param()方法** - 转换为参数格式（用于MCP注册）
4. **execute()方法** - 执行工具逻辑（异步）

## 工具参数格式

```python
{
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "工具描述",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "参数描述"
                }
            },
            "required": ["param1"]
        }
    }
}
```

## 工具结果格式

```python
from app.schema import ToolResult

ToolResult(
    output="执行结果",
    error=None,
    metadata={}
)
```

## 实现示例

参考 `BrowserUseTool`, `Bash`, `StrReplaceEditor` 等工具的实现。
""",
        "type": "reference",
        "tags": ["OpenManus", "BaseTool", "工具基类", "API设计"],
        "source": "third_party/OpenManus/app/tool/base.py"
    })
    
    # 6. ToolCallAgent
    kb_items.append({
        "title": "OpenManus - ToolCallAgent工具调用Agent",
        "content": """# ToolCallAgent - 工具调用Agent基类

## 类定义

```python
from app.agent.toolcall import ToolCallAgent
from app.agent.base import BaseAgent

class ToolCallAgent(BaseAgent):
    \"\"\"支持工具调用的Agent基类\"\"\"
    
    available_tools: ToolCollection
    max_steps: int = 20
    max_observe: int = 10000
```

## 核心功能

1. **工具管理**
   - `available_tools`: 可用工具集合
   - 工具选择和调用

2. **思考循环**
   - `think()`: 思考下一步行动
   - `run()`: 执行任务循环
   - `step()`: 执行单步

3. **记忆管理**
   - `memory`: Agent记忆
   - 消息历史
   - 工具调用历史

## Agent工作流程

1. **初始化** - 设置工具、提示词
2. **思考** - 分析当前状态，选择工具
3. **执行** - 调用工具执行任务
4. **观察** - 获取工具执行结果
5. **更新记忆** - 保存执行历史
6. **判断终止** - 检查是否完成任务

## 使用示例

```python
from app.agent.toolcall import ToolCallAgent

class MyAgent(ToolCallAgent):
    available_tools = ToolCollection(
        MyTool1(),
        MyTool2()
    )
    
    system_prompt = "You are a helpful assistant"
    max_steps = 20

agent = MyAgent()
result = await agent.run("执行任务")
```

## 在TRQuant中的应用

TRQuant的 `OpenManusAgent` 基于ToolCallAgent模式设计，但简化了实现，直接调用工具而不使用LLM推理。
""",
        "type": "reference",
        "tags": ["OpenManus", "ToolCallAgent", "Agent基类", "工具调用"],
        "source": "third_party/OpenManus/app/agent/toolcall.py"
    })
    
    # 7. MCP Clients
    kb_items.append({
        "title": "OpenManus - MCP客户端工具集成",
        "content": """# MCPClients - MCP客户端工具集成

## 类定义

```python
from app.tool.mcp import MCPClients, MCPClientTool

class MCPClients:
    \"\"\"MCP客户端集合，管理多个MCP服务器连接\"\"\"
    
    clients: List[MCPClient] = []
    tools: List[MCPClientTool] = []
```

## 核心功能

1. **连接管理**
   - `connect_sse()`: 通过SSE连接MCP服务器
   - `connect_stdio()`: 通过stdio连接MCP服务器
   - `disconnect()`: 断开连接

2. **工具管理**
   - 自动发现MCP服务器的工具
   - 将MCP工具封装为MCPClientTool
   - 提供统一的工具接口

3. **工具调用**
   - 通过MCP协议调用远程工具
   - 处理工具结果

## MCPClientTool

MCP工具封装类，将MCP服务器的工具封装为可调用的工具对象。

## 在Agent中使用

```python
from app.agent.manus import Manus

agent = Manus()

# 连接MCP服务器
await agent.connect_mcp_server(
    server_url="http://localhost:8000",
    server_id="my_server"
)

# MCP工具会自动添加到available_tools
# 可以在think()循环中使用
```

## 在TRQuant中的应用

TRQuant的MCP客户端 (`core.mcp.client.MCPClient`) 独立实现，不直接使用OpenManus的MCPClients，但设计理念相似。
""",
        "type": "reference",
        "tags": ["OpenManus", "MCPClients", "MCP客户端", "工具集成"],
        "source": "third_party/OpenManus/app/tool/mcp.py"
    })
    
    # 8. TRQuant集成
    kb_items.append({
        "title": "OpenManus在TRQuant中的集成方案",
        "content": """# OpenManus在TRQuant中的集成

## 集成架构

TRQuant采用**封装式集成**，而不是直接使用OpenManus的Agent框架。

### 架构设计

```
OpenManus源码 (third_party/OpenManus/)
    ↓ 封装
TRQuant Core模块 (core/automation/)
    ↓ 使用
工作流增强 (core/workflow/openmanus_integration.py)
```

### 核心模块

1. **BrowserAgent** (`core/automation/browser_agent.py`)
   - 封装Playwright浏览器操作
   - 可选集成OpenManus的BrowserUseTool
   - 提供统一的浏览器API

2. **OpenManusAgent** (`core/automation/openmanus_agent.py`)
   - 简化版Agent（不使用LLM推理）
   - 直接工具调用
   - 任务解析和执行

3. **FinancialCollector** (`core/data_collection/financial_collector.py`)
   - 财经数据收集
   - 新闻和公告抓取
   - MongoDB存储

4. **WorkflowEnhancer** (`core/workflow/openmanus_integration.py`)
   - R0数据源检测增强
   - R1市场趋势分析增强（使用MarketTrendAnalyzer）
   - R2主线轮动研究增强

### 性能优化模块

- **RequestCache** - 请求缓存
- **BrowserPool** - 浏览器连接池
- **ParallelExecutor** - 并行执行器
- **PerformanceMonitor** - 性能监控

### MCP服务器配置

OpenManus MCP服务器已配置到Cursor (`~/.cursor/mcp.json`)，提供：
- `browser` - 浏览器工具
- `bash` - Shell命令
- `editor` - 代码编辑器
- `terminate` - 终止工具

### 使用示例

```python
# 使用BrowserAgent
from core.automation import BrowserAgent

async with BrowserAgent() as agent:
    result = await agent.navigate("https://www.eastmoney.com")
    content = await agent.get_content()

# 使用WorkflowEnhancer
from core.workflow import WorkflowEnhancer

async with WorkflowEnhancer() as enhancer:
    r1 = await enhancer.enhance_r1_market_trend(index_code="000300.XSHG")
    print(f"市场趋势: {r1.data['trend_label']}")
```

### 集成原则

1. **不直接使用OpenManus Agent框架**（需要LLM API）
2. **封装工具功能**（浏览器、数据收集）
3. **统一API接口**（与TRQuant架构一致）
4. **性能优化**（缓存、连接池、并行处理）
5. **工作流增强**（R0/R1/R2步骤增强）

### 文档位置

- 集成计划: `docs/research/OPENMANUS_INTEGRATION_PLAN.md`
- 完成报告: `docs/research/OPENMANUS_INTEGRATION_COMPLETE.md`
- 状态文档: `docs/research/OPENMANUS_STATUS.md`
""",
        "type": "lesson",
        "tags": ["OpenManus", "TRQuant", "集成", "架构", "设计"],
        "source": "docs/research/OPENMANUS_INTEGRATION_COMPLETE.md"
    })
    
    # 9. 工具列表
    kb_items.append({
        "title": "OpenManus - 可用工具清单",
        "content": """# OpenManus可用工具清单

## 标准工具

### 浏览器工具 (BrowserUseTool)
- **go_to_url** - 访问网页
- **click_element** - 点击元素
- **input_text** - 输入文本
- **extract_content** - 提取内容（需LLM API）
- **screenshot** - 截图
- **scroll_down/scroll_up** - 滚动
- **wait** - 等待
- **go_back** - 返回
- **refresh** - 刷新
- **switch_tab/open_tab/close_tab** - 标签管理

### 代码执行 (PythonExecute)
- 执行Python代码
- 支持交互式执行
- 结果捕获

### 编辑器 (StrReplaceEditor)
- 文件编辑
- 字符串替换
- 代码修改

### Shell命令 (Bash)
- 执行Shell命令
- 命令输出捕获

### 搜索工具
- **GoogleSearch** - Google搜索
- **BingSearch** - Bing搜索
- **BaiduSearch** - 百度搜索
- **DuckDuckGoSearch** - DuckDuckGo搜索

### 其他工具
- **AskHuman** - 询问用户
- **Terminate** - 终止执行
- **FileOperators** - 文件操作
- **ComputerUseTool** - 计算机使用
- **Crawl4AI** - 网页爬取

## MCP工具

通过MCP服务器提供的工具：
- **browser** - 浏览器自动化
- **bash** - Shell命令
- **editor** - 代码编辑器
- **terminate** - 终止工具

## 在TRQuant中的使用

TRQuant主要使用：
1. **BrowserAgent** - 浏览器自动化（封装BrowserUseTool）
2. **FinancialCollector** - 数据收集（使用BrowserAgent）
3. **MCP工具** - 通过Cursor Chat调用

## 工具选择建议

- **基础操作** - BrowserUseTool, Bash
- **代码编辑** - StrReplaceEditor
- **数据提取** - BrowserUseTool.extract_content（需LLM API）
- **批量操作** - 使用TRQuant的ParallelExecutor
""",
        "type": "reference",
        "tags": ["OpenManus", "工具", "工具清单", "API"],
        "source": "third_party/OpenManus/app/tool/"
    })
    
    # 10. 配置和使用
    kb_items.append({
        "title": "OpenManus - 配置和使用指南",
        "content": """# OpenManus配置和使用指南

## 安装

### 方法1: 使用conda
```bash
conda create -n open_manus python=3.12
conda activate open_manus
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus
pip install -r requirements.txt
```

### 方法2: 使用uv（推荐）
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 浏览器工具（可选）
```bash
playwright install
```

## 配置

### 1. 配置文件

创建 `config/config.toml`:

```toml
# LLM配置
[llm]
model = "claude-3-7-sonnet-20250219"
base_url = "https://api.anthropic.com/v1/"
api_key = "YOUR_API_KEY"
max_tokens = 8192
temperature = 0.0

# MCP配置
[mcp]
server_reference = "app.mcp.server"

# Daytona配置（可选）
[daytona]
daytona_api_key = ""
```

### 2. MCP服务器配置（Cursor）

在 `~/.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "openmanus": {
      "command": "/path/to/OpenManus/.venv/bin/python",
      "args": ["-m", "app.mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/OpenManus",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

## 使用方式

### 1. 作为独立项目使用

```python
from app.agent.manus import Manus

agent = await Manus.create()
result = await agent.run("访问网站并提取内容")
await agent.cleanup()
```

### 2. 作为MCP服务器使用

```bash
python -m app.mcp.server
```

在Cursor Chat中使用：
```
"使用browser工具访问 https://www.eastmoney.com"
```

### 3. 在TRQuant中使用

```python
from core.automation import BrowserAgent, OpenManusAgent
from core.workflow import WorkflowEnhancer

# 使用BrowserAgent
async with BrowserAgent() as agent:
    result = await agent.navigate("https://www.eastmoney.com")

# 使用WorkflowEnhancer
async with WorkflowEnhancer() as enhancer:
    result = await enhancer.enhance_r1_market_trend()
```

## 注意事项

1. **LLM API配置** - 某些功能（如extract_content）需要LLM API
2. **浏览器安装** - BrowserUseTool需要安装Playwright浏览器
3. **MCP服务器** - 需要重启Cursor才能加载MCP服务器配置
4. **权限问题** - 确保有足够的权限执行命令和访问网络

## TRQuant集成优势

1. **无需LLM API** - TRQuant封装了工具功能，不需要LLM推理
2. **统一接口** - 与TRQuant架构一致
3. **性能优化** - 缓存、连接池、并行处理
4. **工作流集成** - 直接集成到研究流程
""",
        "type": "lesson",
        "tags": ["OpenManus", "配置", "使用指南", "安装", "TRQuant"],
        "source": "third_party/OpenManus/README.md"
    })
    
    return kb_items


def add_to_knowledge_base(kb_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    将知识库条目添加到RAG知识库
    
    Args:
        kb_items: 知识库条目列表
    
    Returns:
        Dict: 添加结果
    """
    try:
        from mcp_servers.unified_dev_server import knowledge_add
        
        results = {
            'success': 0,
            'failed': 0,
            'errors': [],
            'knowledge_ids': []
        }
        
        print(f"\n📚 准备存入 {len(kb_items)} 个知识库条目...")
        print("=" * 70)
        
        for i, item in enumerate(kb_items, 1):
            print(f"\n[{i}/{len(kb_items)}] {item['title']}")
            
            try:
                result = knowledge_add(
                    title=item['title'],
                    content=item['content'],
                    type=item['type'],
                    tags=item['tags'],
                    source=item.get('source', '')
                )
                
                if result.get('success') or result.get('knowledge_id'):
                    results['success'] += 1
                    kb_id = result.get('knowledge_id') or result.get('id') or 'unknown'
                    results['knowledge_ids'].append(kb_id)
                    print(f"  ✅ 成功存入 (ID: {kb_id})")
                else:
                    results['failed'] += 1
                    error_msg = result.get('error', 'Unknown error')
                    results['errors'].append(f"{item['title']}: {error_msg}")
                    print(f"  ❌ 失败: {error_msg}")
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{item['title']}: {str(e)}")
                print(f"  ❌ 异常: {str(e)}")
        
        print("\n" + "=" * 70)
        print("📊 存入结果")
        print("=" * 70)
        print(f"成功: {results['success']} 个")
        print(f"失败: {results['failed']} 个")
        print(f"总计: {len(kb_items)} 个")
        
        return results
        
    except ImportError:
        return {
            'success': False,
            'error': 'MCP工具不可用',
            'items': kb_items
        }


def build_vector_index(kb_file: Path = None, force_rebuild: bool = False) -> Dict[str, Any]:
    """
    构建向量索引（RAG知识库）
    
    Args:
        kb_file: 知识库JSON文件路径（默认使用标准知识库文件）
        force_rebuild: 是否强制重建索引
    
    Returns:
        Dict: 构建结果
    """
    try:
        from mcp_servers.knowledge_vector_index import build_vector_index as build_index
        
        # 确定知识库文件路径
        if kb_file is None:
            DATA_DIR = PROJECT_ROOT / "data"
            KNOWLEDGE_DIR = DATA_DIR / "knowledge"
            kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
            
            if not kb_file.exists():
                # 尝试另一个路径
                kb_file = PROJECT_ROOT / ".trquant" / "dev" / "knowledge" / "knowledge_base.json"
        
        if not kb_file.exists():
            return {
                'success': False,
                'error': f'知识库文件不存在: {kb_file}'
            }
        
        print(f"\n🔍 构建向量索引（RAG知识库）...")
        print(f"   知识库文件: {kb_file}")
        print(f"   索引目录: {PROJECT_ROOT / '.trquant' / 'dev' / 'knowledge' / 'vector_index'}")
        
        result = build_index(kb_file, force_rebuild=force_rebuild)
        
        if result.get('success'):
            print(f"  ✅ 向量索引构建成功")
            print(f"  条目数量: {result.get('items_count', 0)}")
            print(f"  模型: {result.get('model', 'N/A')}")
            print(f"  向量维度: {result.get('embedding_dim', 'N/A')}")
            print(f"  索引路径: {result.get('index_path', 'N/A')}")
        else:
            error_msg = result.get('error', 'Unknown error')
            if '依赖缺失' in error_msg:
                print(f"  ⚠️  向量索引构建失败: {error_msg}")
                print(f"  提示: 请安装依赖: pip install sentence-transformers chromadb")
            else:
                print(f"  ⚠️  向量索引构建失败: {error_msg}")
        
        return result
        
    except ImportError:
        return {
            'success': False,
            'error': '向量索引模块不可用'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """主函数"""
    print("=" * 70)
    print("📚 OpenManus代码知识库构建（向量RAG知识库）")
    print("=" * 70)
    
    # 1. 创建知识库条目
    print("\n📝 创建知识库条目...")
    kb_items = create_openmanus_kb_items()
    print(f"✅ 共创建 {len(kb_items)} 个知识库条目")
    
    # 2. 保存为JSON文件（备份）
    output_file = PROJECT_ROOT / "docs" / "research" / "openmanus_kb_items.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kb_items, f, ensure_ascii=False, indent=2)
    print(f"✅ 知识库条目已保存: {output_file}")
    
    # 3. 添加到知识库
    print("\n💾 添加到RAG知识库...")
    add_result = add_to_knowledge_base(kb_items)
    
    if add_result.get('success') is not False:
        print(f"\n✅ 知识库条目添加完成")
        print(f"   成功: {add_result.get('success', 0)} 个")
        if add_result.get('failed', 0) > 0:
            print(f"   失败: {add_result.get('failed', 0)} 个")
            print(f"⚠️  部分条目添加失败，请检查错误信息")
        
        # 4. 构建向量索引（RAG知识库）
        print("\n" + "=" * 70)
        index_result = build_vector_index(force_rebuild=False)
        
        if index_result.get('success'):
            print(f"\n✅ OpenManus知识库向量RAG构建完成！")
            print(f"   现在可以在开发中使用向量检索搜索OpenManus相关内容")
        else:
            print(f"\n⚠️  向量索引构建失败，但不影响知识库条目的使用")
            print(f"   提示: 向量检索需要安装 sentence-transformers 和 chromadb")
    else:
        print(f"⚠️  {add_result.get('error', '添加失败')}")
        print(f"知识库条目已保存到: {output_file}")


if __name__ == "__main__":
    main()
