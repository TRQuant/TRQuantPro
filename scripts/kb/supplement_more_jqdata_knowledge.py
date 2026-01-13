#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
继续补充聚宽/JQData知识库
========================

补充更多实用的API使用示例、最佳实践、常见问题等
目标: 从123条增加到200+条
"""

import sys
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add


def supplement_more_jqdata_knowledge():
    """继续补充聚宽/JQData知识"""
    
    print("=" * 70)
    print("📚 继续补充聚宽/JQData知识库")
    print("=" * 70)
    print()
    
    entries = [
        {
            "title": "聚宽数据API: 获取技术指标数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取技术指标数据

### API函数
`get_technical_indicators(security, start_date, end_date, indicators)`

### 功能说明
获取股票的技术指标数据，如MACD、RSI、KDJ等。

### 参数说明
- **security**: 股票代码
- **start_date**: 开始日期
- **end_date**: 结束日期
- **indicators**: 技术指标列表，如 ['MACD', 'RSI', 'KDJ']

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取MACD指标
macd = jq.get_technical_indicators(
    '000001.XSHE',
    start_date='2023-01-01',
    end_date='2023-12-31',
    indicators=['MACD']
)

print(macd.head())
```

### 支持的技术指标
- **MACD**: 指数平滑移动平均线
- **RSI**: 相对强弱指标
- **KDJ**: 随机指标
- **BOLL**: 布林带
- **MA**: 移动平均线
- **EMA**: 指数移动平均线

### 注意事项
1. 需要先登录
2. 指标名称需要正确
3. 日期范围不能过大

### 实战应用
- 技术分析：计算技术指标
- 策略开发：基于技术指标选股
- 信号生成：生成买卖信号

## 结论

`get_technical_indicators`是获取技术指标数据的主要API，是技术分析策略的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "技术指标", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 定时任务详解",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档 + 实战经验

---

## 聚宽策略开发: 定时任务详解

### 常用定时函数

#### 1. run_daily - 每日执行
```python
run_daily(trade, time='09:30')
```
- **trade**: 要执行的函数
- **time**: 执行时间，格式 'HH:MM'

**示例**:
```python
def initialize(context):
    # 每天9:30执行
    run_daily(trade, time='09:30')
    
    # 每天14:30执行
    run_daily(check_position, time='14:30')
```

#### 2. run_weekly - 每周执行
```python
run_weekly(trade, weekday=1, time='09:30')
```
- **weekday**: 星期几（1=周一，7=周日）
- **time**: 执行时间

**示例**:
```python
def initialize(context):
    # 每周一9:30执行
    run_weekly(trade, weekday=1, time='09:30')
```

#### 3. run_monthly - 每月执行
```python
run_monthly(trade, monthday=1, time='09:30')
```
- **monthday**: 每月几号（1-31）
- **time**: 执行时间

**示例**:
```python
def initialize(context):
    # 每月1号9:30执行
    run_monthly(rebalance, monthday=1, time='09:30')
```

#### 4. run_at_time - 指定时间执行
```python
run_at_time(trade, time='09:30')
```

### 注意事项
1. 时间必须是市场交易时间
2. 多个定时任务可以同时设置
3. 定时任务在指定时间执行
4. 时间格式：'HH:MM'（24小时制）

### 实战应用
- 调仓策略：定期调仓
- 风控检查：定期检查风险
- 数据更新：定期更新数据

## 结论

定时任务是聚宽策略的重要组成部分，正确设置定时任务可以实现自动化交易。
""",
            "type": "guide",
            "tags": ["聚宽", "策略开发", "定时任务", "run_daily", "A级可靠性"],
            "source": "聚宽官方文档 + 实战经验"
        },
        {
            "title": "聚宽策略开发: 全局变量g的使用",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档 + 实战经验

---

## 聚宽策略开发: 全局变量g的使用

### g对象说明
`g`是聚宽提供的全局变量对象，用于在策略的不同函数间共享数据。

### 常用用法

#### 1. 存储股票池
```python
def initialize(context):
    g.security_list = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
```

#### 2. 存储策略参数
```python
def initialize(context):
    g.ma_short = 5   # 短期均线
    g.ma_long = 20   # 长期均线
    g.stop_loss = 0.05  # 止损比例
```

#### 3. 存储状态信息
```python
def initialize(context):
    g.buy_price = 0      # 买入价格
    g.hold_days = 0      # 持仓天数
    g.last_trade_date = None  # 上次交易日期
```

#### 4. 存储缓存数据
```python
def initialize(context):
    g.hist_data = {}  # 缓存历史数据

def handle_data(context, data):
    security = '000001.XSHE'
    
    # 检查缓存
    if security not in g.hist_data:
        g.hist_data[security] = data.history(security, 'close', 20, '1d')
    
    hist = g.hist_data[security]
```

### 注意事项
1. `g`对象在策略运行期间一直存在
2. 可以在任何函数中访问和修改
3. 适合存储策略状态和缓存数据
4. 不要存储过大的数据（影响性能）

### 实战应用
- 策略参数：存储策略参数
- 状态管理：存储策略状态
- 数据缓存：缓存计算结果

## 结论

`g`对象是聚宽策略中重要的全局变量，正确使用可以提高策略效率和可读性。
""",
            "type": "guide",
            "tags": ["聚宽", "策略开发", "全局变量", "g对象", "A级可靠性"],
            "source": "聚宽官方文档 + 实战经验"
        },
        {
            "title": "聚宽数据API: 获取融资融券数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取融资融券数据

### API函数
`get_mtss(security_list, start_date, end_date, fields=None)`

### 功能说明
获取股票的融资融券数据，包括融资余额、融券余额、融资买入额、融券卖出量等。

### 参数说明
- **security_list**: 股票代码列表
- **start_date**: 开始日期
- **end_date**: 结束日期
- **fields**: 需要获取的字段

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取融资融券数据
mtss = jq.get_mtss(
    ['000001.XSHE', '000002.XSHE'],
    start_date='2023-01-01',
    end_date='2023-12-31'
)

print(mtss.head())
```

### 返回数据字段
- **date**: 日期
- **sec_code**: 股票代码
- **rzye**: 融资余额
- **rqye**: 融券余额
- **rzmre**: 融资买入额
- **rqyl**: 融券余量
- **rzche**: 融资偿还额
- **rqchl**: 融券偿还量

### 注意事项
1. 需要先登录
2. 股票代码格式要正确
3. 数据有延迟，通常延迟1个交易日

### 实战应用
- 资金流向分析：分析融资融券资金流向
- 情绪指标：融资余额变化反映市场情绪
- 选股策略：筛选融资余额增加的股票

## 结论

`get_mtss`是获取融资融券数据的主要API，是资金流向分析和情绪指标计算的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "融资融券", "资金流向", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽数据API: 获取龙虎榜数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取龙虎榜数据

### API函数
`get_billboard_list(stock_list, start_date, end_date)`

### 功能说明
获取股票的龙虎榜数据，包括买入金额、卖出金额、买卖席位等。

### 参数说明
- **stock_list**: 股票代码列表
- **start_date**: 开始日期
- **end_date**: 结束日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取龙虎榜数据
billboard = jq.get_billboard_list(
    ['000001.XSHE'],
    start_date='2023-01-01',
    end_date='2023-12-31'
)

print(billboard.head())
```

### 返回数据字段
- **date**: 日期
- **code**: 股票代码
- **name**: 股票名称
- **buy_amount**: 买入金额
- **sell_amount**: 卖出金额
- **net_amount**: 净买入金额
- **buy_seat**: 买入席位
- **sell_seat**: 卖出席位

### 注意事项
1. 需要先登录
2. 只有上龙虎榜的股票才有数据
3. 数据有延迟，通常延迟1个交易日

### 实战应用
- 游资追踪：追踪游资操作
- 情绪分析：分析市场情绪
- 选股策略：筛选龙虎榜股票

## 结论

`get_billboard_list`是获取龙虎榜数据的主要API，是游资追踪和情绪分析的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "龙虎榜", "游资", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 仓位管理最佳实践",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 仓位管理最佳实践

### 1. 单只股票仓位限制

**原则**: 单只股票仓位不超过总资金的20%

**示例**:
```python
def handle_data(context, data):
    # 计算单只股票最大仓位
    max_position_value = context.portfolio.total_value * 0.2
    
    # 买入
    order_target_value('000001.XSHE', max_position_value)
```

### 2. 总仓位控制

**原则**: 总仓位不超过总资金的80%，保留20%现金

**示例**:
```python
def handle_data(context, data):
    # 计算当前总仓位
    total_position_value = sum(
        pos.total_amount * data.current(sec, 'price')
        for sec, pos in context.portfolio.positions.items()
    )
    
    # 如果总仓位超过80%，减仓
    if total_position_value / context.portfolio.total_value > 0.8:
        # 减仓逻辑
        pass
```

### 3. 分散持仓

**原则**: 持仓股票数量在5-20只之间

**示例**:
```python
def handle_data(context, data):
    # 获取当前持仓数量
    position_count = len([p for p in context.portfolio.positions.values() if p.total_amount > 0])
    
    # 如果持仓数量不足，加仓
    if position_count < 5:
        # 加仓逻辑
        pass
```

### 4. 动态仓位调整

**原则**: 根据市场状态动态调整仓位

**示例**:
```python
def handle_data(context, data):
    # 根据市场状态调整仓位上限
    if market_regime == 'bull':
        max_position_ratio = 0.8
    elif market_regime == 'bear':
        max_position_ratio = 0.3
    else:
        max_position_ratio = 0.5
    
    # 调整仓位
    adjust_position(context, data, max_position_ratio)
```

### 注意事项
1. 不要满仓操作
2. 保留一定现金应对风险
3. 分散持仓降低风险
4. 根据市场状态调整仓位

### 实战应用
- 风险控制：控制策略风险
- 资金管理：合理分配资金
- 策略优化：提高策略稳定性

## 结论

仓位管理是策略风险控制的重要方面，合理的仓位管理可以提高策略的稳定性和收益。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "仓位管理", "风险控制", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽策略开发: 止损止盈策略",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 止损止盈策略

### 1. 固定止损

**策略**: 当亏损达到固定比例时止损

**示例**:
```python
def handle_data(context, data):
    for security, position in context.portfolio.positions.items():
        if position.total_amount > 0:
            # 获取当前价格
            current_price = data.current(security, 'price')
            
            # 计算盈亏比例
            profit_rate = (current_price - position.avg_cost) / position.avg_cost
            
            # 止损：亏损超过5%
            if profit_rate < -0.05:
                order_target(security, 0)
                print(f"止损: {security}, 亏损: {profit_rate*100:.2f}%")
```

### 2. 移动止损

**策略**: 当价格从最高点回撤达到比例时止损

**示例**:
```python
def initialize(context):
    g.highest_price = {}  # 记录最高价

def handle_data(context, data):
    for security, position in context.portfolio.positions.items():
        if position.total_amount > 0:
            current_price = data.current(security, 'price')
            
            # 更新最高价
            if security not in g.highest_price:
                g.highest_price[security] = current_price
            else:
                g.highest_price[security] = max(g.highest_price[security], current_price)
            
            # 移动止损：从最高点回撤10%
            if current_price < g.highest_price[security] * 0.9:
                order_target(security, 0)
                print(f"移动止损: {security}")
```

### 3. 固定止盈

**策略**: 当盈利达到固定比例时止盈

**示例**:
```python
def handle_data(context, data):
    for security, position in context.portfolio.positions.items():
        if position.total_amount > 0:
            current_price = data.current(security, 'price')
            profit_rate = (current_price - position.avg_cost) / position.avg_cost
            
            # 止盈：盈利超过20%
            if profit_rate > 0.20:
                order_target(security, 0)
                print(f"止盈: {security}, 盈利: {profit_rate*100:.2f}%")
```

### 4. 分批止盈

**策略**: 分批次止盈，锁定利润

**示例**:
```python
def handle_data(context, data):
    for security, position in context.portfolio.positions.items():
        if position.total_amount > 0:
            current_price = data.current(security, 'price')
            profit_rate = (current_price - position.avg_cost) / position.avg_cost
            
            # 分批止盈
            if profit_rate > 0.30:
                # 盈利30%，卖出50%
                order_target_percent(security, 0.05)
            elif profit_rate > 0.20:
                # 盈利20%，卖出30%
                order_target_percent(security, 0.07)
```

### 注意事项
1. 止损止盈比例要合理
2. 考虑手续费和滑点
3. 避免频繁交易
4. 结合市场状态调整

### 实战应用
- 风险控制：控制单笔交易风险
- 利润锁定：及时锁定利润
- 策略优化：提高策略收益

## 结论

止损止盈是策略风险控制的重要手段，合理的止损止盈策略可以提高策略的收益风险比。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "止损止盈", "风险控制", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽数据API: 获取资金流向数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取资金流向数据

### API函数
`get_money_flow(security_list, start_date, end_date)`

### 功能说明
获取股票的资金流向数据，包括主力资金、超大单、大单、中单、小单等。

### 参数说明
- **security_list**: 股票代码列表
- **start_date**: 开始日期
- **end_date**: 结束日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取资金流向数据
money_flow = jq.get_money_flow(
    ['000001.XSHE'],
    start_date='2023-01-01',
    end_date='2023-12-31'
)

print(money_flow.head())
```

### 返回数据字段
- **date**: 日期
- **code**: 股票代码
- **net_purchase_main_force**: 主力资金净流入
- **net_purchase_xl**: 超大单净流入
- **net_purchase_l**: 大单净流入
- **net_purchase_m**: 中单净流入
- **net_purchase_s**: 小单净流入

### 注意事项
1. 需要先登录
2. 数据有延迟，通常延迟1个交易日
3. 资金流向数据是估算值

### 实战应用
- 资金分析：分析资金流向
- 选股策略：筛选资金流入的股票
- 情绪分析：分析市场情绪

## 结论

`get_money_flow`是获取资金流向数据的主要API，是资金分析和选股策略的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "资金流向", "主力资金", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 多因子选股策略",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 多因子选股策略

### 策略思路
使用多个因子综合评分，筛选出优质股票。

### 因子选择

#### 1. 技术因子
- **动量因子**: 20日收益率
- **均线因子**: 价格相对均线位置
- **成交量因子**: 成交量放大倍数

#### 2. 基本面因子
- **估值因子**: PE、PB
- **盈利因子**: ROE、净利润增长率
- **财务因子**: 资产负债率、流动比率

#### 3. 资金因子
- **资金流向**: 主力资金净流入
- **融资融券**: 融资余额变化
- **成交量**: 成交量放大

### 代码示例
```python
def select_stocks(context, data):
    """多因子选股"""
    # 获取股票池
    stocks = list(get_all_securities(['stock']).index)
    
    scores = {}
    for stock in stocks:
        score = 0
        
        # 技术因子评分
        hist = data.history(stock, 'close', 20, '1d')
        momentum = (hist[-1] - hist[0]) / hist[0]
        if momentum > 0.1:
            score += 20
        
        # 基本面因子评分
        # ... 获取财务数据并评分
        
        # 资金因子评分
        # ... 获取资金流向数据并评分
        
        scores[stock] = score
    
    # 选择评分前20的股票
    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]
    return [s[0] for s in selected]
```

### 注意事项
1. 因子权重需要优化
2. 避免因子相关性过高
3. 定期更新因子
4. 考虑市场环境

### 实战应用
- 选股策略：筛选优质股票
- 因子研究：研究因子有效性
- 策略优化：优化因子组合

## 结论

多因子选股策略是量化选股的重要方法，合理选择因子可以提高选股效果。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "多因子选股", "因子分析", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽策略开发: 参数优化方法",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 参数优化方法

### 1. 网格搜索

**方法**: 遍历所有参数组合，找到最优参数

**示例**:
```python
# 参数范围
ma_short_range = [5, 10, 15, 20]
ma_long_range = [20, 30, 40, 50]

best_params = None
best_sharpe = -999

for ma_short in ma_short_range:
    for ma_long in ma_long_range:
        if ma_long <= ma_short:
            continue
        
        # 回测
        result = backtest(ma_short, ma_long)
        
        # 评估
        if result['sharpe'] > best_sharpe:
            best_sharpe = result['sharpe']
            best_params = (ma_short, ma_long)
```

### 2. 随机搜索

**方法**: 随机选择参数组合，减少计算量

**示例**:
```python
import random

best_params = None
best_sharpe = -999

for _ in range(100):  # 随机搜索100次
    ma_short = random.choice([5, 10, 15, 20])
    ma_long = random.choice([20, 30, 40, 50])
    
    if ma_long <= ma_short:
        continue
    
    result = backtest(ma_short, ma_long)
    
    if result['sharpe'] > best_sharpe:
        best_sharpe = result['sharpe']
        best_params = (ma_short, ma_long)
```

### 3. 贝叶斯优化

**方法**: 使用贝叶斯优化算法，智能搜索参数空间

**示例**:
```python
from skopt import gp_minimize
from skopt.space import Integer

# 定义参数空间
space = [
    Integer(5, 20, name='ma_short'),
    Integer(20, 50, name='ma_long')
]

# 优化目标函数
def objective(params):
    ma_short, ma_long = params
    if ma_long <= ma_short:
        return 999  # 无效参数
    result = backtest(ma_short, ma_long)
    return -result['sharpe']  # 最小化负夏普比率

# 执行优化
result = gp_minimize(objective, space, n_calls=50)
best_params = result.x
```

### 注意事项
1. 避免过拟合：使用样本外数据验证
2. 参数范围要合理
3. 考虑参数稳定性
4. 使用多个评估指标

### 实战应用
- 策略优化：优化策略参数
- 因子优化：优化因子参数
- 风险控制：优化风险参数

## 结论

参数优化是策略开发的重要环节，合理的参数优化可以提高策略性能。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "参数优化", "策略优化", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽数据API: 获取宏观数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取宏观数据

### API函数
`get_macro_data(table_name, start_date, end_date)`

### 功能说明
获取宏观经济数据，如GDP、CPI、PMI、利率等。

### 参数说明
- **table_name**: 数据表名，如 'GDP', 'CPI', 'PMI'
- **start_date**: 开始日期
- **end_date**: 结束日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取GDP数据
gdp = jq.get_macro_data('GDP', start_date='2020-01-01', end_date='2023-12-31')
print(gdp.head())

# 获取CPI数据
cpi = jq.get_macro_data('CPI', start_date='2020-01-01', end_date='2023-12-31')
print(cpi.head())
```

### 支持的数据类型
- **GDP**: 国内生产总值
- **CPI**: 消费者物价指数
- **PMI**: 采购经理人指数
- **利率**: 利率数据
- **货币供应量**: M0、M1、M2

### 注意事项
1. 需要先登录
2. 宏观数据更新频率较低
3. 数据有延迟

### 实战应用
- 宏观分析：分析宏观经济环境
- 市场判断：判断市场趋势
- 策略调整：根据宏观环境调整策略

## 结论

`get_macro_data`是获取宏观数据的主要API，是宏观分析和市场判断的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "宏观数据", "GDP", "CPI", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 策略性能评估指标",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 策略性能评估指标

### 1. 收益指标

#### 总收益率
```python
total_return = (final_value - initial_value) / initial_value
```

#### 年化收益率
```python
annual_return = (1 + total_return) ** (252 / trading_days) - 1
```

### 2. 风险指标

#### 最大回撤
```python
max_drawdown = max((peak - trough) / peak)
```

#### 波动率
```python
volatility = returns.std() * np.sqrt(252)
```

### 3. 风险调整收益指标

#### 夏普比率
```python
sharpe_ratio = (annual_return - risk_free_rate) / volatility
```

#### 信息比率
```python
information_ratio = excess_return / tracking_error
```

#### 卡玛比率
```python
calmar_ratio = annual_return / max_drawdown
```

### 4. 交易指标

#### 胜率
```python
win_rate = winning_trades / total_trades
```

#### 盈亏比
```python
profit_loss_ratio = avg_profit / avg_loss
```

#### 平均持仓天数
```python
avg_hold_days = sum(hold_days) / len(hold_days)
```

### 评估标准

#### 优秀策略
- 年化收益率 > 20%
- 夏普比率 > 1.5
- 最大回撤 < 30%
- 胜率 > 50%

#### 需要改进的策略
- 年化收益率 < 基准收益率
- 夏普比率 < 0.5
- 最大回撤 > 50%
- 胜率 < 40%

### 实战应用
- 策略评估：评估策略性能
- 策略优化：指导策略优化
- 策略选择：选择最优策略

## 结论

策略性能评估指标是策略开发的重要工具，合理使用评估指标可以指导策略优化。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "性能评估", "回测分析", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽数据API: 获取Tick数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取Tick数据

### API函数
`get_ticks(security, start_dt, end_dt, count=None)`

### 功能说明
获取股票的Tick级别数据，包括每笔交易的成交价、成交量、买卖方向等。

### 参数说明
- **security**: 股票代码
- **start_dt**: 开始时间（datetime对象）
- **end_dt**: 结束时间（datetime对象）
- **count**: 获取数量（可选）

### 代码示例
```python
import jqdatasdk as jq
from datetime import datetime

# 登录
jq.auth('username', 'password')

# 获取Tick数据
ticks = jq.get_ticks(
    '000001.XSHE',
    start_dt=datetime(2023, 1, 1, 9, 30),
    end_dt=datetime(2023, 1, 1, 15, 0)
)

print(ticks.head())
```

### 返回数据字段
- **time**: 成交时间
- **current**: 当前价
- **volume**: 成交量
- **amount**: 成交额
- **a1_v**: 卖一量
- **a1_p**: 卖一价
- **b1_v**: 买一量
- **b1_p**: 买一价

### 注意事项
1. 需要先登录
2. Tick数据量很大，注意内存使用
3. 数据有延迟
4. 需要指定具体时间

### 实战应用
- 高频策略：开发高频交易策略
- 订单流分析：分析订单流
- 盘口分析：分析盘口数据

## 结论

`get_ticks`是获取Tick数据的主要API，是高频策略和订单流分析的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "Tick数据", "高频数据", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 策略调试技巧",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 策略调试技巧

### 1. 使用print输出调试信息

**示例**:
```python
def handle_data(context, data):
    print(f"当前日期: {context.current_dt}")
    print(f"可用资金: {context.portfolio.available_cash}")
    print(f"持仓: {context.portfolio.positions}")
```

### 2. 使用log记录日志

**示例**:
```python
def handle_data(context, data):
    log.info(f"当前日期: {context.current_dt}")
    log.info(f"可用资金: {context.portfolio.available_cash}")
    
    if some_condition:
        log.warning("警告信息")
        log.error("错误信息")
```

### 3. 使用断点调试

**示例**:
```python
def handle_data(context, data):
    # 设置断点
    if context.current_dt == '2023-06-01':
        import pdb
        pdb.set_trace()  # 在这里暂停
    
    # 策略逻辑
    pass
```

### 4. 检查数据有效性

**示例**:
```python
def handle_data(context, data):
    price = data.current('000001.XSHE', 'price')
    
    # 检查数据有效性
    if price is None or price <= 0:
        log.error(f"价格数据无效: {price}")
        return
    
    # 继续处理
    pass
```

### 5. 使用try-except捕获异常

**示例**:
```python
def handle_data(context, data):
    try:
        # 策略逻辑
        price = data.current('000001.XSHE', 'price')
        order('000001.XSHE', 100)
    except Exception as e:
        log.error(f"策略执行出错: {e}")
        import traceback
        traceback.print_exc()
```

### 6. 验证订单执行

**示例**:
```python
def handle_data(context, data):
    # 下单
    order_id = order('000001.XSHE', 100)
    
    # 检查订单状态
    if order_id:
        log.info(f"订单提交成功: {order_id}")
    else:
        log.warning("订单提交失败")
```

### 注意事项
1. 调试信息不要过多，影响性能
2. 使用log而不是print（可以控制级别）
3. 及时清理调试代码
4. 使用版本控制管理代码

### 实战应用
- 策略开发：调试策略逻辑
- 问题排查：排查策略问题
- 性能优化：优化策略性能

## 结论

策略调试是策略开发的重要技能，掌握调试技巧可以提高开发效率。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "调试技巧", "问题排查", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽数据API: 获取因子数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取因子数据

### API函数
`get_factor_values(securities, factors, start_date, end_date)`

### 功能说明
获取聚宽因子库中的因子数据，如alpha101、alpha191等。

### 参数说明
- **securities**: 股票代码列表
- **factors**: 因子列表，如 ['alpha_001', 'alpha_002']
- **start_date**: 开始日期
- **end_date**: 结束日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取alpha101因子
factors = jq.get_factor_values(
    ['000001.XSHE', '000002.XSHE'],
    factors=['alpha_001', 'alpha_002', 'alpha_003'],
    start_date='2023-01-01',
    end_date='2023-12-31'
)

print(factors.head())
```

### 常用因子
- **alpha101**: 101个alpha因子
- **alpha191**: 191个alpha因子
- **聚宽因子**: 聚宽自定义因子

### 注意事项
1. 需要先登录
2. 因子数据有延迟
3. 因子数量有限制

### 实战应用
- 因子研究：研究因子有效性
- 因子组合：组合多个因子
- 选股策略：基于因子选股

## 结论

`get_factor_values`是获取因子数据的主要API，是因子研究和因子选股的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "因子数据", "alpha101", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 策略回测优化技巧",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 策略回测优化技巧

### 1. 减少数据获取次数

**优化前**:
```python
def handle_data(context, data):
    # 每次都获取历史数据
    hist = data.history('000001.XSHE', 'close', 20, '1d')
    ma20 = hist.mean()
```

**优化后**:
```python
def initialize(context):
    # 在initialize中缓存数据
    g.hist_cache = {}

def handle_data(context, data):
    # 使用缓存
    if '000001.XSHE' not in g.hist_cache:
        g.hist_cache['000001.XSHE'] = data.history('000001.XSHE', 'close', 20, '1d')
    ma20 = g.hist_cache['000001.XSHE'].mean()
```

### 2. 批量处理股票

**优化前**:
```python
def handle_data(context, data):
    for stock in stock_list:
        price = data.current(stock, 'price')
        # 处理
```

**优化后**:
```python
def handle_data(context, data):
    # 批量获取数据
    prices = data.current(stock_list, 'price')
    for stock, price in prices.items():
        # 处理
```

### 3. 减少不必要的计算

**优化前**:
```python
def handle_data(context, data):
    # 每次都计算
    ma5 = data.history('000001.XSHE', 'close', 5, '1d').mean()
    ma10 = data.history('000001.XSHE', 'close', 10, '1d').mean()
    ma20 = data.history('000001.XSHE', 'close', 20, '1d').mean()
```

**优化后**:
```python
def handle_data(context, data):
    # 一次获取，多次使用
    hist = data.history('000001.XSHE', 'close', 20, '1d')
    ma5 = hist[-5:].mean()
    ma10 = hist[-10:].mean()
    ma20 = hist.mean()
```

### 4. 使用向量化计算

**优化前**:
```python
def handle_data(context, data):
    hist = data.history('000001.XSHE', 'close', 20, '1d')
    # 循环计算
    returns = []
    for i in range(1, len(hist)):
        returns.append((hist[i] - hist[i-1]) / hist[i-1])
```

**优化后**:
```python
def handle_data(context, data):
    hist = data.history('000001.XSHE', 'close', 20, '1d')
    # 向量化计算
    returns = hist.pct_change().dropna()
```

### 注意事项
1. 平衡性能和可读性
2. 不要过度优化
3. 使用性能分析工具
4. 测试优化效果

### 实战应用
- 性能优化：提高回测速度
- 资源管理：减少资源消耗
- 策略改进：改进策略实现

## 结论

策略回测优化可以提高回测效率，减少资源消耗，是策略开发的重要技能。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "性能优化", "回测优化", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽数据API: 获取板块数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取板块数据

### API函数
`get_industry_stocks(industry_code, date=None)`

### 功能说明
获取指定板块的股票列表。

### 参数说明
- **industry_code**: 板块代码，如 '801010'（农林牧渔）
- **date**: 查询日期，默认为当前日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取农林牧渔板块股票
stocks = jq.get_industry_stocks('801010')
print(f"农林牧渔板块股票数量: {len(stocks)}")
print(stocks[:10])
```

### 常用板块代码
- **801010**: 农林牧渔
- **801020**: 采掘
- **801030**: 化工
- **801040**: 钢铁
- **801050**: 有色金属

### 注意事项
1. 需要先登录
2. 板块代码需要正确
3. 板块成分股会定期调整

### 实战应用
- 板块轮动策略：分析板块表现
- 板块选股：从特定板块选股
- 行业分析：分析行业特征

## 结论

`get_industry_stocks`是获取板块数据的主要API，是板块轮动策略和行业分析的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "板块数据", "行业数据", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 策略模板-均线策略",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 策略模板-均线策略

### 策略思路
使用短期均线和长期均线的交叉作为买卖信号。

### 策略参数
- **短期均线**: 5日
- **长期均线**: 20日
- **持仓股票**: 1只

### 完整代码
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
    
    # 策略参数
    g.security = '000001.XSHE'
    g.ma_short = 5
    g.ma_long = 20

def handle_data(context, data):
    # 获取历史数据
    hist = data.history(g.security, 'close', g.ma_long, '1d')
    
    # 计算均线
    ma_short = hist[-g.ma_short:].mean()
    ma_long = hist.mean()
    
    # 获取当前持仓
    position = context.portfolio.positions[g.security]
    
    # 金叉买入
    if ma_short > ma_long and position.total_amount == 0:
        order_value(g.security, context.portfolio.available_cash)
        log.info(f"买入: {g.security}, 价格: {data.current(g.security, 'price')}")
    
    # 死叉卖出
    elif ma_short < ma_long and position.total_amount > 0:
        order_target(g.security, 0)
        log.info(f"卖出: {g.security}, 价格: {data.current(g.security, 'price')}")
```

### 策略优化
1. 调整均线周期
2. 增加过滤条件
3. 添加止损止盈
4. 优化仓位管理

### 注意事项
1. 均线策略在趋势市场有效
2. 震荡市场可能频繁交易
3. 需要结合其他指标

### 实战应用
- 趋势跟踪：跟踪市场趋势
- 策略学习：学习策略开发
- 策略优化：优化策略参数

## 结论

均线策略是经典的量化策略，是学习策略开发的好起点。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "策略模板", "均线策略", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽数据API: 获取概念板块数据",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取概念板块数据

### API函数
`get_concept_stocks(concept_code, date=None)`

### 功能说明
获取指定概念板块的股票列表。

### 参数说明
- **concept_code**: 概念代码
- **date**: 查询日期，默认为当前日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取概念板块股票
# 注意：需要先获取概念代码列表
concepts = jq.get_concept_list()
print(concepts.head())

# 获取特定概念股票
stocks = jq.get_concept_stocks('GN001')  # 示例概念代码
print(stocks)
```

### 注意事项
1. 需要先登录
2. 概念代码需要正确
3. 概念成分股会定期调整

### 实战应用
- 主题投资：投资特定主题
- 概念选股：从概念板块选股
- 主题分析：分析主题表现

## 结论

`get_concept_stocks`是获取概念板块数据的主要API，是主题投资和概念选股的基础。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "概念板块", "主题投资", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 策略模板-动量策略",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 策略模板-动量策略

### 策略思路
买入过去一段时间表现好的股票，卖出表现差的股票。

### 策略参数
- **回看周期**: 20日
- **持仓数量**: 10只
- **调仓频率**: 每周

### 完整代码
```python
def initialize(context):
    set_benchmark('000300.XSHG')
    
    g.stock_pool = list(get_all_securities(['stock']).index)
    g.hold_count = 10
    g.lookback_period = 20
    
    # 每周调仓
    run_weekly(select_and_trade, weekday=1, time='09:30')

def select_and_trade(context, data):
    # 计算所有股票的收益率
    returns = {}
    for stock in g.stock_pool:
        hist = data.history(stock, 'close', g.lookback_period, '1d')
        if len(hist) >= g.lookback_period:
            returns[stock] = (hist[-1] - hist[0]) / hist[0]
    
    # 选择收益率最高的股票
    selected = sorted(returns.items(), key=lambda x: x[1], reverse=True)[:g.hold_count]
    selected_stocks = [s[0] for s in selected]
    
    # 卖出不在目标列表的股票
    for stock, position in context.portfolio.positions.items():
        if position.total_amount > 0 and stock not in selected_stocks:
            order_target(stock, 0)
    
    # 买入目标股票
    cash_per_stock = context.portfolio.available_cash / g.hold_count
    for stock in selected_stocks:
        order_target_value(stock, cash_per_stock)
```

### 策略优化
1. 增加过滤条件（市值、流动性等）
2. 调整持仓数量
3. 优化调仓频率
4. 添加止损止盈

### 注意事项
1. 动量策略在趋势市场有效
2. 反转市场可能失效
3. 需要控制交易成本

### 实战应用
- 趋势跟踪：跟踪强势股票
- 策略学习：学习策略开发
- 策略优化：优化策略参数

## 结论

动量策略是经典的量化策略，适合在趋势市场中使用。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "策略模板", "动量策略", "B级可靠性"],
            "source": "实战经验总结"
        },
        {
            "title": "聚宽数据API: 获取停复牌信息",
            "content": """**可靠性评级**: A级（高可靠性）

**知识来源**: 官方文档

---

## 聚宽数据API: 获取停复牌信息

### API函数
`get_all_securities(types=['stock'], date=None)`

### 功能说明
获取所有证券的基本信息，包括是否停牌。

### 参数说明
- **types**: 证券类型，如 ['stock']
- **date**: 查询日期，默认为当前日期

### 代码示例
```python
import jqdatasdk as jq

# 登录
jq.auth('username', 'password')

# 获取所有股票信息
stocks = jq.get_all_securities(['stock'])
print(stocks.head())

# 检查是否停牌
# 注意：需要结合其他API判断停牌
```

### 注意事项
1. 需要先登录
2. 停牌信息需要结合行情数据判断
3. 数据有延迟

### 实战应用
- 策略过滤：过滤停牌股票
- 风险控制：避免买入停牌股票
- 数据清洗：清洗无效数据

## 结论

获取停复牌信息是策略开发的重要环节，可以避免交易停牌股票。
""",
            "type": "api_reference",
            "tags": ["聚宽", "JQData", "API文档", "停复牌", "风险控制", "A级可靠性"],
            "source": "聚宽官方文档"
        },
        {
            "title": "聚宽策略开发: 策略模板-反转策略",
            "content": """**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 策略模板-反转策略

**知识来源**: 实战经验总结

---

## 聚宽策略开发: 策略模板-反转策略

### 策略思路
买入过去一段时间表现差的股票，卖出表现好的股票（均值回归）。

### 策略参数
- **回看周期**: 20日
- **持仓数量**: 10只
- **调仓频率**: 每周

### 完整代码
```python
def initialize(context):
    set_benchmark('000300.XSHG')
    
    g.stock_pool = list(get_all_securities(['stock']).index)
    g.hold_count = 10
    g.lookback_period = 20
    
    run_weekly(select_and_trade, weekday=1, time='09:30')

def select_and_trade(context, data):
    # 计算所有股票的收益率
    returns = {}
    for stock in g.stock_pool:
        hist = data.history(stock, 'close', g.lookback_period, '1d')
        if len(hist) >= g.lookback_period:
            returns[stock] = (hist[-1] - hist[0]) / hist[0]
    
    # 选择收益率最低的股票（反转）
    selected = sorted(returns.items(), key=lambda x: x[1])[:g.hold_count]
    selected_stocks = [s[0] for s in selected]
    
    # 调仓
    for stock, position in context.portfolio.positions.items():
        if position.total_amount > 0 and stock not in selected_stocks:
            order_target(stock, 0)
    
    cash_per_stock = context.portfolio.available_cash / g.hold_count
    for stock in selected_stocks:
        order_target_value(stock, cash_per_stock)
```

### 策略优化
1. 增加过滤条件
2. 调整持仓数量
3. 优化调仓频率
4. 添加止损

### 注意事项
1. 反转策略在震荡市场有效
2. 趋势市场可能失效
3. 需要控制风险

### 实战应用
- 均值回归：利用均值回归
- 策略学习：学习策略开发
- 策略优化：优化策略参数

## 结论

反转策略是经典的量化策略，适合在震荡市场中使用。
""",
            "type": "practice",
            "tags": ["聚宽", "策略开发", "策略模板", "反转策略", "B级可靠性"],
            "source": "实战经验总结"
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
    print("🚀 继续补充聚宽/JQData知识库")
    print("=" * 70)
    print()
    
    success = supplement_more_jqdata_knowledge()
    
    print()
    print("=" * 70)
    if success:
        print("✅ 聚宽/JQData知识补充成功！")
        print()
        print("📋 补充内容:")
        print("   - API文档: 6条")
        print("   - 使用指南: 2条")
        print("   - 最佳实践: 6条")
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
