# JQData finance.STK_CASHFLOW_STATEMENT 现金流量表使用指南

> **来源**: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9888  
> **更新时间**: 2025-12-20  
> **历史范围**: 2005年至今  
> **更新频率**: 交易日24:00更新（按季度更新）

---

## 📋 权限说明

### ✅ 可用方法

**`finance.run_query()`** - **可以使用**

```python
from jqdatasdk import query, finance

q = query(finance.STK_CASHFLOW_STATEMENT).filter(
    finance.STK_CASHFLOW_STATEMENT.code == '000001.XSHE'
)
df = finance.run_query(q)  # ✅ 成功
```

### ❌ 不可用方法

**`get_fundamentals()`** - **权限限制**

```python
from jqdatasdk import query, finance, get_fundamentals

q = query(finance.STK_CASHFLOW_STATEMENT).filter(
    finance.STK_CASHFLOW_STATEMENT.code == '000001.XSHE'
)
df = get_fundamentals(q, statDate='2024Q3')  # ❌ 返回"非法查询"
```

---

## 📊 字段列表（共93个字段）

### 基础字段

- `code` - 股票代码（带后缀.XSHE/.XSHG）
- `end_date` - 报告期结束日期（注意：不是`statDate`）
- `pub_date` - 公司发布财报日期
- `id` - 记录ID

### 经营活动相关字段（6个）

- `subtotal_operate_cash_inflow` - 经营活动现金流入小计(元)
- `subtotal_operate_cash_outflow` - 经营活动现金流出小计(元)
- `net_operate_cash_flow` - 经营活动产生的现金流量净额(元)
- `net_operate_cash_flow_indirect` - 间接法计算的经营活动现金流量净额(元)
- `operate_payable_increase` - 经营性应付项目增加(元)
- `operate_receivables_decrease` - 经营性应收项目减少(元)

### 投资活动相关字段（11个）

- `subtotal_invest_cash_inflow` - 投资活动现金流入小计(元)
- `subtotal_invest_cash_outflow` - 投资活动现金流出小计(元)
- `net_invest_cash_flow` - 投资活动产生的现金流量净额(元)
- `invest_proceeds` - 收回投资收到的现金(元)
- `invest_withdrawal_cash` - 取得投资收益收到的现金(元)
- `cash_from_invest` - 处置固定资产、无形资产和其他长期资产收回的现金净额(元)
- `cash_from_mino_s_invest_sub` - 处置子公司及其他营业单位收到的现金净额(元)
- `invest_cash_paid` - 购建固定资产、无形资产和其他长期资产支付的现金(元)
- `invest_loss` - 投资支付的现金(元)
- `investment_property_depreciation` - 投资性房地产折旧(元)
- `net_insurer_deposit_investment` - 保户储金及投资款净增加额(元)

### 筹资活动相关字段（6个）

- `subtotal_finance_cash_inflow` - 筹资活动现金流入小计(元)
- `subtotal_finance_cash_outflow` - 筹资活动现金流出小计(元)
- `net_finance_cash_flow` - 筹资活动产生的现金流量净额(元)
- `cash_from_borrowing` - 取得借款收到的现金(元)
- `cash_from_bonds_issue` - 发行债券收到的现金(元)
- `net_borrowing_from_finance_co` - 向其他金融机构拆入资金净增加额(元)

### 现金相关字段（34个）

- `cash_equivalents_at_beginning` - 期初现金及现金等价物余额(元)
- `cash_equivalents_at_end` - 期末现金及现金等价物余额(元)
- `cash_equivalent_increase` - 现金及现金等价物净增加额(元)
- `cash_equivalent_increase_indirect` - 间接法计算的现金及现金等价物净增加额(元)
- `cash_at_beginning` - 期初现金余额(元)
- `cash_at_end` - 期末现金余额(元)
- `equivalents_at_beginning` - 期初现金等价物余额(元)
- `equivalents_at_end` - 期末现金等价物余额(元)
- `exchange_rate_change_effect` - 汇率变动对现金及现金等价物的影响(元)

### 主要经营活动流入字段

- `goods_sale_and_service_render_cash` - 销售商品、提供劳务收到的现金(元)
- `tax_levy_refund` - 收到的税费返还(元)
- `other_cashin_related_operate` - 收到其他与经营活动有关的现金(元)
- `net_deposit_increase` - 客户存款和同业存放款项净增加额(元)
- `net_borrowing_from_central_bank` - 向中央银行借款净增加额(元)
- `net_original_insurance_cash` - 收到原保险合同保费取得的现金(元)
- `net_cash_received_from_reinsurance_business` - 收到再保险业务现金净额(元)
- `net_deal_trading_assets` - 处置交易性金融资产净增加额(元)
- `interest_and_commission_cashin` - 收取利息、手续费及佣金的现金(元)
- `net_increase_in_placements` - 拆入资金净增加额(元)
- `net_buyback` - 回购业务资金净增加额(元)

### 主要经营活动流出字段

- `goods_and_services_cash_paid` - 购买商品、接受劳务支付的现金(元)
- `net_loan_and_advance_increase` - 客户贷款及垫款净增加额(元)
- `net_deposit_in_cb_and_ib` - 存放中央银行和同业款项净增加额(元)
- `original_compensation_paid` - 支付原保险合同赔付款项的现金(元)
- `handling_charges_and_commission` - 支付利息、手续费及佣金的现金(元)
- `policy_dividend_cash_paid` - 支付保单红利的现金(元)
- `staff_behalf_paid` - 支付给职工以及为职工支付的现金(元)
- `tax_payments` - 支付的各项税费(元)
- `other_operate_cash_paid` - 支付其他与经营活动有关的现金(元)

### 其他重要字段

- `borrowing_repayment` - 偿还债务支付的现金(元)
- `dividend_interest_payment` - 分配股利、利润或偿付利息支付的现金(元)
- `financial_cost` - 财务费用(元)
- `financial_lease_fixed_assets` - 融资租入固定资产(元)
- `fix_intan_other_asset_acqui_cash` - 购建固定资产、无形资产和其他长期资产支付的现金(元)
- `fix_intan_other_asset_dispo_cash` - 处置固定资产、无形资产和其他长期资产收回的现金净额(元)
- `assets_depreciation_reserves` - 资产减值准备(元)
- `fixed_assets_depreciation` - 固定资产折旧(元)
- `deffered_tax_asset_decrease` - 递延所得税资产减少(元)
- `deffered_tax_liability_increase` - 递延所得税负债增加(元)
- `defferred_expense_amortization` - 长期待摊费用摊销(元)
- `fair_value_change_loss` - 公允价值变动损失(元)
- `fixed_asset_scrap_loss` - 固定资产报废损失(元)
- `fix_intan_other_asset_dispo_loss` - 处置固定资产、无形资产和其他长期资产损失(元)
- `credit_impairment_loss` - 信用减值损失(元)
- `debt_to_capital` - 债务转为资本(元)
- `cbs_expiring_in_one_year` - 一年内到期的可转换公司债券(元)
- `proceeds_from_sub_to_mino_s` - 取得子公司及其他营业单位支付的现金净额(元)
- `other_finance_act_payment` - 支付其他与筹资活动有关的现金(元)

---

## 💡 使用示例

### 示例1: 基本查询

```python
from jqdatasdk import query, finance
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

# 认证
jq_client = JQDataClient()
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq_client.authenticate(jq_config['username'], jq_config['password'])

# 查询现金流量表数据
q = query(
    finance.STK_CASHFLOW_STATEMENT.code,
    finance.STK_CASHFLOW_STATEMENT.end_date,
    finance.STK_CASHFLOW_STATEMENT.net_operate_cash_flow,
    finance.STK_CASHFLOW_STATEMENT.net_invest_cash_flow,
    finance.STK_CASHFLOW_STATEMENT.net_finance_cash_flow
).filter(
    finance.STK_CASHFLOW_STATEMENT.code == '000001.XSHE',
    finance.STK_CASHFLOW_STATEMENT.end_date >= '2024-01-01',
    finance.STK_CASHFLOW_STATEMENT.end_date <= '2024-12-31'
).order_by(
    finance.STK_CASHFLOW_STATEMENT.end_date.desc()
)

df = finance.run_query(q)  # ✅ 使用run_query
print(df)
```

### 示例2: 查询经营活动现金流

```python
# 查询经营活动现金流相关字段
q = query(
    finance.STK_CASHFLOW_STATEMENT.code,
    finance.STK_CASHFLOW_STATEMENT.end_date,
    finance.STK_CASHFLOW_STATEMENT.goods_sale_and_service_render_cash,  # 销售商品收到的现金
    finance.STK_CASHFLOW_STATEMENT.goods_and_services_cash_paid,        # 购买商品支付的现金
    finance.STK_CASHFLOW_STATEMENT.staff_behalf_paid,                   # 支付给职工的现金
    finance.STK_CASHFLOW_STATEMENT.tax_payments,                        # 支付的税费
    finance.STK_CASHFLOW_STATEMENT.subtotal_operate_cash_inflow,        # 经营活动现金流入小计
    finance.STK_CASHFLOW_STATEMENT.subtotal_operate_cash_outflow,       # 经营活动现金流出小计
    finance.STK_CASHFLOW_STATEMENT.net_operate_cash_flow                # 经营活动现金流量净额
).filter(
    finance.STK_CASHFLOW_STATEMENT.code == '000001.XSHE',
    finance.STK_CASHFLOW_STATEMENT.end_date >= '2024-01-01'
).order_by(
    finance.STK_CASHFLOW_STATEMENT.end_date.desc()
)

df = finance.run_query(q)
print(df)
```

### 示例3: 查询多只股票

```python
symbols = ['000001.XSHE', '000002.XSHE', '600000.XSHG']

q = query(
    finance.STK_CASHFLOW_STATEMENT.code,
    finance.STK_CASHFLOW_STATEMENT.end_date,
    finance.STK_CASHFLOW_STATEMENT.net_operate_cash_flow,
    finance.STK_CASHFLOW_STATEMENT.cash_equivalents_at_end
).filter(
    finance.STK_CASHFLOW_STATEMENT.code.in_(symbols),
    finance.STK_CASHFLOW_STATEMENT.end_date >= '2024-01-01'
).order_by(
    finance.STK_CASHFLOW_STATEMENT.code,
    finance.STK_CASHFLOW_STATEMENT.end_date.desc()
)

df = finance.run_query(q)
print(df)
```

### 示例4: 计算现金流比率

```python
import pandas as pd

# 查询现金流量数据
q = query(
    finance.STK_CASHFLOW_STATEMENT.code,
    finance.STK_CASHFLOW_STATEMENT.end_date,
    finance.STK_CASHFLOW_STATEMENT.net_operate_cash_flow,
    finance.STK_CASHFLOW_STATEMENT.cash_equivalents_at_beginning,
    finance.STK_CASHFLOW_STATEMENT.cash_equivalents_at_end
).filter(
    finance.STK_CASHFLOW_STATEMENT.code == '000001.XSHE',
    finance.STK_CASHFLOW_STATEMENT.end_date >= '2023-01-01'
).order_by(
    finance.STK_CASHFLOW_STATEMENT.end_date
)

df = finance.run_query(q)

# 计算现金流相关比率
if len(df) > 0:
    df['cash_flow_growth'] = df['net_operate_cash_flow'].pct_change() * 100  # 现金流增长率
    df['cash_balance'] = df['cash_equivalents_at_end'] / 1e8  # 转换为亿元
    print(df[['end_date', 'net_operate_cash_flow', 'cash_flow_growth', 'cash_balance']])
```

---

## ⚠️ 重要注意事项

### 1. 字段名差异

- ❌ **不要使用** `statDate`（不存在）
- ✅ **使用** `end_date`（报告期结束日期）

### 2. 查询方法

- ❌ **不要使用** `get_fundamentals()`（权限限制）
- ✅ **使用** `finance.run_query()`（可用）

### 3. 日期格式

- `end_date` 使用日期格式：`'2024-09-30'`（季度结束日期）
- 不是 `'2024Q3'` 格式

### 4. 数据限制

- `finance.run_query()` 最多返回 **5000条** 数据
- 如需更多数据，使用 `finance.run_offset_query()`（最多20万条）

### 5. 数据单位

- 金额字段单位为 **元**
- 需要转换为万元或亿元时，除以相应倍数

---

## 📖 相关文档

- Query使用指南: `docs/JQDATA_QUERY_USAGE_GUIDE.md`
- finance.STK_INCOME_STATEMENT: `docs/JQDATA_FINANCE_INCOME_STATEMENT.md`
- finance.STK_BALANCE_SHEET: `docs/JQDATA_BALANCE_SHEET_COMPLETE.md`
- 官方文档: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9888

---

*文档版本: 1.0 | 创建时间: 2025-12-20*
