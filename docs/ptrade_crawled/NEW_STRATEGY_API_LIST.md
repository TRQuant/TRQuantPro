# PTrade API - 新建策略页面可调用接口列表

> **页面**: https://ptradeapi.com/#%E6%96%B0%E5%BB%BA%E7%AD%96%E7%95%A5 (新建策略)  
> **生成时间**: 2026-01-09  
> **说明**: 新建策略后可以调用的所有API接口

---

## 📋 业务流程框架

PTrade量化引擎以事件触发为基础，通过以下事件来完成每个交易日的策略任务：

### 事件触发流程

```
initialize (初始化) 
    ↓
before_trading_start (盘前) [可选]
    ↓
handle_data (盘中) [必选]
    ↓
tick_data (tick级别) [可选]
    ↓
after_trading_end (盘后) [可选]
```

---

## 🔧 必选函数（必须实现）

### 1. `initialize(context)` - 初始化函数

**说明**: 策略初始化函数，在策略开始运行时调用一次

**调用时机**: 策略启动时执行一次

**用途**:
- 设置股票池
- 设置基准
- 设置佣金费率
- 设置滑点
- 初始化全局变量

**示例**:
```python
def initialize(context):
    # 设置股票池
    g.security = "600570.SS"
    set_universe(g.security)
    
    # 设置基准
    set_benchmark("000300.XSHG")
    
    # 设置佣金费率
    set_commission(Commission(buycost=0.0003, sellcost=0.0013, mincost=5))
```

---

### 2. `handle_data(context, data)` - 盘中处理函数

**说明**: 盘中处理函数，在每个交易周期（日线/分钟线）触发

**调用时机**: 
- 日线级别：每个交易日触发一次
- 分钟级别：每分钟触发一次

**用途**:
- 获取行情数据
- 计算技术指标
- 执行交易逻辑
- 风险控制

**限制**: 
- 仅支持日线和分钟级别的盘中处理
- tick级别需要使用 `tick_data()` 或 `run_interval()`

**示例**:
```python
def handle_data(context, data):
    # 获取当前价格
    current_price = data.current(g.security, 'close')
    
    # 执行交易逻辑
    if current_price > 10:
        order(g.security, 100)
```

---

## 🔧 可选函数（按需实现）

### 3. `before_trading_start(context, data)` - 盘前处理函数

**说明**: 盘前处理函数，在每个交易日开盘前调用

**调用时机**: 每个交易日开盘前

**用途**:
- 盘前数据准备
- 盘前交易计划
- 盘前风险检查

**示例**:
```python
def before_trading_start(context, data):
    # 盘前准备
    log.info("交易日开始")
```

---

### 4. `after_trading_end(context)` - 盘后处理函数

**说明**: 盘后处理函数，在每个交易日收盘后调用

**调用时机**: 每个交易日收盘后

**用途**:
- 盘后数据统计
- 盘后报告生成
- 盘后数据保存

**示例**:
```python
def after_trading_end(context):
    # 盘后处理
    positions = get_positions()
    log.info(f"当前持仓: {positions}")
```

---

### 5. `tick_data(context, tick)` - Tick级别处理函数

**说明**: Tick级别处理函数，用于处理逐笔行情数据

**调用时机**: 每个tick数据到达时

**用途**:
- 高频交易策略
- 实时行情处理
- Tick级别交易

**限制**: 仅支持tick级别的盘中处理

**示例**:
```python
def tick_data(context, tick):
    # 处理tick数据
    if tick.security == g.security:
        # 执行tick级别逻辑
        pass
```

---

### 6. `on_order_response(context, order)` - 委托主推事件

**说明**: 委托响应回调函数，当委托状态变化时触发

**调用时机**: 委托状态变化时

**用途**:
- 委托状态监控
- 委托失败处理
- 委托确认逻辑

**示例**:
```python
def on_order_response(context, order):
    if order.status == 'filled':
        log.info(f"委托成交: {order.security}")
```

---

### 7. `on_trade_response(context, trade)` - 交易主推事件

**说明**: 交易响应回调函数，当交易成交时触发

**调用时机**: 交易成交时

**用途**:
- 成交确认
- 成交后处理
- 成交统计

**示例**:
```python
def on_trade_response(context, trade):
    log.info(f"交易成交: {trade.security}, 数量: {trade.amount}")
```

---

## ⚙️ 设置函数（在initialize中调用）

### 股票池设置

#### `set_universe(security_list)` - 设置股票池

**说明**: 设置策略要操作的股票池

**参数**:
- `security_list`: 股票代码列表或单个股票代码

**示例**:
```python
set_universe(['600570.SS', '000001.SZ'])
# 或
set_universe('600570.SS')
```

---

#### `set_benchmark(security)` - 设置基准

**说明**: 设置策略的基准指数

**参数**:
- `security`: 基准指数代码（如：'000300.XSHG' 沪深300）

**示例**:
```python
set_benchmark('000300.XSHG')  # 沪深300
```

---

### 交易成本设置

#### `set_commission(commission)` - 设置佣金费率

**说明**: 设置交易佣金费率

**参数**:
- `commission`: Commission对象，包含买入成本、卖出成本、最小成本

**示例**:
```python
from ptrade import Commission

set_commission(Commission(
    buycost=0.0003,   # 买入佣金率 0.03%
    sellcost=0.0013,  # 卖出佣金率 0.13%（含印花税）
    mincost=5         # 最小佣金 5元
))
```

---

#### `set_slippage(slippage)` - 设置滑点

**说明**: 设置交易滑点

**参数**:
- `slippage`: Slippage对象

**示例**:
```python
from ptrade import Slippage

set_slippage(Slippage(0.002))  # 0.2%滑点
```

---

#### `set_fixed_slippage(slippage)` - 设置固定滑点

**说明**: 设置固定金额滑点

**参数**:
- `slippage`: 固定滑点金额

**示例**:
```python
set_fixed_slippage(0.01)  # 固定0.01元滑点
```

---

### 其他设置

#### `set_volume_ratio(ratio)` - 设置成交比例

**说明**: 设置回测时的成交比例

**参数**:
- `ratio`: 成交比例（0-1之间）

**示例**:
```python
set_volume_ratio(0.25)  # 25%成交比例
```

---

#### `set_limit_mode(mode)` - 设置回测成交数量限制模式

**说明**: 设置回测时的成交数量限制模式

**参数**:
- `mode`: 限制模式

---

#### `set_yesterday_position(positions)` - 设置底仓（股票）

**说明**: 设置策略的初始持仓（底仓）

**参数**:
- `positions`: 持仓列表

**示例**:
```python
set_yesterday_position([
    {'security': '600570.SS', 'amount': 1000}
])
```

---

#### `set_parameters(**kwargs)` - 设置策略配置参数

**说明**: 设置策略的配置参数

**参数**:
- `**kwargs`: 参数字典

**示例**:
```python
set_parameters(
    period=20,
    threshold=0.05
)
```

---

#### `set_email_info(email, password, smtp_server, smtp_port)` - 设置邮件信息

**说明**: 设置邮件通知信息

**参数**:
- `email`: 邮箱地址
- `password`: 邮箱密码
- `smtp_server`: SMTP服务器
- `smtp_port`: SMTP端口

---

## 📅 定时周期性函数

### `run_daily(func, time)` - 按日周期处理

**说明**: 设置每日定时执行的任务

**参数**:
- `func`: 要执行的函数
- `time`: 执行时间（格式：'HH:MM'）

**示例**:
```python
def daily_task(context):
    log.info("每日任务执行")

run_daily(daily_task, '14:30')  # 每天14:30执行
```

---

### `run_interval(func, interval)` - 按设定周期处理

**说明**: 设置按指定周期执行的任务

**参数**:
- `func`: 要执行的函数
- `interval`: 执行周期（秒）

**示例**:
```python
def interval_task(context):
    log.info("周期任务执行")

run_interval(interval_task, 60)  # 每60秒执行一次
```

---

## 📊 获取信息函数

### 获取基础信息

- `get_trading_day()` - 获取交易日期
- `get_all_trades_days()` - 获取全部交易日期
- `get_trade_days(start_date, end_date)` - 获取指定范围交易日期

### 获取行情信息

- `get_history(security_list, count, unit, fields, ...)` - 获取历史行情
- `get_price(security_list, start_date, end_date, frequency, fields, ...)` - 获取历史数据
- `get_snapshot(security_list, fields)` - 获取行情快照
- `get_tick_direction(security, date)` - 获取分时成交行情
- `get_individual_entrust(security, date)` - 获取逐笔委托行情
- `get_individual_transaction(security, date)` - 获取逐笔成交行情

### 获取股票信息

- `get_stock_name(security)` - 获取股票名称
- `get_stock_info(security)` - 获取股票基础信息
- `get_index_stocks(index_code, date)` - 获取指数成份股
- `get_fundamentals(security_list, date, fields)` - 获取财务数据信息

---

## 💰 交易相关函数

### 股票交易函数

- `order(security, amount)` - 按数量买卖
- `order_target(security, amount)` - 指定目标数量买卖
- `order_value(security, value)` - 指定目标价值买卖
- `order_target_value(security, value)` - 指定持仓市值买卖
- `order_market(security, amount)` - 按市价进行委托
- `get_positions(security_list)` - 获取多支股票持仓信息
- `get_position(security)` - 获取持仓信息

### 公共交易函数

- `cancel_order(order_id)` - 撤单
- `get_open_orders()` - 获取未完成订单
- `get_orders()` - 获取全部订单
- `get_trades()` - 获取当日成交订单

---

## 📝 其他函数

- `log(message, level='INFO')` - 日志记录
- `is_trade(security)` - 业务代码场景判断
- `check_limit(security)` - 代码涨跌停状态判断

---

## 📚 参考文档

- **业务流程框架**: https://ptradeapi.com/#业务流程框架
- **策略API介绍**: https://ptradeapi.com/#策略API介绍
- **设置函数**: https://ptradeapi.com/#设置函数

---

**生成时间**: 2026-01-09  
**来源**: PTrade API文档知识库
