# TRQuant 模块索引 - 快速查找手册

> **目的**: 避免重复开发、错误导入，确保快速调用成熟模块

---

## 📦 核心模块导入规范

### 1. JQData 数据客户端
```python
# ✅ 正确导入
from jqdata.client import JQDataClient

# ❌ 错误导入 (不存在)
from core.data.jqdata_provider import JQDataClient  # 这个类叫 JQDataProvider

# 使用方式
jq_client = JQDataClient()
if not jq_client.is_authenticated():
    from config.config_manager import get_config_manager
    config = get_config_manager().get_jqdata_config()
    jq_client.authenticate(config["username"], config["password"])
```

### 2. 主线扫描器
```python
# ✅ 正确导入
from core.mainline_scanner import MainlineBasedScanner

# 使用方式
scanner = MainlineBasedScanner(jq_client=jq_client)
result = scanner.scan_from_mainlines(
    period="medium",
    min_score=60.0,
    max_mainlines=10
)
```

### 3. 候选池构建器
```python
# ✅ 正确导入
from core.candidate_pool_builder import CandidatePoolBuilder

# 使用方式
builder = CandidatePoolBuilder(jq_client=jq_client)
pool = builder.build_from_mainline(
    mainline_name="人工智能",
    mainline_type="concept"
)
```

### 4. 配置管理
```python
# ✅ 正确导入
from config.config_manager import get_config_manager

# 使用方式
config_manager = get_config_manager()
jq_config = config_manager.get_jqdata_config()  # JQData配置
db_config = config_manager.get_database_config()  # MongoDB配置
```

---

## 📂 模块目录结构

```
TRQuant/
├── jqdata/                    # JQData客户端模块
│   └── client.py              # JQDataClient 类
│
├── core/                      # 核心业务逻辑
│   ├── mainline_scanner.py    # MainlineBasedScanner
│   ├── candidate_pool_builder.py  # CandidatePoolBuilder  
│   ├── momentum_growth_scanner.py # MomentumGrowthScanner
│   ├── five_dimension_scorer.py   # FiveDimensionScorer
│   ├── backtest_engine.py     # BacktestEngine
│   ├── strategy_generator.py  # StrategyGenerator
│   └── data/
│       └── jqdata_provider.py # JQDataProvider (不是Client!)
│
├── config/                    # 配置模块
│   ├── config_manager.py      # get_config_manager()
│   └── jqdata_config.json     # JQData配置文件
│
├── mcp_servers/              # MCP服务器
│   ├── workflow_9steps_server.py  # 9步工作流
│   ├── market_server_v2.py    # 市场分析
│   ├── data_source_server_v2.py   # 数据源
│   ├── factor_server.py       # 因子推荐
│   └── backtest_server.py     # 回测
│
└── extension/                # VS Code扩展
    └── python/bridge.py      # Python桥接
```

---

## 🔑 关键配置文件

| 配置 | 路径 | 说明 |
|------|------|------|
| JQData | `config/jqdata_config.json` | 聚宽账号密码 |
| MongoDB | `config/database_config.json` | 数据库连接 |
| MCP | `.cursor/mcp.json` | MCP服务器配置 |

---

## ⚠️ 常见错误及修复

### 错误1: `cannot import name 'JQDataClient'`
```python
# 原因: 导入路径错误
# 修复: 使用正确路径
from jqdata.client import JQDataClient  # ✅
```

### 错误2: `MainlineScanner not found`
```python
# 原因: 类名已更改
# 修复: 使用新类名
from core.mainline_scanner import MainlineBasedScanner  # ✅
```

### 错误3: `JQData未认证`
```python
# 原因: 未加载配置
# 修复: 从配置管理器获取
from config.config_manager import get_config_manager
config = get_config_manager().get_jqdata_config()
jq_client.authenticate(config["username"], config["password"])
```

---

## 📋 9步工作流MCP调用映射

| 步骤 | MCP工具 | 底层模块 |
|------|---------|----------|
| 1.信息获取 | `data_source.health_check` | `data_source_server_v2._handle_health_check` |
| 2.市场趋势 | `market.status` | `market_server_v2._handle_status` |
| 3.投资主线 | `market.mainlines` | `MainlineBasedScanner.scan_from_mainlines` |
| 4.候选池 | `data_source.candidate_pool` | `CandidatePoolBuilder.build_from_mainline` |
| 5.因子构建 | `factor.recommend` | `factor_server._handle_recommend` |
| 6.策略生成 | `template.generate` | `strategy_template_server._handle_generate` |
| 7.回测验证 | `backtest.quick` | `backtest_server._handle_quick_backtest` |
| 8.策略优化 | `optimizer.grid_search` | `optimizer_server._handle_grid_search` |
| 9.报告生成 | `report.generate` | `report_server._handle_generate` |

---

*创建时间: 2025-12-19 | 版本: 1.0*

---

## 🔄 工作流相关模块

### WorkflowOrchestrator
```python
from core.workflow_orchestrator import WorkflowOrchestrator

orchestrator = WorkflowOrchestrator()
result = orchestrator.identify_mainlines()
mainlines = result.details.get('top_mainlines', [])  # 注意字段名
```

### CacheManager
```python
from core.cache_manager import CacheManager

cache = CacheManager()
if cache.is_cache_valid("mainline"):
    data = cache.load_cache("mainline")
cache.save_cache("mainline", data)
```

### WorkflowStateManager
```python
from core.workflow.state_manager import get_state_manager

mgr = get_state_manager()
workflow = mgr.create_workflow("我的工作流")
mgr.start_step(workflow.workflow_id, 0)
mgr.complete_step(workflow.workflow_id, 0, {"result": "..."})
```

---

*更新时间: 2025-12-19*

---

## 🔟 十倍股早期识别系统

### TenbaggerEvaluator
```python
from mcp_servers.utils.tenbagger_evaluator import get_evaluator

evaluator = get_evaluator()
report = evaluator.evaluate(symbol, name, data)
# 返回: TenbaggerReport (包含等级、总分、阶段、维度评分等)
```

### MCP工具 (trquant-core服务器)
- `tenbagger.evaluate` - 评估单只股票
- `tenbagger.report` - 获取评估报告
- `tenbagger.rank` - 获取排名
- `tenbagger.history` - 获取历史
- `tenbagger.batch` - 批量评估
- `tenbagger.filter` - 按等级筛选
- `tenbagger.stats` - 统计信息

### StageMachine (阶段状态机)
```python
from mcp_servers.utils.stage_machine import StageMachine

sm = StageMachine()
record = sm.get_stage(symbol)
stage = record.current_stage  # S0-S5
```

### ScoreCard (7维评分卡)
```python
from mcp_servers.utils.scorecard import get_scorecard_engine

engine = get_scorecard_engine()
card = engine.compute(symbol, financial_data, stage_record)
# 返回: ScoreCard (包含7个维度评分和总分)
```

---

*更新时间: 2025-12-19*

---

## 📚 十倍股系统完整调用链

### 完整数据流调用
```python
# 1. 数据获取
from utils.datasource_manager import get_datasource_manager
manager = get_datasource_manager()
data = manager.fetch_for_tenbagger(["000001.XSHE"])

# 2. 阶段判断
from utils.stage_machine import StageMachine
sm = StageMachine()
record = sm.get_or_create("000001.XSHE")
stage = record.current_stage  # S0-S5

# 3. 评分计算
from utils.scorecard import get_scorecard_engine
engine = get_scorecard_engine()
card = engine.compute("000001.XSHE", data["financials"]["000001.XSHE"], {"current_stage": stage})
# 返回: ScoreCard (total_score, grade, dimensions)

# 4. 综合评估
from utils.tenbagger_evaluator import get_evaluator
evaluator = get_evaluator()
report = evaluator.evaluate("000001.XSHE", "股票名称", {
    "stage": stage,
    "scorecard": {"total_score": card.total_score},
    "financials": data["financials"]["000001.XSHE"]
})
# 返回: TenbaggerReport (eval_level, total_score, dimensions, strengths, risks)

# 5. MCP工具调用
from core.mcp.client import MCPClient
client = MCPClient()
result = client.call_tool("tenbagger.evaluate", {...})
```

### 数据源配置
- JQData: `config/jqdata_config.json` (已认证)
- MongoDB: `mongodb://localhost:27017/jqquant` (已连接)

---

*更新时间: 2025-12-19*
