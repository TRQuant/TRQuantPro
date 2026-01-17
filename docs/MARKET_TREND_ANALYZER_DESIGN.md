# MarketTrendAnalyzer 设计文档

> **版本**: v1.0  
> **基线**: TrendAnalyzer + SimpleHMM (已回测验证)  
> **创建日期**: 2026-01-05

---

## 1. 概述

`MarketTrendAnalyzer` 是市场趋势分析的核心模块，用于识别周、月、季三个周期的市场趋势，并输出供下游模块直接使用的工作流参数。

### 1.1 设计目标

- **多周期趋势识别**: 周(5交易日) / 月(21交易日) / 季(63交易日)
- **融合模型**: TrendAnalyzer (0.8) + SimpleHMM (0.2) 加权
- **标准化输出**: 统一的 `MarketTrendSignal` 数据结构
- **工作流集成**: 直接输出 `workflow_params` 和 `investment_universe_filters`
- **回测友好**: 严格支持历史日期 (`as_of_date`)，不使用未来数据

### 1.2 基线说明

| 模块 | 文件 | 说明 |
|------|------|------|
| TrendAnalyzer | `core/trend_analyzer.py` | 8维技术指标体系，已回测验证 |
| SimpleHMM | `core/trend_ml.py` | 改进版HMM，A股特色参数 |

**注意**: 不使用 `TrendAnalyzerV2` 或 `HMMV2`，以保持与已回测基线的一致性。

---

## 2. 周期口径定义

### 2.1 标准周期

| 周期 | 交易日 | 说明 | 状态 |
|------|--------|------|------|
| week | 5 | 周度趋势 | ✅ 已实现 |
| month | 21 | 月度趋势 | ✅ 已实现 |
| quarter | 63 | 季度趋势 | ✅ 已实现 |
| half_year | 126 | 半年趋势 | 预留入口 |
| year | 252 | 年度趋势 | 预留入口 |
| multi_year | 756 | 多年趋势 | 预留入口 |

### 2.2 配置方式

```python
PERIOD_CONFIG = {
    "week": 5,
    "month": 21,
    "quarter": 63,
    "half_year": 126,  # 预留
    "year": 252,       # 预留
    "multi_year": 756, # 预留
}

ACTIVE_PERIODS = ["week", "month", "quarter"]  # 当前激活
```

---

## 3. 权重配置

### 3.1 模型权重

| 模型 | 权重 | 说明 |
|------|------|------|
| TrendAnalyzer | 0.8 | 技术指标主导 |
| SimpleHMM | 0.2 | 隐状态辅助 |

### 3.2 指标权重 (TrendAnalyzer 8维体系)

| 指标 | 权重 | 说明 |
|------|------|------|
| MA | 0.20 | 均线系统 |
| MACD | 0.18 | 动能指标 |
| RSI | 0.10 | 超买超卖 |
| BB | 0.10 | 布林带 |
| VOL | 0.12 | 成交量 |
| KDJ | 0.10 | 随机指标 |
| ADX | 0.10 | 趋势强度 |
| FLOW | 0.10 | 资金流向 |

### 3.3 未来扩展

权重模型预留非线性扩展入口，可替换为:
- 动态权重 (基于波动率/一致性)
- 机器学习权重 (训练优化)

---

## 4. 数据结构定义

### 4.1 MarketTrendAnalyzerConfig

```python
@dataclass
class MarketTrendAnalyzerConfig:
    periods: Dict[str, int]           # 周期窗口
    active_periods: List[str]         # 激活周期
    weights: Dict[str, float]         # 模型权重
    data_source_priority: List[str]   # 数据源优先级
    indicator_weights: Dict[str, float]  # 指标权重
```

### 4.2 MarketTrendSignal (核心输出)

```python
@dataclass
class MarketTrendSignal:
    date: str                         # 分析日期
    index_code: str                   # 指数代码
    period_signals: Dict[str, PeriodSignal]  # 各周期信号
    hmm_signal: Optional[HMMSignal]   # HMM信号
    ensemble_score: float             # 综合得分 (-100 ~ +100)
    ensemble_direction: TrendDirection  # 综合方向
    ensemble_confidence: float        # 置信度
    workflow_params: WorkflowParams   # 工作流参数
    investment_universe_filters: InvestmentUniverseFilters  # 投资标的筛选
```

### 4.3 WorkflowParams (下游直接使用)

```python
@dataclass
class WorkflowParams:
    position_target: float            # 目标仓位 (0-1)
    risk_budget: float                # 风险预算
    allowed_actions: Dict[str, bool]  # 允许操作
    rebalance_frequency: str          # 调仓频率
    regime_tag: str                   # 市场状态标签
```

### 4.4 InvestmentUniverseFilters (投资标的筛选)

```python
@dataclass
class InvestmentUniverseFilters:
    min_momentum_score: float         # 最小动量得分
    min_trend_score: float            # 最小趋势得分
    max_volatility: float             # 最大波动率
    sector_preferences: List[str]     # 偏好板块
    avoid_sectors: List[str]          # 回避板块
```

---

## 5. 数据流

```
┌─────────────────────────────────────────────────────────────┐
│                     Notebook 配置                           │
│  - PERIOD_CONFIG, ACTIVE_PERIODS                           │
│  - WEIGHT_CONFIG, BACKTEST_START/END                       │
│  - VERSION_TAG, SAMPLE_INTERVAL                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     检查模块                                │
│  1. 查缓存 (config_hash 精确匹配)                          │
│  2. 查MongoDB (最新结果)                                    │
│  → 命中: 加载结果，跳过运行                                 │
│  → 未命中: 执行运行模块                                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 MarketTrendAnalyzer                         │
│  ┌──────────────┐    ┌──────────────┐                      │
│  │ TrendAnalyzer│    │  SimpleHMM   │                      │
│  │  (0.8权重)   │    │  (0.2权重)   │                      │
│  └──────┬───────┘    └──────┬───────┘                      │
│         │                   │                               │
│         └───────┬───────────┘                               │
│                 ▼                                           │
│         加权融合 → MarketTrendSignal                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     保存模块                                │
│  → MarketTrendStorage.save_backtest_result()               │
│  → version_tag, config_hash, algorithm_version             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              结果列表 / 可视化 / 对比                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 回测原则

### 6.1 时间区间策略

| 阶段 | 区间 | 目的 |
|------|------|------|
| 短周期快速验证 | 3个月 | 验证代码能跑通 |
| 长周期完整验证 | 3年+ | 验证预测准确性 |

### 6.2 数据集切分

```python
TRAIN_RATIO = 0.7  # 70% 训练集, 30% 验证集
```

### 6.3 结果管理原则

1. **相同配置不重复**: 基于 `config_hash` 判断
2. **优先缓存**: cache → MongoDB 两级查找
3. **必须带版本标签**: `version_tag` 用于区分不同运行
4. **不覆盖历史**: 使用 upsert 策略

### 6.4 严格历史数据

- `as_of_date` 参数必须是历史日期
- 所有数据获取必须使用 `end_date=as_of_date`
- 禁止使用 `date.today()` 获取数据

---

## 7. Notebook 工作流

### 7.1 标准章节结构

| 章节 | 内容 | 独立Cell |
|------|------|----------|
| 1 | 环境与路径 | ✅ |
| 2 | 全局配置 | ✅ |
| 3 | 连接检查 | ✅ |
| 4 | 检查模块 | ✅ |
| 5 | 运行模块 | ✅ |
| 6 | 保存模块 | ✅ |
| 7 | 结果列表 | ✅ |
| 8 | 可视化 | ✅ |
| 9 | 版本对比 | ✅ |

### 7.2 配置变量命名

```python
# 周期
PERIOD_CONFIG = {...}
ACTIVE_PERIODS = [...]

# 权重
WEIGHT_CONFIG = {"trend": 0.8, "hmm": 0.2}

# 回测区间
BACKTEST_START = "2024-06-01"
BACKTEST_END = "2024-08-31"

# 采样
SAMPLE_INTERVAL = 5

# 版本
VERSION_TAG = "dev_20260105_120000"
```

---

## 8. 文件清单

| 文件 | 说明 |
|------|------|
| `core/market_trend_analyzer.py` | 核心分析器 |
| `core/trend_analyzer.py` | TrendAnalyzer (基线) |
| `core/trend_ml.py` | SimpleHMM (基线) |
| `core/market_trend_storage.py` | 存储与缓存 |
| `notebooks/research/01_Market_Trend_Analyzer.ipynb` | 开发版Notebook |
| `docs/MARKET_TREND_ANALYZER_DESIGN.md` | 本文档 |

---

## 9. 验收标准

- [ ] Notebook 具备 9 个独立章节 Cell
- [ ] 同参重复运行不触发回测 (命中缓存/MongoDB)
- [ ] 保存结果带 `version_tag`
- [ ] 支持结果列表选择与版本对比
- [ ] 输出字段命名统一 (`investment_universe_filters`, `workflow_params`)
- [ ] 周期口径固定 5/21/63

---

## 10. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-01-05 | 初始版本 |
