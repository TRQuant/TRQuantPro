# JQData基础数据范围和试用账户权限说明

> **数据来源**: 聚宽官方说明  
> **更新时间**: 2025-12-19

---

## 📋 试用账户权限

| 项目 | 试用账号 | 正式账号 |
|------|----------|----------|
| 账号有效期 | 3个月 | 12个月 |
| 历史数据范围 | 前15个月~前3个月 | 不限制 |
| 连接数 | 1个 | 3个 |
| 每日流量 | 100万条 | 20000万条 |

**历史数据范围说明**:
- 前15个月~前3个月（即距今15个月前至距今最近3个月）
- 不包含最近3个月
- 可调取的历史范围最长为1年

---

## ✅ 基础数据包括（试用账户全部开放）

### 1. 沪深A股行情数据

**包括**:
- 实时和历史行情信息
- 日线、分钟线K线数据
- 价格、成交量、成交额等

**主要接口**:
- `get_price()` - 获取历史K线数据
- `get_bars()` - 获取K线数据（固定划分）
- `get_current_data()` - 获取当前数据

**权限**: ✅ 试用账户完全开放

---

### 2. 上市公司财务数据

**包括**:
- 财务报表数据
- 财务指标（ROE、ROA、增长率等）
- 估值数据（PE、PB、市值等）

**主要接口**:
- `get_fundamentals()` - 查询财务数据
- `indicator` 表 - 财务指标表（36个字段，✅ 无权限限制）
- `valuation` 表 - 市值表（✅ 无权限限制）

**权限说明**:
- ✅ `indicator`表：完全开放（36个字段）
- ✅ `valuation`表：完全开放
- ❌ `finance.STK_CASHFLOW_STATEMENT`：权限限制（需要正式账户）
- ❌ `finance.STK_BALANCE_SHEET`：权限限制（需要正式账户）
- ⚠️ `finance.STK_INCOME_STATEMENT`：需要验证

---

### 3. 指数数据

**包括**:
- 各类市场指数的成分股
- 指数行情信息
- 指数历史数据

**主要接口**:
- `get_index_stocks()` - 获取指数成分股
- `get_all_securities()` - 获取所有证券信息
- `get_price()` - 获取指数行情

**权限**: ✅ 试用账户完全开放

---

### 4. 场内基金数据

**包括**:
- 交易所上市基金的相关数据
- 基金净值、份额等

**主要接口**:
- `get_fundamentals()` - 查询基金数据
- `get_price()` - 获取基金行情

**权限**: ✅ 试用账户完全开放

---

### 5. 场外基金数据

**包括**:
- 非上市基金的净值
- 基金其他信息

**主要接口**:
- `get_fundamentals()` - 查询基金数据

**权限**: ✅ 试用账户完全开放

---

### 6. 期货数据

**包括**:
- 期货合约的行情数据
- 期货交易数据

**主要接口**:
- `get_price()` - 获取期货行情
- `get_fundamentals()` - 查询期货数据

**权限**: ✅ 试用账户完全开放

---

### 7. 期权数据

**包括**:
- 期权合约的相关信息
- 期权行情数据

**主要接口**:
- `get_price()` - 获取期权行情
- `get_fundamentals()` - 查询期权数据

**权限**: ✅ 试用账户完全开放

---

### 8. 宏观经济数据

**包括**:
- 宏观经济指标
- 统计数据

**主要接口**:
- `get_macro_data()` - 获取宏观经济数据

**权限**: ✅ 试用账户完全开放

---

## 🔒 权限限制说明

### ✅ 无权限限制（试用账户可用）

1. **indicator表**: 所有36个字段都可以访问
2. **valuation表**: 完全开放
3. **get_price**: 价格、成交量等完全开放
4. **get_index_stocks**: 指数成分股完全开放
5. **get_all_securities**: 证券信息完全开放

### ❌ 有权限限制（需要正式账户）

1. **finance.STK_CASHFLOW_STATEMENT** (现金流量表)
   - 错误: "非法查询"
   - 说明: 试用账户无法访问

2. **finance.STK_BALANCE_SHEET** (资产负债表)
   - 错误: "非法查询"
   - 说明: 试用账户无法访问

### ⚠️ 特色数据（需要单独申请）

- 需要联系微信号JQData02
- 需要提交公司名片
- 不在基础数据范围内

---

## 💡 使用建议

### 1. 优先使用无限制接口

```python
# ✅ 推荐：indicator表（无权限限制）
from jqdatasdk import query, indicator
q = query(indicator.roe, indicator.net_profit_margin)
df = get_fundamentals(q, date='2025-09-18')

# ✅ 推荐：valuation表（无权限限制）
from jqdatasdk import query, valuation
q = query(valuation.pe_ratio, valuation.market_cap)
df = get_fundamentals(q, date='2025-09-18')

# ✅ 推荐：get_price（无权限限制）
df = get_price('000001.XSHE', start_date='2024-09-11', end_date='2025-09-18')
```

### 2. 现金流数据替代方案

由于现金流量表受权限限制，可以使用indicator表的代理指标：
- `ocf_to_operating_profit`: 经营现金流/营业利润
- `ocf_to_revenue`: 经营现金流/营业收入

### 3. 历史数据范围

- 确保查询日期在权限范围内（前15个月~前3个月）
- 使用`get_permission()`检查权限范围
- 使用`get_available_end_date()`获取最新可用日期

---

## 📊 基础数据接口总结

| 数据类型 | 主要接口 | 试用账户权限 |
|---------|---------|------------|
| 行情数据 | `get_price()`, `get_bars()` | ✅ 完全开放 |
| 财务指标 | `indicator`表 | ✅ 完全开放（36个字段） |
| 估值数据 | `valuation`表 | ✅ 完全开放 |
| 指数数据 | `get_index_stocks()` | ✅ 完全开放 |
| 基金数据 | `get_fundamentals()` | ✅ 完全开放 |
| 期货数据 | `get_price()` | ✅ 完全开放 |
| 期权数据 | `get_price()` | ✅ 完全开放 |
| 宏观数据 | `get_macro_data()` | ✅ 完全开放 |
| 现金流量表 | `finance.STK_CASHFLOW_STATEMENT` | ❌ 权限限制 |
| 资产负债表 | `finance.STK_BALANCE_SHEET` | ❌ 权限限制 |

---

## 🔄 与之前测试的对比

### 测试结果

1. ✅ **indicator表**: 36个字段全部可用，无权限限制
2. ✅ **valuation表**: 完全可用，无权限限制
3. ✅ **get_price**: 完全可用，无权限限制
4. ❌ **finance.STK_CASHFLOW_STATEMENT**: 权限限制
5. ❌ **finance.STK_BALANCE_SHEET**: 权限限制

### 结论

- **基础数据所有接口对试用账户开放** ✅
- 但部分财务表（现金流量表、资产负债表）受权限限制
- 可以使用indicator表的代理指标替代

---

## 📚 相关文档

- JQData官方文档: https://www.joinquant.com/help/api/help?name=api
- Indicator表字段列表: `docs/JQDATA_INDICATOR_FIELDS_REPORT.md`
- API完整参考: `docs/JQDATA_API_COMPLETE.md`

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

