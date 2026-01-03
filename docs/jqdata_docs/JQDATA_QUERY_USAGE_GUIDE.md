# JQData Query 使用方式完整指南

> **来源**: https://www.kdocs.cn/l/cgLJ9Kpu2M79  
> **整理时间**: 2025-12-20  
> **基于**: 代码实际使用和官方文档

---

## 📚 目录

1. [Query基础概念](#query基础概念)
2. [基本语法](#基本语法)
3. [常用表](#常用表)
4. [查询示例](#查询示例)
5. [高级用法](#高级用法)
6. [注意事项](#注意事项)

---

## Query基础概念

### 什么是Query？

Query是JQData中用于构建数据库查询的对象，类似于SQL的SELECT语句。通过Query可以：
- 指定要查询的表
- 指定要查询的字段
- 添加查询条件（WHERE子句）
- 组合多个表的数据

### Query的核心方法

- `query()`: 创建查询对象
- `.filter()`: 添加查询条件
- `.limit()`: 限制返回行数
- `.order_by()`: 排序

---

## 基本语法

### 1. 导入必要的模块

```python
from jqdatasdk import query, get_fundamentals
from jqdatasdk import valuation, indicator, finance
```

### 2. 创建Query对象

```python
# 方式1：查询整个表
q = query(valuation)

# 方式2：查询指定字段
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio
)
```

### 3. 添加过滤条件

```python
# 单条件
q = query(valuation).filter(
    valuation.code == '000001.XSHE'
)

# 多条件（AND关系）
q = query(valuation).filter(
    valuation.code == '000001.XSHE',
    valuation.pe_ratio < 20
)

# 多只股票（IN关系）
q = query(valuation).filter(
    valuation.code.in_(['000001.XSHE', '000002.XSHE'])
)
```

### 4. 执行查询

```python
# 使用date参数（查询指定日期的最新数据）
df = get_fundamentals(q, date='2025-09-18')

# 使用statDate参数（查询指定报告期的数据）
df = get_fundamentals(q, statDate='2024Q3')  # 季度
df = get_fundamentals(q, statDate='2024')    # 年度
```

---

## 常用表

### 1. valuation - 估值表（每日更新）

```python
from jqdatasdk import query, valuation

q = query(
    valuation.code,
    valuation.pe_ratio,      # 市盈率
    valuation.pb_ratio,      # 市净率
    valuation.ps_ratio,      # 市销率
    valuation.market_cap,    # 总市值（百万元）
    valuation.circulating_market_cap  # 流通市值（百万元）
)
```

### 2. indicator - 财务指标表（季度更新）

```python
from jqdatasdk import query, indicator

q = query(
    indicator.code,
    indicator.roe,                           # 净资产收益率
    indicator.roa,                           # 总资产收益率
    indicator.gross_profit_margin,           # 毛利率
    indicator.net_profit_margin,             # 净利率
    indicator.inc_revenue_year_on_year,      # 营收同比增长
    indicator.inc_net_profit_year_on_year,  # 净利润同比增长
    indicator.eps                            # 每股收益
)
```

### 3. finance表（季度更新，部分需要正式账户）

```python
from jqdatasdk import query, finance

# 现金流量表（需要正式账户）
q = query(
    finance.STK_CASHFLOW_STATEMENT.code,
    finance.STK_CASHFLOW_STATEMENT.net_operate_cash_flow,
    finance.STK_CASHFLOW_STATEMENT.net_invest_cash_flow
)

# 资产负债表（需要正式账户）
q = query(
    finance.STK_BALANCE_SHEET.code,
    finance.STK_BALANCE_SHEET.total_assets,
    finance.STK_BALANCE_SHEET.total_liability
)
```

---

## 查询示例


### 示例 1: 基本查询 - 单表查询

**说明**: 查询valuation表的所有字段

```python
from jqdatasdk import query, valuation, get_fundamentals

# 查询单只股票的估值数据
q = query(valuation).filter(
    valuation.code == '000001.XSHE'
)
df = get_fundamentals(q, date='2025-09-18')
```


### 示例 2: 指定字段查询

**说明**: 只查询需要的字段，提高效率

```python
from jqdatasdk import query, valuation, indicator, get_fundamentals

# 查询指定字段
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    valuation.market_cap,
    indicator.roe,
    indicator.gross_profit_margin
).filter(
    valuation.code == '000001.XSHE'
)
df = get_fundamentals(q, date='2025-09-18')
```


### 示例 3: 多只股票查询

**说明**: 使用in_()方法查询多只股票

```python
from jqdatasdk import query, valuation, get_fundamentals

# 查询多只股票
symbols = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
q = query(valuation).filter(
    valuation.code.in_(symbols)
)
df = get_fundamentals(q, date='2025-09-18')
```


### 示例 4: 条件过滤

**说明**: 使用filter()添加查询条件

```python
from jqdatasdk import query, indicator, get_fundamentals

# 查询ROE大于10%的股票
q = query(
    indicator.code,
    indicator.roe
).filter(
    indicator.roe > 10
)
df = get_fundamentals(q, date='2025-09-18')
```


### 示例 5: 多条件查询

**说明**: 多个条件用逗号分隔，表示AND关系

```python
from jqdatasdk import query, valuation, indicator, get_fundamentals

# 多条件组合
q = query(
    valuation.code,
    valuation.pe_ratio,
    indicator.roe
).filter(
    valuation.pe_ratio < 20,
    indicator.roe > 10
)
df = get_fundamentals(q, date='2025-09-18')
```


### 示例 6: 指定报告期查询

**说明**: 使用statDate参数查询指定报告期的财务数据

```python
from jqdatasdk import query, indicator, get_fundamentals

# 查询指定报告期的数据
q = query(indicator).filter(
    indicator.code == '000001.XSHE'
)
# 使用statDate指定报告期
df = get_fundamentals(q, statDate='2024Q3')  # 2024年第三季度
# 或
df = get_fundamentals(q, statDate='2024')  # 2024年度（返回Q4数据）
```


---

## 高级用法

### 1. 组合多个表

```python
from jqdatasdk import query, valuation, indicator, get_fundamentals

# 同时查询估值和财务指标
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    indicator.roe,
    indicator.gross_profit_margin
).filter(
    valuation.code == indicator.code,  # 关联条件
    valuation.code == '000001.XSHE'
)
df = get_fundamentals(q, date='2025-09-18')
```

### 2. 使用limit限制返回行数

```python
q = query(valuation).filter(
    valuation.pe_ratio < 20
).limit(100)  # 最多返回100行
df = get_fundamentals(q, date='2025-09-18')
```

### 3. 使用order_by排序

```python
q = query(valuation).filter(
    valuation.pe_ratio > 0
).order_by(valuation.pe_ratio.asc())  # 按PE升序
df = get_fundamentals(q, date='2025-09-18')
```

### 4. 使用finance.run_query查询历史数据

```python
from jqdatasdk import finance

# 查询年度数据
q = query(finance.STK_INCOME_STATEMENT).filter(
    finance.STK_INCOME_STATEMENT.code == '000001.XSHE',
    finance.STK_INCOME_STATEMENT.statDate == '2024'
)
df = finance.run_query(q)  # 返回所有2024年的季度数据
```

---

## 注意事项

### 1. date vs statDate

- **date**: 查询指定交易日收盘后能看到的最新数据（用于valuation等每日更新的表）
- **statDate**: 查询指定报告期的数据（用于indicator、finance等季度更新的表）
- **不能同时使用**：date和statDate参数只能传入一个

### 2. 权限限制

- **试用账户**: 可以访问valuation、indicator表
- **正式账户**: 可以访问所有表，包括finance.STK_CASHFLOW_STATEMENT、finance.STK_BALANCE_SHEET

### 3. 数据单位

- **market_cap**: 单位为百万元，需要除以100转为亿元
- **股本字段**: 单位为股
- **比率字段**: 无单位，直接使用

### 4. 性能优化

- 只查询需要的字段，不要查询整个表
- 使用filter()限制查询范围
- 避免查询过多股票（建议单次不超过1000只）

### 5. 错误处理

```python
from jqdatasdk import query, valuation, get_fundamentals

try:
    q = query(valuation).filter(valuation.code == '000001.XSHE')
    df = get_fundamentals(q, date='2025-09-18')
    
    if df is None or df.empty:
        print("未返回数据")
    else:
        print(df)
except Exception as e:
    print(f"查询失败: {e}")
```

---

## 常见问题

### Q1: 如何查询多只股票的数据？

A: 使用`.in_()`方法：
```python
q = query(valuation).filter(
    valuation.code.in_(['000001.XSHE', '000002.XSHE', '600000.XSHG'])
)
```

### Q2: 如何查询指定报告期的数据？

A: 使用`statDate`参数：
```python
df = get_fundamentals(q, statDate='2024Q3')  # 季度
df = get_fundamentals(q, statDate='2024')    # 年度
```

### Q3: 如何组合多个查询条件？

A: 在filter()中用逗号分隔多个条件（AND关系）：
```python
q = query(valuation).filter(
    valuation.pe_ratio < 20,
    valuation.pb_ratio < 3,
    valuation.market_cap > 100  # 市值大于100百万元
)
```

### Q4: 为什么查询finance表返回"非法查询"？

A: 试用账户无法访问finance.STK_CASHFLOW_STATEMENT和finance.STK_BALANCE_SHEET，需要使用正式账户。

---

## 📖 相关文档

- JQData官方文档: https://www.joinquant.com/help/api/doc
- valuation表字段: `docs/JQDATA_VALUATION_COMPLETE.md`
- indicator表字段: `docs/JQDATA_INDICATOR_FIELDS_REPORT.md`
- finance表权限: `docs/JQDATA_FINANCE_TABLES_PERMISSION.md`

---

## 🖼️ 文档截图

> 注：完整文档截图已保存在 `/tmp/kdocs_query_guide_full.png`
> 如需查看完整内容，请运行交互式爬取脚本：
> ```bash
> cd /home/taotao/dev/QuantTest/TRQuant
> source venv/bin/activate
> python3 scripts/crawl_kdocs_after_login.py
> ```

---

## 📥 交互式爬取脚本

如果文档需要登录才能查看完整内容，可以使用以下脚本：

**文件**: `scripts/crawl_kdocs_after_login.py`

**使用方法**:
```bash
cd /home/taotao/dev/QuantTest/TRQuant
source venv/bin/activate
python3 scripts/crawl_kdocs_after_login.py
```

脚本会：
1. 打开浏览器（非无头模式）
2. 访问文档页面
3. 等待您在浏览器中完成登录
4. 按Enter后自动提取文档内容
5. 保存到 `/tmp/kdocs_content.html` 和 `/tmp/kdocs_content.txt`

---

*文档版本: 1.0 | 创建时间: 2025-12-20*
*最后更新: 2025-12-20*

