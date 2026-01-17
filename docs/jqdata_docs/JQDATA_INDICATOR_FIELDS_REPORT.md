# JQData Indicator表字段测试报告

> **测试时间**: 2025-12-19  
> **数据来源**: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9885&keyword=Indicator  
> **测试账户**: 试用账户

---

## 📊 测试结果总结

| 类别 | 数量 | 说明 |
|------|------|------|
| ✅ 可用字段 | 36个 | 试用账户可访问 |
| ❌ 权限限制字段 | 0个 | indicator表无权限限制 |
| ⚠️ 错误字段 | 2个 | 可能是字段不存在 |

**结论**: indicator表的所有字段在试用账户中都可以访问，**无权限限制**。

---

## ✅ 完整可用字段列表（36个）

### 1. 基础字段（5个）

| 字段名 | 说明 |
|--------|------|
| `code` | 股票代码 |
| `day` | 日期 |
| `id` | 记录ID |
| `pubDate` | 发布日期 |
| `statDate` | 报告期 |

### 2. 盈利能力指标（6个）

| 字段名 | 说明 |
|--------|------|
| `roe` | 净资产收益率 |
| `roa` | 总资产收益率 |
| `net_profit_margin` | 净利率 |
| `gross_profit_margin` | 毛利率 |
| `operating_profit` | 营业利润 |
| `adjusted_profit` | 调整后净利润 |

### 3. 增长率指标（10个）

| 字段名 | 说明 |
|--------|------|
| `inc_revenue_year_on_year` | 营收同比增长 |
| `inc_revenue_annual` | 营收年增长率 |
| `inc_net_profit_year_on_year` | 净利润同比增长 |
| `inc_net_profit_annual` | 净利润年增长率 |
| `inc_operation_profit_year_on_year` | 营业利润同比增长 |
| `inc_operation_profit_annual` | 营业利润年增长率 |
| `inc_total_revenue_year_on_year` | 总收入同比增长 |
| `inc_total_revenue_annual` | 总收入年增长率 |
| `inc_net_profit_to_shareholders_year_on_year` | 归属净利润同比增长 |
| `inc_net_profit_to_shareholders_annual` | 归属净利润年增长率 |

### 4. 每股指标（1个）

| 字段名 | 说明 |
|--------|------|
| `eps` | 每股收益 |

### 5. 比率指标（9个）

| 字段名 | 说明 |
|--------|------|
| `adjusted_profit_to_profit` | 调整后净利润/净利润 |
| `expense_to_total_revenue` | 费用/总收入 |
| `financing_expense_to_total_revenue` | 财务费用/总收入 |
| `ga_expense_to_total_revenue` | 管理费用/总收入 |
| `operating_expense_to_total_revenue` | 营业费用/总收入 |
| `net_profit_to_total_revenue` | 净利润/总收入 |
| `operation_profit_to_total_revenue` | 营业利润/总收入 |
| `operating_profit_to_profit` | 营业利润/利润总额 |
| `invesment_profit_to_profit` | 投资收益/利润总额 |

### 6. 现金流相关（2个）

| 字段名 | 说明 |
|--------|------|
| `ocf_to_operating_profit` | 经营现金流/营业利润 |
| `ocf_to_revenue` | 经营现金流/营业收入 |

### 7. 其他指标（3个）

| 字段名 | 说明 |
|--------|------|
| `goods_sale_and_service_to_revenue` | 商品销售和服务/营业收入 |
| `value_change_profit` | 公允价值变动收益 |
| `inc_return` | 收益率 |

---

## 🔒 权限限制说明

### ✅ 无权限限制的表

1. **indicator表**: 所有36个字段都可以访问
2. **valuation表**: 可访问（pe_ratio, pb_ratio, market_cap等）
3. **get_price**: 可访问（价格、成交量等）

### ❌ 有权限限制的表

1. **finance.STK_CASHFLOW_STATEMENT** (现金流量表)
   - 错误: "非法查询"
   - 说明: 试用账户无法访问现金流量表数据

2. **finance.STK_BALANCE_SHEET** (资产负债表)
   - 错误: "非法查询"
   - 说明: 试用账户无法访问资产负债表数据

3. **finance.STK_INCOME_STATEMENT** (利润表)
   - 可能限制: 需要验证
   - 说明: 建议使用indicator表替代

---

## 💡 使用建议

### 1. 优先使用indicator表

indicator表提供了丰富的财务指标，且**无权限限制**，是试用账户的最佳选择。

### 2. 现金流数据替代方案

由于现金流量表受权限限制，可以使用indicator表的代理指标：
- `ocf_to_operating_profit`: 经营现金流/营业利润（反映现金流质量）
- `ocf_to_revenue`: 经营现金流/营业收入（反映现金流强度）

### 3. 资产负债率计算

由于资产负债表受权限限制，无法直接计算资产负债率。建议：
- 使用其他财务指标替代（如debt_ratio使用默认值或估算）
- 或升级到正式账户获取完整数据

### 4. 数据获取策略

```python
# 推荐的数据获取顺序
1. indicator表 → 财务指标（无限制）
2. valuation表 → 估值数据（无限制）
3. get_price → 价格数据（无限制）
4. finance表 → 需要正式账户
```

---

## 📝 代码示例

### 获取indicator表数据

```python
from jqdatasdk import query, indicator

# 查询所有可用字段
q = query(
    indicator.code,
    indicator.roe,
    indicator.roa,
    indicator.net_profit_margin,
    indicator.gross_profit_margin,
    indicator.inc_revenue_year_on_year,
    indicator.inc_net_profit_year_on_year,
    indicator.eps,
    indicator.ocf_to_operating_profit,  # 现金流代理指标
    indicator.ocf_to_revenue
).filter(
    indicator.code == '000001.XSHE'
)

df = get_fundamentals(q, date='2025-09-18')
```

---

## 🔄 与之前实现的对比

### 之前的问题

1. ❌ 使用了不存在的字段：`indicator.asset_liability_ratio`
2. ❌ 使用了不存在的字段：`indicator.current_ratio`
3. ❌ 尝试访问受限表：`finance.STK_CASHFLOW_STATEMENT`
4. ❌ 尝试访问受限表：`finance.STK_BALANCE_SHEET`

### 现在的解决方案

1. ✅ 只使用indicator表的36个可用字段
2. ✅ 使用`ocf_to_operating_profit`和`ocf_to_revenue`作为现金流代理
3. ✅ 对于受限字段使用默认值或估算
4. ✅ 所有数据获取都基于可用字段

---

## 📚 相关文档

- JQData官方文档: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9885&keyword=Indicator
- 知识库条目: JQData Indicator表完整字段列表和权限说明

---

*报告版本: 1.0 | 创建时间: 2025-12-19*

