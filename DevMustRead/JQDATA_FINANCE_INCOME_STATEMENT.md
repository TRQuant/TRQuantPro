# JQData finance.STK_INCOME_STATEMENT 使用指南

## ✅ 权限状态

**可以通过 `finance.run_query()` 调用！**

测试结果：
- ✅ `finance.run_query()` - 成功，返回数据
- ❌ `get_fundamentals()` - 权限限制，返回"非法查询"

## 📊 字段说明

共70个字段，主要字段：
- `end_date` - 报告期结束日期（注意：不是statDate）
- `operating_revenue` - 营业收入
- `net_profit` - 净利润
- `total_profit` - 利润总额

## 💡 使用示例

```python
from jqdatasdk import query, finance

q = query(
    finance.STK_INCOME_STATEMENT.code,
    finance.STK_INCOME_STATEMENT.end_date,
    finance.STK_INCOME_STATEMENT.operating_revenue,
    finance.STK_INCOME_STATEMENT.net_profit
).filter(
    finance.STK_INCOME_STATEMENT.code == '000001.XSHE',
    finance.STK_INCOME_STATEMENT.end_date >= '2024-01-01'
)

df = finance.run_query(q)  # ✅ 成功
```

完整文档：docs/JQDATA_FINANCE_INCOME_STATEMENT.md
