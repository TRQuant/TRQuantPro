# JQData Query 调用示例完整指南

> **更新时间**: 2025-12-20  
> **来源**: 知识库 + PDF官方文档

---

## 📚 快速开始

### 1. 基本查询

```python
from jqdatasdk import query, valuation, get_fundamentals
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

# 认证
jq_client = JQDataClient()
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq_client.authenticate(jq_config['username'], jq_config['password'])

# 获取可用日期
date = jq_client.get_available_end_date()
symbol = "000001.XSHE"

# 基本查询
q = query(valuation).filter(valuation.code == symbol)
df = get_fundamentals(q, date=date)
print(df)
```

### 2. 查询指定字段

```python
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    valuation.market_cap
).filter(valuation.code == symbol)
df = get_fundamentals(q, date=date)
```

### 3. 多只股票查询

```python
symbols = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
q = query(valuation).filter(valuation.code.in_(symbols))
df = get_fundamentals(q, date=date)
```

### 4. 条件过滤

```python
q = query(valuation).filter(
    valuation.pe_ratio < 20,
    valuation.pb_ratio < 3
)
df = get_fundamentals(q, date=date)
```

### 5. 组合表查询

```python
from jqdatasdk import indicator

q = query(
    valuation.code,
    valuation.pe_ratio,
    indicator.roe
).filter(
    valuation.code == indicator.code,
    valuation.code == symbol
)
df = get_fundamentals(q, date=date)
```

### 6. 批量查询

```python
from jqdatasdk import finance

q = query(finance.STK_INCOME_STATEMENT).filter(
    finance.STK_INCOME_STATEMENT.code == symbol
)
# 最多5000条
df = finance.run_query(q)
# 最多20万条
df = finance.run_offset_query(q)
```

---

## 🔍 知识库查询示例

```python
# 使用MCP工具查询知识库
from mcp_xuanyuan_knowledge_search import mcp_xuanyuan_knowledge_search

# 搜索Query使用方式
results = mcp_xuanyuan_knowledge_search(query="JQData Query")

# 搜索特定方法
results = mcp_xuanyuan_knowledge_search(query="run_offset_query")
```

---

## 📖 完整文档

- 完整示例: `docs/JQDATA_QUERY_USAGE_EXAMPLES.md`
- PDF提取: `docs/JQDATA_QUERY_PDF_EXTRACTED.md`
- 测试脚本: `scripts/test_query_examples.py`

