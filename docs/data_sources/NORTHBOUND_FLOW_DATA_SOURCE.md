# 北向资金数据源使用指南

> **创建时间**: 2026-01-13  
> **最后更新**: 2026-01-13  
> **目的**: 说明如何获取北向资金最新数据

---

## 📋 数据源选择

### 推荐方案：AKShare（实时数据）

**优势**:
- ✅ **免费**: 无需付费账号
- ✅ **实时**: 数据更新及时
- ✅ **简单**: API调用简单
- ✅ **完整**: 包含沪股通、深股通详细数据

**数据范围**:
- 实时数据：当日数据
- 历史数据：支持历史查询

---

## 🔧 使用方法

### 方法1: AKShare直接调用（推荐）

#### 1.1 汇总数据API（最新推荐）

```python
import akshare as ak

# 获取沪深港通资金流向汇总
df = ak.stock_hsgt_fund_flow_summary_em()

# 筛选北向资金（沪股通+深股通）
north_df = df[df["资金方向"] == "北向"]

# 获取沪股通和深股通数据
sh_data = north_df[north_df["板块"] == "沪股通"]
sz_data = north_df[north_df["板块"] == "深股通"]

# 提取数据
if not sh_data.empty:
    sh_row = sh_data.iloc[0]
    sh_net = float(sh_row.get("成交净买额", 0)) / 1e8  # 转换为亿元
    print(f"沪股通净流入: {sh_net:.2f} 亿元")

if not sz_data.empty:
    sz_row = sz_data.iloc[0]
    sz_net = float(sz_row.get("成交净买额", 0)) / 1e8  # 转换为亿元
    print(f"深股通净流入: {sz_net:.2f} 亿元")
```

**返回字段**:
- `交易日`: 交易日期
- `板块`: 沪股通/深股通
- `资金方向`: 北向/南向
- `成交净买额`: 成交净买额（元）
- `资金净流入`: 资金净流入（元）
- `当日资金余额`: 当日资金余额
- `上涨数/持平数/下跌数`: 统计信息
- `相关指数`: 相关指数名称
- `指数涨跌幅`: 指数涨跌幅

#### 1.2 历史数据API

```python
import akshare as ak

# 获取北向资金历史数据
df = ak.stock_hsgt_hist_em(symbol='北向资金')

# 获取最新数据
latest = df.iloc[-1]
print(f"日期: {latest['日期']}")
print(f"当日成交净买额: {latest['当日成交净买额']:.2f} 亿元")
print(f"买入成交额: {latest['买入成交额']:.2f} 亿元")
print(f"卖出成交额: {latest['卖出成交额']:.2f} 亿元")
```

---

### 方法2: 使用项目封装模块（推荐）

#### 2.1 CapitalFlowAnalyzer（简单易用）

```python
from core.capital_flow import CapitalFlowAnalyzer

analyzer = CapitalFlowAnalyzer()
flows = analyzer.get_northbound_flow(days=20)  # 获取20天数据

# 获取最新数据
latest = flows[-1] if flows else None
if latest:
    print(f"日期: {latest.date}")
    print(f"沪股通净流入: {latest.sh_net:.2f} 亿元")
    print(f"深股通净流入: {latest.sz_net:.2f} 亿元")
    print(f"总净流入: {latest.total_net:.2f} 亿元")
```

**返回数据结构**:
- `date`: 日期
- `sh_net`: 沪股通净流入（亿元）
- `sz_net`: 深股通净流入（亿元）
- `total_net`: 总净流入（亿元）
- `sh_buy/sz_buy`: 买入金额（亿元）
- `sh_sell/sz_sell`: 卖出金额（亿元）

#### 2.2 RealDataFetcher（实时数据）

```python
from markets.ashare.mainline.real_data_fetcher import RealDataFetcher

fetcher = RealDataFetcher()
result = fetcher.fetch_northbound_flow()

if result.success:
    data = result.data
    print(f"今日净流入: {data['today_net']:.2f} 亿元")
    print(f"周净流入: {data['week_net']:.2f} 亿元")
    print(f"月净流入: {data['month_net']:.2f} 亿元")
    
    # 详细信息
    for detail in data['details']:
        print(f"{detail['板块']}: {detail['成交净买额']:.2f} 亿元")
```

#### 2.3 NorthFundAnalyzer（支持JQData和AKShare）

```python
from core.astock_indicators import NorthFundAnalyzer

# 使用AKShare（默认）
analyzer = NorthFundAnalyzer(jq_client=None)
data = analyzer.analyze(target_date=None)  # None表示使用最新日期

print(f"日期: {data.date}")
print(f"沪股通净买入: {data.sh_net_buy:.2f} 亿元")
print(f"深股通净买入: {data.sz_net_buy:.2f} 亿元")
print(f"合计净买入: {data.net_buy_amount:.2f} 亿元")
print(f"5日累计: {data.net_buy_5d:.2f} 亿元")
print(f"10日累计: {data.net_buy_10d:.2f} 亿元")
print(f"信号评分: {data.signal_score:.2f}")
print(f"信号描述: {data.signal_description}")
```

**返回数据结构**:
- `date`: 日期
- `sh_net_buy/sz_net_buy`: 沪股通/深股通净买入（亿元）
- `net_buy_amount`: 合计净买入（亿元）
- `net_buy_5d/10d/20d`: 5日/10日/20日累计净买入（亿元）
- `signal_score`: 信号评分（-100 ~ +100）
- `signal_description`: 信号描述

---

## 📊 测试结果

### 测试时间
2026-01-13 20:16:24

### 测试结果

#### 1. AKShare直接调用
- ✅ `stock_hsgt_fund_flow_summary_em()`: 成功获取数据
- ❌ `stock_hsgt_north_net_flow_in_em()`: API不存在（可能是旧版本API）

#### 2. CapitalFlowAnalyzer
- ✅ 成功获取数据
- ✅ 数据格式正确
- ✅ 返回5条记录

#### 3. RealDataFetcher
- ✅ 数据获取成功
- ✅ 数据结构完整
- ✅ 包含详细信息和汇总数据

#### 4. NorthFundAnalyzer
- ✅ 分析成功
- ✅ 支持JQData和AKShare自动切换
- ✅ 包含信号分析和评分
- ⚠️ 返回的是历史数据（2024-08-16），这是JQData的最后一个有完整数据的日期

---

## ⚠️ 注意事项

### 1. 数据更新时间
- **实时数据**: 通常在交易日收盘后更新（约15:00-16:00）
- **历史数据**: 数据可能延迟1-2个交易日

### 2. API变更
- `stock_hsgt_north_net_flow_in_em()` 在当前AKShare版本中不存在
- 推荐使用 `stock_hsgt_fund_flow_summary_em()` 获取最新数据

### 3. JQData限制
- JQData的北向资金数据在**2024-08-18之后不再披露买卖分项**
- 仅能获取成交总额，无法计算净买入
- 适用于历史回测（2014-11 ~ 2024-08-16）

### 4. 数据单位
- AKShare返回的数据单位是**元**，需要转换为**亿元**（除以1e8）
- 项目封装模块已自动处理单位转换

---

## 🚀 推荐使用方案

### 场景1: 获取最新实时数据
```python
# 推荐: 使用CapitalFlowAnalyzer
from core.capital_flow import CapitalFlowAnalyzer

analyzer = CapitalFlowAnalyzer()
flows = analyzer.get_northbound_flow(days=1)
latest = flows[-1] if flows else None
```

### 场景2: 需要历史数据分析
```python
# 推荐: 使用NorthFundAnalyzer（支持JQData历史数据）
from core.astock_indicators import NorthFundAnalyzer

analyzer = NorthFundAnalyzer(jq_client=jq_client)  # 如果有JQData账号
data = analyzer.analyze(target_date='2024-08-16')  # 指定日期
```

### 场景3: 简单快速获取
```python
# 推荐: 直接使用AKShare
import akshare as ak

df = ak.stock_hsgt_fund_flow_summary_em()
north_df = df[df["资金方向"] == "北向"]
```

---

## 📚 相关文档

- **AKShare文档**: https://akshare.akfamily.xyz/
- **JQData文档**: https://www.joinquant.com/help/api/doc
- **项目数据源指南**: `docs/03_modules/DATA_SOURCE_DEVELOPMENT.md`
- **资金流向分析**: `docs/03_modules/FUNDS_DIMENSION_DATA_ANALYSIS.md`

---

## 🔧 快速测试

运行测试脚本：

```bash
python scripts/test_northbound_flow.py
```

测试脚本会验证：
1. AKShare直接调用
2. CapitalFlowAnalyzer封装
3. RealDataFetcher封装
4. NorthFundAnalyzer封装

---

**最后更新**: 2026-01-13  
**维护**: TRQuant Team
