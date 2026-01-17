# BulletTrade回测修复总结

> **生成时间**: 2026-01-09 (更新: 10:50)
> **回测日期**: 2024-10-14 至 2024-10-21
> **状态**: ✅ **回测成功运行**

---

## ✅ 已修复的问题

### 1. get_fundamentals导入问题 ✅
- **问题**: `name 'get_fundamentals' is not defined`
- **原因**: BulletTrade环境中，`from jqdata import *` 可能不包含 `get_fundamentals`
- **修复**: 显式从 `jqdatasdk` 导入 `get_fundamentals`，并在策略开头进行认证
- **代码**: 
  ```python
  import jqdatasdk
  from jqdatasdk import query, valuation, indicator, get_fundamentals
  jqdatasdk.auth('username', 'password')
  ```

### 2. Position对象属性错误 ✅
- **问题**: `'Position' object has no attribute 'total_value'`
- **原因**: BulletTrade的Position对象使用不同的属性名
- **修复**: 使用兼容性检查，支持多种属性名
- **代码**: 
  ```python
  if hasattr(position, 'value'):
      current_value = position.value
  elif hasattr(position, 'market_value'):
      current_value = position.market_value
  elif hasattr(position, 'total_amount') and hasattr(position, 'last_price'):
      current_value = position.total_amount * position.last_price
  ```

### 3. 选股阈值过高 ✅
- **问题**: `MIN_TOTAL_SCORE=60.0` 导致无股票通过筛选
- **修复**: 降低到 `30.0`
- **结果**: 现在有279只股票通过得分筛选

### 4. get_price返回MultiIndex列名 ✅ (新增)
- **问题**: BulletTrade的`get_price`返回的DataFrame列名是MultiIndex（如`('close', 'code')`），导致`'code' in df.columns`返回`False`
- **原因**: BulletTrade数据API包装层返回的数据格式与标准JQData不同
- **修复**: 在处理`get_price`返回值之前，将MultiIndex列名展平
- **代码**:
  ```python
  if isinstance(prices_20.columns, pd.MultiIndex):
      prices_20.columns = [col[-1] if isinstance(col, tuple) else col for col in prices_20.columns]
  ```

### 5. 市值单位转换错误 ✅ (新增)
- **问题**: JQData返回的`market_cap`单位已经是亿元，代码中又除以1亿，导致市值接近0
- **原因**: 错误地假设JQData返回的是元单位
- **修复**: 直接使用`market_cap`值，不做单位转换
- **代码**:
  ```python
  # 修复前（错误）
  df['market_cap'] = df['code'].map(dict(zip(fund_df['code'], fund_df['market_cap'] / 100000000))).fillna(0.0)
  
  # 修复后（正确）
  df['market_cap'] = df['code'].map(dict(zip(fund_df['code'], fund_df['market_cap']))).fillna(0.0)
  ```

---

## 📊 回测结果 (最新)

### 基本指标
- **策略收益**: -4.00%
- **策略年化收益**: -154.00%
- **最大回撤**: 0.00%
- **夏普比率**: 0.00
- **卡玛比率**: 0.00
- **胜率**: 0.00%

### 因子计算验证 ✅
- **20日动量**: min=-7.1%, max=97.8% ✅（之前是0）
- **市值**: min=172.2亿, max=23788.9亿 ✅（之前是0）
- **得分范围**: min=15.0, max=72.3 ✅

### 选股流程
```
初始股票池: 300只（HS300成分股）
→ 得分筛选 (≥30.0): 300 → 279只
→ 20日动量筛选 (5.0~30.0%): 279 → 203只
→ 相对位置筛选 (≤80.0%): 203 → 193只
→ 市值筛选 (30.0~200.0亿): 193 → 1只
→ 放宽条件后: 最终选择10只
```

### 交易统计
- **交易天数**: 6天
- **总交易次数**: 10次

---

## 📝 修复文件清单

1. **`core/advisor_v4/bullettrade_strategy_generator.py`**
   - 修复 `get_fundamentals` 导入和认证
   - 修复 `Position` 对象属性访问
   - 降低 `min_total_score` 阈值
   - 修复 `get_price` 返回的 MultiIndex 列名处理
   - 修复市值单位转换

2. **`scripts/run_bullettrade_backtest_v4.py`**
   - 回测脚本，用于执行策略回测

---

## 🔍 后续建议

### 1. 延长回测时间
- 当前仅6天回测时间太短，无法评估策略真实表现
- 建议回测至少1-3个月

### 2. 调整选股参数
- 市值筛选范围 `30.0~200.0亿` 对沪深300股票池来说太严格
- 可以考虑：
  - 扩大市值范围（如50-500亿）
  - 或换用中小盘股票池

### 3. 策略优化
- 当前策略因严格筛选条件导致选股数量不足
- 放宽条件时的选股质量可能受影响
- 考虑调整因子阈值或权重

---

*更新时间: 2026-01-09 10:50*
