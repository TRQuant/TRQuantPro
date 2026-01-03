# JQData 估值数据表 (valuation) 完整字段列表

> **数据来源**: 聚宽官方API  
> **文档链接**: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9884  
> **字段总数**: 21个  
> **更新时间**: 2025-12-20  
> **权限**: 试用账户和正式账户均可访问 ✅

---

## 📊 字段分类

### 基础字段 (5个)

- `code`
- `day`
- `id`
- `metadata`
- `registry`

### 市值相关 (4个)

- `a_market_cap`
- `circulating_market_cap`
- `free_market_cap`
- `market_cap`

### 股本相关 (4个)

- `a_cap`
- `capitalization`
- `circulating_cap`
- `free_cap`

### 估值比率 (6个)

- `pb_ratio`
- `pcf_ratio`
- `pcf_ratio2`
- `pe_ratio`
- `pe_ratio_lyr`
- `ps_ratio`

### 其他指标 (2个)

- `dividend_ratio`
- `turnover_ratio`

---

## 🔑 关键字段说明

### 估值比率
- `pe_ratio`: 市盈率（TTM，滚动市盈率）
- `pe_ratio_lyr`: 市盈率（LYR，静态市盈率）
- `pb_ratio`: 市净率
- `ps_ratio`: 市销率
- `pcf_ratio`: 市现率（Price to Cash Flow）
- `pcf_ratio2`: 市现率2（另一种计算方式）

### 市值相关
- `market_cap`: 总市值（单位：元，需要除以1e8转为亿元）
- `circulating_market_cap`: 流通市值（单位：元）
- `a_market_cap`: A股总市值
- `free_market_cap`: 自由流通市值

### 股本相关
- `capitalization`: 总股本（单位：股）
- `circulating_cap`: 流通股本（单位：股）
- `a_cap`: A股股本
- `free_cap`: 自由流通股本

### 其他指标
- `turnover_ratio`: 换手率（%）
- `dividend_ratio`: 股息率（%）

---

## ⚠️ 重要说明

### 数据单位
- **市值字段**（`market_cap`, `circulating_market_cap`等）：单位为**元**，需要除以1e8转为亿元
- **股本字段**（`capitalization`, `circulating_cap`等）：单位为**股**
- **比率字段**（`pe_ratio`, `pb_ratio`等）：无单位，直接使用

### 权限说明
✅ **试用账户和正式账户均可访问**，无权限限制

---

## 💻 使用示例

```python
from jqdatasdk import query, valuation, get_fundamentals

# 查询估值数据
q = query(
    valuation.code,
    valuation.pe_ratio,           # 市盈率
    valuation.pb_ratio,            # 市净率
    valuation.ps_ratio,           # 市销率
    valuation.pcf_ratio,          # 市现率
    valuation.market_cap,         # 总市值（元）
    valuation.circulating_market_cap,  # 流通市值（元）
    valuation.turnover_ratio,     # 换手率
    valuation.dividend_ratio      # 股息率
).filter(
    valuation.code == '000001.XSHE'
)

df = get_fundamentals(q, date='2025-09-18')

# 注意：market_cap需要除以1e8转为亿元
if not df.empty:
    market_cap_yi = df['market_cap'].iloc[0] / 100  # 转为亿元
    pe_ratio = df['pe_ratio'].iloc[0]
    pb_ratio = df['pb_ratio'].iloc[0]
    print(f"总市值: {{market_cap_yi:.2f}}亿元")
    print(f"市盈率: {{pe_ratio:.2f}}")
    print(f"市净率: {{pb_ratio:.2f}}")
```

### 批量查询

```python
# 查询多只股票的估值数据
symbols = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    valuation.market_cap
).filter(
    valuation.code.in_(symbols)
)

df = get_fundamentals(q, date='2025-09-18')
df['market_cap_yi'] = df['market_cap'] / 100  # 转为亿元
print(df)
```

---

## 📝 字段名规范

JQData使用**snake_case**（下划线命名）规范：
- ✅ 正确: `pe_ratio`, `market_cap`, `circulating_market_cap`
- ❌ 错误: `PE_RATIO`, `marketCap`, `MarketCap`

---

## 🔍 字段查找方法

```python
from jqdatasdk import valuation

# 获取所有字段
val_fields = [attr for attr in dir(valuation) 
              if not attr.startswith('_') and not callable(getattr(valuation, attr))]

# 查找包含特定关键词的字段
ratio_fields = [f for f in val_fields if 'ratio' in f.lower()]
cap_fields = [f for f in val_fields if 'cap' in f.lower()]
```

---

## ⚡ 常见问题

### Q1: market_cap的单位是什么？
A: 单位为**元**，需要除以1e8转为亿元。例如：1000百万元 = 10亿元

### Q2: pe_ratio和pe_ratio_lyr的区别？
A: 
- `pe_ratio`: TTM（滚动市盈率），使用最近12个月的净利润
- `pe_ratio_lyr`: LYR（静态市盈率），使用最近一个完整年度的净利润

### Q3: 为什么有些股票的pe_ratio为None或负数？
A: 
- None: 可能是新上市股票或数据缺失
- 负数: 表示公司亏损，净利润为负

### Q4: 试用账户可以访问吗？
A: ✅ 可以，valuation表对试用账户和正式账户都开放

---

*文档版本: 1.0 | 创建时间: 2025-12-20*
