# JQData finance表权限验证报告

> **测试时间**: 2025-12-19  
> **测试账户**: 试用账户

---

## 📋 测试结果

### finance.STK_CASHFLOW_STATEMENT（现金流量表）

**测试结果**: ❌ 权限限制

**错误信息**: "非法查询"

**测试字段**:
- `net_operate_cash_flow`: ❌ 权限限制
- `operating_cash_flow`: ❌ 字段不存在
- `cash_flow_from_operating_activities`: ❌ 字段不存在

**说明**: 
- 试用账户访问现金流量表时返回"非法查询"错误
- 官方文档未明确说明这是权限限制
- 可能是试用账户的功能限制

---

### finance.STK_BALANCE_SHEET（资产负债表）

**测试结果**: ❌ 权限限制

**错误信息**: "非法查询"

**测试字段**:
- `total_assets`: ❌ 权限限制
- `total_liability`: ❌ 权限限制
- `total_current_assets`: ❌ 权限限制
- `total_current_liability`: ❌ 权限限制

**说明**:
- 试用账户访问资产负债表时返回"非法查询"错误
- 官方文档未明确说明这是权限限制
- 可能是试用账户的功能限制

---

## 🔍 字段名规范

### 标准命名规范

JQData使用**snake_case**（下划线命名）规范：

- ✅ 正确: `net_operate_cash_flow`, `total_assets`, `total_liability`
- ❌ 错误: `N_CASHFLOW_ACT_OPERATE`, `TOTAL_ASSETS`, `TOTAL_LIAB`

### 字段查找方法

```python
from jqdatasdk import finance

# 查看所有字段
cf_fields = [attr for attr in dir(finance.STK_CASHFLOW_STATEMENT) if not attr.startswith('_')]
bs_fields = [attr for attr in dir(finance.STK_BALANCE_SHEET) if not attr.startswith('_')]

# 查找包含特定关键词的字段
operating_fields = [attr for attr in cf_fields if 'operating' in attr.lower()]
total_fields = [attr for attr in bs_fields if 'total' in attr.lower()]
```

---

## ⚠️ 权限说明

### 官方文档说明

根据聚宽官方说明：
- **基础数据所有接口对试用账户开放**
- 但实际测试中，finance.STK_CASHFLOW_STATEMENT和STK_BALANCE_SHEET返回"非法查询"错误

### 可能的原因

1. **功能限制**: 可能是试用账户的功能限制，而非明确的权限限制
2. **数据范围限制**: 可能只限制特定历史范围的数据
3. **接口版本**: 可能需要使用不同的接口或参数

### 建议

1. **联系客服**: 如需确认权限，可联系聚宽客服
2. **使用替代方案**: 使用indicator表的代理指标
3. **升级账户**: 如需完整数据，可考虑升级到正式账户

---

## 💡 替代方案

### 现金流数据替代

使用indicator表的代理指标：

```python
from jqdatasdk import query, indicator

# 经营现金流/营业利润（反映现金流质量）
q = query(
    indicator.code,
    indicator.ocf_to_operating_profit,
    indicator.ocf_to_revenue
).filter(indicator.code == '000001.XSHE')

df = get_fundamentals(q, date='2025-09-18')
```

### 资产负债率替代

由于无法获取资产负债表数据，建议：
1. 使用默认值（如50%）
2. 使用其他财务指标估算
3. 从其他数据源获取

---

## 📝 代码中使用标准术语

### 正确的字段名

```python
# ✅ 使用snake_case命名
from jqdatasdk import query, finance

# 现金流量表（如果可用）
q_cf = query(
    finance.STK_CASHFLOW_STATEMENT.code,
    finance.STK_CASHFLOW_STATEMENT.net_operate_cash_flow,  # snake_case
    finance.STK_CASHFLOW_STATEMENT.net_invest_cash_flow
).filter(finance.STK_CASHFLOW_STATEMENT.code == symbol)

# 资产负债表（如果可用）
q_bs = query(
    finance.STK_BALANCE_SHEET.code,
    finance.STK_BALANCE_SHEET.total_assets,      # snake_case
    finance.STK_BALANCE_SHEET.total_liability    # snake_case
).filter(finance.STK_BALANCE_SHEET.code == symbol)
```

### 错误示例

```python
# ❌ 不要使用大写下划线命名
finance.STK_CASHFLOW_STATEMENT.N_CASHFLOW_ACT_OPERATE  # 错误
finance.STK_BALANCE_SHEET.TOTAL_ASSETS                 # 错误
```

---

## 📚 相关文档

- JQData官方文档: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9886
- Indicator表字段: `docs/JQDATA_INDICATOR_FIELDS_REPORT.md`
- 基础数据范围: `docs/JQDATA_BASIC_DATA_SCOPE.md`

---

*报告版本: 1.0 | 创建时间: 2025-12-19*

