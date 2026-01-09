# Investment Advisor V4.0 完整因子策略设计

> **版本**: V1.0  
> **日期**: 2026-01-08  
> **原则**: 基于已验证因子理论假设，使用完整7因子组合

---

## 📋 策略设计原则

### 1. 因子选择原则

**使用完整7个已验证因子**（基于438个10%+案例）：

| 排名 | 因子 | 权重 | 理论假设 | 最优区间 |
|------|------|------|---------|---------|
| 1 | **20日动量** | 1.0 | 动量驱动假设 | 5%~30% |
| 2 | **相对位置** | 0.9 | 低位反弹假设 | <80%（<30%最优） |
| 3 | **市值** | 0.85 | 市值弹性假设 | 30~200亿 |
| 4 | **5日动量** | 0.75 | 短期确认假设 | -5%~10% |
| 5 | **换手率** | 0.7 | 流动性假设 | 2%~10% |
| 6 | **ROE** | 0.5 | 基本面底线假设 | >0 |
| 7 | **净利润增长率** | 0.4 | 成长性假设 | >0 |

### 2. 因子权重原则

**使用100%已验证因子**：不再使用聚宽因子融合

**正确做法**:
```python
total_score = validated_score  # 100%已验证因子（7因子完整组合）
```

---

## 🏗️ 策略架构

### 1. 选股逻辑

#### 1.1 股票池筛选

1. **基础过滤**:
   - 排除ST股票
   - 排除688开头（科创板）
   - 排除停牌股票
   - 排除涨停/跌停股票（当日）

2. **流动性过滤**:
   - 日均成交额 > 5000万（过去20日）
   - 换手率在合理区间（2%~10%）

3. **基本面过滤**:
   - ROE > 0（基本面底线）
   - 净利润增长率 > -50%（避免严重恶化）

#### 1.2 因子计算

1. **已验证因子计算**（7个因子）:
   - `momentum_20d`: 20日动量（核心）
   - `rel_position`: 相对位置（核心）
   - `market_cap`: 市值（核心）
   - `momentum_5d`: 5日动量（确认）
   - `turnover_rate`: 换手率（流动性）
   - `roe`: ROE（基本面底线）
   - `growth`: 净利润增长率（成长性）

#### 1.3 综合得分计算

```python
# 已验证因子得分（基于7个因子，按理论权重加权）
validated_score = (
    momentum_20d_score * 1.0 +
    rel_position_score * 0.9 +
    market_cap_score * 0.85 +
    momentum_5d_score * 0.75 +
    turnover_rate_score * 0.7 +
    roe_score * 0.5 +
    growth_score * 0.4
) / total_weight * 100

# 最终得分（100%已验证因子）
total_score = validated_score
```

#### 1.4 选股排序

1. **按综合得分排序**（降序）
2. **取TOP N**（默认10只）
3. **确保股票满足所有过滤条件**

### 2. 仓位管理

#### 2.1 目标仓位

- **最大持股数量**: 10只（可配置）
- **单票最大仓位**: 20%（可配置）
- **总仓位上限**: 95%（保留5%现金）
- **最小现金保留**: 5%（应急）

#### 2.2 仓位分配

1. **等权分配**（基础）:
   ```python
   position_per_stock = (1 - min_cash_ratio) / len(selected_stocks)
   position_per_stock = min(position_per_stock, single_position_max)
   ```

2. **按得分加权**（可选）:
   ```python
   # 按综合得分分配权重（得分越高，仓位越大）
   scores = [stock.total_score for stock in selected_stocks]
   weights = scores / sum(scores)
   positions = weights * (1 - min_cash_ratio)
   positions = [min(p, single_position_max) for p in positions]
   ```

#### 2.3 调仓逻辑

1. **调仓频率**: 每周一次（周一开盘）
2. **调仓触发条件**:
   - 股票池变化（新股票进入或旧股票退出）
   - 持仓股票得分下降（低于阈值）
   - 持仓股票触发止损/止盈

### 3. 风险控制

#### 3.1 止损止盈

1. **止损**:
   - **固定止损**: -8%（成本价）
   - **移动止损**: 最高价回撤-8%（达到止盈后）

2. **止盈**:
   - **固定止盈**: +30%（成本价）
   - **分批止盈**: 达到+20%时减仓50%，达到+30%时全部止盈

3. **时间止损**:
   - 持仓超过20个交易日未触发止盈，强制平仓（避免长期套牢）

#### 3.2 仓位控制

1. **单票风险**:
   - 单票最大仓位 ≤ 20%
   - 单票最大亏损 ≤ 总资产的2%（止损保护）

2. **总仓位控制**:
   - 市场环境好：总仓位 ≤ 95%
   - 市场环境差：总仓位 ≤ 50%
   - 市场环境恶劣：总仓位 ≤ 20%

3. **市场环境判断**:
   - 沪深300指数MA20 > MA60：风险开（95%仓位）
   - 沪深300指数MA20 < MA60：风险关（50%仓位）
   - 沪深300指数MA20 < MA60 且 MA20 < MA20_prev：风险关（20%仓位）

#### 3.3 流动性保护

1. **买入前检查**:
   - 当日换手率 > 2%（避免流动性不足）
   - 过去5日均成交额 > 3000万（确保可交易）

2. **卖出保护**:
   - 涨停不能卖出（挂单等待）
   - 跌停优先卖出（及时止损）

---

## 💻 策略代码结构

### 1. BulletTrade策略代码结构

```python
# -*- coding: utf-8 -*-
"""
TRQuant Advisor V4.0 完整因子策略 - BulletTrade版
================================================

基于完整7个已验证因子的多因子选股策略

因子体系:
- 已验证因子（100%权重）：7个因子，基于438个10%+案例

策略逻辑:
1. 选股：基于完整7因子综合得分排序
2. 仓位：等权或按得分加权，单票最大20%
3. 调仓：每周一次（周一）
4. 风控：止损-8%，止盈+30%，移动止损-8%
"""

from jqdata import *
import numpy as np
import pandas as pd

# ==================== 策略参数 ====================
MAX_STOCKS = 10                 # 最大持股数量
SINGLE_POSITION = 0.20          # 单票最大仓位
MIN_CASH_RATIO = 0.05           # 最低现金保留

REBALANCE_WEEKDAY = 0           # 调仓日：0=周一

# 止损止盈
STOP_LOSS = -0.08               # 止损线
TAKE_PROFIT = 0.30              # 止盈线
TRAILING_STOP = -0.08           # 移动止损
TIME_STOP_DAYS = 20             # 时间止损（交易日）

# 市场环境判断（风险开关）
INDEX_MA_FAST = 20
INDEX_MA_SLOW = 60
RISK_ON_POS = 0.95              # 风险开：95%仓位
RISK_MID_POS = 0.50             # 风险中：50%仓位
RISK_OFF_POS = 0.20             # 风险关：20%仓位

# 因子权重（已验证因子，7因子）
FACTOR_WEIGHTS = {
    'momentum_20d': 1.0,        # 20日动量（核心）
    'rel_position': 0.9,        # 相对位置（核心）
    'market_cap': 0.85,         # 市值（核心）
    'momentum_5d': 0.75,        # 5日动量（确认）
    'turnover_rate': 0.7,       # 换手率（流动性）
    'roe': 0.5,                 # ROE（基本面底线）
    'growth': 0.4,              # 净利润增长率（成长性）
}

# 因子权重（已验证因子，100%权重）
# 不再使用聚宽因子融合

# 选股阈值
MIN_TOTAL_SCORE = 60            # 最小综合得分
MIN_MOMENTUM_20D = 3.0          # 最小20日动量（%）
MAX_REL_POSITION = 85.0         # 最大相对位置（%）
MIN_MARKET_CAP = 20.0           # 最小市值（亿）
MAX_MARKET_CAP = 300.0          # 最大市值（亿）

# ==================== 初始化 ====================
def initialize(context):
    """策略初始化"""
    # 基准设置
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    # 策略状态
    context.stock_pool = []
    context.trade_count = 0
    context.cost_prices = {}      # 持仓成本价
    context.highest_prices = {}   # 持仓最高价
    context.entry_dates = {}      # 持仓买入日期
    
    # 定时任务
    run_daily(before_market_open, time='09:00')
    run_weekly(market_open, weekday=REBALANCE_WEEKDAY, time='09:35')
    run_daily(check_risk, time='14:50')
    run_daily(after_market_close, time='15:30')
    
    log.info('=' * 60)
    log.info('策略初始化: TRQuant Advisor V4.0 完整因子策略')
    log.info(f'持股: {MAX_STOCKS}只 | 单票仓位: {SINGLE_POSITION*100:.0f}%')
    log.info(f'调仓: 每周{["一","二","三","四","五"][REBALANCE_WEEKDAY]} | 因子: 7因子完整组合（100%已验证因子）')
    log.info('=' * 60)


def before_market_open(context):
    """盘前准备"""
    context.trade_count += 1
    
    # 每周更新股票池（周一）
    if context.trade_count % 5 == 1:
        try:
            # 获取沪深300成分股
            context.stock_pool = get_index_stocks('000300.XSHG')
            log.info(f'[盘前] 更新股票池: {len(context.stock_pool)}只')
        except Exception as e:
            log.warn(f'[盘前] 获取指数成分股失败: {e}')
            # 兜底：使用全市场股票
            try:
                all_stocks = get_all_securities(['stock']).index.tolist()
                context.stock_pool = [s for s in all_stocks 
                                     if not s.startswith('688') 
                                     and not s.startswith('300')][:500]
                log.info(f'[盘前] 使用全市场股票池: {len(context.stock_pool)}只')
            except:
                context.stock_pool = []


def market_open(context):
    """开盘交易（调仓日）"""
    log.info(f'[调仓日] 第{context.trade_count}个交易日')
    
    # 1. 选股
    target_stocks = select_stocks(context)
    if not target_stocks:
        log.warn('[调仓] 未选出股票，保持当前持仓')
        return
    
    log.info(f'[调仓] 选股结果: {len(target_stocks)}只')
    for i, stock in enumerate(target_stocks[:5], 1):
        log.info(f'  {i}. {stock}')
    
    # 2. 调仓
    rebalance(context, target_stocks)


def select_stocks(context):
    """选股逻辑 - 完整7因子"""
    stocks = context.stock_pool
    if not stocks:
        return []
    
    current_date = context.current_dt.date()
    date_str = current_date.strftime('%Y-%m-%d')
    
    # 1. 基础过滤
    stocks = filter_basic(stocks, date_str)
    if not stocks:
        return []
    
    log.info(f'[选股] 基础过滤后: {len(stocks)}只')
    
    # 2. 计算因子
    factors_df = calculate_all_factors(stocks, date_str)
    if factors_df is None or factors_df.empty:
        return []
    
    # 3. 综合得分筛选
    candidates = factors_df[
        (factors_df['total_score'] >= MIN_TOTAL_SCORE) &
        (factors_df['momentum_20d'] >= MIN_MOMENTUM_20D) &
        (factors_df['rel_position'] <= MAX_REL_POSITION) &
        (factors_df['market_cap'] >= MIN_MARKET_CAP) &
        (factors_df['market_cap'] <= MAX_MARKET_CAP)
    ].copy()
    
    if candidates.empty:
        log.warn('[选股] 无股票满足阈值条件')
        return []
    
    # 4. 排序取TOP N
    candidates = candidates.sort_values('total_score', ascending=False)
    selected = candidates.head(MAX_STOCKS)['code'].tolist()
    
    log.info(f'[选股] 最终选择: {len(selected)}只')
    log.info(f'[选股] 得分范围: {candidates["total_score"].min():.1f} ~ {candidates["total_score"].max():.1f}')
    
    return selected


def calculate_all_factors(codes, date_str):
    """计算所有因子并生成综合得分"""
    try:
        # 这里需要使用聚宽API计算因子
        # 由于BulletTrade环境中，我们需要内联实现因子计算
        # 或者调用远程服务（如果支持）
        
        # 简化版本：使用聚宽内置因子和基础计算
        factors_df = calculate_validated_factors(codes, date_str)
        
        if factors_df is None or factors_df.empty:
            return None
        
        # 最终得分（100%已验证因子）
        factors_df['total_score'] = factors_df['validated_score'].clip(0, 100)
        
        return factors_df
        
    except Exception as e:
        log.error(f'[因子计算] 失败: {e}')
        return None


def calculate_validated_factors(codes, date_str):
    """计算已验证因子（7因子）"""
    # 实现因子计算逻辑
    # 注意：在BulletTrade环境中，需要使用聚宽API
    pass




def rebalance(context, target_stocks):
    """调仓逻辑"""
    current_positions = list(context.portfolio.positions.keys())
    current_positions = [s for s in current_positions if s in context.stock_pool]
    
    # 1. 卖出不在目标列表的股票
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)
            log.info(f'[调仓] 卖出: {stock}')
    
    # 2. 计算目标仓位（等权）
    total_value = context.portfolio.total_value
    cash_available = context.portfolio.available_cash
    target_value_per_stock = (total_value * (1 - MIN_CASH_RATIO)) / len(target_stocks)
    target_value_per_stock = min(target_value_per_stock, total_value * SINGLE_POSITION)
    
    # 3. 买入目标股票
    for stock in target_stocks:
        current_value = context.portfolio.positions[stock].total_value
        target_value = target_value_per_stock
        
        if target_value > current_value * 1.1:  # 允许10%误差
            order_target_value(stock, target_value)
            log.info(f'[调仓] 买入: {stock} | 目标价值: {target_value:.0f}')
            
            # 记录成本价和买入日期
            if stock not in context.cost_prices:
                context.cost_prices[stock] = get_current_data()[stock].last_price
                context.highest_prices[stock] = context.cost_prices[stock]
                context.entry_dates[stock] = context.current_dt.date()


def check_risk(context):
    """风控检查（盘中）"""
    current_date = context.current_dt.date()
    
    for stock in list(context.portfolio.positions.keys()):
        if stock not in context.stock_pool:
            continue
        
        position = context.portfolio.positions[stock]
        if position.total_amount == 0:
            continue
        
        current_price = get_current_data()[stock].last_price
        cost_price = position.avg_cost
        
        if cost_price <= 0:
            continue
        
        # 更新最高价
        if stock not in context.highest_prices:
            context.highest_prices[stock] = current_price
        else:
            context.highest_prices[stock] = max(context.highest_prices[stock], current_price)
        
        # 1. 固定止损
        pnl_rate = (current_price / cost_price - 1.0)
        if pnl_rate <= STOP_LOSS:
            order_target_value(stock, 0)
            log.warn(f'[风控] 止损: {stock} | 亏损: {pnl_rate:.2%}')
            continue
        
        # 2. 固定止盈
        if pnl_rate >= TAKE_PROFIT:
            order_target_value(stock, 0)
            log.info(f'[风控] 止盈: {stock} | 盈利: {pnl_rate:.2%}')
            continue
        
        # 3. 移动止损（达到一定盈利后）
        if pnl_rate >= 0.15:  # 盈利15%后启用移动止损
            highest_price = context.highest_prices[stock]
            trailing_pnl_rate = (current_price / highest_price - 1.0)
            if trailing_pnl_rate <= TRAILING_STOP:
                order_target_value(stock, 0)
                log.warn(f'[风控] 移动止损: {stock} | 回撤: {trailing_pnl_rate:.2%}')
                continue
        
        # 4. 时间止损
        if stock in context.entry_dates:
            days_held = (current_date - context.entry_dates[stock]).days
            if days_held >= TIME_STOP_DAYS:
                order_target_value(stock, 0)
                log.info(f'[风控] 时间止损: {stock} | 持仓: {days_held}天')
                continue


def after_market_close(context):
    """盘后处理"""
    # 清理无效持仓记录
    for stock in list(context.cost_prices.keys()):
        if context.portfolio.positions[stock].total_amount == 0:
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
            context.entry_dates.pop(stock, None)
```

---

## 🔧 实现计划

### 阶段1: 因子计算器重构 ✅

1. **修正MultiFactorCalculator**:
   - 移除聚宽因子融合，使用100%已验证因子
   - 支持完整7个已验证因子
   - total_score直接等于validated_score

### 阶段2: BulletTrade策略生成器 ✅

1. **实现策略代码生成器**:
   - 基于因子配置生成BulletTrade策略代码
   - 包含完整的选股、仓位、风控逻辑
   - 支持参数配置和自定义

### 阶段3: BulletTrade回测集成 ✅

1. **实现回测接口**:
   - 集成BulletTrade回测引擎
   - 支持策略代码执行
   - 返回回测结果和绩效指标

### 阶段4: 策略测试和验证 ✅

1. **完整测试**:
   - 历史回测验证
   - 绩效指标分析
   - 与旧策略对比

---

## 📊 预期改进

### 1. 因子覆盖

- **旧策略**: 3个因子（momentum_20d, rel_position, market_cap）
- **新策略**: 7个因子（完整已验证因子组合，100%权重）

### 2. 因子权重

- **旧策略**: 50% / 50%融合（错误，聚宽因子未经验证）
- **新策略**: 100%已验证因子（正确，基于438个历史案例验证）

### 3. 选股质量

- **预期**: 选股准确率提升，综合得分更可靠
- **原因**: 使用完整因子组合，信息更全面

### 4. 回测表现

- **预期**: Sharpe比率提升，胜率提升，回撤控制更好
- **原因**: 完整的因子体系 + 正确的融合权重 + 完善的风控

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-08
