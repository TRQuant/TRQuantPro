# 策略代码格式详细说明

## 📋 当前代码格式

**当前文件**: `strategies/qmt/TRQuant_AI_Theme_V1.py`

**格式类型**: **QMT格式** (迅投极速交易终端)

---

## 🔍 格式识别特征

### QMT格式特征（当前代码）

```python
#coding:gbk  # QMT必须使用GBK编码

def init(ContextInfo):  # 初始化函数
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    ContextInfo.money = ContextInfo.capital

def handlebar(ContextInfo):  # 主循环函数
    d = ContextInfo.barpos  # 当前bar位置
    price = ContextInfo.get_history_data(1, '1d', 'open', 0)
    # 交易逻辑...
```

**关键特征**:
- ✅ `def init(ContextInfo):` - 初始化函数
- ✅ `def handlebar(ContextInfo):` - 主循环函数
- ✅ `ContextInfo.get_history_data()` - 获取历史数据
- ✅ `ContextInfo.get_sector()` - 获取板块股票
- ✅ `ContextInfo.set_universe()` - 设置股票池
- ✅ `ContextInfo.barpos` - 当前bar位置
- ✅ `#coding:gbk` - GBK编码声明

---

## 📊 三种主流格式对比

### 1. QMT格式（当前代码）

| 项目 | QMT格式 |
|------|---------|
| **平台** | 迅投极速交易终端 (QMT) |
| **编码** | GBK (`#coding:gbk`) |
| **初始化** | `def init(ContextInfo):` |
| **主循环** | `def handlebar(ContextInfo):` |
| **获取数据** | `ContextInfo.get_history_data(days, '1d', field, mode)` |
| **股票池** | `ContextInfo.get_sector('000300.SH')` |
| **当前时间** | `ContextInfo.barpos` (bar位置) |
| **下单** | 手动模拟 or `ContextInfo.order()` |
| **持仓** | `ContextInfo.holdings` (dict) |
| **资金** | `ContextInfo.money` / `ContextInfo.capital` |

**示例代码**:
```python
#coding:gbk
def init(ContextInfo):
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    ContextInfo.holdings = {}
    ContextInfo.money = ContextInfo.capital

def handlebar(ContextInfo):
    d = ContextInfo.barpos
    if d > 22 and d % 5 == 0:
        # 调仓逻辑
        data = ContextInfo.get_history_data(22, '1d', 'close', 0)
        # ...
```

---

### 2. 聚宽格式 (JoinQuant)

| 项目 | 聚宽格式 |
|------|---------|
| **平台** | 聚宽量化平台 |
| **编码** | UTF-8 |
| **初始化** | `def initialize(context):` |
| **主循环** | `def handle_data(context, data):` |
| **获取数据** | `get_price()` / `history()` |
| **股票池** | `get_index_stocks('000300.XSHG')` |
| **当前时间** | `context.current_dt` |
| **下单** | `order()` / `order_target()` |
| **持仓** | `context.portfolio.positions` |
| **资金** | `context.portfolio.available_cash` |

**示例代码**:
```python
# -*- coding: utf-8 -*-
def initialize(context):
    g.stocks = get_index_stocks('000300.XSHG')
    set_order_cost(OrderCost(
        open_commission=0.0003,
        close_commission=0.0003,
        close_tax=0.001,
        min_commission=5
    ), type='stock')

def handle_data(context, data):
    current_date = context.current_dt.date()
    if current_date.weekday() == 0:  # 周一调仓
        # 调仓逻辑
        prices = history(20, '1d', 'close', g.stocks)
        # ...
        order_target_percent(stock, 0.1)
```

---

### 3. PTrade格式 (聚宽PTrade)

| 项目 | PTrade格式 |
|------|-----------|
| **平台** | 聚宽PTrade平台 |
| **编码** | UTF-8 |
| **初始化** | `def initialize(context):` |
| **主循环** | `def handle_data(context, data):` |
| **获取数据** | `get_price()` / `history()` |
| **股票池** | `get_all_securities()` |
| **当前时间** | `context.current_dt` |
| **下单** | `order()` / `order_target()` |
| **持仓** | `context.portfolio.positions` |
| **资金** | `context.portfolio.available_cash` |

**示例代码**:
```python
# -*- coding: utf-8 -*-
def initialize(context):
    g.stocks = get_all_securities(types=['stock']).index.tolist()
    set_order_cost(OrderCost(
        open_commission=0.0003,
        close_commission=0.0003,
        close_tax=0.001,
        min_commission=5
    ), type='stock')

def handle_data(context, data):
    current_date = context.current_dt.date()
    # 交易逻辑
    order_target_percent(stock, 0.1)
```

---

## 🔄 格式转换对照表

### 函数名对照

| 功能 | QMT | 聚宽 | PTrade |
|------|-----|------|--------|
| 初始化 | `init(ContextInfo)` | `initialize(context)` | `initialize(context)` |
| 主循环 | `handlebar(ContextInfo)` | `handle_data(context, data)` | `handle_data(context, data)` |
| 盘前 | - | `before_trading_start(context)` | `before_trading_start(context)` |
| 盘后 | - | `after_trading_end(context)` | `after_trading_end(context)` |

### 数据获取对照

| 功能 | QMT | 聚宽 | PTrade |
|------|-----|------|--------|
| 历史价格 | `ContextInfo.get_history_data(22, '1d', 'close', 0)` | `history(22, '1d', 'close', stocks)` | `history(22, '1d', 'close', stocks)` |
| 当前价格 | `ContextInfo.get_history_data(1, '1d', 'open', 0)` | `data[stock].close` | `data[stock].close` |
| 股票池 | `ContextInfo.get_sector('000300.SH')` | `get_index_stocks('000300.XSHG')` | `get_all_securities(types=['stock'])` |

### 交易函数对照

| 功能 | QMT | 聚宽 | PTrade |
|------|-----|------|--------|
| 买入 | 手动模拟 | `order(stock, amount)` | `order(stock, amount)` |
| 卖出 | 手动模拟 | `order(stock, -amount)` | `order(stock, -amount)` |
| 目标仓位 | 手动计算 | `order_target_percent(stock, 0.1)` | `order_target_percent(stock, 0.1)` |

### 持仓和资金对照

| 功能 | QMT | 聚宽 | PTrade |
|------|-----|------|--------|
| 持仓数量 | `ContextInfo.holdings[stock]` | `context.portfolio.positions[stock].total_amount` | `context.portfolio.positions[stock].total_amount` |
| 可用资金 | `ContextInfo.money` | `context.portfolio.available_cash` | `context.portfolio.available_cash` |
| 总资产 | 手动计算 | `context.portfolio.total_value` | `context.portfolio.total_value` |

---

## 📝 当前代码详细说明

### 文件位置
```
strategies/qmt/TRQuant_AI_Theme_V1.py
```

### 格式确认

✅ **QMT格式** - 用于迅投极速交易终端

### 关键代码片段

```python
# 1. 编码声明（QMT必须）
#coding:gbk

# 2. 初始化函数（QMT标准）
def init(ContextInfo):
    ContextInfo.s = AI_THEME_STOCKS
    ContextInfo.set_universe(ContextInfo.s)
    ContextInfo.holdings = {}
    ContextInfo.money = ContextInfo.capital

# 3. 主循环函数（QMT标准）
def handlebar(ContextInfo):
    d = ContextInfo.barpos  # 当前bar位置
    
    # 4. 获取历史数据（QMT方式）
    data_close = ContextInfo.get_history_data(22, '1d', 'close', 0)
    
    # 5. 获取当前价格（QMT方式）
    current_prices = ContextInfo.get_history_data(1, '1d', 'open', 0)
    
    # 6. 手动模拟交易（QMT常用方式）
    order_shares(stock, amount, price, ContextInfo)
```

---

## ⚠️ 重要区别

### 1. 编码格式

| 格式 | 编码 | 说明 |
|------|------|------|
| QMT | GBK | 必须使用 `#coding:gbk` |
| 聚宽 | UTF-8 | 使用 `# -*- coding: utf-8 -*-` |
| PTrade | UTF-8 | 使用 `# -*- coding: utf-8 -*-` |

### 2. 数据获取方式

**QMT**:
```python
# 返回dict格式 {stock: [values]}
data = ContextInfo.get_history_data(22, '1d', 'close', 0)
close = data.get(stock, [])
```

**聚宽/PTrade**:
```python
# 返回DataFrame
prices = history(22, '1d', 'close', stocks)
close = prices[stock].values
```

### 3. 股票代码格式

| 格式 | 示例 | 说明 |
|------|------|------|
| QMT | `000300.SH` | 上海用`.SH`，深圳用`.SZ` |
| 聚宽 | `000300.XSHG` | 上海用`.XSHG`，深圳用`.XSHE` |
| PTrade | `000300.XSHG` | 同聚宽格式 |

### 4. 交易执行

**QMT**: 通常需要手动模拟交易（计算资金、持仓、费用）
```python
def order_shares(stock, amount, price, ContextInfo):
    trade_value = amount * price
    fee = calculate_trade_cost(trade_value, direction)
    ContextInfo.money -= trade_value + fee
    ContextInfo.holdings[stock] += amount // 100
```

**聚宽/PTrade**: 平台自动处理
```python
order(stock, amount)  # 平台自动计算费用和持仓
```

---

## 🎯 总结

### 当前代码格式

✅ **QMT格式** (迅投极速交易终端)

### 使用场景

- ✅ 在QMT客户端中回测
- ✅ 在QMT客户端中实盘交易
- ❌ 不能在聚宽平台使用
- ❌ 不能在PTrade平台使用

### 如需转换为其他格式

如果需要转换为聚宽或PTrade格式，需要：
1. 修改函数名：`init` → `initialize`, `handlebar` → `handle_data`
2. 修改数据获取：`get_history_data()` → `history()`
3. 修改交易方式：手动模拟 → `order()` / `order_target()`
4. 修改编码：GBK → UTF-8
5. 修改股票代码格式：`.SH`/`.SZ` → `.XSHG`/`.XSHE`

---

**最后更新**: 2026-01-12
**文档作者**: TRQuant Team
