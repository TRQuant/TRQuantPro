# QMT回测结果分析与修复

> **日期**: 2026-01-10  
> **策略版本**: V4.7  
> **问题**: 缓存导致历史数据不更新，所有调仓选出相同股票

---

## 🔍 问题诊断

### 观察到的现象

1. **✅ 缓存正常工作**：
   - 第1次调仓：下载数据（25秒）
   - 第2次+调仓：从缓存加载（<1秒）

2. **❌ 严重问题**：
   - **所有12次调仓，选出的Top 10股票完全相同**
   - **所有12次调仓，股票分数完全相同**（73.1, 67.0, 66.9, 65.0, 64.6...）
   - **从第2次调仓开始，没有轮动**：`[Buy Info] No stocks to buy (all 10 target stocks already held)`

3. **回报率无法计算**：
   - 初始资金：1,000,000.00
   - 最终现金：141,220.56
   - 持仓价值：未显示（策略没有计算最终持仓市值）
   - 总交易：仅10笔买入，之后无任何交易

### 根本原因

**缓存使用了固定的历史数据，没有随barpos更新**：

```python
# 问题代码
# 第1次调仓（bar 5770）：下载22天数据 → 保存到缓存（close_22）
# 第2次调仓（bar 5775）：从缓存加载（close_22）→ 使用的是第1次的数据！
# 第3次调仓（bar 5780）：从缓存加载（close_22）→ 还是第1次的数据！
```

**QMT的`get_history_data`是相对于当前bar的**：
- `ContextInfo.get_history_data(22, '1d', 'close', 0)` 返回从**当前bar往前推22天**的数据
- 不同bar应该返回不同的数据（时间窗口不同）
- 但缓存保存的是第一次的数据，后续都复用，导致使用的是**过时的历史数据**

---

## ✅ 修复方案

### 方案1：缓存键包含barpos（推荐）

```python
# 修复后
cache_key = f"{field}_{days}_{current_bar}"  # 包含barpos
```

**优点**：
- 每个bar使用正确的历史数据
- 缓存仍然有效（同一bar内复用）

**缺点**：
- 缓存文件会增多（每个bar一个）
- 但这是正确的，因为不同bar的数据确实不同

### 方案2：禁用历史数据的磁盘缓存

```python
# 只缓存当日数据（days=1），不缓存历史数据（days>1）
if days > 1:
    use_disk_cache = False  # 历史数据不缓存
```

**优点**：
- 简单直接
- 确保每次使用最新数据

**缺点**：
- 失去历史数据的缓存加速
- 但历史数据下载很快（QMT本地数据）

### 方案3：缓存键包含日期范围

```python
# 计算历史数据的日期范围
start_date = current_date - timedelta(days=days)
cache_key = f"{field}_{days}_{start_date}_{current_date}"
```

**优点**：
- 精确匹配日期范围
- 可以跨bar复用（如果日期范围相同）

**缺点**：
- 实现复杂
- 需要计算日期范围

---

## 🎯 推荐修复（方案1）

修改缓存键生成逻辑，包含barpos：

```python
def get_all_stock_data(ContextInfo, stocks, field, days, use_disk_cache=True):
    # 获取当前bar
    current_bar = getattr(ContextInfo, 'barpos', 0)
    
    # 缓存键包含barpos（确保不同bar使用不同数据）
    cache_key = f"{field}_{days}_{current_bar}"
    
    # 检查内存缓存
    if cache_key in _data_cache:
        return _data_cache[cache_key]
    
    # 检查磁盘缓存（也包含barpos）
    if use_disk_cache:
        disk_data = _load_from_disk_cache(field, days, current_bar)
        if disk_data is not None:
            _data_cache[cache_key] = disk_data
            return disk_data
    
    # API调用
    data = ContextInfo.get_history_data(days, '1d', field, 0)
    # ... 处理数据 ...
    
    # 保存到缓存（包含barpos）
    if use_disk_cache:
        _save_to_disk_cache(field, days, result, current_bar)
    
    return result
```

---

## 📊 预期修复效果

### 修复前
```
Rebalance #1: 选出股票A, B, C... (分数: 73.1, 67.0, 66.9...)
Rebalance #2: 选出股票A, B, C... (分数: 73.1, 67.0, 66.9...) ← 相同！
Rebalance #3: 选出股票A, B, C... (分数: 73.1, 67.0, 66.9...) ← 相同！
```

### 修复后
```
Rebalance #1: 选出股票A, B, C... (分数: 73.1, 67.0, 66.9...)
Rebalance #2: 选出股票D, E, F... (分数: 75.2, 68.3, 65.1...) ← 不同！
Rebalance #3: 选出股票G, H, I... (分数: 72.5, 69.8, 64.2...) ← 不同！
```

---

## 💰 回报率计算

### 当前状态（无法准确计算）

- **初始资金**: 1,000,000.00
- **最终现金**: 141,220.56
- **持仓价值**: 未知（策略未计算）
- **总费用**: 153.44

**问题**：策略没有计算最终持仓市值，无法计算总资产和回报率。

### 需要添加的功能

在回测结束时，计算：
```python
# 获取当前持仓市值
total_market_value = 0
for stock, lots in ContextInfo.holdings.items():
    current_price = ContextInfo.get_last_price(stock)
    total_market_value += current_price * lots * 100

# 总资产
total_assets = ContextInfo.money + total_market_value

# 回报率
return_rate = (total_assets - ContextInfo.capital) / ContextInfo.capital * 100
```

---

## 🚀 优化建议

### 1. 修复缓存问题（优先级：最高）

- 缓存键包含barpos，确保不同bar使用不同数据
- 或禁用历史数据的磁盘缓存

### 2. 添加回报率计算（优先级：高）

- 在回测结束时计算总资产（现金+持仓市值）
- 计算回报率、夏普比率等指标
- 输出完整的回测报告

### 3. 优化选股逻辑（优先级：中）

- 当前只有18只股票通过筛选，可能过于严格
- 考虑调整因子权重或过滤阈值
- 增加选股多样性

### 4. 添加轮动检查（优先级：中）

- 即使选出相同股票，也应该检查是否需要调仓
- 考虑持仓成本、当前价格、止损止盈等

---

## 📝 下一步行动

1. **立即修复缓存问题**：修改缓存键生成逻辑
2. **添加回报率计算**：在策略结束时计算总资产和回报率
3. **重新运行回测**：验证修复效果
4. **分析回测结果**：评估策略表现，进一步优化

---

## 🔧 技术细节

### QMT get_history_data行为

QMT的`get_history_data`是**相对于当前bar**的：
- `get_history_data(22, '1d', 'close', 0)` 返回从**当前bar往前推22天**的数据
- 不同bar返回的数据不同（时间窗口不同）
- 因此，缓存键必须包含barpos，否则会使用错误的数据

### 缓存策略

| 数据类型 | 缓存键 | 说明 |
|---------|--------|------|
| 历史数据（days>1） | `{field}_{days}_{barpos}` | 必须包含barpos |
| 当日数据（days=1） | `{field}_{days}_{date}` | 可以包含日期 |

---

## ⚠️ 当前状态

**策略运行正常**，但**数据有问题**：
- ✅ 代码逻辑正确
- ✅ 缓存机制工作
- ❌ 缓存使用了错误的数据（过时的历史数据）
- ❌ 导致所有调仓选出相同股票
- ❌ 无法计算准确的回报率

**需要立即修复缓存问题，然后重新运行回测。**
