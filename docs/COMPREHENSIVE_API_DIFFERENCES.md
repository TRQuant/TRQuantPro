## ⚠️ 重要说明

根据[BulletTrade官方文档](https://bullettrade.cn/docs/)，BulletTrade是**"兼容聚宽API的量化研究与交易框架"**。

**关键结论**：
- ✅ **BulletTrade和聚宽API完全兼容** - 无需转换
- ✅ 聚宽策略可以在BulletTrade中**无修改运行**
- ⚠️ **只有转换为PTrade时才需要转换** - 因为PTrade使用不同的API

**转换关系**：
```
聚宽策略 → BulletTrade策略: ✅ 完全兼容，只需添加 from jqdata import *
BulletTrade策略 → 聚宽策略: ✅ 完全兼容，无需转换
BulletTrade/聚宽策略 → PTrade策略: ⚠️ 需要转换（使用完整转换器）
```

---

# PTrade vs BulletTrade/聚宽 完整API差异对照表

## 📋 基于网页搜索结果和实际代码分析的完整差异

### 1. 模块导入

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `from jqdata import *` | ❌ **删除** | PTrade API内置，不需要导入 |
| `from kuanke.user_space_api import *` | ❌ **删除** | PTrade不需要 |
| `import pandas as pd` | ✅ 相同 | 需要时导入 |
| `import numpy as np` | ✅ 相同 | 需要时导入 |

### 2. 初始化函数

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `def initialize(context):` | ✅ 相同 | 函数签名相同 |
| `set_universe(security_list)` | ✅ 相同 | 设置股票池 |
| `set_benchmark(security)` | ✅ 相同 | 设置基准 |

### 3. 佣金设置

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')` | `set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))` | **关键差异** |
| `set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))` | ✅ 相同 | 两个平台都支持 |
| `set_commission(commission_ratio=0.0003, min_commission=5.0, type="STOCK")` | ⚠️ 某些版本 | 网页搜索结果，但实际代码使用PerTrade |

**转换规则**:
```python
# 聚宽格式
set_order_cost(OrderCost(
    open_tax=0,
    close_tax=0.001,
    open_commission=0.0003,
    close_commission=0.0003,
    min_commission=5
), type='stock')

# 转换为PTrade格式
buy_cost = 0.0003
sell_cost = 0.0003 + 0.001  # 佣金 + 印花税
set_commission(PerTrade(buy_cost=buy_cost, sell_cost=sell_cost, min_cost=5))
```

### 4. 滑点设置

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `set_slippage(FixedSlippage(0.001))` | ✅ 相同 | 两个平台都支持 |
| `set_slippage(PriceRelatedSlippage(0.002))` | `set_slippage(FixedSlippage(0.002))` | 转换为FixedSlippage |
| `set_slippage(0.001)` | ⚠️ 某些版本 | 直接数值，某些PTrade版本支持 |
| `set_fixed_slippage(fixedslippage=0.02)` | ⚠️ 某些版本 | 网页搜索结果，但实际代码使用set_slippage |

**转换规则**:
```python
# 保持FixedSlippage格式（推荐）
set_slippage(FixedSlippage(0.001))

# PriceRelatedSlippage转换为FixedSlippage
set_slippage(PriceRelatedSlippage(0.002))  # 聚宽
set_slippage(FixedSlippage(0.002))  # PTrade
```

### 5. 数据获取 - 历史数据

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `get_price(security, start_date='2025-01-01', end_date='2025-12-31', frequency='daily', fields=['close'], count=20, panel=False)` | `get_history(20, '1d', security_list, ['close'], skip_paused=False, fq='pre')` | **关键差异** |
| `get_price(security, count=20, end_date=date, frequency='daily', fields=['close'], panel=False)` | `get_history(20, '1d', security_list, ['close'])` | 参数顺序和名称不同 |

**转换规则**:
```python
# 聚宽格式
prices = get_price(
    stocks,
    end_date=context.current_dt.strftime('%Y-%m-%d'),
    frequency='daily',
    fields=['close'],
    count=20,
    panel=False
)
close_df = prices.pivot(index='time', columns='code', values='close')

# PTrade格式
prices = get_history(20, '1d', stocks, ['close'], skip_paused=False, fq='pre')
close_df = prices['close']  # 返回dict格式
```

### 6. 数据获取 - 当前数据

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `get_current_data()` | `get_snapshot(stock_list)` | **关键差异** |
| `current_data = get_current_data()`<br>`data = current_data[stock]` | `snapshots = get_snapshot([stock1, stock2, ...])`<br>`data = snapshots[stock]` | 需要传入股票列表 |

**转换规则**:
```python
# 聚宽格式
current_data = get_current_data()  # 获取所有股票
data = current_data[stock]

# PTrade格式
# 需要传入股票列表
stocks = ['000001.SZ', '000002.SZ']
snapshots = get_snapshot(stocks)
data = snapshots['000001.SZ']
```

### 7. 数据获取 - 股票信息

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `get_security_info(stock)` | `get_instrument(stock)` | 函数名不同 |
| `get_all_securities(['stock'])` | `get_all_securities('stock')` | 参数格式可能不同 |
| `get_index_stocks('000300.XSHG')` | `get_index_stocks('000300.SH')` | 股票代码格式不同 |

### 8. 数据获取 - 其他

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `get_extras('is_st', stocks, start_date=date, end_date=date, df=True)` | ❌ **不支持** | 需要通过股票名称判断 |
| `get_fundamentals(query, date)` | `get_fundamentals(query, date)` | ✅ 可能相同 |
| `attribute_history(security, count, unit, fields)` | `get_history(count, unit, security, fields)` | 函数名不同 |

### 9. 交易执行

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `order(security, amount)` | ✅ 相同 | 函数签名相同 |
| `order_target(security, amount)` | `order_target_volume(security, amount)` | 函数名不同 |
| `order_target_value(security, value)` | ✅ 相同 | 函数签名相同 |
| `order_value(security, value)` | ✅ 可能相同 | 需要验证 |
| `order_percent(security, percent)` | ✅ 可能相同 | 需要验证 |

### 10. 持仓访问

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `context.portfolio.positions` | ✅ 相同 | 两个平台都支持 |
| `context.portfolio.positions[stock]` | ✅ 相同 | 访问方式相同 |
| `context.portfolio.total_value` | ✅ 相同 | 总资产 |
| `context.portfolio.available_cash` | ✅ 可能相同 | 可用现金 |
| `get_positions()` | ⚠️ 网页搜索 | 某些版本可能有此函数 |

### 11. 日志输出

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `log.info('message')` | ✅ 相同 | 两个平台都支持 |
| `log.warn('message')` | ✅ 相同 | 两个平台都支持 |
| `log.error('message')` | ✅ 相同 | 两个平台都支持 |
| `log.debug('message')` | ✅ 可能相同 | 需要验证 |
| `log('message')` | ⚠️ 网页搜索 | 某些版本可能有此函数 |

### 12. 定时任务

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `run_daily(func, time='09:00')` | ✅ 相同 | 函数签名可能相同 |
| `run_daily(func, '09:00')` | ✅ 相同 | 参数格式可能不同 |
| `run_weekly(func, weekday=1, time='09:00')` | ✅ 可能相同 | 需要验证 |
| `run_monthly(func, monthday=1, time='09:00')` | ✅ 可能相同 | 需要验证 |

### 13. 事件处理函数

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `def initialize(context):` | ✅ 相同 | 初始化函数 |
| `def before_market_open(context):` | ✅ 可能相同 | 盘前处理 |
| `def market_open(context):` | ✅ 可能相同 | 开盘处理 |
| `def handle_data(context, data):` | `def on_bar(context, data):` | **关键差异** |
| `def after_market_close(context):` | ✅ 可能相同 | 收盘处理 |
| `def before_trading_start(context, data):` | ✅ 可能相同 | 交易开始前 |

### 14. 数据对象属性

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `data.day_open` | `data.open` | 属性名不同 |
| `data.high_limit` | `data.up_limit` | 属性名不同 |
| `data.low_limit` | `data.down_limit` | 属性名不同 |
| `data.last_price` | `data.last_px` | 属性名不同 |
| `data.paused` | ✅ 可能相同 | 停牌状态 |
| `data.is_st` | ❌ 不支持 | 需要通过名称判断 |

### 15. 股票代码格式

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `'000300.XSHG'` | `'000300.SH'` | 后缀不同 |
| `'000001.XSHE'` | `'000001.SZ'` | 后缀不同 |
| `'600570.SS'` | ⚠️ 网页搜索 | 某些版本使用.SS |

**注意**: 根据实际代码，PTrade可能也支持`.XSHG`和`.XSHE`格式，需要根据实际PTrade版本确定。

### 16. 全局变量

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `g.variable` | ✅ 相同 | 全局变量访问方式相同 |
| `context.variable` | ✅ 相同 | 上下文变量访问方式相同 |

### 17. 其他API

| BulletTrade/聚宽 | PTrade | 说明 |
|-----------------|--------|------|
| `query(...)` | ✅ 可能相同 | 财务数据查询 |
| `get_trade_days(start_date, end_date)` | ✅ 可能相同 | 交易日获取 |
| `is_trade_day(date)` | ✅ 可能相同 | 判断交易日 |

## 🔄 转换优先级

### 必须转换（否则无法运行）

1. ✅ 删除`from jqdata import *`
2. ✅ `get_current_data()` -> `get_snapshot(stocks)`
3. ✅ `get_price()` -> `get_history()`
4. ✅ `set_order_cost()` -> `set_commission(PerTrade(...))`
5. ✅ 属性名转换（`day_open` -> `open`等）

### 建议转换（提高兼容性）

1. ⚠️ `get_security_info()` -> `get_instrument()`
2. ⚠️ `order_target()` -> `order_target_volume()`
3. ⚠️ 股票代码格式（根据PTrade版本）

### 可选转换（功能相同）

1. ℹ️ `log.info()` 保持不变（两个平台都支持）
2. ℹ️ `context.portfolio.positions` 保持不变
3. ℹ️ `run_daily()` 保持不变（参数格式可能不同）

## 📝 转换检查清单

转换完成后，检查以下项目：

- [ ] 无`from jqdata import *`
- [ ] 所有`get_current_data()`已转换为`get_snapshot()`
- [ ] 所有`get_price()`已转换为`get_history()`
- [ ] `set_commission`使用`PerTrade`格式
- [ ] `set_slippage`使用`FixedSlippage`格式
- [ ] 属性访问使用PTrade格式（`open`而不是`day_open`）
- [ ] 股票代码格式正确（根据PTrade版本）
- [ ] 日志输出正常
- [ ] 交易执行正常

## 🔗 参考资源

- PTrade API文档: https://ptradeapi.com/
- 聚宽API文档: https://www.joinquant.com/help/api/help
- BulletTrade文档: 本地文档
- Quant2Ptrader-MCP: https://github.com/guangxiangdebizi/Quant2Ptrader-MCP
