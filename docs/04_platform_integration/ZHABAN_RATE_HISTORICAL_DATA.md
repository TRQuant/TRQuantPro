# 炸板率历史数据获取指南

## 📊 概述

炸板率是陈小群战法的重要指标之一，用于判断市场情绪和风险。本文档说明如何获取历史炸板率数据，特别是回测场景下的使用方法。

---

## 🔍 数据源说明

### AKShare炸板过程接口

**接口**: `ak.stock_zt_pool_zbgc_em(date='YYYYMMDD')`

**特点**:
- ✅ **支持历史日期参数**：可以指定历史日期获取数据
- ⚠️ **只能获取近期数据**：根据AKShare文档，该接口"只能获取近期的数据"
- 📅 **实际可用范围**：通常可以获取最近1-3个月的历史数据（具体取决于数据源）

**示例**:
```python
import akshare as ak

# 获取2024年10月11日的炸板数据
zhaban_data = ak.stock_zt_pool_zbgc_em(date='20241011')
```

---

## 🛠️ 统一工具：`ZhabanRateFetcher`

### 功能特性

1. **自动降级方案**：优先使用AKShare接口，失败时自动降级
2. **数据缓存**：避免重复请求，提高效率
3. **批量获取**：支持批量获取历史日期范围的数据
4. **错误处理**：自动重试和估算值填充

### 基本使用

#### 1. 获取单日炸板率

```python
from core.market_data.zhaban_rate_fetcher import get_zhaban_rate

# 获取指定日期的炸板率
result = get_zhaban_rate('20260114', limit_up_count=102)

print(f"日期: {result['date']}")
print(f"炸板数量: {result['zhaban_count']}只")
print(f"涨停成功: {result['limit_up_count']}只")
print(f"炸板率: {result['zhaban_rate']:.2f}%")
print(f"数据来源: {result['source']}")  # 'akshare'/'fallback'/'estimated'
```

**返回结果**:
```python
{
    'date': '20260114',
    'zhaban_count': 59,
    'limit_up_count': 102,
    'zhaban_rate': 36.65,
    'total_attempts': 161,
    'source': 'akshare',  # 或 'fallback'/'estimated'
    'success': True
}
```

#### 2. 批量获取历史数据

```python
from core.market_data.zhaban_rate_fetcher import get_historical_zhaban_rates

# 批量获取2024年10月的数据
df = get_historical_zhaban_rates(
    start_date='2024-10-01',
    end_date='2024-10-31'
)

print(df.head())
```

**输出**:
```
        date  zhaban_count  limit_up_count  zhaban_rate  total_attempts      source  success
0  20241001            45             120        27.27             165     akshare     True
1  20241002            38             115        24.84             153     akshare     True
2  20241003            52             130        28.57             182     akshare     True
...
```

#### 3. 高级使用（带缓存）

```python
from core.market_data.zhaban_rate_fetcher import ZhabanRateFetcher

# 创建获取器（启用缓存）
fetcher = ZhabanRateFetcher(cache_enabled=True)

# 获取单日数据
result1 = fetcher.get_zhaban_rate('20260114', limit_up_count=102)

# 再次获取相同日期（从缓存读取）
result2 = fetcher.get_zhaban_rate('20260114', limit_up_count=102)  # 快速返回

# 批量获取
df = fetcher.get_historical_zhaban_rates(
    start_date='2024-10-01',
    end_date='2024-10-31',
    delay_between_requests=0.5  # 请求间隔0.5秒，避免频率限制
)

# 清空缓存
fetcher.clear_cache()
```

---

## 📈 回测场景使用

### 场景1：近期历史数据回测（1-3个月）

**适用**：回测最近1-3个月的数据

```python
from core.market_data.zhaban_rate_fetcher import get_historical_zhaban_rates
import pandas as pd

# 获取最近3个月的炸板率数据
end_date = '2026-01-14'
start_date = '2025-10-14'  # 3个月前

zhaban_rates_df = get_historical_zhaban_rates(
    start_date=start_date,
    end_date=end_date
)

# 与回测结果合并
backtest_results = pd.DataFrame({
    'date': ['2025-10-14', '2025-10-15', ...],
    'return': [0.02, -0.01, ...],
    ...
})

# 合并炸板率数据
merged = backtest_results.merge(
    zhaban_rates_df[['date_std', 'zhaban_rate']],
    left_on='date',
    right_on='date_std',
    how='left'
)
```

### 场景2：长期历史数据回测（超过3个月）

**问题**：AKShare接口可能无法获取更早的历史数据

**解决方案**：

#### 方案A：使用估算值（推荐）

```python
from core.market_data.zhaban_rate_fetcher import ZhabanRateFetcher

fetcher = ZhabanRateFetcher()

# 批量获取（自动使用估算值填充缺失数据）
df = fetcher.get_historical_zhaban_rates(
    start_date='2024-01-01',
    end_date='2024-12-31'
)

# 检查数据来源
print(df['source'].value_counts())
# akshare: 近期数据（真实值）
# estimated: 早期数据（估算值，15%）
```

#### 方案B：从其他数据源推算

```python
import jqdatasdk as jq
import pandas as pd

def estimate_zhaban_rate_from_price_data(date: str) -> float:
    """
    从价格数据推算炸板率
    
    思路：
    1. 获取当日所有股票的涨跌幅
    2. 统计涨跌幅在9%-9.5%之间的股票（可能是炸板）
    3. 统计涨停股票数量
    4. 计算炸板率
    """
    # 获取所有股票当日价格
    all_stocks = jq.get_all_securities(types=['stock'], date=date)
    
    # 获取价格数据
    prices = jq.get_price(
        all_stocks.index.tolist(),
        start_date=date,
        end_date=date,
        frequency='daily',
        fields=['close', 'paused']
    )
    
    # 计算涨跌幅（需要前一日收盘价）
    # ... 具体实现 ...
    
    # 统计炸板股票（涨跌幅9%-9.5%）
    # 统计涨停股票（涨跌幅>=9.95%）
    
    # 计算炸板率
    # ...
    
    return zhaban_rate
```

#### 方案C：使用历史平均值

```python
# 如果无法获取历史数据，使用市场历史平均值
HISTORICAL_AVERAGE_ZHABAN_RATE = 15.0  # 15%

# 在回测中使用
for date in backtest_dates:
    # 尝试获取真实数据
    result = get_zhaban_rate(date)
    
    if result['source'] == 'estimated' or not result['success']:
        # 使用历史平均值
        zhaban_rate = HISTORICAL_AVERAGE_ZHABAN_RATE
    else:
        zhaban_rate = result['zhaban_rate']
```

---

## ⚠️ 注意事项

### 1. 数据可用性

- **近期数据（1-3个月）**：✅ 通常可用，使用AKShare接口
- **中期数据（3-12个月）**：⚠️ 部分可用，部分需要估算
- **长期数据（>12个月）**：❌ 通常不可用，需要使用估算值

### 2. 请求频率限制

批量获取历史数据时，建议设置请求间隔：

```python
df = get_historical_zhaban_rates(
    start_date='2024-10-01',
    end_date='2024-10-31',
    delay_between_requests=0.5  # 每次请求间隔0.5秒
)
```

### 3. 数据准确性

| 数据来源 | 准确性 | 说明 |
|---------|--------|------|
| `akshare` | ⭐⭐⭐⭐⭐ | 最准确，来自官方炸板过程接口 |
| `fallback` | ⭐⭐⭐ | 降级方案，可能低估（只统计收盘时9%-9.5%的股票） |
| `estimated` | ⭐⭐ | 估算值（15%），仅供参考 |

### 4. 回测建议

1. **优先使用真实数据**：对于近期数据，尽量使用AKShare接口获取真实值
2. **估算值标注**：在回测报告中明确标注哪些日期使用了估算值
3. **敏感性分析**：测试不同估算值（10%、15%、20%）对回测结果的影响
4. **数据验证**：对比真实数据和估算值，评估估算方法的准确性

---

## 📝 示例：完整回测流程

```python
from core.market_data.zhaban_rate_fetcher import get_historical_zhaban_rates
import pandas as pd
import jqdatasdk as jq

# 1. 认证JQData
jq.auth('username', 'password')

# 2. 获取回测日期范围
start_date = '2024-10-01'
end_date = '2024-12-31'
trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)

# 3. 获取历史炸板率数据
print("📊 获取历史炸板率数据...")
zhaban_rates_df = get_historical_zhaban_rates(
    start_date=start_date,
    end_date=end_date
)

# 4. 检查数据质量
print("\n📊 数据质量统计:")
print(f"总日期数: {len(trade_days)}")
print(f"成功获取: {zhaban_rates_df['success'].sum()}")
print(f"数据来源分布:")
print(zhaban_rates_df['source'].value_counts())

# 5. 与回测结果合并
backtest_results = []  # 你的回测结果

for date in trade_days:
    date_str = date.strftime('%Y-%m-%d')
    date_compact = date.strftime('%Y%m%d')
    
    # 查找对应的炸板率
    zhaban_info = zhaban_rates_df[zhaban_rates_df['date'] == date_compact]
    
    if not zhaban_info.empty:
        zhaban_rate = zhaban_info.iloc[0]['zhaban_rate']
        source = zhaban_info.iloc[0]['source']
    else:
        # 使用估算值
        zhaban_rate = 15.0
        source = 'estimated'
    
    # 执行回测逻辑
    # ...
    
    backtest_results.append({
        'date': date_str,
        'zhaban_rate': zhaban_rate,
        'zhaban_rate_source': source,
        # ... 其他回测指标
    })

# 6. 分析结果
results_df = pd.DataFrame(backtest_results)

# 按数据来源分组分析
print("\n📊 按数据来源分析回测结果:")
for source in ['akshare', 'fallback', 'estimated']:
    subset = results_df[results_df['zhaban_rate_source'] == source]
    if not subset.empty:
        print(f"\n{source}:")
        print(f"  样本数: {len(subset)}")
        print(f"  平均收益率: {subset['return'].mean():.2%}")
        # ... 其他统计指标
```

---

## 🔗 相关文档

- [AKShare数据源文档](../data_sources/AKSHARE_DATA_SOURCE.md)
- [陈小群战法回测指南](../strategies/CHEN_XIAOQUN_BACKTEST.md)
- [市场情绪分析工具](../core/MARKET_SENTIMENT_ANALYZER.md)

---

**最后更新**: 2026-01-14  
**维护者**: TRQuant Team
