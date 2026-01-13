---
name: BulletTrade到QMT策略转换计划
overview: 将已在BulletTrade跑通的7因子策略代码转换为QMT格式，保持算法逻辑完全一致，只做API适配。
todos:
  - id: compare-algorithm
    content: 对比BulletTrade和QMT版本的算法逻辑差异，确认核心逻辑
    status: completed
  - id: fix-factor-calculation
    content: 修复QMT版本的因子计算，使用QMT API获取真实财务数据（市值、ROE、增长率）
    status: completed
  - id: align-scoring
    content: 确保因子评分函数与BulletTrade版本完全一致
    status: completed
  - id: align-filtering
    content: 确保筛选逻辑与BulletTrade版本完全一致
    status: completed
  - id: test-conversion
    content: 在QMT中测试运行，验证转换后的策略能正常选股和交易
    status: pending
---

# BulletTrade到QMT策略转换计划

## 核心原则

**不是重新生成算法，而是将已跑通的BulletTrade策略转换为QMT格式！**

---

## 算法逻辑对比

### BulletTrade版本（已跑通）核心逻辑

**文件**: [`core/advisor_v4/bullettrade_strategy_generator.py`](core/advisor_v4/bullettrade_strategy_generator.py)

#### 1. 因子计算（7因子）

| 因子 | 数据来源 | 计算方法 |

|------|----------|----------|

| momentum_20d | `get_price(count=21)` | `(close[-1] - close[0]) / close[0] * 100` |

| rel_position | `get_price(count=21)` | `(close - low_20) / (high_20 - low_20) * 100` |

| market_cap | `valuation.market_cap` | **直接获取（单位：亿元）** |

| momentum_5d | `get_price(count=6)` | `(close[-1] - close[0]) / close[0] * 100` |

| turnover_rate | `valuation.turnover_ratio` | **直接获取（%）** |

| roe | `indicator.roe` | **直接获取（%）** |

| growth | `indicator.inc_net_profit_year_on_year` | **直接获取（%）** |

#### 2. 因子评分函数（`calculate_factor_scores()`）

```python
# 1. 20日动量：5%~30%最优，中心值17.5%
if 5.0 <= x <= 30.0:
    center = 17.5
    distance = abs(x - center)
    return max(0.0, 1.0 - distance / 12.5)
elif x < 5.0:
    return max(0.0, x / 5.0 * 0.5)
else:
    return max(0.0, 1.0 - (x - 30.0) / 20.0)

# 2. 相对位置：<80%最优，<30%满分
if x <= 30.0:
    return 1.0
elif x <= 80.0:
    return 1.0 - (x - 30.0) / 50.0 * 0.3
else:
    return max(0.0, 1.0 - (x - 80.0) / 20.0)

# 3. 市值：30~200亿最优，中心值115亿
if 30.0 <= x <= 200.0:
    center = 115.0
    distance = abs(x - center)
    return max(0.0, 1.0 - distance / 85.0)
elif x < 30.0:
    return max(0.0, x / 30.0 * 0.7)
else:
    return max(0.0, 1.0 - (x - 200.0) / 300.0)

# ... 其他4个因子类似
```

#### 3. 综合得分计算

```python
df['total_score'] = (
    df['momentum_20d_score'] * FACTOR_WEIGHTS['momentum_20d'] +
    df['rel_position_score'] * FACTOR_WEIGHTS['rel_position'] +
    df['market_cap_score'] * FACTOR_WEIGHTS['market_cap'] +
    df['momentum_5d_score'] * FACTOR_WEIGHTS['momentum_5d'] +
    df['turnover_rate_score'] * FACTOR_WEIGHTS['turnover_rate'] +
    df['roe_score'] * FACTOR_WEIGHTS['roe'] +
    df['growth_score'] * FACTOR_WEIGHTS['growth']
) * 100
```

#### 4. 筛选逻辑

```python
# 1. 得分筛选
candidates = candidates[candidates['total_score'] >= MIN_TOTAL_SCORE]

# 2. 20日动量筛选
candidates = candidates[
    (candidates['momentum_20d'] >= MIN_MOMENTUM_20D) &
    (candidates['momentum_20d'] <= MAX_MOMENTUM_20D)
]

# 3. 相对位置筛选
candidates = candidates[candidates['rel_position'] <= MAX_REL_POSITION]

# 4. 市值筛选
candidates = candidates[
    (candidates['market_cap'] >= MIN_MARKET_CAP) &
    (candidates['market_cap'] <= MAX_MARKET_CAP)
]

# ... 其他因子筛选
```

---

### QMT版本（当前问题）

**文件**: [`strategies/qmt/TRQuant_Weekly_Factor_V4.py`](strategies/qmt/TRQuant_Weekly_Factor_V4.py)

#### 问题1: 因子计算错误

| 因子 | 当前计算（错误） | 应该（参考BulletTrade） |

|------|-----------------|------------------------|

| market_cap | `close * avg_volume * 5 / 1e8` | 使用`ContextInfo.get_financial_data()`获取真实市值 |

| turnover_rate | 依赖错误的market_cap | 使用`ContextInfo.get_financial_data()`获取真实换手率 |

| roe | `10 + price_trend * 100` | 使用`ContextInfo.get_financial_data()`获取真实ROE |

| growth | `mean_return * 5` | 使用`ContextInfo.get_financial_data()`获取真实增长率 |

#### 问题2: 因子评分函数可能不一致

需要对比`calculate_factor_score()`与BulletTrade的`calculate_factor_scores()`是否完全一致。

#### 问题3: 筛选阈值可能过严

- MIN_TOTAL_SCORE = 40.0（BulletTrade版本可能更低）
- 需要确认BulletTrade版本的默认阈值

---

## 转换步骤

### Step 1: 修复因子计算（使用QMT财务数据API）

**修改位置**: `get_stock_factors()` 函数

```python
# 使用QMT API获取财务数据
# ContextInfo.get_financial_data(fieldList, stockList, startDate, endDate)
# ContextInfo.get_last_volume(stockcode)  # 获取流通股本

# 市值：从财务数据获取
# 换手率：从财务数据获取或使用流通股本计算
# ROE：从财务数据获取
# 增长率：从财务数据获取
```

### Step 2: 对齐因子评分函数

**修改位置**: `calculate_factor_score()` 函数

确保与BulletTrade版本的`calculate_factor_scores()`完全一致：

- 相同的评分区间
- 相同的中心值
- 相同的映射函数

### Step 3: 对齐筛选逻辑

**修改位置**: `apply_factor_filters()` 和 `select_stocks()` 函数

确保筛选顺序和阈值与BulletTrade版本一致。

### Step 4: 确认阈值参数

从BulletTrade策略生成器的config中确认默认阈值，确保QMT版本使用相同值。

---

## 关键API转换

### BulletTrade → QMT

| BulletTrade API | QMT API |

|-----------------|---------|

| `get_price(codes, count=21, fields=['close']) `| `ContextInfo.get_history_data(21, '1d', 'close', 0)` |

| `query(valuation.market_cap)` | `ContextInfo.get_financial_data(['market_cap'], stocks, ...)` |

| `query(indicator.roe)` | `ContextInfo.get_financial_data(['roe'], stocks, ...)` |

| `query(valuation.turnover_ratio)` | `ContextInfo.get_financial_data(['turnover_ratio'], stocks, ...)` |

---

## 预期结果

转换后的QMT策略应该：

1. 使用与BulletTrade完全一致的算法逻辑
2. 能正常获取财务数据并计算因子
3. 能正常选股（不再是0只）
4. 能正常执行交易