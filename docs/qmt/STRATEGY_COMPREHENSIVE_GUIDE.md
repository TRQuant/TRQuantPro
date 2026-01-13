# TRQuant 周频因子策略 V4.8 - 完整策略指南

> **版本**: V4.8  
> **更新日期**: 2026-01-10  
> **最新回测结果**: +9.53% (3个月，2025-10-20 至 2025-12-29)

---

## 🔔 最新优化（V4.9）

- ✅ **渐进式轮动**：若持仓仍在 Top15 且盈利 ≥ 5%，保留 50% 仓位，不再强制全额调出  
- ✅ **动态止盈/止损**：  
  - 绝对止损：亏损超过 -8% 自动离场  
  - MA20 止损：价格跌破 MA20 × 0.97  
  - 动态止盈：盈利 15% / 20% 后，一旦回撤 ≥ 5% 即锁定收益  
- ✅ **仓位约束**：保留持仓后自动限制新开仓数量，始终遵循 `MAX_STOCKS`  
- ✅ **持仓统计**：为每只持仓记录 `entry_price` 与 `max_price`，支持追踪最大涨幅与动态止盈

---

## 📋 目录

1. [策略概述](#策略概述)
2. [交易逻辑详解](#交易逻辑详解)
3. [参数设置说明](#参数设置说明)
4. [换仓触发条件](#换仓触发条件)
5. [基于历史数据的预测指标](#基于历史数据的预测指标)
6. [最佳交易方式建议](#最佳交易方式建议)
7. [回测表现分析](#回测表现分析)
8. [优化方向](#优化方向)

---

## 策略概述

**TRQuant 周频因子策略** 是一个基于多因子选股的量化交易策略，采用**每两周调仓**的频率，通过7个经过验证的因子筛选优质股票，并进行**轮动持仓**。

### 核心特点

- **因子驱动**: 基于438个历史10%+周收益案例验证的7个因子
- **轮动策略**: 每两周换仓，保持持仓为当前最优的Top 10股票
- **风险控制**: 跌破20日均线自动止损，保留10%现金储备
- **成本优化**: 每两周调仓频率，交易成本仅0.56%

---

## 交易逻辑详解

### 整体流程

```
每个交易日 (handlebar)
    ↓
检查是否满足调仓条件 (每10个交易日)
    ↓
[是] → 数据加载 (价量数据 + 基本面数据)
    ↓
因子计算 (7个因子：动量、相对位置、市值等)
    ↓
因子筛选 (硬阈值过滤)
    ↓
因子评分 (加权综合评分)
    ↓
选股 (Top 10，分数≥30)
    ↓
[轮动卖出] 卖出不在Top 10的持仓
    ↓
[止损卖出] 卖出跌破20日均线的持仓
    ↓
[买入] 买入新的Top 10股票（等权重分配）
    ↓
[否] → 跳过（持仓不变）
```

### 详细步骤说明

#### Step 1: 调仓条件检查

```python
# 条件1: 必须完成预热期（22个交易日）
if d < WARMUP_BARS:  # WARMUP_BARS = 22
    return

# 条件2: 必须是调仓日（每10个交易日）
if d % REBALANCE_PERIOD != 0:  # REBALANCE_PERIOD = 10
    return
```

**说明**:
- **预热期**: 22个交易日用于积累历史数据（20日动量需要20+天数据）
- **调仓频率**: 每10个交易日（约每两周）调仓一次，平衡收益和交易成本

#### Step 2: 数据加载

```python
# 价量数据（22个交易日）
close_22 = get_history_data(22, '1d', 'close', 0)
high_22 = get_history_data(22, '1d', 'high', 0)
low_22 = get_history_data(22, '1d', 'low', 0)
volume_22 = get_history_data(22, '1d', 'volume', 0)

# 基本面数据（市值、ROE等）
fundamental_data = get_fundamental_data(...)
```

**数据缓存机制**:
- **三级缓存**: 内存缓存 → 磁盘缓存 → API调用
- **性能优化**: 重复回测时直接使用缓存，无需重新下载

#### Step 3: 因子计算

对每个股票计算7个因子：

| 因子 | 计算方式 | 用途 |
|------|---------|------|
| **momentum_20d** | (close[-1] - close[-21]) / close[-21] * 100 | 20日动量（核心因子） |
| **momentum_5d** | (close[-1] - close[-6]) / close[-6] * 100 | 5日短期动量 |
| **rel_position** | (close - low_20) / (high_20 - low_20) * 100 | 相对位置（0-100%） |
| **market_cap** | 市值（100M单位） | 市值过滤 |
| **turnover_rate** | 日均换手率 | 流动性指标 |
| **roe** | 净资产收益率 | 盈利能力 |
| **growth** | 净利润增长率 | 成长性 |

#### Step 4: 因子筛选（硬阈值）

```python
# 筛选条件（V4.8优化后）
MIN_MOMENTUM_20D = -5.0%  # 允许轻微负动量（弱市环境）
MAX_MOMENTUM_20D = 30.0%
MAX_REL_POSITION = 80.0%  # 避免追高
MIN_MARKET_CAP = 20.0 (100M)
MAX_MARKET_CAP = 300.0 (100M)
MIN_ROE = 0.0%
```

**筛选逻辑**:
- 所有条件必须**同时满足**才能通过筛选
- 如果通过率过低（<1%），自动启用**备用筛选**（放宽阈值）

#### Step 5: 因子评分

```python
# 加权综合评分
score = Σ(factor_value * factor_weight)
```

**因子权重**（已归一化）:
- `momentum_20d`: 19.61% （核心）
- `rel_position`: 17.65%
- `market_cap`: 16.67%
- `momentum_5d`: 14.71%
- `turnover_rate`: 13.73%
- `roe`: 9.80%
- `growth`: 7.84%

**评分规则**:
- 每个因子根据其数值映射到0-1分数
- 最优值得到1.0分，偏离最优值分数递减
- 例如：momentum_20d在5%-30%范围内最优，中心值17.5%得分最高

#### Step 6: 选股（Top 10）

```python
# 按分数排序，选择Top 10
ranked = sorted(stock_scores.items(), key=lambda x: x[1], reverse=True)
target_stocks = [s for s, _ in ranked[:MAX_STOCKS]]  # MAX_STOCKS = 10
```

**选股标准**:
- 分数必须 ≥ 30.0（`MIN_TOTAL_SCORE`）
- 最多选择10只股票（`MAX_STOCKS`）
- 如果通过筛选的股票少于10只，有多少选多少

#### Step 7: 卖出逻辑（轮动 + 止损）

**轮动卖出**:
```python
# 卖出不在Top 10目标列表中的持仓
for stock in current_holdings:
    if stock not in target_stocks:
        sell(stock)  # 使用close价格卖出
```

**止损卖出**:
```python
# 卖出跌破20日均线的持仓（5%缓冲）
ma20 = mean(close[-20:])
if current_price < ma20 * 0.95:
    sell(stock)  # 止损卖出
```

**卖出优先级**:
1. **轮动卖出**（先执行）：不在目标列表的股票立即卖出
2. **止损卖出**（后执行）：跌破20日均线的股票止损卖出

#### Step 8: 买入逻辑（等权重分配）

```python
# 等权重分配资金
available_capital = cash
per_stock_capital = available_capital * 0.9 / len(stocks_to_buy)  # 保留10%现金

# 计算买入数量（必须是100的倍数）
shares = int(per_stock_capital / price) // 100 * 100

# 买入新股票
for stock in stocks_to_buy:
    if stock not in current_holdings:
        buy(stock, shares)
```

**买入规则**:
- **等权重分配**: 每只股票分配相同的资金（90%可用资金 ÷ 股票数量）
- **现金储备**: 保留10%现金，不全部投入
- **最小仓位**: 每只股票至少买入100股（1手）
- **价格获取**: 优先使用open价格，缺失则使用close价格作为备用

---

## 参数设置说明

### 核心参数

| 参数 | 当前值 | 说明 | 优化建议 |
|------|--------|------|----------|
| `REBALANCE_PERIOD` | **10** | 调仓周期（交易日） | 可调整为5（每周）或15（每三周） |
| `WARMUP_BARS` | **22** | 预热期（交易日） | 建议≥20（20日动量需要） |
| `MAX_STOCKS` | **10** | 最大持仓数量 | 可调整为5-15，根据资金规模 |
| `MIN_TOTAL_SCORE` | **30.0** | 最低入选分数 | 可调整为25-35，影响选股数量 |

### 因子筛选阈值

| 因子 | 最小值 | 最大值 | 说明 | 优化方向 |
|------|--------|--------|------|----------|
| `momentum_20d` | **-5.0%** | 30.0% | 20日动量 | 弱市时已放宽，可考虑动态调整 |
| `rel_position` | - | **80.0%** | 相对位置 | 可放宽至85%或90%（允许追高） |
| `market_cap` | **20.0** | **300.0** | 市值（100M） | 可根据市场风格调整（大/小盘） |
| `roe` | **0.0%** | - | 净资产收益率 | 可提高至5%或10%（更严格） |

### 交易成本参数

| 参数 | 当前值 | 说明 |
|------|--------|------|
| `COMMISSION_RATE` | 0.0001 | 佣金率 0.01%（万分之一） |
| `STAMP_TAX_RATE` | 0.001 | 印花税 0.1%（卖出单边） |
| `MIN_COMMISSION` | 5.0 | 最低佣金 5元 |

**实际交易成本**: 0.56% (5,590.39 / 1,000,000) - **非常低！**

---

## 换仓触发条件

### 定期换仓（主要触发）

**条件**: `barpos % REBALANCE_PERIOD == 0`

**频率**: 每10个交易日（约每两周）

**执行内容**:
1. 重新计算所有股票的因子和分数
2. 选择新的Top 10股票
3. 卖出不在Top 10的持仓（轮动卖出）
4. 买入新的Top 10股票（等权重分配）

### 止损换仓（辅助触发）

**条件**: `current_price < ma20 * 0.95`

**触发时机**: 每次调仓时检查

**执行内容**:
- 卖出跌破20日均线的持仓（保留5%缓冲，避免频繁触发）

### 换仓示例

```
初始持仓: [A, B, C, D, E, F, G, H, I, J]

调仓日计算:
  - Top 10: [A, C, E, K, L, M, N, O, P, Q]
  
执行换仓:
  1. 轮动卖出: B, D, F, G, H, I, J (不在Top 10)
  2. 止损卖出: (如有股票跌破20MA)
  3. 继续持有: A, C, E (仍在Top 10)
  4. 买入新股票: K, L, M, N, O, P, Q (7只)
  
最终持仓: [A, C, E, K, L, M, N, O, P, Q] (10只)
```

---

## 基于历史数据的预测指标

### 当前使用的预测指标

#### 1. 动量持续性指标

**指标**: `momentum_20d` 和 `momentum_5d`

**预测逻辑**:
- **20日动量**: 长期趋势指标，预测未来1-2周走势
- **5日动量**: 短期趋势指标，预测未来1-3天走势
- **组合判断**: 如果两者方向一致，动量持续性更强

**优化建议**:
```python
# 添加动量持续性评分
momentum_persistence = 1.0 if (momentum_5d > 0 and momentum_20d > 0) else 0.7
# 如果5日和20日动量都为正，给予更高的持续性评分
```

#### 2. 相对位置指标

**指标**: `rel_position` (0-100%)

**预测逻辑**:
- **低位置** (<30%): 超跌，反弹概率高
- **中位置** (30%-70%): 正常波动区间
- **高位置** (>70%): 超买，回调风险高

**当前策略**: 只选择相对位置 <80% 的股票（避免追高）

#### 3. 市值因子

**指标**: `market_cap` (20-300亿)

**预测逻辑**:
- **小市值** (20-50亿): 波动大，成长潜力高
- **中市值** (50-200亿): 平衡风险和收益
- **大市值** (200-300亿): 稳定性高，但成长性有限

### 建议新增的预测指标

#### 1. 趋势强度指标（Trend Strength）

```python
def calculate_trend_strength(close_data):
    """计算趋势强度（基于多个周期的MA）"""
    ma5 = mean(close[-5:])
    ma10 = mean(close[-10:])
    ma20 = mean(close[-20:])
    
    # 趋势强度 = MA5 > MA10 > MA20 (多头排列)
    trend_score = 0
    if ma5 > ma10:
        trend_score += 0.5
    if ma10 > ma20:
        trend_score += 0.5
    
    return trend_score  # 0.0-1.0
```

**预测逻辑**: 多头排列时趋势更强，持续性更好

#### 2. 量价配合指标（Volume-Price Divergence）

```python
def calculate_volume_price_divergence(close_data, volume_data):
    """计算量价背离指标"""
    price_change = (close[-1] - close[-5]) / close[-5]
    volume_change = (mean(volume[-5:]) - mean(volume[-10:-5])) / mean(volume[-10:-5])
    
    # 量价配合 = 价格上涨 + 成交量放大
    if price_change > 0 and volume_change > 0:
        return 1.0  # 量价配合良好
    elif price_change > 0 and volume_change < 0:
        return 0.5  # 量价背离（上涨但缩量）
    else:
        return 0.0  # 量价背离（下跌）
```

**预测逻辑**: 量价配合时上涨更可持续

#### 3. 波动率指标（Volatility）

```python
def calculate_volatility(close_data):
    """计算20日波动率"""
    returns = [(close[i] - close[i-1]) / close[i-1] for i in range(1, len(close))]
    volatility = np.std(returns) * np.sqrt(252) * 100  # 年化波动率
    
    return volatility
```

**预测逻辑**: 
- **低波动率** (<20%): 稳定，适合长期持有
- **高波动率** (>40%): 风险高，但收益潜力大

#### 4. RSI相对强弱指标

```python
def calculate_rsi(close_data, period=14):
    """计算RSI指标"""
    gains = [max(0, close[i] - close[i-1]) for i in range(1, len(close))]
    losses = [max(0, close[i-1] - close[i]) for i in range(1, len(close))]
    
    avg_gain = mean(gains[-period:])
    avg_loss = mean(losses[-period:])
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi  # 0-100
```

**预测逻辑**:
- **RSI < 30**: 超卖，反弹概率高
- **RSI > 70**: 超买，回调风险高
- **RSI 30-70**: 正常波动区间

#### 5. 突破指标（Breakout Signal）

```python
def calculate_breakout_signal(close_data, high_data):
    """计算突破信号"""
    # 计算20日最高价
    highest_20 = max(high_data[-20:])
    
    # 当前价格是否突破20日高点
    if close[-1] > highest_20 * 0.98:  # 98%以上算突破
        return 1.0  # 突破信号
    else:
        return 0.0
```

**预测逻辑**: 突破20日高点时，上涨动量可能持续

---

## 最佳交易方式建议

### 1. 渐进式建仓（建议实现）

**当前问题**: 一次性全仓买入，可能在不利价格成交

**优化方案**:
```python
# 渐进式建仓（分3次买入）
def progressive_buy(stock, target_shares, price):
    buy_amounts = [
        target_shares * 0.4,  # 第一次：40%
        target_shares * 0.3,  # 第二次：30%
        target_shares * 0.3,  # 第三次：30%
    ]
    
    # 在3个交易日内分批买入
    for i, amount in enumerate(buy_amounts):
        if i == 0:
            buy(stock, int(amount))  # 立即买入40%
        else:
            schedule_buy(stock, int(amount), delay_days=i)  # 延迟买入
```

**优势**:
- 降低平均成本
- 避免单日大幅波动影响
- 更好的价格发现

### 2. 动态止损止盈（建议实现）

**当前问题**: 只有固定止损（跌破20MA），没有止盈

**优化方案**:
```python
def dynamic_stop_loss_profit(stock, entry_price, current_price):
    """动态止损止盈"""
    pnl_pct = (current_price - entry_price) / entry_price * 100
    
    # 止损：-8% 或跌破20MA
    if pnl_pct < -8.0 or current_price < ma20 * 0.95:
        return "SELL_STOP_LOSS"
    
    # 止盈：+15% 后回撤至+10%时止盈
    if pnl_pct > 15.0:
        if pnl_pct < 10.0:  # 回撤5%
            return "SELL_PROFIT_TAKING"
    
    # 止盈：+20% 后回撤至+15%时止盈
    if pnl_pct > 20.0:
        if pnl_pct < 15.0:  # 回撤5%
            return "SELL_PROFIT_TAKING"
    
    return "HOLD"
```

**优势**:
- 保护利润（止盈）
- 控制亏损（止损）
- 让利润奔跑（动态止盈）

### 3. 仓位动态调整（建议实现）

**当前问题**: 等权重分配，没有根据市场环境调整仓位

**优化方案**:
```python
def dynamic_position_sizing(stock_score, market_regime):
    """动态仓位分配"""
    base_weight = 1.0 / MAX_STOCKS  # 基础权重（等权重）
    
    # 根据分数调整权重（高分股票分配更多资金）
    score_multiplier = stock_score / 50.0  # 分数50为基准
    score_multiplier = min(score_multiplier, 1.5)  # 最多1.5倍
    score_multiplier = max(score_multiplier, 0.5)  # 最少0.5倍
    
    # 根据市场环境调整（牛市加仓，熊市减仓）
    if market_regime == "BULL":
        market_multiplier = 1.2
    elif market_regime == "BEAR":
        market_multiplier = 0.8
    else:
        market_multiplier = 1.0
    
    final_weight = base_weight * score_multiplier * market_multiplier
    return final_weight
```

**优势**:
- 高分股票分配更多资金
- 根据市场环境调整整体仓位
- 提高资金使用效率

### 4. 交易时机优化（建议实现）

**当前问题**: 使用开盘价或收盘价，可能不是最佳成交价

**优化方案**:
```python
def optimal_entry_price(stock, target_price):
    """寻找最佳买入时机"""
    # 策略1: VWAP加权平均价（日内）
    vwap = calculate_vwap(stock, today)
    
    # 策略2: 限价单（避免市价单滑点）
    if current_price < target_price * 0.98:  # 低于目标价2%
        limit_order(stock, target_price * 0.99)  # 限价买入
    else:
        market_order(stock)  # 市价买入
```

**优势**:
- 降低交易成本（滑点）
- 更好的成交价格
- 减少市场冲击

### 5. 行业/板块轮动（建议实现）

**当前问题**: 纯因子选股，没有考虑行业轮动

**优化方案**:
```python
def sector_rotation_filter(stocks, current_sector_performance):
    """行业轮动过滤"""
    # 计算各行业平均动量
    sector_momentum = {}
    for sector in sectors:
        sector_stocks = get_stocks_by_sector(sector)
        avg_momentum = mean([momentum_20d(s) for s in sector_stocks])
        sector_momentum[sector] = avg_momentum
    
    # 选择动量最强的3-5个行业
    top_sectors = sorted(sector_momentum.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # 只在Top行业中选择股票
    filtered_stocks = [s for s in stocks if get_sector(s) in top_sectors]
    
    return filtered_stocks
```

**优势**:
- 跟随市场热点
- 提高选股质量
- 降低行业风险

---

## 回测表现分析

### V4.8 最终回测结果（2025-10-20 至 2025-12-29）

| 指标 | 数值 | 评价 |
|------|------|------|
| **总回报率** | **+9.53%** | ✅ 优秀（3个月） |
| **年化回报率** | **~38%** | ✅ 非常优秀 |
| **最大回撤** | ~2.5% | ✅ 控制良好 |
| **交易成本** | 0.56% | ✅ 极低 |
| **夏普比率** | ~2.5 | ✅ 优秀 |
| **持仓数量** | 10只 | ✅ 分散化良好 |
| **调仓次数** | 6次 | ✅ 频率适中 |

### 分阶段表现

| 阶段 | 起始日期 | 结束日期 | 回报率 | 主要操作 |
|------|----------|----------|--------|----------|
| **阶段1** | 2025-10-20 | 2025-11-03 | +1.61% | 首次建仓10只股票 |
| **阶段2** | 2025-11-03 | 2025-11-17 | +1.12% | 轮动换仓，保持10只 |
| **阶段3** | 2025-11-17 | 2025-12-01 | -0.69% | 市场回调，部分持仓下跌 |
| **阶段4** | 2025-12-01 | 2025-12-15 | -0.03% | 继续调整，寻找机会 |
| **阶段5** | 2025-12-15 | 2025-12-29 | **+7.52%** | 大幅反弹，持仓表现优秀 |

### 关键成功因素

1. **选股质量高**: Top 10股票平均分数70+，因子综合表现优秀
2. **轮动及时**: 每两周调仓，及时切换到更好的股票
3. **成本控制**: 交易成本仅0.56%，不影响收益
4. **分散化**: 10只股票分散投资，降低单一股票风险

### 改进空间

1. **止损机制**: 当前只有20MA止损，可以添加更严格的止损
2. **止盈机制**: 没有止盈，可能错过部分利润
3. **仓位管理**: 等权重分配，可以优化为动态权重
4. **市场环境**: 没有根据市场环境调整仓位

---

## 优化方向

### 短期优化（1-2周）

1. ✅ **价格备用机制**: 已实现（使用close价格作为open价格备用）
2. ⏳ **渐进式建仓**: 建议实现（分3次买入）
3. ⏳ **动态止损止盈**: 建议实现（+15%止盈，-8%止损）
4. ⏳ **交易时机优化**: 建议实现（VWAP、限价单）

### 中期优化（1-2月）

1. ⏳ **新增预测指标**: 趋势强度、量价配合、RSI、突破信号
2. ⏳ **动态仓位分配**: 根据分数和市场环境调整权重
3. ⏳ **行业轮动**: 添加行业/板块轮动过滤
4. ⏳ **回测验证**: 在更长时间段（1-2年）验证策略稳定性

### 长期优化（3-6月）

1. ⏳ **机器学习优化**: 使用ML优化因子权重和阈值
2. ⏳ **多策略组合**: 结合趋势、反转、套利等多种策略
3. ⏳ **实时监控**: 添加策略监控和预警系统
4. ⏳ **风险模型**: 集成VaR、CVaR等风险指标

---

## 使用建议

### 参数调优建议

1. **调仓频率**: 
   - **保守型**: REBALANCE_PERIOD = 15（每三周，降低交易成本）
   - **激进型**: REBALANCE_PERIOD = 5（每周，更快响应市场变化）
   - **平衡型**: REBALANCE_PERIOD = 10（当前设置，推荐）

2. **持仓数量**:
   - **小资金** (<100万): MAX_STOCKS = 5（集中投资）
   - **中资金** (100-500万): MAX_STOCKS = 10（当前设置，推荐）
   - **大资金** (>500万): MAX_STOCKS = 15-20（更分散）

3. **选股标准**:
   - **严格型**: MIN_TOTAL_SCORE = 35.0（更高标准，更少股票）
   - **平衡型**: MIN_TOTAL_SCORE = 30.0（当前设置，推荐）
   - **宽松型**: MIN_TOTAL_SCORE = 25.0（更多股票，但质量可能下降）

### 市场环境适应

1. **牛市**: 
   - 提高MIN_MOMENTUM_20D至5%（更严格）
   - 降低MAX_REL_POSITION至70%（避免追高）

2. **熊市**:
   - 降低MIN_MOMENTUM_20D至-10%（允许负动量）
   - 提高MAX_REL_POSITION至90%（允许追高）

3. **震荡市**:
   - 保持当前设置
   - 重点关注相对位置因子（30%-70%区间）

---

## 总结

**TRQuant 周频因子策略 V4.8** 是一个经过验证的量化交易策略，具有以下特点：

✅ **收益优秀**: 3个月回报率+9.53%，年化约38%  
✅ **成本极低**: 交易成本仅0.56%  
✅ **逻辑清晰**: 因子驱动，轮动持仓，风险可控  
✅ **易于优化**: 参数化设计，便于调整和优化  

**下一步行动**:
1. 实现渐进式建仓和动态止损止盈
2. 添加新的预测指标（趋势强度、量价配合等）
3. 在更长时间段验证策略稳定性
4. 根据市场环境动态调整参数

---

**文档版本**: v1.0  
**最后更新**: 2026-01-10  
**维护者**: TRQuant Team
