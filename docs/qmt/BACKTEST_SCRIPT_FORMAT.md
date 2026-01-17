# 回测脚本格式详细说明

## 📋 回测脚本格式

**文件**: `scripts/run_ai_theme_recent_month.py`

**格式类型**: **TRQuant独立Python回测脚本**（不是聚宽策略格式，也不是QMT格式）

---

## 🔍 格式识别

### 回测脚本特征

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI主题股票 - 近一个月回测
使用VBTBacktestV5专业回测引擎
"""

import jqdatasdk as jq  # 使用JQData（聚宽数据源）
from core.research.vbt_backtest_v5 import VBTBacktestV5  # TRQuant回测引擎
from core.research.data_provider import DataMatrices
from core.research.signals import SignalMatrices

# 1. 数据获取（使用JQData API）
price_df = jq.get_price(
    stocks,
    start_date=start_date,
    end_date=end_date,
    frequency='daily',
    fields=['open', 'close', 'high', 'low', 'volume'],
)

# 2. 构建数据矩阵
data = DataMatrices(
    close=close,
    open=open_,
    high=high,
    low=low,
    volume=volume,
    is_tradeable=is_tradeable,
)

# 3. 构建信号矩阵
signals = SignalMatrices(
    entries=entries,
    exits=exits,
    scores=scores,
    target_weights=target_weights,
    rebalance_mask=rebalance_mask,
)

# 4. 运行回测
backtest = VBTBacktestV5(
    initial_cash=1_000_000,
    commission_rate=0.0001,
    stamp_duty=0.001,
    ...
)

backtest_result = backtest.run_with_signals(
    data=data,
    signals=signals,
    params=params,
)
```

---

## 📊 三种代码格式对比

### 1. 回测脚本格式（刚才使用的）

| 项目 | 回测脚本格式 |
|------|------------|
| **文件类型** | 独立Python脚本 |
| **数据源** | JQData (聚宽数据API) |
| **回测引擎** | VBTBacktestV5 (TRQuant自研) |
| **数据结构** | DataMatrices, SignalMatrices |
| **执行方式** | 命令行运行 `python script.py` |
| **使用场景** | 本地回测、研究、验证 |

**关键特征**:
- ✅ 使用 `jqdatasdk` 获取数据
- ✅ 使用 `VBTBacktestV5` 回测引擎
- ✅ 使用 `DataMatrices` / `SignalMatrices` 数据结构
- ✅ 独立运行，不依赖平台

---

### 2. 聚宽策略格式

| 项目 | 聚宽策略格式 |
|------|------------|
| **文件类型** | 聚宽平台策略代码 |
| **数据源** | 聚宽平台内置 |
| **回测引擎** | 聚宽平台内置 |
| **数据结构** | context, data |
| **执行方式** | 在聚宽平台运行 |
| **使用场景** | 聚宽平台回测、实盘 |

**关键特征**:
- ✅ `def initialize(context):`
- ✅ `def handle_data(context, data):`
- ✅ 使用 `history()`, `get_price()` 获取数据
- ✅ 使用 `order()` 下单
- ✅ 必须在聚宽平台运行

---

### 3. QMT策略格式

| 项目 | QMT策略格式 |
|------|------------|
| **文件类型** | QMT平台策略代码 |
| **数据源** | QMT平台内置 |
| **回测引擎** | QMT平台内置 |
| **数据结构** | ContextInfo |
| **执行方式** | 在QMT客户端运行 |
| **使用场景** | QMT回测、实盘 |

**关键特征**:
- ✅ `#coding:gbk`
- ✅ `def init(ContextInfo):`
- ✅ `def handlebar(ContextInfo):`
- ✅ 使用 `ContextInfo.get_history_data()` 获取数据
- ✅ 必须在QMT客户端运行

---

## 🔄 格式对比表

| 特征 | 回测脚本（刚才用的） | 聚宽策略 | QMT策略 |
|------|---------------------|---------|---------|
| **文件类型** | 独立Python脚本 | 平台策略代码 | 平台策略代码 |
| **数据源** | JQData API | 聚宽平台 | QMT平台 |
| **回测引擎** | VBTBacktestV5 | 聚宽内置 | QMT内置 |
| **执行方式** | `python script.py` | 聚宽平台 | QMT客户端 |
| **数据获取** | `jq.get_price()` | `history()` | `ContextInfo.get_history_data()` |
| **回测调用** | `backtest.run_with_signals()` | 平台自动 | 平台自动 |
| **编码** | UTF-8 | UTF-8 | GBK |
| **独立性** | ✅ 完全独立 | ❌ 依赖平台 | ❌ 依赖平台 |

---

## 📝 回测脚本详细说明

### 文件位置
```
scripts/run_ai_theme_recent_month.py
```

### 格式确认

✅ **TRQuant独立Python回测脚本**

### 技术栈

1. **数据源**: JQData (聚宽数据API)
   ```python
   import jqdatasdk as jq
   jq.auth(username, password)
   price_df = jq.get_price(stocks, start_date, end_date, ...)
   ```

2. **回测引擎**: VBTBacktestV5 (TRQuant自研)
   ```python
   from core.research.vbt_backtest_v5 import VBTBacktestV5
   backtest = VBTBacktestV5(initial_cash=1_000_000, ...)
   backtest_result = backtest.run_with_signals(data, signals, params)
   ```

3. **数据结构**: DataMatrices / SignalMatrices
   ```python
   from core.research.data_provider import DataMatrices
   from core.research.signals import SignalMatrices
   
   data = DataMatrices(close=..., open=..., ...)
   signals = SignalMatrices(entries=..., exits=..., ...)
   ```

### 执行流程

```python
# 1. 数据获取（JQData）
price_df = jq.get_price(stocks, start_date, end_date, ...)

# 2. 数据转换（转换为DataMatrices）
data = build_data_matrices(stocks, start_date, end_date)

# 3. 信号生成（构建SignalMatrices）
signals = build_signals_from_stocks(data, selected_stocks, ...)

# 4. 回测执行（VBTBacktestV5）
backtest = VBTBacktestV5(...)
result = backtest.run_with_signals(data, signals, params)

# 5. 结果输出
print(f"总收益: {result.total_return:.2f}%")
```

---

## ⚠️ 重要区别

### 1. 数据源 vs 平台

| 格式 | 数据来源 | 说明 |
|------|---------|------|
| 回测脚本 | JQData API | 使用聚宽数据，但独立运行 |
| 聚宽策略 | 聚宽平台 | 数据由平台提供 |
| QMT策略 | QMT平台 | 数据由平台提供 |

### 2. 回测引擎

| 格式 | 回测引擎 | 说明 |
|------|---------|------|
| 回测脚本 | VBTBacktestV5 | TRQuant自研，专业回测引擎 |
| 聚宽策略 | 聚宽内置 | 平台提供的回测引擎 |
| QMT策略 | QMT内置 | 平台提供的回测引擎 |

### 3. 执行环境

| 格式 | 执行环境 | 说明 |
|------|---------|------|
| 回测脚本 | 本地Python环境 | 完全独立，可离线运行 |
| 聚宽策略 | 聚宽平台 | 必须在聚宽网站运行 |
| QMT策略 | QMT客户端 | 必须在QMT软件运行 |

---

## 🎯 使用场景

### 回测脚本（刚才使用的）

✅ **适用场景**:
- 本地回测验证
- 策略研究和开发
- 快速迭代测试
- 批量回测分析

❌ **不适用场景**:
- 聚宽平台回测
- QMT平台回测
- 实盘交易（需要转换为平台格式）

### 聚宽策略格式

✅ **适用场景**:
- 聚宽平台回测
- 聚宽平台实盘

❌ **不适用场景**:
- QMT平台
- 本地独立运行

### QMT策略格式

✅ **适用场景**:
- QMT客户端回测
- QMT客户端实盘

❌ **不适用场景**:
- 聚宽平台
- 本地独立运行

---

## 📋 总结

### 刚才回测的代码格式

✅ **TRQuant独立Python回测脚本**

**特点**:
- 使用JQData作为数据源（聚宽数据API）
- 使用VBTBacktestV5作为回测引擎（TRQuant自研）
- 完全独立运行，不依赖任何平台
- 适合本地研究和验证

**不是**:
- ❌ 不是聚宽策略格式（没有initialize/handle_data）
- ❌ 不是QMT策略格式（没有init/handlebar）
- ✅ 是TRQuant自己的回测框架格式

---

**最后更新**: 2026-01-12
**文档作者**: TRQuant Team
