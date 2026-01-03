# 聚宽平台风控模块指南

> **来源**: 聚宽(JoinQuant)平台最佳实践 + TRQuant项目经验总结  
> **更新时间**: 2024-12-28  
> **用途**: 十倍股策略风控模块设计参考

---

## 📚 目录

1. [聚宽风控理念](#聚宽风控理念)
2. [核心风控指标](#核心风控指标)
3. [风控模块设计原则](#风控模块设计原则)
4. [常见风控策略](#常见风控策略)
5. [聚宽平台风控最佳实践](#聚宽平台风控最佳实践)
6. [TRQuant风控模块实现](#trquant风控模块实现)

---

## 聚宽风控理念

### 1. 多维度风险管理

聚宽平台强调**多层次、多维度的风险管理体系**：

- **策略层面**：止损止盈、仓位控制
- **组合层面**：相关性控制、行业分散
- **系统层面**：最大回撤限制、资金管理

### 2. 动态风控调整

风控参数应该**根据市场环境动态调整**：

- 牛市：适当放宽止损，提高仓位上限
- 熊市：收紧止损，降低仓位，提高现金比例
- 震荡市：使用移动止损，控制单只股票仓位

### 3. 实时监控与预警

聚宽平台提供实时风控监控：

- 实时计算组合风险指标
- 风险超标自动预警
- 支持手动和自动风控干预

---

## 核心风控指标

### 1. 仓位控制指标

| 指标 | 说明 | 推荐值 |
|------|------|--------|
| 最大仓位比例 | 总持仓市值/总资产 | 80-95% |
| 单只股票上限 | 单股持仓市值/总资产 | 10-20% |
| 行业集中度 | 单一行业持仓/总资产 | <30% |
| 持仓数量 | 组合持仓股票数量 | 5-15只 |

### 2. 止损止盈指标

| 指标 | 说明 | 推荐值 |
|------|------|--------|
| 固定止损 | 亏损比例达到阈值 | -10% ~ -15% |
| 移动止损 | 从高点回撤比例 | -10% ~ -20% |
| 固定止盈 | 盈利比例达到阈值 | 50% ~ 100% |
| 跟踪止盈 | 从最高价回撤比例 | -15% ~ -25% |

### 3. 回撤控制指标

| 指标 | 说明 | 推荐值 |
|------|------|--------|
| 最大回撤限制 | 组合最大回撤阈值 | -20% ~ -30% |
| 回撤恢复阈值 | 回撤恢复比例 | 5% ~ 10% |
| 连续回撤天数 | 连续回撤天数限制 | 5-10天 |

### 4. 风险指标

| 指标 | 说明 | 推荐值 |
|------|------|--------|
| 波动率 | 组合收益波动率 | <30% |
| 最大单日亏损 | 单日最大亏损比例 | <5% |
| 夏普比率 | 风险调整后收益 | >1.0 |
| VaR | 风险价值（95%置信度） | <5% |

---

## 风控模块设计原则

### 1. 分层设计

```
风控模块架构：
├── 订单级风控（下单前检查）
│   ├── 单笔交易限额
│   ├── 仓位限制检查
│   └── 价格合理性检查
├── 持仓级风控（持仓期间检查）
│   ├── 止损止盈
│   ├── 移动止损
│   └── 持仓集中度检查
└── 组合级风控（组合层面检查）
    ├── 最大回撤限制
    ├── 行业集中度控制
    └── 相关性控制
```

### 2. 可配置化

风控参数应该**可配置**，支持：

- 不同策略使用不同的风控参数
- 根据市场环境动态调整
- 支持A/B测试和参数优化

### 3. 实时监控

风控模块应该提供：

- 实时风险指标计算
- 风险预警机制
- 风控日志记录
- 风控报告生成

---

## 常见风控策略

### 1. 固定止损止盈

**适用场景**: 震荡市、趋势不明确

```python
def fixed_stop_loss_take_profit(position, current_price, entry_price):
    profit_pct = (current_price / entry_price - 1)
    
    # 止损：-15%
    if profit_pct < -0.15:
        return 'stop_loss'
    
    # 止盈：100%
    if profit_pct > 1.0:
        return 'take_profit'
    
    return 'hold'
```

### 2. 移动止损

**适用场景**: 趋势明确的市场

```python
def trailing_stop_loss(position, current_price, highest_price):
    # 更新最高价
    if current_price > highest_price:
        highest_price = current_price
    
    # 从最高价回撤15%止损
    drawdown = (current_price / highest_price - 1)
    if drawdown < -0.15:
        return 'stop_loss'
    
    return 'hold'
```

### 3. 时间止损

**适用场景**: 长期持有策略

```python
def time_based_stop_loss(position, entry_date, current_date, min_profit=0.05):
    days_held = (current_date - entry_date).days
    
    # 持有超过90天且未盈利5%，止损
    if days_held > 90 and position.profit_pct < min_profit:
        return 'stop_loss'
    
    return 'hold'
```

### 4. 波动率止损

**适用场景**: 高波动市场

```python
def volatility_stop_loss(position, current_price, entry_price, volatility):
    # 止损 = 入场价 - 2倍波动率
    stop_loss_price = entry_price * (1 - 2 * volatility)
    
    if current_price < stop_loss_price:
        return 'stop_loss'
    
    return 'hold'
```

---

## 聚宽平台风控最佳实践

### 1. 初始化风控参数

```python
def initialize(context):
    # 风控参数
    g.risk_params = {
        'max_position_ratio': 0.9,        # 最大仓位90%
        'single_stock_limit': 0.2,        # 单股上限20%
        'stop_loss': -0.15,               # 止损-15%
        'take_profit': 1.0,               # 止盈100%
        'trailing_stop': 0.15,            # 移动止损15%
        'max_drawdown': -0.30,            # 最大回撤-30%
    }
    
    # 记录持仓信息
    g.cost_prices = {}           # 持仓成本价
    g.highest_prices = {}        # 持仓最高价
    g.entry_dates = {}           # 持仓日期
```

### 2. 每日风控检查

```python
def before_trading_start(context):
    # 组合级风控检查
    portfolio_value = context.portfolio.total_value
    cash = context.portfolio.available_cash
    
    # 检查最大回撤
    if check_max_drawdown(context):
        log.warn('超过最大回撤限制，停止交易')
        return
    
    # 检查仓位集中度
    check_position_concentration(context)

def handle_data(context, data):
    # 持仓级风控检查
    risk_control(context)
```

### 3. 订单级风控

```python
def before_order(context, security, amount):
    # 检查单股仓位限制
    total_value = context.portfolio.total_value
    current_value = context.portfolio.positions[security].total_amount * \
                    context.current_data[security].last_price
    
    if (current_value + abs(amount) * context.current_data[security].last_price) / total_value > \
       g.risk_params['single_stock_limit']:
        log.warn(f'{security} 超过单股仓位限制')
        return False
    
    # 检查总仓位限制
    total_position_value = sum(
        pos.total_amount * context.current_data[code].last_price
        for code, pos in context.portfolio.positions.items()
    )
    
    if (total_position_value + abs(amount) * context.current_data[security].last_price) / total_value > \
       g.risk_params['max_position_ratio']:
        log.warn('超过最大仓位限制')
        return False
    
    return True
```

### 4. 持仓级风控

```python
def risk_control(context):
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        current_price = current_data[stock].last_price
        cost_price = g.cost_prices.get(stock, pos.avg_cost)
        highest_price = g.highest_prices.get(stock, cost_price)
        
        if cost_price <= 0:
            continue
        
        # 更新最高价
        if current_price > highest_price:
            g.highest_prices[stock] = current_price
            highest_price = current_price
        
        profit = (current_price - cost_price) / cost_price
        drawdown_from_high = (highest_price - current_price) / highest_price
        
        # 1. 固定止损
        if profit < g.risk_params['stop_loss']:
            log.warn(f'🛑 [止损] {stock} 亏损: {profit*100:.1f}%')
            order_target_value(stock, 0)
            continue
        
        # 2. 固定止盈
        if profit > g.risk_params['take_profit']:
            log.info(f'🎯 [止盈] {stock} 盈利: {profit*100:.1f}%')
            order_target_value(stock, 0)
            continue
        
        # 3. 移动止损（盈利超过10%后启用）
        if profit > 0.10 and drawdown_from_high > g.risk_params['trailing_stop']:
            log.info(f'📉 [移动止损] {stock} 从高点回撤: {drawdown_from_high*100:.1f}%')
            order_target_value(stock, 0)
            continue
```

### 5. 组合级风控

```python
def check_max_drawdown(context):
    """检查最大回撤"""
    portfolio_value = context.portfolio.total_value
    initial_value = context.portfolio.starting_cash
    
    # 计算当前回撤
    current_drawdown = (portfolio_value / initial_value - 1)
    
    if current_drawdown < g.risk_params['max_drawdown']:
        return True  # 超过最大回撤限制
    
    return False

def check_position_concentration(context):
    """检查持仓集中度"""
    portfolio_value = context.portfolio.total_value
    
    # 按持仓价值排序
    positions_value = sorted([
        (code, pos.total_amount * context.current_data[code].last_price)
        for code, pos in context.portfolio.positions.items()
        if pos.total_amount > 0
    ], key=lambda x: x[1], reverse=True)
    
    # 检查前3只股票集中度
    top3_value = sum(v for _, v in positions_value[:3])
    concentration = top3_value / portfolio_value
    
    if concentration > 0.5:  # 前3只股票超过50%
        log.warn(f'持仓集中度过高: {concentration*100:.1f}%')
```

---

## TRQuant风控模块实现

基于聚宽平台的风控理念，我们开发了独立的风控模块：

**文件路径**: `core/risk/risk_manager.py`

### 核心特性

1. **多类型止损止盈**
   - 固定止损/止盈
   - 跟踪止损/止盈
   - 时间止损
   - 波动率止损

2. **仓位管理**
   - 单只股票最大仓位限制
   - 总持仓数限制
   - 持仓集中度控制

3. **回撤控制**
   - 最大回撤限制
   - 回撤恢复阈值
   - 实时回撤监控

4. **风险指标计算**
   - VaR（风险价值）
   - 最大回撤
   - 夏普比率
   - 波动率

### 使用示例

```python
from core.risk.risk_manager import RiskManager, RiskConfig, StopLossType

# 初始化风控管理器（基于聚宽最佳实践）
config = RiskConfig(
    stop_loss_type=StopLossType.TRAILING,      # 跟踪止损
    stop_loss_threshold=-0.15,                  # -15%止损
    take_profit_threshold=1.0,                  # 100%止盈
    max_position_size=0.2,                      # 单只股票最大20%仓位（聚宽推荐）
    max_total_positions=10,                     # 最大持仓10只
    max_drawdown=-0.30                          # 最大回撤-30%
)

risk_manager = RiskManager(config)

# 开仓
risk_manager.add_position(
    stock='600519.XSHG',
    entry_price=1800.0,
    shares=100,
    entry_date='2024-12-28'
)

# 每日更新并检查止损止盈
prices = {'600519.XSHG': 1850.0}
stocks_to_close = risk_manager.update_positions(prices, '2024-12-29')

# 计算组合价值
portfolio_value = risk_manager.calculate_portfolio_value(prices, cash=1000000)

# 计算回撤
drawdown_info = risk_manager.calculate_drawdown()
print(f"最大回撤: {drawdown_info['max_drawdown']*100:.1f}%")
```

---

## 总结

聚宽平台的风控理念强调：

1. **多层次风险管理**：订单级、持仓级、组合级
2. **动态调整**：根据市场环境调整风控参数
3. **实时监控**：实时计算风险指标，及时预警
4. **可配置化**：支持不同策略使用不同风控参数

我们的风控模块基于这些理念设计，提供了完整的风控功能，可以与聚宽平台的策略框架无缝集成。

---

*最后更新: 2024-12-28*




