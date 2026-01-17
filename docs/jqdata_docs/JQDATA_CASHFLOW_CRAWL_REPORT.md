# JQData 现金流量表文档爬取完成报告

> **完成时间**: 2025-12-20  
> **来源URL**: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9888

---

## ✅ 完成工作

### 1. 文档爬取
- ✅ 使用Playwright成功爬取官方文档
- ✅ 提取完整文本内容
- ✅ 提取表格和代码示例

### 2. 字段提取
- ✅ 通过API获取实际字段列表：**93个字段**
- ✅ 分类整理：
  - 基础字段：4个
  - 经营活动相关：6个
  - 投资活动相关：11个
  - 筹资活动相关：6个
  - 现金相关：34个
  - 其他字段：32个

### 3. 文档生成
- ✅ 完整使用指南：`docs/JQDATA_FINANCE_CASHFLOW_STATEMENT.md` (292行)
- ✅ 包含权限说明、字段列表、使用示例、注意事项
- ✅ 已复制到：`DevMustRead/JQDATA_FINANCE_CASHFLOW_STATEMENT.md`

### 4. 知识库存储
- ✅ 知识库ID: `kb_20251220_113827`
- ✅ 标题: "JQData finance.STK_CASHFLOW_STATEMENT 现金流量表使用指南"
- ✅ 类型: api_doc
- ✅ 标签: JQData, finance, STK_CASHFLOW_STATEMENT, 现金流量表, run_query, 权限

---

## 📊 关键信息

### 权限状态
- ✅ `finance.run_query()` - 可以使用
- ❌ `get_fundamentals()` - 权限限制（返回"非法查询"）

### 重要字段
- `end_date` - 报告期结束日期（不是statDate）
- `net_operate_cash_flow` - 经营活动现金流量净额
- `net_invest_cash_flow` - 投资活动现金流量净额
- `net_finance_cash_flow` - 筹资活动现金流量净额
- `cash_equivalents_at_end` - 期末现金及现金等价物余额

### 使用示例
```python
from jqdatasdk import query, finance

q = query(
    finance.STK_CASHFLOW_STATEMENT.code,
    finance.STK_CASHFLOW_STATEMENT.end_date,
    finance.STK_CASHFLOW_STATEMENT.net_operate_cash_flow
).filter(
    finance.STK_CASHFLOW_STATEMENT.code == '000001.XSHE',
    finance.STK_CASHFLOW_STATEMENT.end_date >= '2024-01-01'
)

df = finance.run_query(q)  # ✅ 成功
```

---

## 📁 文件位置

- 完整文档: `docs/JQDATA_FINANCE_CASHFLOW_STATEMENT.md`
- DevMustRead: `DevMustRead/JQDATA_FINANCE_CASHFLOW_STATEMENT.md`
- 字段列表: `/tmp/stk_cashflow_statement_fields.txt`
- 原始提取: `/tmp/jqdata_cashflow_extracted.txt`

---

*报告生成时间: 2025-12-20*
