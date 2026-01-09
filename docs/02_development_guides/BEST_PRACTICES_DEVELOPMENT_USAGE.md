# TRQuant 开发和使用最佳实践指南

> **版本**: v1.0  
> **更新**: 2026-01-06  
> **目的**: 明确Jupyter Notebook、Python代码和MCP Servers的开发和使用方式

---

## 📋 目录

1. [架构概览](#1-架构概览)
2. [三层架构说明](#2-三层架构说明)
3. [开发最佳实践](#3-开发最佳实践)
4. [使用最佳实践](#4-使用最佳实践)
5. [交互模式](#5-交互模式)
6. [常见场景](#6-常见场景)

---

## 1. 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    TRQuant 三层架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  研究阶段前端 (Jupyter Notebook)                      │   │
│  │  - 数据分析和可视化                                    │   │
│  │  - 交互式研究                                          │   │
│  │  - 报告生成                                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                        ↓ 直接调用                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  功能实现层 (Core Python Modules)                    │   │
│  │  - core/market_trend_analyzer.py                     │   │
│  │  - core/trend_analyzer.py                           │   │
│  │  - core/candidate_pool_builder.py                   │   │
│  │  - core/signal_backtest.py                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                        ↓ 封装调用                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  MCP Servers (LLM工具接口)                           │   │
│  │  - mcp_servers/trquant_core_server.py               │   │
│  │  - mcp_servers/workflow_9steps_server.py            │   │
│  │  - mcp_servers/data_source_server_v2.py             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 三层架构说明

### 2.1 研究阶段前端 (Jupyter Notebook)

**位置**: `notebooks/research/`

**职责**:
- ✅ 数据探索和分析
- ✅ 交互式可视化
- ✅ 模型验证和回测
- ✅ 研究报告生成
- ✅ 快速原型开发

**特点**:
- 直接导入和使用 `core/` 模块
- 支持交互式调试和可视化
- 适合研究和实验

**示例**:
```python
# notebooks/research/01_market_trend_comprehensive.ipynb

# 1. 路径设置（第一个cell）
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 2. 直接导入core模块
from core.market_trend_analyzer import MarketTrendAnalyzer
from core.trend_analyzer import TrendAnalyzer
from core.candidate_pool_builder import CandidatePoolBuilder

# 3. 使用
analyzer = MarketTrendAnalyzer()
result = analyzer.analyze(...)
```

### 2.2 功能实现层 (Core Python Modules)

**位置**: `core/`

**职责**:
- ✅ 核心算法实现
- ✅ 数据处理逻辑
- ✅ 业务规则封装
- ✅ 可复用的功能模块

**特点**:
- 纯Python代码，无依赖特定环境
- 可被Notebook直接导入
- 可被MCP Server封装调用
- 保持单一职责原则

**示例**:
```python
# core/market_trend_analyzer.py

class MarketTrendAnalyzer:
    """市场趋势分析器"""
    
    def __init__(self, config: MarketTrendAnalyzerConfig):
        self.config = config
        self.trend_analyzer = TrendAnalyzer()
        self.hmm = SimpleHMM()
    
    def analyze(self, index_code: str, date: str) -> MarketTrendSignal:
        """分析市场趋势"""
        # 实现逻辑
        pass
```

### 2.3 MCP Servers (LLM工具接口)

**位置**: `mcp_servers/`

**职责**:
- ✅ 将core模块封装成MCP工具
- ✅ 提供统一的工具接口
- ✅ 供LLM（Cursor AI）调用
- ✅ 支持工作流自动化

**特点**:
- 遵循MCP协议规范
- 提供工具描述和参数schema
- 封装core模块调用
- 支持异步调用

**示例**:
```python
# mcp_servers/trquant_core_server.py

TOOLS = [
    Tool(
        name="market.trend",
        description="分析市场趋势",
        inputSchema={
            "type": "object",
            "properties": {
                "index_code": {"type": "string"},
                "date": {"type": "string"}
            }
        }
    )
]

@server.call_tool()
async def call_tool(name: str, arguments: Dict) -> List[TextContent]:
    if name == "market.trend":
        # 调用core模块
        from core.market_trend_analyzer import MarketTrendAnalyzer
        analyzer = MarketTrendAnalyzer(config)
        result = analyzer.analyze(...)
        return [TextContent(type="text", text=json.dumps(result))]
```

---

## 3. 开发最佳实践

### 3.1 新功能开发流程

#### 场景1: 开发新的分析功能

**步骤**:
1. **在 `core/` 中实现核心逻辑**
   ```python
   # core/new_analyzer.py
   class NewAnalyzer:
       def analyze(self, ...):
           # 实现核心逻辑
           pass
   ```

2. **在 Notebook 中测试和验证**
   ```python
   # notebooks/research/test_new_analyzer.ipynb
   from core.new_analyzer import NewAnalyzer
   
   analyzer = NewAnalyzer()
   result = analyzer.analyze(...)
   # 可视化结果
   ```

3. **封装成 MCP 工具（可选）**
   ```python
   # mcp_servers/new_analyzer_server.py
   # 如果需要在工作流中使用，封装成MCP工具
   ```

#### 场景2: 扩展现有功能

**步骤**:
1. **在 `core/` 模块中扩展**
   ```python
   # core/market_trend_analyzer.py
   class MarketTrendAnalyzer:
       def new_method(self, ...):  # 新增方法
           pass
   ```

2. **在 Notebook 中测试**
   ```python
   # notebooks/research/test_extension.ipynb
   from core.market_trend_analyzer import MarketTrendAnalyzer
   
   analyzer = MarketTrendAnalyzer(config)
   result = analyzer.new_method(...)
   ```

3. **更新 MCP Server（如需要）**
   ```python
   # mcp_servers/trquant_core_server.py
   # 添加新的工具或更新现有工具
   ```

### 3.2 代码组织原则

#### ✅ 推荐做法

1. **Core模块保持独立**
   - 不依赖Notebook环境
   - 不依赖MCP Server
   - 可单独测试

2. **Notebook直接调用Core**
   - 使用 `from core.xxx import Xxx`
   - 避免通过MCP Server调用（除非需要工作流集成）

3. **MCP Server封装Core**
   - 只封装需要LLM调用的功能
   - 提供清晰的工具描述
   - 处理参数验证和错误

#### ❌ 避免做法

1. **不要在Core模块中导入Notebook相关代码**
   ```python
   # ❌ 错误
   from notebooks.lib import something
   ```

2. **不要在Notebook中直接调用MCP Server**
   ```python
   # ❌ 不推荐（除非需要工作流集成）
   from core.mcp.client import MCPClient
   client = MCPClient()
   result = client.call_tool("market.trend", {...})
   
   # ✅ 推荐
   from core.market_trend_analyzer import MarketTrendAnalyzer
   analyzer = MarketTrendAnalyzer(config)
   result = analyzer.analyze(...)
   ```

3. **不要在MCP Server中实现业务逻辑**
   ```python
   # ❌ 错误
   async def call_tool(name, args):
       # 业务逻辑应该在这里
       data = fetch_data(...)  # 应该在core模块中
       result = process(data)  # 应该在core模块中
   
   # ✅ 正确
   async def call_tool(name, args):
       from core.xxx import Xxx  # 调用core模块
       analyzer = Xxx()
       result = analyzer.process(...)
   ```

---

## 4. 使用最佳实践

### 4.1 Notebook使用方式

#### 标准初始化模式

```python
# Cell 1: 路径设置和环境初始化
import sys
from pathlib import Path

# 自动检测项目根目录
current_dir = Path.cwd()
project_root = None
for parent in [current_dir] + list(current_dir.parents):
    if (parent / 'core').exists() and (parent / 'config').exists():
        project_root = parent
        break

if project_root is None:
    project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f'✅ 项目根目录已添加到路径: {project_root}')

# 使用统一环境初始化（推荐）
from notebooks.lib import setup_research_environment
env = setup_research_environment(verbose=True)
```

#### 直接导入Core模块

```python
# Cell 2: 导入和使用core模块
from core.market_trend_analyzer import MarketTrendAnalyzer, MarketTrendAnalyzerConfig
from core.trend_analyzer import TrendAnalyzer
from core.candidate_pool_builder import CandidatePoolBuilder

# 创建配置
config = MarketTrendAnalyzerConfig(
    scoring_style='smooth_grouped',
    trend_weight=0.8,
    hmm_weight=0.2
)

# 使用
analyzer = MarketTrendAnalyzer(config)
result = analyzer.analyze("000300.XSHG", "2025-01-05")
```

#### 数据可视化

```python
# Cell 3: 可视化
import plotly.graph_objects as go
import pandas as pd

# 使用core模块的结果进行可视化
df = pd.DataFrame(result.signals)
fig = go.Figure(...)
fig.show()
```

### 4.2 MCP Server使用方式

#### 通过Cursor AI调用

```python
# 在Cursor Chat中
"请使用market.trend工具分析当前市场趋势"
```

#### 通过Python代码调用（工作流场景）

```python
# 仅在需要工作流集成时使用
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call_tool(
    "market.trend",
    {"index_code": "000300.XSHG", "date": "2025-01-05"}
)
```

### 4.3 何时使用哪种方式？

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| **研究和实验** | Notebook + Core模块 | 直接、灵活、可调试 |
| **快速验证** | Notebook + Core模块 | 无需额外配置 |
| **工作流自动化** | MCP Server | 统一接口，LLM可调用 |
| **批量处理** | Python脚本 + Core模块 | 高效、可调度 |
| **实时监控** | GUI + Core模块 | 直接调用，低延迟 |

---

## 5. 交互模式

### 5.1 Notebook ↔ Core模块

```
┌─────────────────┐
│ Jupyter Notebook│
└────────┬────────┘
         │ from core.xxx import Xxx
         │ analyzer = Xxx()
         │ result = analyzer.analyze(...)
         ↓
┌─────────────────┐
│  Core Modules   │
│  (core/xxx.py)  │
└─────────────────┘
```

**特点**:
- ✅ 直接导入，无中间层
- ✅ 性能最优
- ✅ 可调试
- ✅ 适合研究和开发

### 5.2 MCP Server ↔ Core模块

```
┌─────────────────┐
│  MCP Server     │
│  (mcp_servers/) │
└────────┬────────┘
         │ from core.xxx import Xxx
         │ analyzer = Xxx()
         │ result = analyzer.analyze(...)
         ↓
┌─────────────────┐
│  Core Modules   │
│  (core/xxx.py)  │
└─────────────────┘
```

**特点**:
- ✅ 封装成工具接口
- ✅ LLM可调用
- ✅ 支持工作流
- ⚠️ 有协议开销

### 5.3 Notebook ↔ MCP Server（不推荐）

```
┌─────────────────┐
│ Jupyter Notebook│
└────────┬────────┘
         │ MCPClient.call_tool(...)
         ↓
┌─────────────────┐
│  MCP Server     │
└────────┬────────┘
         │ from core.xxx import Xxx
         ↓
┌─────────────────┐
│  Core Modules   │
└─────────────────┘
```

**特点**:
- ❌ 不推荐（除非需要工作流集成）
- ⚠️ 增加不必要的中间层
- ⚠️ 性能开销
- ⚠️ 调试困难

---

## 6. 常见场景

### 场景1: 开发新的市场分析功能

**步骤**:
1. 在 `core/market_trend_analyzer.py` 中添加新方法
2. 在 `notebooks/research/01_Market_Trend_Analyzer.ipynb` 中测试
3. 验证结果和可视化
4. 如果需要在工作流中使用，在 `mcp_servers/trquant_core_server.py` 中添加工具

### 场景2: 快速验证一个想法

**步骤**:
1. 创建新的Notebook: `notebooks/research/test_idea.ipynb`
2. 直接导入相关core模块
3. 快速实验和可视化
4. 如果验证成功，再考虑封装到core模块或MCP Server

### 场景3: 集成到工作流

**步骤**:
1. 确保功能已在core模块中实现
2. 在 `mcp_servers/workflow_9steps_server.py` 中添加步骤
3. 或创建新的MCP Server
4. 在 `notebooks/research/00_system_architecture_workflow.ipynb` 中更新文档

### 场景4: 批量数据处理

**步骤**:
1. 创建Python脚本: `scripts/batch_process.py`
2. 直接导入core模块
3. 使用循环或并行处理
4. 保存结果到文件或数据库

---

## 7. 文件组织规范

### 7.1 Core模块命名

```
core/
├── market_trend_analyzer.py      # 市场趋势分析器
├── trend_analyzer.py             # 趋势分析器
├── candidate_pool_builder.py    # 投资标的筛选器
├── signal_backtest.py            # 信号回测器
└── ...
```

**命名规范**:
- 使用小写字母和下划线
- 文件名与类名对应（如 `MarketTrendAnalyzer` → `market_trend_analyzer.py`）

### 7.2 Notebook命名

```
notebooks/research/
├── 00_system_architecture_workflow.ipynb  # 系统架构文档
├── 01_Market_Trend_Analyzer.ipynb          # 市场趋势分析
├── 01_市场趋势判断回测验证.ipynb            # 回测验证
└── ...
```

**命名规范**:
- 使用数字前缀表示顺序
- 使用描述性名称
- 支持中英文

### 7.3 MCP Server命名

```
mcp_servers/
├── trquant_core_server.py        # 核心功能服务器
├── workflow_9steps_server.py    # 工作流服务器
├── data_source_server_v2.py     # 数据源服务器
└── ...
```

**命名规范**:
- 使用 `_server.py` 后缀
- 使用描述性名称
- 版本号使用 `_v2` 后缀

---

## 8. 调试和测试

### 8.1 Notebook调试

```python
# 在Notebook中使用
import logging
logging.basicConfig(level=logging.DEBUG)

# 使用pdb调试
import pdb; pdb.set_trace()

# 使用IPython调试
%debug
```

### 8.2 Core模块测试

```python
# tests/test_market_trend_analyzer.py
import pytest
from core.market_trend_analyzer import MarketTrendAnalyzer

def test_analyze():
    analyzer = MarketTrendAnalyzer(config)
    result = analyzer.analyze(...)
    assert result is not None
```

### 8.3 MCP Server测试

```python
# tests/test_mcp_server.py
from core.mcp.client import MCPClient

def test_market_trend_tool():
    client = MCPClient()
    result = client.call_tool("market.trend", {...})
    assert result["success"] == True
```

---

## 9. 性能优化建议

### 9.1 Notebook性能

- ✅ 使用缓存避免重复计算
- ✅ 使用并行处理（如 `joblib`）
- ✅ 使用增量更新而非全量重算

### 9.2 Core模块性能

- ✅ 使用 `@lru_cache` 缓存结果
- ✅ 使用向量化操作（NumPy/Pandas）
- ✅ 避免重复数据获取

### 9.3 MCP Server性能

- ✅ 使用异步处理
- ✅ 实现结果缓存
- ✅ 批量处理支持

---

## 10. 总结

### 核心原则

1. **Core模块是基础**: 所有功能在core模块中实现
2. **Notebook用于研究**: 直接调用core模块，快速实验
3. **MCP Server用于集成**: 封装core模块，供LLM和工作流调用

### 开发流程

```
新功能开发
    ↓
在core/中实现
    ↓
在Notebook中测试
    ↓
验证和优化
    ↓
（可选）封装成MCP工具
```

### 使用建议

- **研究和开发**: 使用Notebook + Core模块
- **工作流自动化**: 使用MCP Server
- **批量处理**: 使用Python脚本 + Core模块

---

**最后更新**: 2026-01-06  
**维护者**: TRQuant Team
