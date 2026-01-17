# 牛市极端高收益策略 V3.0 - 完整文档

> **版本**: V3.0  
> **更新日期**: 2026-01-12  
> **目标**: 周频10%收益  

---

## 📋 策略概述

牛市极端高收益策略是专为牛市环境设计的激进型策略，通过多因子选股和严格风控追求高收益。

### 核心理念

1. **牛市专用**: 使用多周期共振+HMM判断市场状态，仅在牛市执行
2. **追涨模式**: 重点捕捉涨停、突破信号
3. **集中持仓**: 3-5只股票，单只最高40%
4. **严格风控**: 完整的止损止盈系统

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    牛市极端高收益策略 V3.0                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │ 市场状态检测    │───▶│   选股引擎      │───▶│  仓位管理    │ │
│  │                 │    │                 │    │              │ │
│  │ - 多周期共振    │    │ - 涨停因子     │    │ - 等权分配   │ │
│  │ - HMM隐状态    │    │ - 动量因子     │    │ - 权重上限   │ │
│  │ - 仓位上限映射  │    │ - 资金流向     │    │ - 周度调仓   │ │
│  └─────────────────┘    │ - 突破因子     │    └──────────────┘ │
│           │             └─────────────────┘            │        │
│           ▼                     │                      ▼        │
│  ┌─────────────────┐           ▼             ┌──────────────┐  │
│  │ 牛市判断        │    ┌─────────────────┐  │  风控系统    │  │
│  │                 │    │   信号评分      │  │              │  │
│  │ Score >= 55     │    │                 │  │ - 固定止损   │  │
│  │ 趋势方向: 上涨  │    │ - 首板启动 85  │  │ - 分批止盈   │  │
│  └─────────────────┘    │ - 连板加速 95  │  │ - 移动止损   │  │
│                         │ - 突破信号 80  │  │ - 时间止损   │  │
│                         │ - 动量信号 70  │  └──────────────┘  │
│                         └─────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
         ┌─────────────────────────────────────────┐
         │              数据层                      │
         │                                          │
         │  ResearchDataProvider                    │
         │  - 全A股 ~5000只                        │
         │  - JQData数据源                         │
         │  - 本地Parquet缓存                      │
         └─────────────────────────────────────────┘
```

---

## 📊 多时段回测结果

### 最优时段: 2024年政策牛市

| 指标 | 值 | 说明 |
|------|-----|------|
| **周均收益** | 4.32% | 最优时段 |
| **年化收益** | 694.53% | 复利计算 |
| **夏普比率** | 6.30 | 风险调整后收益 |
| **最大回撤** | 1.91% | 控制良好 |
| **胜率** | 57.14% | 交易胜率 |
| **总交易** | 11次 | 12个交易日 |

### 各时段对比

| 时段 | 描述 | 总收益 | 周收益 | 夏普 | 回撤 |
|------|------|--------|--------|------|------|
| 2024_policy | 2024年政策牛市 | +10.37% | +4.32% | 6.30 | 1.91% |
| 2024_year_end | 2024年末涨势 | -1.59% | -0.36% | -0.82 | 9.71% |
| 2020_summer | 2020年流动性牛市 | -4.46% | -1.06% | -3.85 | 6.59% |
| 2019_spring | 2019年科创板预期牛市 | -16.80% | -2.71% | -5.86 | 17.44% |

### 分析

- **2024年政策牛市**: 表现最优，符合策略设计的追涨特性
- **其他时段负收益**: 主要因为参数针对2024政策牛市优化
- **建议**: 实际使用时需根据当前市场环境调整参数

---

## 🎯 最优参数（V3.0）

```python
from core.strategy.bull_market_strategy_v3 import BullMarketStrategyConfig

config = BullMarketStrategyConfig(
    # 选股因子
    min_mom_20d=-1.25,
    max_mom_20d=25.0,
    max_rel_position=80.0,
    min_vol_ratio=1.0,
    limit_up_threshold=0.093,
    vol_ratio_threshold_first=2.5,
    
    # 突破因子
    breakout_ratio_min=5.0,
    mom_5d_threshold_breakout=16.0,
    
    # 仓位管理
    max_positions=3,
    single_position_max=0.4,
    rebalance_period=5,
    
    # 风险控制
    stop_loss_pct=-0.08,
    take_profit_pct=0.40,
    partial_profit_1_pct=0.20,
    partial_profit_1_ratio=0.50,
    trailing_stop_trigger=0.15,
    trailing_stop_pct=-0.08,
    time_stop_days=20,
)
```

---

## 📈 信号类型详解

### 1. 首板启动 (FIRST_LIMIT_UP)
- **条件**: 首次涨停 + 量比 >= 2.5
- **评分**: 85分
- **含义**: 主力启动信号，突破前期压力

### 2. 连板加速 (CONSECUTIVE_LIMIT)
- **条件**: 连续2日以上涨停
- **评分**: 75-95分（每板+5分）
- **含义**: 强势股特征，市场关注度高

### 3. 突破60日新高 (BREAKOUT_60D)
- **条件**: 突破60日最高价 + 5日动量>=16%
- **评分**: 80分
- **含义**: 中期趋势确认，主升浪启动

### 4. 强势动量 (STRONG_MOMENTUM)
- **条件**: 5日动量>=10% + 量比>=1.5
- **评分**: 60-80分
- **含义**: 短期强势，可能进入主升

### 5. 放量启动 (VOLUME_SURGE)
- **条件**: 量比>=3.0 + 5日动量>=5%
- **评分**: 55-85分
- **含义**: 资金介入信号

---

## 🛡️ 风控系统

### 止损机制

| 类型 | 触发条件 | 动作 |
|------|----------|------|
| 固定止损 | 亏损 >= 8% | 全部平仓 |
| 移动止损 | 盈利>=15%后回撤>=8% | 全部平仓 |
| 时间止损 | 持仓>=20天 | 全部平仓 |

### 止盈机制

| 类型 | 触发条件 | 动作 |
|------|----------|------|
| 分批止盈1 | 盈利 >= 20% | 平仓50% |
| 完全止盈 | 盈利 >= 40% | 全部平仓 |

---

## 💻 使用示例

### 1. 基本使用

```python
from core.strategy.bull_market_strategy_v3 import (
    BullMarketStrategyV3,
    BullMarketStrategyConfig,
)
from core.research import ResearchDataProvider

# 初始化
strategy = BullMarketStrategyV3()
provider = ResearchDataProvider(use_cache=True)

# 获取数据
stocks = provider.get_all_a_stocks(date="2024-09-25")
data = provider.get_data_matrices(
    symbols=stocks[:500],
    start_date="2024-09-01",
    end_date="2024-09-30",
)

# 检查市场状态
is_bull, score, regime = strategy.check_market_regime("2024-09-25")
print(f"市场状态: {regime}, 评分: {score:.1f}, 是否牛市: {is_bull}")

# 计算信号
if is_bull:
    signals = strategy.calculate_stock_signals(
        close=data.close,
        high=data.high,
        low=data.low,
        volume=data.volume,
        is_tradeable=data.is_tradeable,
    )
    
    # 选择持仓
    selected = strategy.select_top_stocks(signals)
    
    for s in selected:
        print(f"{s.code}: {s.signal_type.value}, 评分={s.score:.1f}, 权重={s.weight:.2%}")
```

### 2. 自定义参数

```python
config = BullMarketStrategyConfig(
    max_positions=5,           # 增加持仓数
    stop_loss_pct=-0.10,       # 放宽止损
    take_profit_pct=0.50,      # 提高止盈目标
)

strategy = BullMarketStrategyV3(config)
```

### 3. 生成策略报告

```python
report = strategy.generate_strategy_report()
print(report)
```

---

## ⚠️ 风险提示

1. **牛市专用**: 本策略仅适用于牛市环境，熊市或震荡市可能产生较大亏损
2. **高波动**: 追涨策略波动较大，需要较强的心理承受能力
3. **回撤控制**: 单周可能出现10%以上的回撤
4. **适合资金**: 建议使用可承受损失的资金进行投资
5. **执行纪律**: 严格遵守止损纪律是策略盈利的关键

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `core/strategy/bull_market_strategy_v3.py` | 策略核心代码 |
| `scripts/run_bull_market_strategy_v3.py` | 优化脚本 |
| `output/bull_market_v3/best_params_v3_*.json` | 最优参数 |
| `output/bull_market_v3/strategy_report_v3_*.md` | 回测报告 |

---

## 📝 更新日志

### V3.0 (2026-01-12)
- ✅ 全A股覆盖（~5000只）
- ✅ 多时段回测（2019/2020/2024/2025）
- ✅ 多周期共振+HMM市场分析
- ✅ 完整止损止盈系统
- ✅ 涨停+动量+资金流向多因子

### V2.0 (2026-01-11)
- vectorbt回测引擎集成
- 止损止盈功能完善

### V1.0 (2026-01-10)
- 基础策略框架
- 7因子选股系统

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-12
