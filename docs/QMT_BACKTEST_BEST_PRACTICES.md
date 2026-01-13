# QMT 回测最佳实践

## 概述

本文档总结了在QMT平台进行策略回测的最佳实践，基于实际开发经验和官方文档。

## 1. 策略结构

### 1.1 必需函数

```python
def init(ContextInfo):
    """策略初始化 - 必需"""
    pass

def handlebar(ContextInfo):
    """每个K线bar调用 - 必需"""
    pass
```

### 1.2 可选函数

```python
def after_trading_end(ContextInfo):
    """收盘后调用"""
    pass

def before_trading_start(ContextInfo):
    """开盘前调用"""
    pass
```

## 2. init函数配置

### 2.1 标准配置

```python
def init(ContextInfo):
    # 获取股票池（沪深300）
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    
    # 初始化追踪变量
    ContextInfo.holdings = {i: 0 for i in ContextInfo.s}
    ContextInfo.money = ContextInfo.capital
    ContextInfo.profit = 0
    ContextInfo.accountID = 'testS'  # 回测账户
```

### 2.2 可选：滑点和手续费设置

```python
# 设置滑点 (类型, 值)
# 类型: 0=百分比, 1=固定值
ContextInfo.set_slippage(1, 0.02)  # 固定滑点0.02元

# 设置手续费 [买入印花税, 卖出印花税, 开仓佣金, 平仓佣金, 平今佣金, 最低佣金]
ContextInfo.set_commission(0, [0, 0.001, 0.0003, 0.0003, 0, 5])
```

## 3. handlebar函数

### 3.1 核心模式

```python
def handlebar(ContextInfo):
    d = ContextInfo.barpos  # 当前bar索引
    
    # 获取价格数据
    price = ContextInfo.get_history_data(1, '1d', 'open', 3)
    
    # 控制调仓频率
    if d > 60 and d % 20 == 0:  # 60天预热，每20天调仓
        execute_rebalance(ContextInfo, price)
```

### 3.2 获取日期

```python
def timetag_to_datetime(timetag, format_str='%Y%m%d'):
    from datetime import datetime
    if timetag > 1e10:  # 毫秒级时间戳
        return datetime.fromtimestamp(timetag / 1000.0)
    return datetime.fromtimestamp(timetag)

# 在handlebar中使用
nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')
print(nowDate.strftime('%Y-%m-%d'))
```

## 4. 数据获取

### 4.1 get_history_data

```python
# 函数签名
ContextInfo.get_history_data(count, period, field, stock_list)

# 参数说明
# count: K线数量 (int)
# period: '1d', '1m', '5m', '15m', '30m', '60m'
# field: 'open', 'high', 'low', 'close', 'volume'
# stock_list: 股票列表或索引 (3=全部股票池)

# 返回值: {stock_code: [values]}
```

### 4.2 使用示例

```python
# 获取所有股票最近22天收盘价
data_close = ContextInfo.get_history_data(22, '1d', 'close', 3)

# 检查并使用数据
for stock in ContextInfo.s:
    if stock in data_close and len(data_close[stock]) >= 20:
        close_prices = data_close[stock]
        latest_close = close_prices[-1]
        close_20d_ago = close_prices[-20]
```

## 5. 交易执行

### 5.1 order_shares封装

```python
def order_shares(stock_code, amount, order_type, price, ContextInfo, account_id):
    """
    执行下单
    
    参数:
        stock_code: 股票代码 (如 '000001.SZ')
        amount: 数量 (正数买入，负数卖出)
        order_type: 'fix'=限价, 'market'=市价
        price: 价格
        ContextInfo: 上下文对象
        account_id: 账户ID
    """
    if amount == 0:
        return
    try:
        ContextInfo.order(stock_code, amount, order_type, price, account_id)
        direction = "BUY" if amount > 0 else "SELL"
        print(f"  [{direction}] {stock_code}: {abs(amount)} shares @ {price:.2f}")
    except Exception as e:
        print(f"  [Order Error] {stock_code}: {e}")
```

### 5.2 买卖示例

```python
# 买入
if stock in price and price[stock]:
    buy_price = price[stock][-1] if isinstance(price[stock], list) else price[stock]
    order_amount = int(money_per_stock / buy_price) // 100  # 计算手数
    if order_amount > 0:
        order_shares(stock, order_amount * 100, 'fix', buy_price, ContextInfo, ContextInfo.accountID)
        ContextInfo.holdings[stock] = order_amount
        ContextInfo.buypoint[stock] = buy_price

# 卖出
if ContextInfo.holdings[stock] > 0:
    sell_amount = ContextInfo.holdings[stock] * 100
    order_shares(stock, -sell_amount, 'fix', sell_price, ContextInfo, ContextInfo.accountID)
    ContextInfo.holdings[stock] = 0
```

## 6. 常见问题

### 6.1 handlebar不执行

**原因**: 
- 使用了时间字符串判断（如 `current_time >= '09:35:00'`）
- barpos条件设置不当

**解决**:
```python
# 正确方式：使用barpos控制
if d > 60 and d % 20 == 0:
    # 执行调仓
```

### 6.2 编码错误

**原因**: QMT默认使用GBK编码

**解决**:
```python
# 文件开头添加
#coding:gbk

# 或使用纯ASCII（推荐）
# -*- coding: ascii -*-
```

### 6.3 没有交易记录

**原因**:
- get_history_data返回的是dict，需要检查stock是否在dict中
- 价格数据格式处理不当

**解决**:
```python
if stock in price and price[stock]:
    p = price[stock][-1] if isinstance(price[stock], list) else price[stock]
```

### 6.4 无效股票代码

**原因**: 退市或停牌股票

**解决**: 可以忽略警告，或在选股时过滤

### 6.5 run_time参数错误

**原因**: QMT的run_time不支持weekday参数

**解决**: 在handlebar中用barpos判断周几

## 7. 策略模板

### 7.1 模板位置

```
core/advisor_v4/qmt_templates/
├── __init__.py
├── backtest_basic.py    # 基础回测模板
├── backtest_factor.py   # 多因子回测模板
└── live_basic.py        # 基础实盘模板
```

### 7.2 使用模板

```python
from core.advisor_v4.qmt_templates import get_template, list_templates

# 列出可用模板
print(list_templates())

# 获取模板内容
template_code = get_template('backtest_basic')
```

## 8. MCP工具

### 8.1 策略验证

```python
# 验证QMT策略代码
result = strategy.qmt.validate(code)
# 返回: {valid: bool, errors: [], warnings: [], info: []}
```

### 8.2 文档获取

```python
# 获取QMT API文档
result = strategy.qmt.fetch_docs("get_history_data")
```

### 8.3 策略转换

```python
# 转换策略代码
result = strategy.convert(code, source="jqdata", target="qmt")
```

## 9. 参考资源

- QMT官方文档: https://qmt.ptradeapi.com/QMT_Python_API_Doc.html
- 迅投论坛: https://www.xuntou.net/forum.php
- TRQuant知识库: `kb.search("qmt")`

## 更新日志

- 2026-01-09: 初始版本，基于实际开发经验
