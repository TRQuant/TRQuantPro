# QMT策略测试验证指南

> **文件**: `strategies/qmt/TRQuant_Weekly_Factor_V4.py`  
> **状态**: ✅ 已对齐BulletTrade版本，待QMT测试验证

---

## 测试前检查清单

### 1. 文件编码 ✅
- 文件使用 `#coding:gbk` 编码
- QMT桌面端应能正确读取

### 2. 参数配置 ✅
- `MIN_TOTAL_SCORE = 30.0` (已对齐BulletTrade)
- `MAX_MARKET_CAP = 200.0` (已对齐BulletTrade)
- `REBALANCE_PERIOD = 5` (周频调仓)

### 3. 算法逻辑对齐 ✅
- ✅ 因子计算：7个因子计算逻辑已对齐
- ✅ 评分函数：与BulletTrade版本完全一致
- ✅ 筛选逻辑：6个筛选条件已对齐

---

## QMT测试步骤

### Step 1: 导入策略文件

1. 打开QMT桌面端
2. 进入"策略研究"或"回测"模块
3. 导入 `TRQuant_Weekly_Factor_V4.py`

### Step 2: 配置回测参数

**推荐配置**:
- **回测周期**: 最近3个月（例如：2025-10-01 至 2026-01-09）
- **初始资金**: 100万
- **股票池**: HS300（fast模式）或全A股（full模式）
- **调仓频率**: 每周（5个交易日）

### Step 3: 运行回测并观察

#### 关键观察点：

1. **初始化阶段**
   ```
   [Init] Loaded 300 HS300 stocks
   Configuration:
     Mode: fast (HS300 only)
     Min Score: 30.0
   ```

2. **数据获取阶段**
   ```
   [Data] Retrieved data for 300 stocks
   [Data] Retrieved fundamental data for X stocks
   ```
   - 如果财务数据获取失败，会显示警告，使用回退方法

3. **因子计算阶段**
   ```
   [Filter] X stocks passed filters (score >= 30.0)
   ```
   - **关键**: 应该看到有股票通过筛选（不再是0只）
   - 如果仍是0只，检查日志中的因子值

4. **选股阶段**
   ```
   [Selection] Top 10 stocks:
     1. 000001.SZ: score=XX.X
        m20=XX.X% rp=XX.X% m5=XX.X% tr=XX.X%
   ```

5. **交易执行阶段**
   ```
   [SELL-ROTATE] 000001.SZ: Not in top 10
   [BUY] 000002.SZ: 1000 shares @ XX.XX
   ```

---

## 预期结果

### 成功标志

1. ✅ **有股票通过筛选**: `[Filter] X stocks passed filters` (X > 0)
2. ✅ **能正常选股**: `[Selection] Top X stocks` 显示选中的股票
3. ✅ **能正常交易**: 看到 `[BUY]` 和 `[SELL]` 日志
4. ✅ **财务数据获取**: 如果成功，显示 `[Data] Retrieved fundamental data for X stocks`

### 可能的问题

#### 问题1: 仍无股票通过筛选

**可能原因**:
- 财务数据获取失败，使用回退方法导致因子值不准确
- 筛选条件过严

**解决方案**:
1. 检查日志中的因子值范围
2. 临时降低 `MIN_TOTAL_SCORE` 到 20.0 或更低
3. 检查财务数据是否已下载到本地

#### 问题2: 财务数据获取失败

**可能原因**:
- QMT本地财务数据未下载
- `get_financial_data()` API调用方式不正确

**解决方案**:
1. 在QMT中下载财务数据
2. 检查API调用参数是否正确
3. 代码会自动回退到估算方法

#### 问题3: 编码错误

**可能原因**:
- 文件编码问题

**解决方案**:
- 确保文件使用GBK编码保存
- 如果仍有问题，检查是否有特殊字符

---

## 验证检查点

### 1. 因子计算验证

检查日志中的因子值是否合理：

| 因子 | 合理范围 | 检查方法 |
|------|----------|----------|
| momentum_20d | -50% ~ +50% | 查看日志中的m20值 |
| rel_position | 0% ~ 100% | 查看日志中的rp值 |
| market_cap | 10亿 ~ 5000亿 | 查看日志中的市值（单位：亿元） |
| momentum_5d | -20% ~ +20% | 查看日志中的m5值 |
| turnover_rate | 0.1% ~ 50% | 查看日志中的tr值 |
| roe | -50% ~ +50% | 查看日志中的ROE值 |
| growth | -100% ~ +500% | 查看日志中的增长率值 |

### 2. 评分验证

检查综合得分是否合理：
- 得分范围：0 ~ 100
- 通过筛选的股票得分应 >= 30.0
- 如果所有股票得分都很低，可能是因子计算有问题

### 3. 筛选验证

检查筛选过程：
```
[Filter] 100 stocks passed filters (score >= 30.0)
[Filter] 50 stocks passed 20-day momentum filter
[Filter] 30 stocks passed relative position filter
...
```

---

## 与BulletTrade版本对比

### 应该一致的部分

1. **选股结果**: 在相同日期、相同股票池下，应该选出相似的股票
2. **因子值**: 价量因子（momentum_20d, rel_position, momentum_5d）应该非常接近
3. **综合得分**: 相同股票的得分应该接近（允许财务数据差异）

### 可能差异的部分

1. **财务数据**: 如果QMT无法获取财务数据，使用回退方法会有差异
2. **数据精度**: QMT和BulletTrade的数据源可能略有不同

---

## 调试建议

### 如果遇到问题，按以下顺序检查：

1. **检查初始化日志**: 确认策略参数正确加载
2. **检查数据获取**: 确认价格数据能正常获取
3. **检查财务数据**: 确认财务数据获取状态
4. **检查因子计算**: 查看因子值是否合理
5. **检查筛选过程**: 查看每一步筛选后剩余的股票数
6. **检查评分**: 查看综合得分分布

### 添加调试日志

如果需要更详细的调试信息，可以在代码中添加：

```python
# 在calculate_stock_factors中添加
print(f"[Debug] {stock}: m20={factors['momentum_20d']:.2f}%, mc={factors['market_cap']:.1f}亿")

# 在calculate_factor_score中添加
print(f"[Debug] {stock}: total_score={total_score:.2f}, m20_score={m20_score:.3f}")
```

---

## 成功标准

策略转换成功的标志：

1. ✅ 能在QMT中正常加载和运行
2. ✅ 有股票通过筛选（不再是0只）
3. ✅ 能正常执行交易
4. ✅ 回测结果与BulletTrade版本接近（允许财务数据差异）

---

## 下一步

测试通过后：
1. 记录测试结果和参数
2. 如有问题，根据日志进行针对性修复
3. 优化财务数据获取逻辑（如果需要）
4. 考虑生成PTrade版本
