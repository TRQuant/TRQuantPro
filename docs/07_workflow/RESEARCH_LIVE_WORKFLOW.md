# TRQuant 研究-实战双阶段工作流

## 概述

TRQuant采用"研究阶段"与"实战阶段"分离的双阶段架构，实现从策略研究到实盘交易的完整流程。

```
┌─────────────────────────────────────────────────────────────────┐
│                       研究阶段 (Research)                        │
│  JupyterLab + JQData + 知识库 + 开源工具(Alphalens/Optuna/Qlib) │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼ 策略转换
┌─────────────────────────────────────────────────────────────────┐
│                       实战阶段 (Live Trading)                    │
│            PTrade/QMT + 本地信号桥接 + 风控监控                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 一、研究阶段

### 1.1 环境配置

```python
# Jupyter Notebook 环境
import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

# 导入工具库
from notebooks.lib import (
    get_jqdata_client,           # JQData客户端
    search_knowledge_base,        # 知识库搜索
    save_research_conclusion,     # 保存研究结论
    analyze_factor,               # 因子分析 (Alphalens)
    optimize_strategy_params,     # 参数优化 (Optuna)
    optimize_portfolio,           # 组合优化 (PyPortfolioOpt)
)
```

### 1.2 标准化研究流程 (7个Notebook模板)

| 序号 | Notebook | 功能 | 输入 | 输出 |
|------|----------|------|------|------|
| 01 | `market_analysis.ipynb` | 市场状态分析 | JQData指数数据 | 市场状态报告 |
| 02 | `mainline_identification.ipynb` | 市场主线识别 | 行业板块数据 | 主线行业清单 |
| 03 | `candidate_pool.ipynb` | 候选池构建 | 主线+筛选条件 | 股票候选池 |
| 04 | `factor_research.ipynb` | 因子研究 | 因子数据 | IC/IR分析结果 |
| 05 | `strategy_generation.ipynb` | 策略生成 | 因子+候选池 | 策略配置 |
| 06 | `backtest_analysis.ipynb` | 回测分析 | 策略配置 | 绩效报告 |
| 07 | `optimization.ipynb` | 参数优化 | 策略+参数空间 | 最优参数 |

### 1.3 工具库说明

**位置**: `notebooks/lib/`

| 模块 | 功能 | 依赖 |
|------|------|------|
| `research_utils.py` | JQData客户端、知识库 | JQData |
| `factor_utils.py` | 因子分析 | Alphalens |
| `portfolio_utils.py` | 组合优化 | PyPortfolioOpt |
| `optim_utils.py` | 参数优化 | Optuna |
| `viz_utils.py` | 可视化 | Matplotlib/Plotly |

### 1.4 研究结论存储

```python
# 保存研究结论到知识库
save_research_conclusion(
    module="factor_research",
    findings={"momentum_20d": {"IC": 0.05, "IR": 0.8}},
    recommendation="建议使用20日动量因子",
    valid_until="2026-03-31"
)

# 加载历史结论
conclusions = load_research_conclusions(module="factor_research", limit=5)
```

---

## 二、策略转换

### 2.1 支持的转换路径

```
JQData/BulletTrade ──┬──> PTrade  (ptrade_bridge)
                     │
                     └──> QMT     (jqdata_to_qmt_converter)
```

### 2.2 JQData → PTrade

```python
from core.comprehensive_strategy_converter import convert_strategy_comprehensive

result = convert_strategy_comprehensive(
    input_path="strategies/my_strategy.py",
    output_path="strategies/my_strategy_ptrade.py"
)
```

### 2.3 JQData → QMT

```python
from core.jqdata_to_qmt_converter import convert_jqdata_to_qmt

result = convert_jqdata_to_qmt(
    input_path="strategies/my_strategy.py",
    output_path="strategies/my_strategy_qmt.py"
)
```

### 2.4 转换对照表

| JQData API | PTrade API | QMT API |
|------------|------------|---------|
| `get_price()` | `get_history()` | `xtdata.get_market_data()` |
| `get_current_data()` | `get_snapshot()` | `xtdata.get_full_tick()` |
| `order_target_value()` | `order_target_value()` | `xt_trader.order_stock()` |
| `context.portfolio.positions` | `get_positions()` | `query_stock_positions()` |
| `000001.XSHE` | `000001.SZ` | `000001.SZ` |

---

## 三、实战阶段

### 3.1 PTrade部署

```python
# ptrade_bridge/service.py
from ptrade_bridge import PTradeService

service = PTradeService()
service.deploy_strategy("strategies/my_strategy_ptrade.py")
service.start_live_trading()
```

### 3.2 QMT部署

```python
# qmt_bridge/service.py
from qmt_bridge import QMTService

service = QMTService()
service.deploy_strategy("strategies/my_strategy_qmt.py")
service.start_live_trading()
```

### 3.3 信号桥接模式

对于需要本地计算的策略，使用信号桥接：

```python
# 研究端：生成交易信号
signals = generate_signals_from_research()

# 发送到交易端
from bridge_common import BridgeClient
client = BridgeClient(platform="ptrade")
client.send_signals(signals)
```

---

## 四、知识库集成

### 4.1 查询知识库

```python
# 搜索JQData API文档
result = search_knowledge_base("get_price参数说明")

# 搜索因子库
result = search_knowledge_base("Alpha101因子", type_filter="factor")
```

### 4.2 混合检索 (RAG)

知识库支持混合检索，结合：
- 关键词精确匹配（API函数名、因子名）
- 向量语义搜索（自然语言描述）

```python
# 自动选择最佳检索模式
result = search_knowledge_base("如何获取股票的历史收盘价")
```

---

## 五、目录结构

```
TRQuant/
├── notebooks/
│   ├── lib/                    # 工具库
│   │   ├── __init__.py
│   │   ├── research_utils.py   # 研究工具
│   │   ├── factor_utils.py     # 因子分析
│   │   ├── portfolio_utils.py  # 组合优化
│   │   ├── optim_utils.py      # 参数优化
│   │   └── viz_utils.py        # 可视化
│   └── templates/              # Notebook模板
│       ├── 01_market_analysis.ipynb
│       ├── 02_mainline_identification.ipynb
│       ├── 03_candidate_pool.ipynb
│       ├── 04_factor_research.ipynb
│       ├── 05_strategy_generation.ipynb
│       ├── 06_backtest_analysis.ipynb
│       └── 07_optimization.ipynb
├── core/
│   ├── comprehensive_strategy_converter.py  # JQData→PTrade
│   └── jqdata_to_qmt_converter.py          # JQData→QMT
├── ptrade_bridge/              # PTrade桥接
├── qmt_bridge/                 # QMT桥接
└── bridge_common/              # 通用桥接
```

---

## 六、开源项目依赖

| 项目 | 用途 | 安装 |
|------|------|------|
| Alphalens | 因子分析 | `pip install alphalens-reloaded` |
| PyPortfolioOpt | 组合优化 | `pip install PyPortfolioOpt` |
| Optuna | 参数优化 | `pip install optuna` |
| Qlib | 量化平台 | `pip install pyqlib` |
| Empyrical | 绩效指标 | `pip install empyrical-reloaded` |

---

## 七、最佳实践

1. **研究结论必存**: 每次研究完成后调用`save_research_conclusion()`
2. **知识库先查**: 遇到问题先`search_knowledge_base()`
3. **转换后验证**: 策略转换后必须在目标平台回测验证
4. **版本控制**: 策略代码使用Git管理
5. **增量开发**: 复用已有工具库，避免重复开发

---

*文档版本: 1.0 | 更新时间: 2026-01-01*

