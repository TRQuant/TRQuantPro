---
name: "TRQuant架构规范"
description: "TRQuant三层架构规范和模块组织原则"
type: "always"
tags: ["architecture", "design", "trquant"]
---

# TRQuant三层架构规范

## 架构原则

### 核心原则
1. **Core模块是基础**: 所有功能在 `core/` 中实现
2. **Notebook用于研究**: 直接调用Core模块，快速实验
3. **MCP Server用于集成**: 封装Core模块，供LLM和工作流调用

### 模块组织

```
TRQuant/
├── core/                    # 核心功能实现
│   ├── market_trend_analyzer.py
│   ├── trend_analyzer.py
│   └── candidate_pool_builder.py
├── notebooks/research/      # 研究前端
│   └── 01_Market_Trend_Analyzer.ipynb
└── mcp_servers/             # LLM工具接口
    └── trquant_core_server.py
```

## 交互模式

### ✅ 推荐做法

1. **Notebook直接调用Core模块**
   ```python
   # notebooks/research/xxx.ipynb
   from core.market_trend_analyzer import MarketTrendAnalyzer
   analyzer = MarketTrendAnalyzer(config)
   result = analyzer.analyze(...)
   ```

2. **MCP Server封装Core模块**
   ```python
   # mcp_servers/trquant_core_server.py
   from core.market_trend_analyzer import MarketTrendAnalyzer
   analyzer = MarketTrendAnalyzer(config)
   result = analyzer.analyze(...)
   ```

### ❌ 禁止做法

1. **Notebook通过MCP Server调用Core模块**
   ```python
   # ❌ 不推荐
   from core.mcp.client import MCPClient
   client = MCPClient()
   result = client.call_tool("market.trend", {...})
   ```

2. **Core模块导入Notebook相关代码**
   ```python
   # ❌ 错误
   from notebooks.lib import something
   ```

3. **MCP Server中实现业务逻辑**
   ```python
   # ❌ 错误
   async def call_tool(name, args):
       data = fetch_data(...)  # 应该在core模块中
   ```

## 工作流程术语

### 统一术语（参考 `00_system_architecture_workflow.ipynb`）

- R0: 数据源检测
- R1: 市场趋势分析
- R2: 主线轮动研究
- R3: 因子组合开发
- R4: 投资标的筛选（不是"候选池构建"）
- R5: 风控模块设计
- R6: 策略开发与回测

## 文件命名规范

- Core模块: `snake_case.py` (如 `market_trend_analyzer.py`)
- Notebook: `数字_描述性名称.ipynb` (如 `01_Market_Trend_Analyzer.ipynb`)
- MCP Server: `xxx_server.py` (如 `trquant_core_server.py`)
