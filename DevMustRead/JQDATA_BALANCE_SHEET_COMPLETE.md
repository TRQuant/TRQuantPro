# JQData 资产负债表 (STK_BALANCE_SHEET) 完整字段列表

> **数据来源**: 聚宽官方API  
> **文档链接**: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9887  
> **字段总数**: 127个  
> **更新时间**: 2025-12-20

---

## 📊 字段分类

### 1. 基础字段 (16个)

- `a_code`
- `b_code`
- `code`
- `company_id`
- `company_name`
- `end_date`
- `h_code`
- `id`
- `metadata`
- `pub_date`
- `registry`
- `report_date`
- `report_type`
- `source`
- `source_id`
- `start_date`

### 2. 资产类字段 (38个)

- `account_receivable`
- `affiliated_company_receivable`
- `bill_and_account_receivable`
- `bill_receivable`
- `biological_assets`
- `bought_sellback_assets`
- `cash_equivalents`
- `contract_assets`
- `deferred_tax_assets`
- `derivative_financial_asset`
- `dividend_receivable`
- `expendable_biological_asset`
- `fixed_assets`
- `fixed_assets_liquidation`
- `hold_for_sale_assets`
- `hold_sale_asset`
- `hold_to_maturity_investments`
- `insurance_receivables`
- `intangible_assets`
- `interest_receivable`
- `investment_property`
- `loan_and_advance_current_assets`
- `loan_and_advance_noncurrent_assets`
- `longterm_receivable_account`
- `non_current_asset_in_one_year`
- `oil_gas_assets`
- `other_current_assets`
- `other_non_current_assets`
- `other_non_current_financial_assets`
- `other_receivable`
- `receivable_fin`
- `reinsurance_contract_reserves_receivable`
- `reinsurance_receivables`
- `total_assets`
- `total_current_assets`
- `total_non_current_assets`
- `trading_assets`
- `usufruct_assets`

### 3. 负债类字段 (42个)

- `accounts_payable`
- `affiliated_company_payable`
- `bill_and_account_payable`
- `bond_invest`
- `bonds_payable`
- `borrowing_capital`
- `borrowing_from_centralbank`
- `commission_payable`
- `contract_assets`
- `contract_liability`
- `deferred_tax_liability`
- `derivative_financial_liability`
- `dividend_payable`
- `estimate_liability`
- `estimate_liability_current`
- `hold_sale_liability`
- `insurance_contract_reserves`
- `interest_payable`
- `lease_liability`
- `loan_and_advance_current_assets`
- `loan_and_advance_noncurrent_assets`
- `longterm_account_payable`
- `longterm_loan`
- `longterm_salaries_payable`
- `non_current_liability_in_one_year`
- `notes_payable`
- `other_bond_invest`
- `other_current_liability`
- `other_non_current_liability`
- `other_payable`
- `pepertual_liability_equity`
- `pepertual_liability_noncurrent`
- `reinsurance_contract_reserves_receivable`
- `reinsurance_payables`
- `salaries_payable`
- `shortterm_loan`
- `specific_account_payable`
- `taxs_payable`
- `total_current_liability`
- `total_liability`
- `total_non_current_liability`
- `trading_liability`

### 4. 所有者权益类字段 (19个)

- `borrowing_capital`
- `capital_reserve_fund`
- `equities_parent_company_owners`
- `insurance_contract_reserves`
- `lend_capital`
- `longterm_equity_invest`
- `ordinary_risk_reserve_fund`
- `other_equity_tools`
- `other_equity_tools_invest`
- `paidin_capital`
- `pepertual_liability_equity`
- `preferred_shares_equity`
- `reinsurance_contract_reserves_receivable`
- `retained_profit`
- `specific_reserves`
- `surplus_reserve_fund`
- `total_owner_equities`
- `total_sheet_owner_equities`
- `treasury_stock`

### 5. 其他字段 (20个)

- `advance_payment`
- `advance_peceipts`
- `constru_in_process`
- `construction_materials`
- `deferred_earning`
- `deferred_earning_current`
- `deposit_in_interbank`
- `development_expenditure`
- `foreign_currency_report_conv_diff`
- `good_will`
- `inventories`
- `irregular_item_adjustment`
- `long_deferred_expense`
- `minority_interests`
- `other_comprehensive_income`
- `preferred_shares_noncurrent`
- `proxy_secu_proceeds`
- `receivings_from_vicariously_sold_securities`
- `settlement_provi`
- `sold_buyback_secu_proceeds`

---

## 🔑 关键字段说明

### 资产总计
- `total_assets`: 资产总计
- `total_current_assets`: 流动资产合计
- `total_non_current_assets`: 非流动资产合计

### 负债总计
- `total_liability`: 负债合计
- `total_current_liability`: 流动负债合计
- `total_non_current_liability`: 非流动负债合计

### 所有者权益
- `total_owner_equities`: 所有者权益合计
- `total_sheet_owner_equities`: 股东权益合计

---

## ⚠️ 权限说明

**试用账户**: 无法访问资产负债表数据，返回"非法查询"错误  
**正式账户**: 可以访问完整数据

---

## 💻 使用示例

```python
from jqdatasdk import query, finance, get_fundamentals

# 查询资产负债表关键字段
q = query(
    finance.STK_BALANCE_SHEET.code,
    finance.STK_BALANCE_SHEET.end_date,
    finance.STK_BALANCE_SHEET.total_assets,
    finance.STK_BALANCE_SHEET.total_liability,
    finance.STK_BALANCE_SHEET.total_owner_equities,
    finance.STK_BALANCE_SHEET.cash_equivalents,
    finance.STK_BALANCE_SHEET.account_receivable,
    finance.STK_BALANCE_SHEET.accounts_payable
).filter(
    finance.STK_BALANCE_SHEET.code == '000001.XSHE'
)

df = get_fundamentals(q, date='2025-09-18')
```

---

## 📝 字段名规范

JQData使用**snake_case**（下划线命名）规范：
- ✅ 正确: `total_assets`, `total_liability`, `account_receivable`
- ❌ 错误: `TOTAL_ASSETS`, `totalAssets`, `AccountReceivable`

---

## 🔍 字段查找方法

```python
from jqdatasdk import finance

# 获取所有字段
bs_fields = [attr for attr in dir(finance.STK_BALANCE_SHEET) 
             if not attr.startswith('_') and not callable(getattr(finance.STK_BALANCE_SHEET, attr))]

# 查找包含特定关键词的字段
total_fields = [f for f in bs_fields if 'total' in f.lower()]
asset_fields = [f for f in bs_fields if 'asset' in f.lower()]
liability_fields = [f for f in bs_fields if 'liability' in f.lower()]
```

---

*文档版本: 1.0 | 创建时间: 2025-12-20*
