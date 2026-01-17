# AKShare资金流向接口完整分析

> **创建时间**: 2026-01-14  
> **数据源**: AKShare (东方财富/同花顺)  
> **状态**: ✅ 已验证可用

---

## 📊 可用接口总结

### ✅ 已验证可用的接口

| 接口名称 | 功能 | 数据源 | 速度 | 推荐度 |
|---------|------|--------|------|--------|
| `stock_market_fund_flow` | 大盘资金流向 | 东方财富 | ⚡ 快 | ⭐⭐⭐⭐⭐ |
| `stock_sector_fund_flow_rank` | 行业资金流向排名 | 东方财富 | ⚡ 快 | ⭐⭐⭐⭐⭐ |
| `stock_individual_fund_flow_rank` | 个股资金流向排名 | 东方财富 | ⚡ 较快 | ⭐⭐⭐⭐ |
| `stock_fund_flow_industry` | 行业资金流向（同花顺） | 同花顺 | ⚡ 较快 | ⭐⭐⭐ |
| `stock_fund_flow_concept` | 概念资金流向 | 同花顺 | ⚡ 较慢 | ⭐⭐⭐ |
| `stock_fund_flow_individual` | 个股资金流向 | 东方财富 | 🐌 慢 | ⭐⭐ |

---

## 🔍 详细接口分析

### 1. stock_market_fund_flow (大盘资金流向) ⭐⭐⭐⭐⭐

**接口**: `ak.stock_market_fund_flow()`

**功能**: 获取大盘资金流向数据

**字段**:
- `日期`
- `上证-收盘价`, `上证-涨跌幅`
- `深证-收盘价`, `深证-涨跌幅`
- `主力净流入-净额` (单位: 元，需除以1e8转换为亿元)
- `主力净流入-净占比` (%)
- `超大单净流入-净额`, `超大单净流入-净占比`
- `大单净流入-净额`, `大单净流入-净占比`
- `中单净流入-净额`, `中单净流入-净占比`
- `小单净流入-净额`, `小单净流入-净占比`

**优势**:
- ✅ 提供详细的分类（超大单、大单、中单、小单）
- ✅ 提供净占比（相对成交额的比例）
- ✅ 数据来源可靠（东方财富）
- ✅ 免费使用
- ✅ 速度快

**使用示例**:
```python
import akshare as ak

market_flow = ak.stock_market_fund_flow()
latest = market_flow.iloc[0]

# 单位转换（元 -> 亿元）
main_net_inflow = latest['主力净流入-净额'] / 1e8
main_net_pct = latest['主力净流入-净占比']
```

**当前状态**: ✅ 已在Notebook中使用

---

### 2. stock_sector_fund_flow_rank (行业资金流向排名) ⭐⭐⭐⭐⭐

**接口**: `ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")`

**功能**: 获取行业资金流向排名

**参数**:
- `indicator`: "今日" | "5日" | "10日" | "20日"
- `sector_type`: "行业资金流" | "概念资金流"

**字段**:
- `序号`, `名称`
- `今日涨跌幅`
- `今日主力净流入-净额` (单位: 元)
- `今日主力净流入-净占比` (%)
- `今日超大单净流入-净额`, `今日超大单净流入-净占比`
- `今日大单净流入-净额`, `今日大单净流入-净占比`
- `今日中单净流入-净额`, `今日中单净流入-净占比`
- `今日小单净流入-净额`, `今日小单净流入-净占比`
- `今日主力净流入最大股`

**优势**:
- ✅ 提供详细的分类（超大单、大单、中单、小单）
- ✅ 提供净占比
- ✅ 提供主力净流入最大股（龙头股）
- ✅ 支持多周期（今日/5日/10日/20日）
- ✅ 免费使用

**使用示例**:
```python
import akshare as ak

# 今日行业资金流向
sector_flow = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")

# 如果今日数据为空，使用5日数据
if sector_flow.empty or sector_flow['今日主力净流入-净额'].isna().all():
    sector_flow = ak.stock_sector_fund_flow_rank(indicator="5日", sector_type="行业资金流")

# 计算总净流入（转换为亿元）
total_inflow = sector_flow['今日主力净流入-净额'].sum() / 1e8
```

**当前状态**: ✅ 已在Notebook中使用

---

### 3. stock_individual_fund_flow_rank (个股资金流向排名) ⭐⭐⭐⭐

**接口**: `ak.stock_individual_fund_flow_rank(indicator="今日")`

**功能**: 获取个股资金流向排名

**参数**:
- `indicator`: "今日" | "3日" | "5日" | "10日" | "20日"

**字段**:
- `序号`, `代码`, `名称`
- `最新价`, `今日涨跌幅`
- `今日主力净流入-净额` (单位: 元)
- `今日主力净流入-净占比` (%)
- `今日超大单净流入-净额`, `今日超大单净流入-净占比`
- `今日大单净流入-净额`, `今日大单净流入-净占比`
- `今日中单净流入-净额`, `今日中单净流入-净占比`
- `今日小单净流入-净额`, `今日小单净流入-净占比`

**优势**:
- ✅ 提供详细的分类（超大单、大单、中单、小单）
- ✅ 提供净占比
- ✅ 支持多周期
- ✅ 比`stock_fund_flow_individual`更快（排名数据）
- ✅ 免费使用

**使用场景**:
- 分析涨停股票的资金流向
- 识别主力资金关注的个股
- 验证情绪周期的资金支持

**使用示例**:
```python
import akshare as ak

# 获取今日个股资金流向排名
individual_flow = ak.stock_individual_fund_flow_rank(indicator="今日")

# 筛选涨停股票的资金流向
limit_up_stocks = ['000001', '000002', ...]  # 涨停股票代码
limit_up_flow = individual_flow[individual_flow['代码'].isin(limit_up_stocks)]

# 计算涨停股票的平均主力净流入
avg_main_inflow = limit_up_flow['今日主力净流入-净额'].mean() / 1e8
```

**当前状态**: ⚠️ 未使用，建议添加

---

### 4. stock_fund_flow_industry (行业资金流向-同花顺) ⭐⭐⭐

**接口**: `ak.stock_fund_flow_industry(symbol="即时")`

**功能**: 获取行业资金流向（同花顺数据源）

**参数**:
- `symbol`: "即时" | "3日" | "5日" | "10日" | "20日"

**字段**:
- `序号`, `行业`
- `行业指数`, `行业-涨跌幅`
- `流入资金`, `流出资金`, `净额` (单位: 亿元)
- `公司家数`
- `领涨股`, `领涨股-涨跌幅`, `当前价`

**优势**:
- ✅ 数据来源不同（同花顺 vs 东方财富），可作为对比验证
- ✅ 单位已经是亿元，无需转换
- ✅ 提供领涨股信息

**劣势**:
- ⚠️ 不提供超大单/大单/中单/小单的详细分类
- ⚠️ 速度较慢（需要遍历多个页面）

**使用场景**:
- 与`stock_sector_fund_flow_rank`对比验证
- 获取领涨股信息

**当前状态**: ⚠️ 未使用，可选

---

### 5. stock_fund_flow_concept (概念资金流向) ⭐⭐⭐

**接口**: `ak.stock_fund_flow_concept(symbol="即时")`

**功能**: 获取概念板块资金流向

**参数**:
- `symbol`: "即时" | "3日" | "5日" | "10日" | "20日"

**字段**:
- `序号`, `行业` (概念名称)
- `行业指数`, `行业-涨跌幅`
- `流入资金`, `流出资金`, `净额` (单位: 亿元)
- `公司家数`
- `领涨股`, `领涨股-涨跌幅`, `当前价`

**优势**:
- ✅ 提供概念板块资金流向（可用于热点分析）
- ✅ 单位已经是亿元，无需转换
- ✅ 提供领涨股信息

**劣势**:
- ⚠️ 不提供超大单/大单/中单/小单的详细分类
- ⚠️ 速度较慢

**使用场景**:
- 识别热点概念
- 分析概念板块资金流向
- 辅助情绪周期判断

**当前状态**: ⚠️ 未使用，可选

---

### 6. stock_fund_flow_individual (个股资金流向) ⭐⭐

**接口**: `ak.stock_fund_flow_individual(symbol="即时")`

**功能**: 获取所有个股的资金流向

**参数**:
- `symbol`: "即时"

**字段**:
- `序号`, `股票代码`, `股票简称`
- `最新价`, `涨跌幅`, `换手率`
- `流入资金`, `流出资金`, `净额` (单位: 亿元)
- `成交额`

**劣势**:
- ⚠️ 速度很慢（需要遍历所有股票，约3分钟）
- ⚠️ 不提供超大单/大单/中单/小单的详细分类
- ⚠️ 连接可能不稳定

**建议**:
- ❌ 不推荐使用
- ✅ 使用`stock_individual_fund_flow_rank`代替

---

## 💡 优化建议

### 当前实现（已优化）

1. **大盘资金流向**: ✅ 使用`stock_market_fund_flow`
   - 已优化单位处理（自动检测并转换）
   - 已添加错误处理

2. **行业资金流向**: ✅ 使用`stock_sector_fund_flow_rank`
   - 已添加降级策略（今日 → 5日）
   - 已优化单位处理

### 建议添加的功能

1. **个股资金流向分析**（用于涨停股票）
   ```python
   # 获取涨停股票的资金流向
   individual_flow = ak.stock_individual_fund_flow_rank(indicator="今日")
   limit_up_flow = individual_flow[individual_flow['代码'].isin(limit_up_codes)]
   
   # 分析涨停股票的主力资金支持
   avg_main_inflow = limit_up_flow['今日主力净流入-净额'].mean() / 1e8
   ```

2. **概念资金流向分析**（用于热点识别）
   ```python
   # 获取概念资金流向
   concept_flow = ak.stock_fund_flow_concept(symbol="即时")
   
   # 识别热点概念
   hot_concepts = concept_flow.nlargest(10, '净额')
   ```

3. **多数据源对比验证**
   ```python
   # 东方财富 vs 同花顺
   sector_flow_eastmoney = ak.stock_sector_fund_flow_rank(...)
   sector_flow_ths = ak.stock_fund_flow_industry(...)
   
   # 对比验证
   ```

---

## 📊 数据单位说明

### 东方财富接口（stock_market_fund_flow, stock_sector_fund_flow_rank）

- **净额字段**: 单位是**元**，需要除以`1e8`转换为**亿元**
- **净占比字段**: 单位是**百分比**，直接使用

### 同花顺接口（stock_fund_flow_industry, stock_fund_flow_concept）

- **净额字段**: 单位已经是**亿元**，直接使用
- **涨跌幅字段**: 单位是**百分比**，直接使用

---

## ⚠️ 注意事项

1. **单位不一致**: 不同接口的单位可能不同，需要统一处理
2. **数据延迟**: 实时数据可能有延迟，建议添加时间戳验证
3. **接口稳定性**: 部分接口可能不稳定，需要添加重试机制
4. **速度差异**: 不同接口速度差异较大，需要合理选择

---

## ✅ 当前Notebook中的使用

**Cell 13**:
- ✅ `stock_market_fund_flow` - 大盘资金流向
- ✅ `stock_sector_fund_flow_rank` - 行业资金流向

**建议添加**:
- ⚠️ `stock_individual_fund_flow_rank` - 个股资金流向排名（用于涨停股票分析）

---

**更新时间**: 2026-01-14  
**参考**: [AKShare文档](https://akshare.akfamily.xyz/data/stock/stock.html#id119)
