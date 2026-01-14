# AKShare资金流向接口日期限制说明

> **创建时间**: 2026-01-14  
> **测试日期**: 2026-01-13  
> **数据源**: AKShare

---

## 📅 日期限制总结

### ✅ 可以获取2026-01-13的数据

**测试结果**：
- ✅ `stock_market_fund_flow` - 大盘资金流向：**可以获取**
- ✅ `stock_sector_fund_flow_hist` - 行业资金流向历史：**可以获取**（需指定行业）
- ⚠️ `stock_sector_fund_flow_rank` - 行业资金流向排名：**'今日'指最新交易日**

---

## 🔍 各接口详细说明

### 1. stock_market_fund_flow (大盘资金流向)

**日期限制**：
- 返回最近**120个交易日**的数据
- 日期范围：约**3-6个月**
- 如果目标日期在范围内，可以直接获取

**获取2026-01-13数据**：
```python
import akshare as ak
import pandas as pd

market_flow = ak.stock_market_fund_flow()
market_flow['日期'] = pd.to_datetime(market_flow['日期'])

# 筛选目标日期
target_date = pd.to_datetime('2026-01-13')
target_data = market_flow[market_flow['日期'] == target_date]

if not target_data.empty:
    data = target_data.iloc[0]
    main_inflow = data['主力净流入-净额'] / 1e8  # 转换为亿元
    print(f"主力净流入: {main_inflow:.2f}亿元")
```

**测试结果**：
- ✅ 2026-01-13数据存在
- ✅ 数据完整（包含超大单、大单、中单、小单）
- ✅ 日期范围：2025-07-18 至 2026-01-13

---

### 2. stock_sector_fund_flow_rank (行业资金流向排名)

**日期限制**：
- `indicator="今日"`：指**最新交易日**，无法指定历史日期
- `indicator="5日"`：最近5个交易日的汇总数据
- `indicator="10日"`：最近10个交易日的汇总数据
- `indicator="20日"`：最近20个交易日的汇总数据

**获取2026-01-13数据**：
```python
import akshare as ak

# 如果2026-01-13是最新交易日，可以直接获取
sector_flow = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")

# 如果2026-01-13不是最新交易日，需要使用历史接口
# 见下面的 stock_sector_fund_flow_hist
```

**测试结果**：
- ⚠️ 无法直接指定历史日期
- ✅ 如果目标日期是最新交易日，可以获取

---

### 3. stock_sector_fund_flow_hist (行业资金流向历史)

**日期限制**：
- 返回指定行业的最近**120个交易日**的数据
- 需要指定行业名称（`symbol`参数）

**获取2026-01-13数据**：
```python
import akshare as ak
import pandas as pd

# 方法1: 获取单个行业的历史数据
industry = "互联网服务"
hist_data = ak.stock_sector_fund_flow_hist(symbol=industry)
hist_data['日期'] = pd.to_datetime(hist_data['日期'])

target_date = pd.to_datetime('2026-01-13')
target_data = hist_data[hist_data['日期'] == target_date]

if not target_data.empty:
    data = target_data.iloc[0]
    inflow = data['主力净流入-净额'] / 1e8
    print(f"{industry} 主力净流入: {inflow:.2f}亿元")

# 方法2: 汇总多个行业（模拟行业总资金流向）
sector_flow_today = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
top_industries = sector_flow_today.head(10)['名称'].tolist()

total_inflow = 0.0
for industry in top_industries:
    try:
        hist_data = ak.stock_sector_fund_flow_hist(symbol=industry)
        hist_data['日期'] = pd.to_datetime(hist_data['日期'])
        target = pd.to_datetime('2026-01-13')
        if target in hist_data['日期'].values:
            data = hist_data[hist_data['日期'] == target].iloc[0]
            total_inflow += data['主力净流入-净额'] / 1e8
    except:
        continue

print(f"行业总主力净流入: {total_inflow:.2f}亿元")
```

**测试结果**：
- ✅ 可以获取指定行业的历史数据
- ✅ 2026-01-13数据存在
- ⚠️ 需要遍历多个行业并汇总才能得到总数据

---

## 📊 日期范围说明

### 数据更新规则

1. **实时数据**：
   - 交易时间内：实时更新
   - 盘后：通常在**T+1日**更新（即次日更新）

2. **历史数据**：
   - 返回最近**120个交易日**（约3-6个月）
   - 如果目标日期在范围内，可以获取
   - 如果目标日期不在范围内，需要等待数据更新

3. **未来日期**：
   - 无法获取未来日期的数据
   - 需要等待数据更新（通常T+1日）

---

## 💡 获取指定日期数据的建议

### 方案1: 直接筛选（推荐）

```python
import akshare as ak
import pandas as pd

target_date = "2026-01-13"

# 大盘资金流向
market_flow = ak.stock_market_fund_flow()
market_flow['日期'] = pd.to_datetime(market_flow['日期'])
target_data = market_flow[market_flow['日期'] == pd.to_datetime(target_date)]

if not target_data.empty:
    # 使用数据
    pass
else:
    print(f"⚠️  {target_date}数据不在返回列表中")
```

### 方案2: 使用历史接口（行业数据）

```python
# 获取行业列表
sector_flow = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
industries = sector_flow['名称'].tolist()

# 遍历获取历史数据
total_inflow = 0.0
for industry in industries:
    hist_data = ak.stock_sector_fund_flow_hist(symbol=industry)
    # 筛选目标日期
    # ...
```

---

## ⚠️ 注意事项

1. **日期格式**：
   - 使用`pd.to_datetime()`统一日期格式
   - 注意时区问题（中国时区UTC+8）

2. **数据延迟**：
   - 实时数据可能有延迟
   - 历史数据通常在T+1日更新

3. **数据范围**：
   - 所有接口返回最近120个交易日
   - 如果目标日期不在范围内，无法获取

4. **单位统一**：
   - 东方财富接口：单位是**元**，需除以1e8转换为**亿元**
   - 同花顺接口：单位已经是**亿元**

---

## ✅ 对于2026-01-13的结论

**可以获取**：
- ✅ 大盘资金流向：可以直接获取
- ✅ 行业资金流向：可以通过`stock_sector_fund_flow_hist`获取（需指定行业）

**日期限制**：
- 📅 返回最近120个交易日（约3-6个月）
- 📅 如果目标日期在范围内，可以获取
- 📅 如果目标日期不在范围内，需要等待数据更新

**当前状态**：
- ✅ 2026-01-13数据已确认存在
- ✅ 数据完整可用

---

**更新时间**: 2026-01-14
