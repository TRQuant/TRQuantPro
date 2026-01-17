# BulletTrade到QMT策略转换完成总结

> **日期**: 2026-01-10  
> **文件**: `strategies/qmt/TRQuant_Weekly_Factor_V4.py`  
> **状态**: ✅ 转换完成，待QMT测试验证

---

## ✅ 已完成的修复

### 1. 阈值参数对齐 ✅

**修改内容**:
- `MIN_TOTAL_SCORE`: 40.0 → **30.0** (与BulletTrade版本一致)
- `MAX_MARKET_CAP`: 2000.0 → **200.0** (与BulletTrade版本一致，单位：亿元)
- 新增 `MIN_MOMENTUM_5D = -5.0`, `MAX_MOMENTUM_5D = 10.0`
- 新增 `MIN_TURNOVER_RATE = 2.0`, `MAX_TURNOVER_RATE = 10.0`

**位置**: 第18行、第47-48行

---

### 2. 因子计算修复 ✅

**新增函数**: `get_fundamental_data_qmt()`
- 使用 `ContextInfo.get_financial_data()` 获取财务数据
- 支持获取：market_cap, roe, turnover_ratio, inc_net_profit_year_on_year
- 失败时回退到 `get_last_volume()` 估算

**修改函数**: `calculate_stock_factors()`
- **市值**: 优先从财务数据获取，失败时估算
- **换手率**: 优先从财务数据获取，失败时用流通股本计算
- **ROE**: 优先从财务数据获取，失败时用价格趋势代理
- **增长率**: 优先从财务数据获取，失败时用收益率代理
- **动量计算**: 对齐BulletTrade（使用21日和6日数据）

**位置**: 第172-232行（新增函数），第235-350行（修改函数）

---

### 3. 因子评分函数对齐 ✅

**修改函数**: `calculate_factor_score()`

完全对齐BulletTrade版本的`calculate_factor_scores()`：

| 因子 | 评分逻辑（与BulletTrade一致） |
|------|------------------------------|
| momentum_20d | 5%~30%最优，中心值17.5% |
| rel_position | <30%满分，<80%最优 |
| market_cap | 30~200亿最优，中心值115亿 |
| momentum_5d | -5%~10%最优，中心值2.5% |
| turnover_rate | 2%~10%最优 |
| roe | >0最优，最高10%ROE得满分 |
| growth | >0最优，最高100%增长得满分 |

**位置**: 第352-454行

---

### 4. 筛选逻辑对齐 ✅

**修改函数**: `apply_factor_filters()`

添加了与BulletTrade版本完全一致的筛选条件：
1. 20日动量筛选 (5%~30%)
2. 相对位置筛选 (≤80%)
3. 市值筛选 (30~200亿)
4. **5日动量筛选** (新增: -5%~10%)
5. **换手率筛选** (新增: 2%~10%)
6. ROE筛选 (≥0%)

**位置**: 第457-503行

---

### 5. 调用更新 ✅

**修改位置**: `select_stocks()` 函数

- 添加了 `get_fundamental_data_qmt()` 调用
- 更新 `calculate_stock_factors()` 调用，传入 `fundamental_data` 参数

**位置**: 第673-687行

---

## 📊 算法逻辑对比

### 已对齐的部分

| 项目 | BulletTrade | QMT | 状态 |
|------|------------|-----|------|
| 因子权重 | 7因子归一化权重 | ✅ 完全一致 | ✅ |
| 20日动量计算 | `(close[-1] - close[0]) / close[0]` | ✅ 对齐 | ✅ |
| 相对位置计算 | `(close - low_20) / (high_20 - low_20)` | ✅ 对齐 | ✅ |
| 5日动量计算 | `(close[-1] - close[0]) / close[0]` (count=6) | ✅ 对齐 | ✅ |
| 因子评分函数 | calculate_factor_scores() | ✅ 完全一致 | ✅ |
| 综合得分计算 | 7因子加权求和 * 100 | ✅ 完全一致 | ✅ |
| 筛选阈值 | MIN_TOTAL_SCORE=30.0 | ✅ 已对齐 | ✅ |
| 筛选条件 | 6个硬过滤条件 | ✅ 已对齐 | ✅ |

### 需要QMT API支持的部分

| 因子 | BulletTrade数据源 | QMT API | 状态 |
|------|------------------|---------|------|
| market_cap | `valuation.market_cap` | `get_financial_data(['market_cap'])` | ⚠️ 需测试 |
| turnover_rate | `valuation.turnover_ratio` | `get_financial_data(['turnover_ratio'])` | ⚠️ 需测试 |
| roe | `indicator.roe` | `get_financial_data(['roe'])` | ⚠️ 需测试 |
| growth | `indicator.inc_net_profit_year_on_year` | `get_financial_data(['inc_net_profit_year_on_year'])` | ⚠️ 需测试 |

**注意**: QMT的`get_financial_data()`需要本地财务数据支持。如果获取失败，代码会回退到估算方法。

---

## 🔍 关键修改点

### 1. 因子计算数据获取

```python
# 新增：获取财务数据
fundamental_data = get_fundamental_data_qmt(ContextInfo, stocks, date_str)

# 更新：传入财务数据
factors = calculate_stock_factors(
    ContextInfo, stock, close_22, high_22, low_22, volume_22, fundamental_data
)
```

### 2. 评分函数对齐

```python
# 对齐BulletTrade的评分逻辑
# 例如：相对位置评分
if rp <= 30.0:
    rp_score = 1.0  # 满分
elif rp <= 80.0:
    rp_score = 1.0 - (rp - 30.0) / 50.0 * 0.3  # 线性递减
else:
    rp_score = max(0.0, 1.0 - (rp - 80.0) / 20.0)  # 快速下降
```

### 3. 筛选条件完善

```python
# 新增5日动量和换手率筛选
if m5 < MIN_MOMENTUM_5D or m5 > MAX_MOMENTUM_5D:
    return False
if tr < MIN_TURNOVER_RATE or tr > MAX_TURNOVER_RATE:
    return False
```

---

## ⚠️ 注意事项

1. **QMT财务数据依赖**: `get_financial_data()`需要本地财务数据支持。如果数据不可用，代码会使用回退方法（价格趋势代理）。

2. **编码问题**: 文件使用`#coding:gbk`，但Python编译器可能报编码错误。这不影响QMT运行（QMT使用GBK编码）。

3. **测试验证**: 需要在QMT中实际运行回测，验证：
   - 财务数据是否能正常获取
   - 是否有股票通过筛选
   - 交易是否能正常执行

---

## 📝 下一步

1. **在QMT中测试运行**:
   - 检查财务数据获取是否成功
   - 观察是否有股票通过筛选
   - 验证交易执行是否正常

2. **如果财务数据获取失败**:
   - 检查QMT本地财务数据是否已下载
   - 考虑使用`get_last_volume()`估算市值和换手率
   - 或暂时放宽筛选条件，先验证其他逻辑

3. **如果仍无股票通过筛选**:
   - 检查因子计算值是否合理
   - 考虑进一步降低`MIN_TOTAL_SCORE`阈值
   - 检查筛选条件是否过严

---

## 📄 相关文件

- **QMT策略文件**: `strategies/qmt/TRQuant_Weekly_Factor_V4.py`
- **BulletTrade生成器**: `core/advisor_v4/bullettrade_strategy_generator.py`
- **转换计划**: `.cursor/plans/qmt策略完整修复_35ba9e4d.plan.md`
