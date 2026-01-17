# 策略改进版本 V2 说明

## 📋 改进概述

基于专业分析，创建了改进版策略 `TRQuant_momentum_v3_improved_v2.py`，修复了原策略的关键问题。

## 🔧 关键改进点

### 1. 分批获取价格数据（修复核心问题）
**原问题**：只对前50只股票取价，导致选股偏差
```python
# 原代码（错误）
test_stocks = stocks[:50]
prices = get_price(test_stocks, ...)
```

**改进**：分批获取全部候选股票价格
```python
# 改进后
close = batch_get_price_pivot(stocks, end, fields=['close'], 
                              count=MOM_L+5, batch=120)
```

### 2. 改进兜底策略（基于流动性）
**原问题**：数据获取失败时直接取前N只，等同随机
```python
# 原代码（错误）
selected = stocks[:MAX_STOCKS]
```

**改进**：按近20日成交额排序
```python
# 改进后
money = df.groupby('code')['money'].sum().sort_values(ascending=False)
return money.index[:MAX_STOCKS + BUFFER].tolist()
```

### 3. 使用真实成本价（pos.avg_cost）
**原问题**：用下单时的 last_price 记录成本，导致风控误触发
```python
# 原代码（错误）
context.cost_prices[stock] = current_data[stock].last_price
```

**改进**：使用系统提供的真实成交均价
```python
# 改进后
def sync_cost_prices(context):
    for s, pos in context.portfolio.positions.items():
        if pos.total_amount > 0:
            context.cost[s] = pos.avg_cost
```

### 4. 周频调仓（降低换手）
**原问题**：2天一调仓，换手爆炸，手续费/滑点侵蚀利润
```python
# 原代码
REBALANCE_DAYS = 2
if context.trade_count % REBALANCE_DAYS != 1:
    return
```

**改进**：周频调仓
```python
# 改进后
REBALANCE_WEEKDAY = 1  # 周二调仓
wd = context.current_dt.weekday()
if wd != REBALANCE_WEEKDAY:
    return
```

### 5. 自适应风控（ATR/波动）
**原问题**：固定阈值止损/止盈，不适应市场波动
```python
# 原代码
if profit < STOP_LOSS:  # 固定-5%
    order_target_value(stock, 0)
```

**改进**：基于ATR的自适应风控
```python
# 改进后
atr = calc_atr(s, day, ATR_N)
stop_price = cost - STOP_ATR * atr  # 2.2倍ATR
if lp < stop_price:
    order_target_value(s, 0)
```

### 6. 指数趋势判断控制仓位
**新增功能**：根据指数趋势动态调整仓位
```python
def judge_market_risk(context):
    # MA20 > MA60：风险开（满仓）
    # MA20 < MA60：风险关（空仓）
    # 其他：风险中（半仓）
```

### 7. ST过滤全覆盖
**原问题**：只对前100只做ST过滤，后面的ST不会被剔除
```python
# 原代码（错误）
st = get_extras('is_st', filtered[:100], ...)
```

**改进**：分批处理，确保全覆盖
```python
# 改进后
def filter_st_flags(context, stocks, batch=200):
    for i in range(0, len(stocks), batch):
        part = stocks[i:i+batch]
        # 处理每批
```

### 8. 保留机制（降低抖动）
**新增功能**：持仓若仍在前 MAX+BUFFER，不卖
```python
# 改进后
target_pool = target_ranked[:]  # MAX+BUFFER
keep = [s for s in current if s in target_pool]
# 先保留现有，再补足
```

## 📊 参数对比

| 参数 | 原版本 | 改进版 | 说明 |
|------|--------|--------|------|
| 调仓频率 | 2天 | 周频（周二） | 降低换手 |
| 止损方式 | 固定-5% | ATR自适应 | 适应波动 |
| 移动止损 | 固定8% | ATR自适应 | 更合理 |
| 成本记录 | last_price | pos.avg_cost | 真实成本 |
| 选股范围 | 前50只 | 全部候选 | 避免偏差 |
| 兜底策略 | 原顺序 | 流动性排序 | 更科学 |

## 🎯 预期效果

1. **降低换手率**：周频调仓 + 保留机制，减少不必要的交易
2. **提高选股质量**：分批取价确保覆盖全部候选，避免偏差
3. **更准确的风控**：真实成本 + ATR自适应，减少误触发
4. **风险控制**：指数趋势判断，市场不好时自动降仓/空仓

## 📝 使用说明

### 运行回测
```bash
bullet-trade backtest strategies/bullettrade/TRQuant_momentum_v3_improved_v2.py \
  --start 2025-08-14 \
  --end 2025-09-13 \
  --cash 1000000 \
  --benchmark 000300.XSHG \
  --output backtest_results/improved_v2_test
```

### 可配置参数
- `REBALANCE_WEEKDAY`: 调仓日期（0=周一, 1=周二...）
- `STOP_ATR`: 止损ATR倍数（默认2.2）
- `TRAIL_ATR`: 移动止损ATR倍数（默认2.8）
- `RISK_ON_POS`: 风险开时仓位（默认1.0）
- `RISK_OFF_POS`: 风险关时仓位（默认0.0）

## ⚠️ 注意事项

1. **周频调仓**：只在指定weekday调仓，其他日期只做风控
2. **风险状态**：根据指数MA20/MA60判断，自动控制仓位
3. **ATR计算**：需要至少14天数据，新上市股票可能无法计算
4. **行业/概念过滤**：当前版本未启用，需要配置后使用

## 🔄 后续优化方向

1. **主线行业过滤**：配置行业代码，只选主线行业股票
2. **概念标签过滤**：预处理概念标签，过滤AI/算力等概念
3. **质量因子**：加入ROE、营收增速等基本面因子
4. **流动性下限**：要求近20日成交额>阈值

---

**创建时间**: 2025-12-15
**版本**: V2 改进版
**状态**: ✅ 已完成

