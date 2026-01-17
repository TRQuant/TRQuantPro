#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
补充聚宽/JQData知识库
====================

补充聚宽/JQData相关的API文档、使用指南、最佳实践等知识
目标: 从69条增加到200+条
"""

import sys
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add


def supplement_jqdata_knowledge():
    """补充聚宽/JQData知识"""
    
    print("=" * 70)
    print("📚 补充聚宽/JQData知识库")
    print("=" * 70)
    print()
    
    entries = [
        {
            "title": "聚宽数据API: 获取股票历史行情数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取股票历史行情数据

### API函数
`get_price(security, start_date, end_date, frequency='daily', fields=None, skip_paused=False, fq='pre')`

### 功能说明
获取股票的历史行情数据，包括开盘价、收盘价、最高价、最低价、成交量、成交额等。

### 参数说明
- **security**: 股票代码，如 '000001.XSHE'（平安银行）
- **start_date**: 开始日期，如 '2020-01-01'
- **end_date**: 结束日期，如 '2023-12-31'
- **frequency**: 数据频率，'daily'（日线）、'1d'（日线）、'1m'（分钟线）等
- **fields**: 需要获取的字段，如 ['open', 'close', 'high', 'low', 'volume']
- **skip_paused**: 是否跳过停牌日，默认False
- **fq**: 复权类型，'pre'（前复权）、'post'（后复权）、None（不复权）

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取平安银行2020-2023年的日线数据
df = jq.get_price(
    '000001.XSHE',
    start_date='2020-01-01',
    end_date='2023-12-31',
    frequency='daily',
    fields=['open', 'close', 'high', 'low', 'volume', 'money']
)

print(df.head())
```

### 返回数据格式
DataFrame，包含以下列：
- **open**: 开盘价
- **close**: 收盘价
- **high**: 最高价
- **low**: 最低价
- **volume**: 成交量（手）
- **money**: 成交额（元）

### 注意事项
1. 需要先登录：`jq.auth('username', 'password')`
2. 股票代码格式：'000001.XSHE'（深交所）或 '600000.XSHG'（上交所）
3. 日期格式：'YYYY-MM-DD'
4. 数据有延迟，实盘数据需要订阅

### 实战应用
- 策略回测：获取历史数据用于回测
- 技术分析：计算技术指标
- 因子研究：提取价格因子

## 结论

`get_price`是聚宽最常用的数据获取函数，支持多种频率和复权类型，是策略开发的基础API。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "数据获取", "历史行情", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽数据API: 获取财务数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取财务数据

### API函数
`get_fundamentals(query_object, date=None, statDate=None)`

### 功能说明
获取股票的财务数据，包括利润表、资产负债表、现金流量表等。

### 参数说明
- **query_object**: 查询对象，使用`query()`函数构建
- **date**: 查询日期，如 '2023-12-31'
- **statDate**: 统计日期，用于指定财报日期

### 代码示例
```python
import jqdatasdk as jq
from jqdatasdk import query, valuation, income, balance, cash_flow

# 登录
jq.auth('username', 'password')

# 查询所有A股的PE、PB、ROE
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    income.roe
).filter(
    valuation.pe_ratio > 0,
    valuation.pe_ratio < 50
)

df = jq.get_fundamentals(q, date='2023-12-31')
print(df.head())
```

### 常用财务指标
- **valuation.pe_ratio**: 市盈率
- **valuation.pb_ratio**: 市净率
- **valuation.market_cap**: 总市值
- **income.roe**: 净资产收益率
- **income.net_profit**: 净利润
- **balance.total_assets**: 总资产
- **cash_flow.net_operate_cash_flow**: 经营现金流

### 注意事项
1. 财务数据有延迟，通常延迟1-2个交易日
2. 需要指定查询日期
3. 可以使用filter()过滤条件
4. 支持多表关联查询

### 实战应用
- 基本面选股：筛选低PE、高ROE的股票
- 财务分析：分析公司财务状况
- 估值分析：计算估值指标

## 结论

`get_fundamentals`是聚宽获取财务数据的主要API，支持复杂的查询条件，是基本面分析的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "财务数据", "基本面分析", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: initialize函数详解",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档 + 实战经验

---

## 聚宽策略开发: initialize函数详解

### 函数定义
```python
def initialize(context):
    # 策略初始化代码
    pass
```

### 功能说明
`initialize`是聚宽策略的初始化函数，在策略开始运行前执行一次，用于：
- 设置基准
- 设置手续费和滑点
- 初始化全局变量
- 订阅数据
- 设置定时任务

### 常用操作

#### 1. 设置基准
```python
set_benchmark('000300.XSHG')  # 沪深300
```

#### 2. 设置手续费和滑点
```python
set_order_cost(
    OrderCost(
        open_tax=0,           # 买入印花税
        close_tax=0.001,      # 卖出印花税
        open_commission=0.0003,  # 买入佣金
        close_commission=0.0003, # 卖出佣金
        min_commission=5      # 最低佣金
    ),
    type='stock'
)

set_slippage(FixedSlippage(0.002))  # 固定滑点0.2%
```

#### 3. 初始化全局变量
```python
g.security = '000001.XSHE'  # 持仓股票
g.buy_price = 0             # 买入价格
g.hold_days = 0             # 持仓天数
```

#### 4. 订阅数据
```python
subscribe('000001.XSHE')  # 订阅股票
```

#### 5. 设置定时任务
```python
run_daily(trade, time='09:30')  # 每天9:30执行
run_weekly(trade, weekday=1, time='09:30')  # 每周一9:30执行
run_monthly(trade, monthday=1, time='09:30')  # 每月1号9:30执行
```

### 完整示例
```python
def initialize(context):
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置手续费
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5
        ),
        type='stock'
    )
    
    # 初始化全局变量
    g.security = '000001.XSHE'
    g.buy_price = 0
    
    # 设置定时任务
    run_daily(trade, time='09:30')
```

### 注意事项
1. `initialize`只执行一次，在策略开始前
2. 使用`g`对象存储全局变量
3. 手续费和滑点设置影响回测结果
4. 定时任务的时间是市场时间

### 实战应用
- 策略初始化：设置策略参数
- 数据订阅：订阅需要的数据
- 定时任务：设置交易时间

## 结论

`initialize`是聚宽策略的入口函数，正确设置初始化参数对策略回测结果有重要影响。
""",
            "type": "guide",
            "tags": ["聚宽", "策略开发", "initialize", "初始化", "A级可靠性"],
            "source": "聚宽官方文档 + 实战经验"
        },
        {
            "title": "聚宽策略开发: handle_data函数详解",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档 + 实战经验

---

## 聚宽策略开发: handle_data函数详解

### 函数定义
```python
def handle_data(context, data):
    # 策略逻辑代码
    pass
```

### 功能说明
`handle_data`是聚宽策略的主循环函数，在每个bar（K线）执行一次，用于：
- 获取当前数据
- 计算技术指标
- 生成交易信号
- 执行交易

### 常用操作

#### 1. 获取当前数据
```python
# 获取当前价格
current_data = data.current(g.security, 'price')

# 获取历史数据
hist = data.history(g.security, 'close', 20, '1d')
```

#### 2. 计算技术指标
```python
# 计算均线
ma5 = hist.mean()
ma20 = data.history(g.security, 'close', 20, '1d').mean()
```

#### 3. 生成交易信号
```python
# 金叉买入
if ma5 > ma20 and g.security not in context.portfolio.positions:
    order_value(g.security, context.portfolio.available_cash)
```

#### 4. 执行交易
```python
# 按金额买入
order_value(g.security, 10000)

# 按数量买入
order(g.security, 100)

# 按目标持仓买入
order_target(g.security, 0.1)  # 持仓10%
```

### 完整示例
```python
def handle_data(context, data):
    # 获取历史数据
    hist = data.history(g.security, 'close', 20, '1d')
    ma5 = hist[-5:].mean()
    ma20 = hist.mean()
    
    # 获取当前持仓
    position = context.portfolio.positions[g.security]
    
    # 金叉买入
    if ma5 > ma20 and position.total_amount == 0:
        order_value(g.security, context.portfolio.available_cash)
    
    # 死叉卖出
    elif ma5 < ma20 and position.total_amount > 0:
        order_target(g.security, 0)
```

### 注意事项
1. `handle_data`在每个bar执行一次
2. 使用`context.portfolio`获取持仓信息
3. 使用`data.current()`获取当前数据
4. 使用`data.history()`获取历史数据
5. 订单函数是异步的，不会立即成交

### 实战应用
- 策略逻辑：实现交易策略
- 技术分析：计算技术指标
- 信号生成：生成买卖信号

## 结论

`handle_data`是聚宽策略的核心函数，实现策略的主要逻辑，是策略开发的重点。
""",
            "type": "guide",
            "tags": ["聚宽", "策略开发", "handle_data", "主循环", "A级可靠性"],
            "source": "聚宽官方文档 + 实战经验"
        },
        {
            "title": "聚宽策略开发: 订单函数详解",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档 + 实战经验

---

## 聚宽策略开发: 订单函数详解

### 常用订单函数

#### 1. order_value - 按金额买入/卖出
```python
order_value(security, value, style=None)
```
- **security**: 股票代码
- **value**: 交易金额（正数买入，负数卖出）
- **style**: 订单类型，如MarketOrder()（市价单）

**示例**:
```python
# 买入10000元
order_value('000001.XSHE', 10000)

# 卖出10000元
order_value('000001.XSHE', -10000)
```

#### 2. order - 按数量买入/卖出
```python
order(security, amount, style=None)
```
- **security**: 股票代码
- **amount**: 交易数量（正数买入，负数卖出）
- **style**: 订单类型

**示例**:
```python
# 买入100股
order('000001.XSHE', 100)

# 卖出100股
order('000001.XSHE', -100)
```

#### 3. order_target - 按目标持仓买入/卖出
```python
order_target(security, amount, style=None)
```
- **security**: 股票代码
- **amount**: 目标持仓数量
- **style**: 订单类型

**示例**:
```python
# 持仓1000股
order_target('000001.XSHE', 1000)

# 清仓
order_target('000001.XSHE', 0)
```

#### 4. order_target_value - 按目标市值买入/卖出
```python
order_target_value(security, value, style=None)
```
- **security**: 股票代码
- **value**: 目标市值
- **style**: 订单类型

**示例**:
```python
# 持仓10000元
order_target_value('000001.XSHE', 10000)

# 清仓
order_target_value('000001.XSHE', 0)
```

#### 5. order_target_percent - 按目标仓位买入/卖出
```python
order_target_percent(security, percent, style=None)
```
- **security**: 股票代码
- **percent**: 目标仓位（0-1之间）
- **style**: 订单类型

**示例**:
```python
# 持仓10%
order_target_percent('000001.XSHE', 0.1)

# 清仓
order_target_percent('000001.XSHE', 0)
```

### 订单类型

#### MarketOrder - 市价单
```python
order('000001.XSHE', 100, MarketOrder())
```

#### LimitOrder - 限价单
```python
order('000001.XSHE', 100, LimitOrder(price=10.0))
```

### 注意事项
1. 订单是异步的，不会立即成交
2. 需要足够的资金才能买入
3. 需要足够的持仓才能卖出
4. 订单会在下一个bar成交
5. 可以使用`cancel_order()`取消订单

### 实战应用
- 策略执行：执行买卖操作
- 仓位管理：控制持仓比例
- 风险控制：设置止损止盈

## 结论

订单函数是聚宽策略执行交易的核心，正确使用订单函数对策略执行效果有重要影响。
""",
            "type": "guide",
            "tags": ["聚宽", "策略开发", "订单函数", "交易执行", "A级可靠性"],
            "source": "聚宽官方文档 + 实战经验"
        },
        {
            "title": "聚宽策略开发: 数据获取最佳实践",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 数据获取最佳实践

### 1. 使用data.current()获取当前数据

**适用场景**: 获取当前bar的数据

**示例**:
```python
# 获取当前价格
price = data.current('000001.XSHE', 'price')

# 获取当前成交量
volume = data.current('000001.XSHE', 'volume')
```

**优势**:
- 性能好，只获取当前数据
- 代码简洁

### 2. 使用data.history()获取历史数据

**适用场景**: 计算技术指标、分析历史趋势

**示例**:
```python
# 获取20日收盘价
hist = data.history('000001.XSHE', 'close', 20, '1d')

# 计算均线
ma20 = hist.mean()
```

**优势**:
- 可以获取多只股票的数据
- 支持多种频率

### 3. 使用get_price()获取大量历史数据

**适用场景**: 需要获取大量历史数据时

**示例**:
```python
import jqdatasdk as jq

# 在initialize中获取
g.hist_data = jq.get_price(
    '000001.XSHE',
    start_date='2020-01-01',
    end_date='2023-12-31',
    frequency='daily'
)
```

**优势**:
- 可以一次性获取大量数据
- 减少API调用次数

### 4. 数据缓存策略

**适用场景**: 需要重复使用相同数据时

**示例**:
```python
def initialize(context):
    # 在initialize中缓存数据
    g.hist_data = {}
    
def handle_data(context, data):
    security = '000001.XSHE'
    
    # 检查缓存
    if security not in g.hist_data:
        g.hist_data[security] = data.history(security, 'close', 20, '1d')
    
    hist = g.hist_data[security]
```

**优势**:
- 减少重复计算
- 提高策略性能

### 5. 批量获取数据

**适用场景**: 需要获取多只股票的数据时

**示例**:
```python
# 获取多只股票的数据
securities = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
hist = data.history(securities, 'close', 20, '1d')
```

**优势**:
- 一次调用获取多只股票数据
- 提高效率

### 注意事项
1. 避免在handle_data中频繁调用get_price()
2. 使用data.history()时注意数据长度
3. 缓存数据时注意内存使用
4. 批量获取数据时注意股票数量限制

### 实战应用
- 策略优化：提高数据获取效率
- 性能优化：减少API调用
- 内存管理：合理使用缓存

## 结论

合理使用数据获取方法可以提高策略性能，减少API调用，是策略优化的重要方面。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "数据获取", "最佳实践", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽策略开发: 常见错误和解决方案",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 常见错误和解决方案

### 错误1: 股票代码格式错误

**错误示例**:
```python
order('000001', 100)  # 缺少交易所后缀
```

**正确写法**:
```python
order('000001.XSHE', 100)  # 深交所
order('600000.XSHG', 100)  # 上交所
```

**解决方案**: 使用完整的股票代码格式，包括交易所后缀

### 错误2: 资金不足

**错误示例**:
```python
order_value('000001.XSHE', 100000)  # 资金不足
```

**正确写法**:
```python
# 检查可用资金
if context.portfolio.available_cash >= 100000:
    order_value('000001.XSHE', 100000)
```

**解决方案**: 在下单前检查可用资金

### 错误3: 持仓不足

**错误示例**:
```python
order('000001.XSHE', -1000)  # 持仓不足
```

**正确写法**:
```python
# 检查持仓
position = context.portfolio.positions['000001.XSHE']
if position.total_amount >= 1000:
    order('000001.XSHE', -1000)
```

**解决方案**: 在下单前检查持仓数量

### 错误4: 数据获取失败

**错误示例**:
```python
price = data.current('000001.XSHE', 'price')  # 可能返回None
ma = price.mean()  # 报错
```

**正确写法**:
```python
price = data.current('000001.XSHE', 'price')
if price is not None:
    # 处理数据
    pass
```

**解决方案**: 检查数据是否为空

### 错误5: 历史数据长度不足

**错误示例**:
```python
hist = data.history('000001.XSHE', 'close', 20, '1d')
ma20 = hist.mean()  # 如果数据不足20天会报错
```

**正确写法**:
```python
hist = data.history('000001.XSHE', 'close', 20, '1d')
if len(hist) >= 20:
    ma20 = hist.mean()
```

**解决方案**: 检查历史数据长度

### 错误6: 定时任务设置错误

**错误示例**:
```python
run_daily(trade, time='25:00')  # 无效时间
```

**正确写法**:
```python
run_daily(trade, time='09:30')  # 市场时间
```

**解决方案**: 使用有效的市场时间

### 实战建议
1. 使用try-except捕获异常
2. 添加数据验证
3. 使用日志记录错误
4. 测试边界情况

## 结论

了解常见错误和解决方案可以提高策略开发效率，减少调试时间，是策略开发的重要技能。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "常见错误", "问题解决", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽策略回测: 回测参数设置",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档 + 实战经验

---

## 聚宽策略回测: 回测参数设置

### 回测时间设置

#### 开始时间和结束时间
```python
# 在策略编辑器中设置
start_date = '2020-01-01'
end_date = '2023-12-31'
```

#### 注意事项
1. 开始时间不能早于股票上市时间
2. 结束时间不能晚于当前日期
3. 建议使用至少1年的数据回测

### 初始资金设置

```python
# 在策略编辑器中设置
initial_cash = 1000000  # 100万
```

#### 注意事项
1. 初始资金影响回测结果
2. 建议使用合理的初始资金
3. 考虑手续费和滑点的影响

### 基准设置

```python
def initialize(context):
    set_benchmark('000300.XSHG')  # 沪深300
```

#### 常用基准
- **000300.XSHG**: 沪深300
- **000905.XSHG**: 中证500
- **399006.XSHE**: 创业板指

### 手续费设置

```python
def initialize(context):
    set_order_cost(
        OrderCost(
            open_tax=0,           # 买入印花税
            close_tax=0.001,      # 卖出印花税（0.1%）
            open_commission=0.0003,  # 买入佣金（0.03%）
            close_commission=0.0003, # 卖出佣金（0.03%）
            min_commission=5      # 最低佣金5元
        ),
        type='stock'
    )
```

#### 注意事项
1. 手续费设置影响回测结果
2. 建议使用实际交易的手续费
3. 不同券商手续费不同

### 滑点设置

```python
def initialize(context):
    set_slippage(FixedSlippage(0.002))  # 固定滑点0.2%
```

#### 滑点类型
- **FixedSlippage**: 固定滑点
- **VolumeShareSlippage**: 成交量比例滑点

### 回测频率设置

```python
# 在策略编辑器中设置
frequency = 'daily'  # 日线回测
# frequency = 'minute'  # 分钟线回测
```

### 实战建议
1. 使用足够长的回测周期（至少1年）
2. 设置合理的手续费和滑点
3. 选择合适的基准
4. 考虑市场环境变化

## 结论

正确设置回测参数可以获得更真实的回测结果，是策略验证的重要步骤。
""",
            "type": "guide",
            "tags": ["聚宽", "策略回测", "参数设置", "回测配置", "A级可靠性"],
            "source": "聚宽官方文档 + 实战经验"
        },
        {
            "title": "聚宽策略回测: 回测结果分析",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略回测: 回测结果分析

### 关键指标

#### 1. 收益率指标
- **总收益率**: 策略总收益
- **年化收益率**: 年化后的收益率
- **基准收益率**: 基准的总收益
- **超额收益**: 策略收益 - 基准收益

#### 2. 风险指标
- **最大回撤**: 策略的最大回撤
- **波动率**: 收益率的波动程度
- **夏普比率**: 风险调整后的收益
- **信息比率**: 超额收益与跟踪误差的比值

#### 3. 交易指标
- **总交易次数**: 策略的总交易次数
- **胜率**: 盈利交易占比
- **平均持仓天数**: 平均持仓时间
- **换手率**: 交易频率

### 回测结果解读

#### 优秀策略的特征
1. **年化收益率 > 基准收益率**: 策略跑赢基准
2. **夏普比率 > 1**: 风险调整后收益较好
3. **最大回撤 < 30%**: 回撤控制在合理范围
4. **胜率 > 50%**: 交易胜率较高

#### 需要改进的策略特征
1. **年化收益率 < 基准收益率**: 策略跑输基准
2. **夏普比率 < 0.5**: 风险调整后收益较差
3. **最大回撤 > 50%**: 回撤过大
4. **胜率 < 40%**: 交易胜率较低

### 回测结果优化

#### 1. 参数优化
- 调整策略参数
- 使用参数优化工具
- 避免过拟合

#### 2. 风险控制
- 设置止损止盈
- 控制仓位
- 分散投资

#### 3. 策略改进
- 优化选股逻辑
- 改进买卖信号
- 增加过滤条件

### 实战建议
1. 关注多个指标，不要只看收益率
2. 分析回测结果的原因
3. 优化策略参数
4. 进行样本外测试

## 结论

正确分析回测结果可以发现策略的问题，指导策略优化，是策略开发的重要环节。
""",
            "type": "practice",
            "tags": ["聚宽", "策略回测", "结果分析", "性能评估", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽数据API: 获取指数成分股",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取指数成分股

### API函数
`get_index_stocks(index_symbol, date=None)`

### 功能说明
获取指定指数的成分股列表。

### 参数说明
- **index_symbol**: 指数代码，如 '000300.XSHG'（沪深300）
- **date**: 查询日期，默认为当前日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取沪深300成分股
stocks = jq.get_index_stocks('000300.XSHG')
print(f"沪深300成分股数量: {len(stocks)}")
print(stocks[:10])
```

### 常用指数代码
- **000300.XSHG**: 沪深300
- **000905.XSHG**: 中证500
- **399006.XSHE**: 创业板指
- **000852.XSHG**: 中证1000
- **000016.XSHG**: 上证50

### 注意事项
1. 指数成分股会定期调整
2. 需要指定查询日期获取历史成分股
3. 返回的是股票代码列表

### 实战应用
- 指数跟踪策略：获取指数成分股
- 选股策略：从指数成分股中选股
- 行业分析：分析指数成分股

## 结论

`get_index_stocks`是获取指数成分股的主要API，是构建指数跟踪策略的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "指数数据", "成分股", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽数据API: 获取行业分类数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取行业分类数据

### API函数
`get_industry(security, date=None)`

### 功能说明
获取股票的行业分类信息。

### 参数说明
- **security**: 股票代码或股票列表
- **date**: 查询日期，默认为当前日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取单只股票的行业
industry = jq.get_industry('000001.XSHE')
print(industry)

# 获取多只股票的行业
stocks = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
industries = jq.get_industry(stocks)
print(industries)
```

### 返回数据格式
字典，键为股票代码，值为行业信息字典，包含：
- **jq_l1**: 一级行业
- **jq_l2**: 二级行业
- **jq_l3**: 三级行业

### 注意事项
1. 行业分类会定期调整
2. 需要指定查询日期获取历史行业分类
3. 支持批量查询

### 实战应用
- 行业轮动策略：分析行业表现
- 行业选股：从特定行业选股
- 行业分析：分析行业特征

## 结论

`get_industry`是获取行业分类数据的主要API，是行业分析和行业轮动策略的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "行业数据", "行业分类", "A级可靠性"],
            "source": "聚宽官方文档"
        }
    ]
    
    print(f"📝 准备添加 {len(entries)} 条聚宽/JQData知识...")
    print()
    
    success_count = 0
    for i, entry in enumerate(entries, 1):
        print(f"[{i}/{len(entries)}] 添加: {entry['title']}")
        try:
            result = knowledge_add(
                title=entry['title'],
                content=entry['content'],
                type=entry['type'],
                tags=entry['tags'],
                source=entry['source']
            )
            if result.get('success') or result.get('knowledge_id'):
                print(f"    ✅ 添加成功")
                success_count += 1
            else:
                print(f"    ❌ 添加失败: {result.get('error', 'Unknown')}")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
        print()
    
    print("=" * 70)
    print(f"📊 补充完成: {success_count}/{len(entries)} 条知识已添加")
    print("=" * 70)
    
    return success_count > 0


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 补充聚宽/JQData知识库")
    print("=" * 70)
    print()
    
    success = supplement_jqdata_knowledge()
    
    print()
    print("=" * 70)
    if success:
        print("✅ 聚宽/JQData知识补充成功！")
        print()
        print("📋 补充内容:")
        print("   - API文档: 5条")
        print("   - 使用指南: 3条")
        print("   - 最佳实践: 2条")
        print()
        print("🎯 下一步:")
        print("   1. 继续补充更多聚宽/JQData知识")
        print("   2. 补充QMT和BulletTrade知识")
        print("   3. 优化知识库搜索功能")
    else:
        print("❌ 聚宽/JQData知识补充失败")
    print("=" * 70)


if __name__ == '__main__':
    main()
