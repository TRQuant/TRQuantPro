# TRQuant 韬睿量化系统 - AI助手上下文文档

> **版本**: v1.2  
> **更新**: 2026-01-08  
> **目的**: 为Claude AI提供项目上下文，指导开发和使用

---

## 📋 项目概览

**TRQuant（韬睿量化）** 是一个专业的量化交易研究系统，采用**研究-实战双阶段分离架构**。

### 核心定位

- **研究阶段**: Jupyter Notebook（数据研究、可视化、模型验证）
- **实战阶段**: GUI面板 + API（策略执行、实盘交易）
- **数据源**: JQData（聚宽）优先，AKShare补充
- **存储**: MongoDB（信号、回测结果、版本管理）

---

## 🏗️ 系统架构

### 三层架构（核心原则）

```
┌─────────────────────────────────────────┐
│  研究阶段前端 (Jupyter Notebook)        │
│  notebooks/research/                    │
│  - 直接导入Core模块                      │
│  - 交互式研究和可视化                    │
└─────────────────────────────────────────┘
              ↓ 直接调用
┌─────────────────────────────────────────┐
│  功能实现层 (Core Python Modules)       │
│  core/                                   │
│  - 所有功能在这里实现                    │
│  - 可被Notebook和MCP Server调用         │
└─────────────────────────────────────────┘
              ↓ 封装调用
┌─────────────────────────────────────────┐
│  MCP Servers (LLM工具接口)              │
│  mcp_servers/                           │
│  - 封装Core模块供LLM调用                │
│  - 支持工作流自动化                      │
└─────────────────────────────────────────┘
```

### 关键原则

1. **Core模块是基础**: 所有功能在 `core/` 中实现
2. **Notebook直接调用Core**: `from core.xxx import Xxx`
3. **MCP Server封装Core**: 供LLM和工作流调用
4. **禁止Notebook通过MCP调用Core**: 除非需要工作流集成

---

## 🔄 工作流程（统一术语）

参考 `notebooks/research/00_system_architecture_workflow.ipynb`:

- **R0**: 数据源检测
- **R1**: 市场趋势分析
- **R2**: 主线轮动研究
- **R3**: 因子组合开发
- **R4**: 投资标的筛选（不是"候选池构建"）
- **R5**: 风控模块设计
- **R6**: 策略开发与回测

**重要**: 统一使用"投资标的筛选"，不使用"候选池构建"。

---

## 📁 目录结构

### 核心目录

```
TRQuant/
├── core/                          # 核心功能实现
│   ├── market_trend_analyzer.py   # 市场趋势分析器
│   ├── trend_analyzer.py          # 趋势分析器（基线）
│   ├── candidate_pool_builder.py  # 投资标的筛选器
│   ├── signal_backtest.py         # 信号回测器
│   └── ...
├── notebooks/research/             # 研究前端
│   ├── 00_system_architecture_workflow.ipynb  # 系统架构文档
│   ├── 01_Market_Trend_Analyzer.ipynb         # 市场趋势分析
│   └── ...
├── mcp_servers/                    # MCP工具接口
│   ├── trquant_core_server.py     # 核心功能服务器
│   ├── workflow_9steps_server.py # 工作流服务器
│   └── ...
├── config/                         # 配置文件
│   └── jqdata_config.json         # JQData配置
└── docs/                           # 文档
    └── 02_development_guides/     # 开发指南
```

---

## 💻 开发规范

### Python编码规范

- **命名**: `snake_case`（函数、变量）、`PascalCase`（类）、`UPPER_CASE`（常量）
- **导入**: 标准库 → 第三方库 → 本地模块
- **文档**: 所有公共函数必须有Google风格docstring
- **类型**: 所有函数参数和返回值必须有类型提示

### Notebook开发规范

**第一个Cell必须包含**:
```python
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

# 使用统一环境初始化
from notebooks.lib import setup_research_environment
env = setup_research_environment(verbose=True)
```

**导入Core模块**:
```python
# ✅ 推荐
from core.market_trend_analyzer import MarketTrendAnalyzer
from core.trend_analyzer import TrendAnalyzer

# ❌ 不推荐（除非需要工作流集成）
from core.mcp.client import MCPClient
```

**数据源检测（可选，推荐）**:
```python
from notebooks.lib import ErrorBoundary

# 检测JQData连接
jqdata_status = "❌ 未连接"
jq = None
with ErrorBoundary("检测JQData连接", suppress=True) as eb:
    jq = env.get_jqdata_client()
    if jq and hasattr(jq, 'is_authenticated') and jq.is_authenticated():
        jqdata_status = "✅ 已连接"
    elif jq:
        jqdata_status = "✅ 已连接"
```

**错误处理原则**:
- 使用 `ErrorBoundary` 包装可能失败的初始化
- 设置 `suppress=True` 使失败不影响后续代码
- 提供友好的错误提示和降级方案

---

## 🎯 核心模块说明

### MarketTrendAnalyzer

**位置**: `core/market_trend_analyzer.py`

**功能**:
- 多周期趋势分析（周/月/季 = 5/21/63交易日）
- HMM隐状态识别（SimpleHMM）
- 加权融合输出（Trend 0.8 + HMM 0.2）
- 生成workflow_params和investment_universe_filters

**基线**: TrendAnalyzer + SimpleHMM（已回测验证）

**配置**:
- `scoring_style`: `'smooth_grouped'`（推荐）或 `'legacy'`
- 周期定义: 周/月/季 = 5/21/63交易日（可扩展）

### TrendAnalyzer

**位置**: `core/trend_analyzer.py`

**功能**: 8维技术指标打分体系

**评分风格**:
- `legacy`: 传统硬阈值方式
- `smooth_grouped`: 连续映射 + 因子分组（推荐）

### CandidatePoolBuilder

**位置**: `core/candidate_pool_builder.py`

**功能**: 投资标的筛选（基于投资主线）

**注意**: 统一术语为"投资标的筛选"，不是"候选池构建"。

### A股多周期共振状态系统

**位置**: `core/resonance_state_model.py`, `core/market_trend_analyzer.py`, `core/rotation/sector_resonance.py`, `core/selection/stock_filters.py`, `core/backtest/resonance_event_study.py`

**功能**: A股本土化的多周期共振状态识别系统，作为"系统开关"用于仓位控制和风险预算

**三层结构**:
1. **Layer 1 - 市场总开关**: 沪深300 + 中证1000 多指数共振 → 仓位上限映射
2. **Layer 2 - 行业轮动**: 申万一级行业 + 主题ETF 共振TopN → 可投资池
3. **Layer 3 - 个股过滤**: RS相对强度 + 流动性 + 涨跌停/ATR异常检测 → 最终标的

**核心原则**:
- 共振不负责买点，负责"系统开关"
- 仓位控制比买卖点更重要
- 持续性确认：共振连续出现2~3次才升级仓位

**验证Notebook**: `notebooks/research/01_market_trend_resonance_mvp.ipynb`

**关键配置**:
- 短周期: 5日（情绪/短线资金）
- 中周期: 21日（主线/波段资金）
- 长周期: 63日（机构趋势）
- 确认窗口: 2次（共振持续性确认）
- 行业TopN: 5（可投资行业数量）

---

## 🔧 MCP工具使用

### 可用工具

- `market.trend` - 分析市场趋势
- `market.mainlines` - 识别投资主线
- `data.candidate_pool` - 筛选投资标的
- `factor.recommend` - 推荐因子
- `backtest.run` - 运行回测
- `workflow9.execute` - 执行工作流
- `knowledge.add` - 添加知识库条目
- `knowledge.search` - 搜索知识库
- `crawler.fetch` - 爬取网页内容

### 使用方式

#### 方式1: 在Cursor Chat中直接使用

在Cursor Chat中：
```
"请使用market.trend工具分析当前市场趋势"
```

#### 方式2: 在Python脚本中使用MCPClient

**基本用法**:
```python
from core.mcp.client import MCPClient

# 创建MCP客户端
client = MCPClient()

# 调用MCP工具
result = client.call(
    tool_name='knowledge.add',
    arguments={
        'title': '知识条目标题',
        'content': '知识内容...',
        'type': 'lesson',  # lesson/practice/reference
        'tags': ['标签1', '标签2'],
        'source': '来源信息'
    },
    timeout=30.0
)

# 检查结果
if result.success:
    print(f'✅ 调用成功 (Trace ID: {result.trace_id})')
    print(f'耗时: {result.duration:.2f}秒')
    data = result.data
    if isinstance(data, str):
        import json
        data = json.loads(data)
    print(f'结果: {data}')
else:
    print(f'❌ 调用失败: {result.error}')
```

**完整示例：Git仓库导入到知识库**:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将GitHub仓库的Markdown文件导入到RAG知识库
"""
import sys
from pathlib import Path
from core.mcp.client import MCPClient

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def import_markdown_to_kb(md_file: Path):
    """将Markdown文件导入到知识库"""
    # 读取文件
    content = md_file.read_text(encoding='utf-8')
    
    # 提取标题
    import re
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_file.stem
    
    # 创建MCP客户端
    client = MCPClient()
    
    # 调用MCP工具添加知识
    result = client.call(
        tool_name='knowledge.add',
        arguments={
            'title': f'聚宽学习 - {title}',
            'content': content,
            'type': 'lesson',
            'tags': ['聚宽', 'JoinQuant', '量化交易'],
            'source': f'https://github.com/user/repo/blob/main/{md_file.name}'
        },
        timeout=30.0
    )
    
    if result.success:
        print(f'✅ 成功添加: {title} (Trace ID: {result.trace_id})')
        return True
    else:
        print(f'❌ 失败: {result.error}')
        return False

# 使用示例
if __name__ == '__main__':
    md_file = Path('/tmp/repo/README.md')
    import_markdown_to_kb(md_file)
```

**带回退机制的调用**:
```python
from core.mcp.client import MCPClient
from mcp_servers.unified_dev_server import knowledge_add as direct_knowledge_add

def add_knowledge_with_fallback(title, content, type='lesson', tags=None, source=None):
    """添加知识，优先使用MCP工具，失败则回退到直接函数调用"""
    tags = tags or []
    
    # 方式1: 尝试MCP工具调用
    try:
        client = MCPClient()
        result = client.call(
            tool_name='knowledge.add',
            arguments={
                'title': title,
                'content': content,
                'type': type,
                'tags': tags,
                'source': source
            },
            timeout=30.0
        )
        
        if result.success:
            data = result.data
            if isinstance(data, str):
                import json
                data = json.loads(data)
            
            if data.get('success') or data.get('knowledge_id'):
                return {'success': True, 'method': 'mcp', 'id': data.get('knowledge_id')}
    except Exception as e:
        print(f'⚠️ MCP调用异常: {e}')
    
    # 方式2: 回退到直接函数调用
    try:
        result = direct_knowledge_add(
            title=title,
            content=content,
            type=type,
            tags=tags,
            source=source
        )
        if result.get('success') or result.get('knowledge_id'):
            return {'success': True, 'method': 'direct', 'id': result.get('knowledge_id')}
    except Exception as e:
        print(f'❌ 直接调用也失败: {e}')
    
    return {'success': False}
```

### MCP工具调用最佳实践

1. **优先使用MCP工具调用**: 通过`MCPClient.call()`调用，符合MCP标准
2. **添加错误处理**: 检查`result.success`并处理错误
3. **设置合理超时**: 根据工具类型设置`timeout`（默认30秒）
4. **记录Trace ID**: 使用`result.trace_id`追踪调用
5. **回退机制**: 当MCP调用失败时，可回退到直接函数调用
6. **日志输出**: 显示调用过程（工具名、参数、Trace ID、耗时）

### 实际应用示例

**批量导入Git仓库到知识库**:
```bash
# 使用脚本导入
python scripts/import_jointquant_learning_to_kb.py --repo-path /path/to/repo

# 自动克隆并导入
python scripts/import_jointquant_learning_to_kb.py --clone

# 预览模式（不实际添加）
python scripts/import_jointquant_learning_to_kb.py --repo-path /path/to/repo --dry-run
```

**脚本位置**: `scripts/import_jointquant_learning_to_kb.py`

该脚本展示了：
- ✅ 使用`MCPClient.call()`调用MCP工具
- ✅ 显示调用详情（Trace ID、耗时、参数）
- ✅ 自动回退机制（MCP失败时使用直接函数调用）
- ✅ 完整的错误处理和日志输出

---

## 📊 数据源配置

### JQData（聚宽）

**重要**: JQData是正式账号，有完整历史数据权限，无数据范围限制。

**配置文件**: `config/jqdata_config.json`

**使用**:
```python
from config.config_manager import get_config_manager
import jqdatasdk as jq

cm = get_config_manager()
jq_config = cm.get_config('jqdata')
jq.auth(jq_config['username'], jq_config['password'])
```

**文档**: `docs/JQDATA_CONFIGURATION_GUIDE.md`

### MongoDB

**用途**: 存储信号、回测结果、版本管理

**集合**:
- `market_trend` - 市场趋势信号
- `backtest_results` - 回测结果
- `candidate_pool` - 投资标的池

---

## 🚫 常见错误和避免

### 1. Notebook通过MCP调用Core

```python
# ❌ 错误
from core.mcp.client import MCPClient
client = MCPClient()
result = client.call_tool("market.trend", {...})

# ✅ 正确
from core.market_trend_analyzer import MarketTrendAnalyzer
analyzer = MarketTrendAnalyzer(config)
result = analyzer.analyze(...)
```

### 2. Core模块导入Notebook代码

```python
# ❌ 错误
from notebooks.lib import something

# ✅ 正确
# Core模块应该独立，不依赖Notebook
```

### 3. 术语不一致

- ❌ "候选池构建"
- ✅ "投资标的筛选"

### 4. Notebook初始化代码错误

**问题**: 初始化代码中路径错误或缺少错误处理

**正确做法**:
```python
# ✅ 正确：使用正确的项目路径和错误处理
if project_root is None:
    project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')

# ✅ 正确：使用ErrorBoundary和suppress参数
with ErrorBoundary("初始化评估引擎", suppress=True) as eb:
    evaluator = env.get_market_evaluator()
if eb.has_error:
    print(f"⚠️ 初始化失败: {eb.error_message} (可继续使用其他功能)")
```

### 5. 语法错误：if语句后缺少代码块

**问题**: `if` 语句后只有空行，没有实际代码块

**示例**:
```python
# ❌ 错误
def get_market_regime_detector():
    global _detector
    if _detector is None:
        # 这里缺少代码

# ✅ 正确
def get_market_regime_detector():
    global _detector
    if _detector is None:
        _detector = MarketRegimeDetector()
    return _detector
```

---

## 📚 重要文档

- **系统架构**: `notebooks/research/00_system_architecture_workflow.ipynb`
- **市场趋势分析**: `notebooks/research/01_Market_Trend_Analyzer.ipynb`
- **A股共振系统MVP**: `notebooks/research/01_market_trend_resonance_mvp.ipynb`
- **开发最佳实践**: `docs/02_development_guides/BEST_PRACTICES_DEVELOPMENT_USAGE.md`
- **Cursor 2.3功能**: `docs/02_development_guides/CURSOR_2.3_FEATURES_RESEARCH.md`
- **JQData配置**: `docs/JQDATA_CONFIGURATION_GUIDE.md`
- **Rules配置**: `.cursor/rules/` 目录

---

## 🎯 开发任务指导

### 创建新功能

1. **在Core模块中实现**
   ```python
   # core/new_feature.py
   class NewFeature:
       def process(self, ...):
           # 实现逻辑
           pass
   ```

2. **在Notebook中测试**
   ```python
   # notebooks/research/test_new_feature.ipynb
   from core.new_feature import NewFeature
   feature = NewFeature()
   result = feature.process(...)
   ```

3. **（可选）封装成MCP工具**
   ```python
   # mcp_servers/xxx_server.py
   from core.new_feature import NewFeature
   # 封装成MCP工具
   ```

### 修改现有功能

1. **先查看相关文档和Rules**
2. **遵循架构规范**
3. **更新相关文档**
4. **测试验证**

---

## 💡 AI助手使用建议

### 当用户请求开发任务时

1. **理解上下文**: 参考本文件和Rules
2. **遵循架构**: 三层架构原则
3. **使用正确术语**: "投资标的筛选"不是"候选池构建"
4. **直接调用Core**: Notebook中直接导入Core模块
5. **提供完整代码**: 包含路径设置、导入、使用示例

### 当用户请求分析任务时

1. **使用MCP工具**: 如 `market.trend`、`data.candidate_pool`
2. **或直接调用Core**: 在Notebook中直接使用Core模块
3. **提供可视化**: 使用Plotly生成交互式图表

---

## 📂 工作目录规则

### 操作性工作统一放在 `worktrees/TRQuant/ope` 目录

所有回测验证、策略开发、数据分析等操作性工作文件统一存放：

```
工作目录: /home/taotao/.cursor/worktrees/TRQuant/ope/
Python环境: /home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python
```

**目录结构**:
```
worktrees/TRQuant/ope/
├── venv/                    # Python虚拟环境
├── scripts/                 # 脚本文件
│   └── stage_backtest/     # 回测验证脚本
├── docs/                    # 文档
├── data/                    # 数据文件（按需创建）
└── results/                 # 结果输出（按需创建）
```

**Python环境规则**:
- **Python可执行文件路径**: `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python`
- **Python3可执行文件路径**: `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python3`
- **pip可执行文件路径**: `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/pip`
- **所有Python脚本必须使用此虚拟环境中的Python解释器**

**运行脚本示例**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 使用完整路径
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python scripts/stage_backtest/stage_backtest_validator.py

# 或使用相对路径（在项目根目录下）
./venv/bin/python scripts/stage_backtest/stage_backtest_validator.py

# 或使用python3
./venv/bin/python3 scripts/test_factor_optimization_v4.py
```

**重要**: 
- 所有操作性工作文件必须放在此目录
- Python虚拟环境也在此目录下
- 脚本中的路径引用应使用此工作目录
- **执行Python脚本时，必须使用 `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python` 或 `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python3`**
- 不要使用系统Python（`/usr/bin/python` 或 `/usr/bin/python3`），必须使用项目虚拟环境中的Python

---

## 🔄 版本和更新

- **项目路径**: `/home/taotao/.cursor/worktrees/TRQuant/ope`
- **Python版本**: 3.11+
- **主要依赖**: pandas, numpy, jqdatasdk, pymongo, plotly

### 最新更新 (2026-01-09)

- ✅ **JQData账号确认**: JQData是正式账号，有完整历史数据权限，无数据范围限制
- ✅ **run_bullettrade_backtest_v4.py加速功能**: 添加数据预加载、GPU加速、性能统计功能
- ✅ **批量回测验证器**: 完成BatchBacktestValidator开发，支持多时间段回测
- ✅ **收益率计算修复**: 修复收益率显示错误（移除多余的*100操作）
- ✅ **get_index_stocks修复**: 添加日期参数传递，确保获取历史成分股
- ✅ **数据缓存集成**: 策略代码生成时传递缓存目录，实现零Token消耗

### 历史更新 (2026-01-08)

- ✅ **MCP工具调用方式**: 添加完整的MCP工具调用文档和示例
- ✅ **Git仓库导入工具**: 新增`import_jointquant_learning_to_kb.py`脚本，支持批量导入Markdown到知识库
- ✅ **知识库扩展**: 新增44条vibe-coding相关内容和9条聚宽学习内容
- ✅ **A股多周期共振状态系统**: 完成三层架构实现（市场总开关、行业轮动、个股过滤）
- ✅ **修复语法错误**: `core/market_regime/market_regime_detector.py` 中 `get_market_regime_detector()` 函数
- ✅ **改进Notebook初始化**: 增强错误处理和数据源检测
- ✅ **新增验证Notebook**: `01_market_trend_resonance_mvp.ipynb`
- ✅ **因子优化系统**: 完成因子选择与权重递归优化系统（V4.0）
- ✅ **Python环境规则**: 明确指定Python虚拟环境路径规则

---

**最后更新**: 2026-01-09  
**维护者**: TRQuant Team
